from typing import List, Tuple
from sentence_transformers import CrossEncoder

class CrossEncode:
    def __init__(self, model_name: str = "cross-encoder/ms-marco-MiniLM-L-12-v2", max_length: int = None):
        """
        Initializes the CrossEncode with a specified model.

        Parameters
        ----------
        model_name : str, optional
            The name of the CrossEncoder model to use (default is "cross-encoder/ms-marco-MiniLM-L-12-v2")
        max_length : int, optional
            The maximum length of the input sequences (default is None)
        """
        self.model = CrossEncoder(model_name, max_length=max_length)

    def rank(self, query: str, x: List[str], y: List[str]) -> List[Tuple[str, float]]:
        """
        Re-ranks sentences formed by combining two lists based on their relevance to a single query using the CrossEncoder model.

        Parameters
        ----------
        query : str
            The query to use for re-ranking
        x : List[str]
            The first list of sentences
        y : List[str]
            The second list of sentences

        Returns
        -------
        List[Tuple[str, float]]
            A list of ranked sentences with their scores
        """
        sentences = x + y
        if not sentences:
            return []

        scores = self.model.predict([(query, sentence) for sentence in sentences])

        ranked_sentences = [(sentence, score) for sentence, score in sorted(zip(sentences, scores), key=lambda x: x[1], reverse=True)]

        return ranked_sentences

if __name__ == "__main__":
    cross_encode = CrossEncode()
    
    query = "What is the capital of France?"
    x = ["Paris is the capital", "London is the capital"]
    y = ["of France", "of England"]
    
    ranked_sentences = cross_encode.rank(query, x, y)
    print(ranked_sentences)