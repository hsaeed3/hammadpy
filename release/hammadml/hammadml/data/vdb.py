from hammadml.text.util import Embedder, Chunker
from hammadml.data.db import Database
from hammadpy.core import Text
from typing import Union, List, Tuple, Optional
import os
import uuid
from annoy import AnnoyIndex

class VectorDatabase:
    def __init__(self, dimension: Optional[int] = None):
        self.text = Text()
        self.index = None
        self.dimension = dimension
        self.document_ids = []
        self.sentences = []
        self.vectors = []

    def load(self, index_path: str):
        if not os.path.isfile(index_path):
            raise FileNotFoundError(f"Index file not found: {index_path}")

        self.index = AnnoyIndex(self.dimension, 'angular')
        self.index.load(index_path)

    def create(self, input_data: Union[str, List[str], List[Tuple[str, list]]],
               model_name: str = "all-MiniLM-L6-v2", num_trees: int = 10):
        if isinstance(input_data, str):
            if os.path.isdir(input_data):
                self.sentences, self.document_ids = self._load_sentences_from_directory(input_data)
            else:
                raise ValueError("Invalid input_data. Expected a directory path.")
        elif isinstance(input_data, list):
            if all(isinstance(item, str) for item in input_data):
                chunker = Chunker()
                self.sentences = [sentence for text in input_data for sentence in chunker.chunk_text(text)]
                self.document_ids = [str(uuid.uuid4()) for _ in self.sentences]
            elif all(isinstance(item, tuple) and len(item) == 2 for item in input_data):
                self.sentences, self.vectors = zip(*input_data)
                self.document_ids = [str(uuid.uuid4()) for _ in input_data]
            else:
                raise ValueError("Invalid input_data. Expected a list of strings or a list of tuples.")
        else:
            raise ValueError("Invalid input_data. Expected a directory path, a list of strings, or a list of tuples.")

        if not self.dimension:
            self.dimension = len(self.vectors[0]) if self.vectors else Embedder(model_name).model.get_sentence_embedding_dimension()

        self.index = AnnoyIndex(self.dimension, 'angular')

        if self.vectors:
            for i, vector in enumerate(self.vectors):
                self.index.add_item(i, vector)
        else:
            embedder = Embedder(model_name)
            for i, sentence in enumerate(self.sentences):
                vector = embedder.embed([sentence])[0][1]
                self.index.add_item(i, vector)

        self.index.build(num_trees)

    def _load_sentences_from_directory(self, directory: str) -> Tuple[List[str], List[str]]:
        sentences = []
        document_ids = []
        chunker = Chunker()
        for file_name in os.listdir(directory):
            if file_name.endswith(".txt"):
                file_path = os.path.join(directory, file_name)
                with open(file_path, "r", encoding="utf-8") as file:
                    content = file.read().strip()
                    sentences.extend(chunker.chunk_text(content))
                    document_ids.extend([str(uuid.uuid4()) for _ in chunker.chunk_text(content)])
        return sentences, document_ids
    
    def create_from_database(self, db_path: str, model_name: str = "all-MiniLM-L6-v2", num_trees: int = 10):
        self.db = Database()
        self.db.load(db_path)
        embedder = Embedder(model_name)
        
        self.sentences = []
        self.document_ids = []
        self.vectors = []
        
        for doc in self.db.ix.searcher().documents():
            self.sentences.append(doc["content"])
            self.document_ids.append(doc["id"])
            self.vectors.append(embedder.embed([doc["content"]])[0][1])
        
        if not self.dimension:
            self.dimension = len(self.vectors[0])
        
        self.index = AnnoyIndex(self.dimension, 'angular')
        for i, vector in enumerate(self.vectors):
            self.index.add_item(i, vector)
        self.index.build(num_trees)

    def search_database(self, query: str, k: int = 5):
        if not self.index:
            raise ValueError("Index has not been built. Please call create_from_database() first.")

        embedder = Embedder("all-MiniLM-L6-v2")
        query_vector = embedder.embed([query])[0][1]
        indices = self.index.get_nns_by_vector(query_vector, k, include_distances=False)
        results = []
        for index in indices:
            sentence = self.sentences[index]
            document_id = self.document_ids[index]
            vector = self.index.get_item_vector(index)
            results.append((index, sentence, document_id, vector))
        return results

    def search(self, query: str, k: int = 5) -> List[Tuple[int, str, str, List[float]]]:
        if not self.index:
            raise ValueError("Index has not been built or loaded.")

        embedder = Embedder("all-MiniLM-L6-v2")
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
    # Example 1: Create a vector database from a list of sentences
    sentences = [
        "This is the first sentence.",
        "This is the second sentence.",
        "This is the third sentence.",
        "This is the fourth sentence.",
        "This is the fifth sentence."
    ]

    vdb_sentences = VectorDatabase()
    vdb_sentences.create(sentences)

    search_query = "third"
    search_results = vdb_sentences.search(search_query)

    print("Example 1: Search results for a list of sentences")
    print(f"Search query: '{search_query}'")
    for index, sentence, document_id, _ in search_results:
        print(f"Index: {index}")
        print(f"Document ID: {document_id}")
        print(f"Sentence: {sentence}")
        print()

    # Example 2: Create a vector database from loaded documents
    """
    db = Database()
    db.create()
    db.load_docs("./data")

    vdb_docs = VectorDatabase()
    vdb_docs.create_from_database("./databases/db")

    search_query = "test"
    search_results = vdb_docs.search_database(search_query)

    print("Example 2: Search results for loaded documents")
    print(f"Search query: '{search_query}'")
    for index, sentence, document_id, _ in search_results:
        print(f"Index: {index}")
        print(f"Document ID: {document_id}")
        print(f"Sentence: {sentence}")
        print()
    """