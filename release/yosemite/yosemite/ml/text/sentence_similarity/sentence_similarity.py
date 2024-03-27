from sentence_transformers import SentenceTransformer, util
from typing import List, Tuple

class SentenceSimilarity:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Constructs all the necessary attributes for the SentenceSimilarity object.

        Parameters
        ----------
        model_name : str, optional
            The name of the SentenceTransformer model to use (default is "all-MiniLM-L6-v2")
        """
        self.model = SentenceTransformer(model_name)

    def compute_similarity(self, sentences1: List[str], sentences2: List[str]) -> List[Tuple[str, str, float]]:
        """
        Computes the cosine similarity between two lists of sentences.

        Parameters
        ----------
        sentences1 : List[str]
            The first list of sentences
        sentences2 : List[str]
            The second list of sentences

        Returns
        -------
        List[Tuple[str, str, float]]
            A list of tuples, each containing a pair of sentences and their cosine similarity
        """
        embeddings1 = self.model.encode(sentences1, convert_to_tensor=True)
        embeddings2 = self.model.encode(sentences2, convert_to_tensor=True)
        cosine_scores = util.cos_sim(embeddings1, embeddings2)
        return [(sentences1[i], sentences2[j], cosine_scores[i][j].item()) for i in range(len(sentences1)) for j in range(len(sentences2))]

if __name__ == "__main__":
    sentence_similarity = SentenceSimilarity()
    
    sentences1 = [
        "The cat is sitting on the mat.",
        "The dog is playing in the park.",
    ]
    sentences2 = [
        "A feline is resting on the rug.",
        "A canine is running in the garden.",
    ]
    
    similarities = sentence_similarity.compute_similarity(sentences1, sentences2)
    for sentence1, sentence2, score in similarities:
        print(f"{sentence1} - {sentence2} (Similarity: {score:.2f})")