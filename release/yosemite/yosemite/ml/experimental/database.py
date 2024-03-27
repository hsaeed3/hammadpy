from yosemite.ml.text.util import Chunker, SentenceTransformer
from yosemite.ml.text.cross_encode import CrossEncoder as CrossEncode
from typing import Union, List, Tuple, Optional, Dict
import os
import uuid
from pyspark.sql import SparkSession, DataFrame, functions as F
from pyspark.ml.feature import Tokenizer, StopWordsRemover, CountVectorizer, IDF
from pyspark.ml.pipeline import Pipeline
from pyspark.ml.linalg import Vectors, VectorUDT
import pandas as pd
from PyPDF2 import PdfReader
from ebooklib import epub
import numpy as np

class YosemiteDatabase:
    def __init__(self, dimension: Optional[int] = None, model_name: str = "all-MiniLM-L6-v2"):
        self.dimension = dimension
        self.model_name = model_name
        self.spark = SparkSession.builder \
            .appName("YosemiteDatabase") \
            .config("spark.driver.memory", "3g") \
            .config("spark.executor.memory", "3g") \
            .getOrCreate()
        self.df = None

    def load_dataset(self, path: str, id_column: str, content_column: str):
        try:
            df = self.spark.read.csv(path, header=True, inferSchema=True)
            chunker = Chunker()
            embedder = SentenceTransformer(self.model_name)
            
            @F.udf(returnType="array<string>")
            def chunk_udf(content):
                return chunker.chunk_text(content)
            
            @F.udf(returnType="array<array<float>>")
            def embed_udf(chunks):
                return [embedder.embed([chunk])[0].tolist() for chunk in chunks]
            
            self.df = df.select(
                F.col(id_column).alias("id"),
                F.col(content_column).alias("content"),
                chunk_udf(F.col(content_column)).alias("chunks"),
                embed_udf(chunk_udf(F.col(content_column))).alias("vectors")
            )
        except Exception as e:
            print(f"Error loading dataset: {str(e)}")

    def load_docs(self, dir: str):
        try:
            if not os.path.exists(dir):
                raise FileNotFoundError(f"Directory {dir} does not exist.")

            chunker = Chunker()
            embedder = SentenceTransformer(self.model_name)
            data = []

            for file_path in os.listdir(dir):
                file_path = os.path.join(dir, file_path)
                if file_path.endswith(".txt"):
                    with open(file_path, "r", encoding="utf-8") as file:
                        content = file.read()
                elif file_path.endswith(".pdf"):
                    with open(file_path, "rb") as file:
                        reader = PdfReader(file)
                        content = " ".join(page.extract_text() for page in reader.pages)
                elif file_path.endswith(".epub"):
                    book = epub.read_epub(file_path)
                    content = " ".join(item.get_content().decode("utf-8") for item in book.get_items_of_type(9))
                else:
                    continue

                doc_id = str(uuid.uuid4())
                chunks = chunker.chunk_text(content)
                vectors = [embedder.embed([chunk])[0].tolist() for chunk in chunks]
                data.append((doc_id, content, chunks, vectors))

            self.df = self.spark.createDataFrame(data, ["id", "content", "chunks", "vectors"])
        except Exception as e:
            print(f"Error loading documents: {str(e)}")

    def add(self, documents: List[Dict[str, str]], shared_id: Optional[bool] = False):
        try:
            chunker = Chunker()
            embedder = SentenceTransformer(self.model_name)
            data = []

            for doc in documents:
                if shared_id:
                    doc_id = "shared"
                else:
                    doc_id = doc.get("id", str(uuid.uuid4()))
                doc_content = doc["content"]
                chunks = chunker.chunk_text(doc_content)
                vectors = [embedder.embed([chunk])[0].tolist() for chunk in chunks]
                data.append((doc_id, doc_content, chunks, vectors))

            new_df = self.spark.createDataFrame(data, ["id", "content", "chunks", "vectors"])
            if self.df is None:
                self.df = new_df
            else:
                self.df = self.df.union(new_df)
        except Exception as e:
            print(f"Error adding documents: {str(e)}")

    def search(self, query: str, k: int = 5) -> List[Tuple[str, str, List[float]]]:
        try:
            if self.df is None:
                raise ValueError("Data has not been loaded.")

            embedder = SentenceTransformer(self.model_name)
            query_vector = embedder.embed([query])[0].tolist()
            
            @F.udf(returnType=VectorUDT())
            def vector_udf(vec):
                return Vectors.dense(vec)
            
            self.df = self.df.withColumn("vector", vector_udf(F.col("vectors")))
            
            query_df = self.spark.createDataFrame([(query_vector,)], ["query_vector"])
            
            joined_df = self.df.crossJoin(query_df)
            
            @F.udf(returnType="float")
            def cosine_similarity(vec1, vec2):
                return float(vec1.dot(vec2) / (vec1.norm(2) * vec2.norm(2)))
            
            results_df = joined_df.withColumn("similarity", cosine_similarity(F.col("vector"), vector_udf(F.col("query_vector"))))
            top_docs_df = results_df.orderBy(F.desc("similarity")).limit(k)
            
            ranked_results = []
            for row in top_docs_df.collect():
                doc_id = row["id"]
                doc_content = row["content"]
                doc_vectors = row["vectors"]
                ranked_results.append((doc_id, doc_content, doc_vectors))
            
            return ranked_results
        except Exception as e:
            print(f"Error performing search: {str(e)}")
            return []

    def search_and_rank(self, query: str, k: int = 5) -> List[Tuple[str, str, float]]:
        try:
            if self.df is None:
                raise ValueError("Data has not been loaded.")
            
            # Perform search using PySpark SQL
            self.df.createOrReplaceTempView("documents")
            query_result = self.spark.sql(f"SELECT id, chunks FROM documents WHERE content LIKE '%{query}%'")
            pyspark_chunks = [row["chunks"] for row in query_result.collect()]
            
            # Perform search using vector similarity
            search_results = self.search(query, k)
            vector_chunks = [chunk for _, chunk, _ in search_results]

            combined_results = pyspark_chunks + vector_chunks
            cross_encode = CrossEncode()
            ranked_results = cross_encode.rank(query, [' '.join(chunk) for chunk in combined_results])
            return [(doc_id, chunk, score) for (doc_id, chunk), score in ranked_results]
        except Exception as e:
            print(f"Error performing search and rank: {str(e)}")
            return []

if __name__ == "__main__":
    try:
        db = YosemiteDatabase()
        documents = [
            {"This is a test document."},
            {"This is another test document."}
        ]
        for document in documents:
            db.add([document])
        results = db.search("test")
        print("Search Results:")
        for doc_id, doc_content, doc_vectors in results:
            print(f"Document ID: {doc_id}")
            print(f"Content: {doc_content}")
            print(f"Vectors: {doc_vectors}")
            print("---")
        
        ranked_results = db.search_and_rank("test")
        print("Ranked Results:")
        for doc_id, chunk, score in ranked_results:
            print(f"Document ID: {doc_id}")
            print(f"Chunk: {chunk}")
            print(f"Score: {score}")
            print("---")
    except Exception as e:
        print(f"Error in main: {str(e)}")