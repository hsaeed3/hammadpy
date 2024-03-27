from yosemite.ml.text.util import Chunker, SentenceTransformer
from yosemite.ml.data.db import Database
from typing import Union, List, Tuple, Optional
import os
import uuid
from annoy import AnnoyIndex

class VectorDatabase:
    def __init__(self, dimension: Optional[int] = None, model_name: str = "all-MiniLM-L6-v2"):
        self.index = None
        self.dimension = dimension
        self.document_ids = []
        self.sentences = []
        self.vectors = []
        self.model_name = model_name

    def load(self, index_path: str):
        if not os.path.isfile(index_path):
            raise FileNotFoundError(f"Index file not found: {index_path}")

        self.index = AnnoyIndex(self.dimension, 'angular')
        self.index.load(index_path)

    def create(self, input_data: Union[str, List[str], List[Tuple[str, list]]], num_trees: int = 10):
        if isinstance(input_data, str):
            if os.path.isdir(input_data):
                self._load_data_from_directory(input_data)
            else:
                raise ValueError("Invalid input_data. Expected a directory path.")
        elif isinstance(input_data, list):
            if all(isinstance(item, str) for item in input_data):
                self._load_data_from_strings(input_data)
            elif all(isinstance(item, tuple) and len(item) == 2 for item in input_data):
                self._load_data_from_tuples(input_data)
            else:
                raise ValueError("Invalid input_data. Expected a list of strings or a list of tuples.")
        else:
            raise ValueError("Invalid input_data. Expected a directory path, a list of strings, or a list of tuples.")

        self._build_index(num_trees)

    def _load_data_from_directory(self, directory: str):
        chunker = Chunker()
        for file_name in os.listdir(directory):
            if file_name.endswith(".txt"):
                file_path = os.path.join(directory, file_name)
                with open(file_path, "r", encoding="utf-8") as file:
                    content = file.read().strip()
                    self.sentences.extend(chunker.chunk_text(content))
                    self.document_ids.extend([str(uuid.uuid4()) for _ in chunker.chunk_text(content)])

    def _load_data_from_strings(self, strings: List[str]):
        chunker = Chunker()
        self.sentences = [sentence for text in strings for sentence in chunker.chunk_text(text)]
        self.document_ids = [str(uuid.uuid4()) for _ in self.sentences]

    def _load_data_from_tuples(self, tuples: List[Tuple[str, list]]):
        self.sentences, self.vectors = zip(*tuples)
        self.document_ids = [str(uuid.uuid4()) for _ in tuples]

    def _build_index(self, num_trees: int):
        if not self.dimension:
            self.dimension = len(self.vectors[0]) if self.vectors else SentenceTransformer(self.model_name).model.get_sentence_embedding_dimension()

        self.index = AnnoyIndex(self.dimension, 'angular')

        if self.vectors:
            for i, vector in enumerate(self.vectors):
                self.index.add_item(i, vector)
        else:
            embedder = SentenceTransformer(self.model_name)
            for i, sentence in enumerate(self.sentences):
                vector = embedder.embed([sentence])[0][1]
                self.index.add_item(i, vector)

        self.index.build(num_trees)
    
    def create_from_database(self, db_path: str, num_trees: int = 10):
        self.db = Database()
        self.db.load(db_path)
        chunker = Chunker()
        embedder = SentenceTransformer(self.model_name)
        
        for doc in self.db.ix.searcher().documents():
            doc_id = doc["id"]
            doc_content = doc["content"]
            
            chunks = chunker.chunk_text(doc_content)
            for chunk in chunks:
                self.sentences.append(chunk)
                self.document_ids.append(doc_id)
                
                vector = embedder.embed([chunk])[0][1]
                self.vectors.append(vector)
        
        self._build_index(num_trees)

    def search(self, query: str, k: int = 5) -> List[Tuple[int, str, str, List[float]]]:
        if not self.index:
            raise ValueError("Index has not been built or loaded.")

        embedder = SentenceTransformer(self.model_name)
        query_vector = embedder.embed([query])[0][1]
        indices = self.index.get_nns_by_vector(query_vector, k, include_distances=False)
        results = []
        for index in indices:
            sentence = self.sentences[index]
            document_id = self.document_ids[index]
            vector = self.index.get_item_vector(index)
            results.append((index, sentence, document_id, vector))
        return results
    
if __name__ == "__main__":
    # Create a VectorDatabase from a list of strings
    documents = [
        "Paris is the capital of France.",
        "London is the capital of the United Kingdom.",
        "Berlin is the capital of Germany."
    ]
    vdb = VectorDatabase()
    vdb.create(documents)
    
    # Perform a search
    query = "What is the capital of France?"
    results = vdb.search(query)
    for index, sentence, document_id, vector in results:
        print(f"Index: {index}, Sentence: {sentence}, Document ID: {document_id}, Vector: {vector}")