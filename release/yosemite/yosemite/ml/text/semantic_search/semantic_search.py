from sentence_transformers import SentenceTransformer, util
import torch
from typing import List, Tuple

class SemanticSearch:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Constructs all the necessary attributes for the SemanticSearch object.

        Parameters
        ----------
        model_name : str, optional
            The name of the SentenceTransformer model to use (default is "all-MiniLM-L6-v2")
        """
        self.model = SentenceTransformer(model_name)

    def encode_corpus(self, corpus: List[str]) -> torch.Tensor:
        """
        Encodes a list of sentences into embeddings.

        Parameters
        ----------
        corpus : List[str]
            The list of sentences to encode

        Returns
        -------
        torch.Tensor
            A tensor containing the embeddings of the sentences
        """
        return self.model.encode(corpus, convert_to_tensor=True)

    def search(self, query: str, corpus_embeddings: torch.Tensor, corpus: List[str], top_k: int = 5) -> List[Tuple[str, float]]:
        """
        Performs semantic search on a list of sentences.

        Parameters
        ----------
        query : str
            The query sentence
        corpus_embeddings : torch.Tensor
            The embeddings of the corpus sentences
        corpus : List[str]
            The list of sentences to search
        top_k : int, optional
            The number of results to return (default is 5)

        Returns
        -------
        List[Tuple[str, float]]
            A list of tuples, each containing a sentence from the corpus and its similarity score to the query
        """
        query_embedding = self.model.encode(query, convert_to_tensor=True)
        cos_scores = util.cos_sim(query_embedding, corpus_embeddings)[0]
        
        # Check if top_k is within the valid range
        top_k = min(top_k, len(corpus))
        
        top_results = torch.topk(cos_scores, k=top_k)
        return [(corpus[idx], score.item()) for score, idx in zip(top_results[0], top_results[1])]

if __name__ == "__main__":
    semantic_search = SemanticSearch()
    
    corpus = [
        "Paris is the capital of France.",
        "London is the capital of England.",
        "Berlin is the capital of Germany.",
    ]
    corpus_embeddings = semantic_search.encode_corpus(corpus)
    
    query = "What is the capital of France?"
    
    # Check if the corpus is empty
    if len(corpus) == 0:
        print("Corpus is empty. Please provide a non-empty corpus.")
    else:
        results = semantic_search.search(query, corpus_embeddings, corpus)
        
        for sentence, score in results:
            print(f"{sentence} (Score: {score:.2f})")