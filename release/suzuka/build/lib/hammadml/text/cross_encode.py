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

    def rank(self, query: str, x: List[str], y: List[str]) -> List[Tuple[str, str, float]]:
        """
        Re-ranks pairs formed by two lists of chunks based on their relevance to a single query using the CrossEncoder model.

        Parameters
        ----------
        query : str
            The query to use for re-ranking
        x : List[str]
            The first list of chunks
        y : List[str]
            The second list of chunks

        Returns
        -------
        List[Tuple[str, str, float]]
            A list of ranked pairs with their scores
        """
        if not x:
            return [(y_item, 0) for y_item in y]
        if not y:
            return [(x_item, 0) for x_item in x]

        if len(x) == 1:
            x = x * len(y)
        if len(y) == 1:
            y = y * len(x)
            
        min_length = min(len(x), len(y))
        x = x[:min_length]
        y = y[:min_length]
        pairs = [(query, chunk1 + " " + chunk2) for chunk1, chunk2 in zip(x, y)]
        scores = self.model.predict(pairs)
        ranked_pairs = [(x[i], y[i], score) for i, score in sorted(enumerate(scores), key=lambda x: x[1], reverse=True)]
        return ranked_pairs

if __name__ == "__main__":
    cross_encode = CrossEncode()
    
    query = "What is the capital of France?"
    x = ["Paris is the capital", "London is the capital"]
    y = ["of France", "of England"]
    
    ranked_pairs = cross_encode.rank(query, x, y)
    print(f"Re-ranked pairs for query '{query}':")
    for pair in ranked_pairs:
        print(f"{pair[0]} {pair[1]} (Score: {pair[2]:.2f})")