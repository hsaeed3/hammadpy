from typing import List, Tuple
from sentence_transformers import SentenceTransformer
import spacy

class Embedder:
    def __init__(self, model: str = "paraphrase-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model)

    def embed(self, sentences: List[str]) -> List[Tuple[str, List[float]]]:
        if not sentences:
            return []
        return [(sentence, self.model.encode(sentence)) for sentence in sentences]

class Chunker:
    def __init__(self, model: str = "en_core_web_sm"):
        self.nlp = spacy.load(model)

    def chunk_text(self, text: str) -> List[str]:
        if not text:
            return []
        doc = self.nlp(text)
        return [sent.text.strip() for sent in doc.sents]

if __name__ == "__main__":
    transformer = Embedder()
    sentences = ["This is a sample sentence.", "Here's another sentence."]
    embeddings = transformer.embed(sentences)
    print("Transformer Example:")
    for sentence, embedding in embeddings:
        print(f"Sentence: {sentence}")
        print(f"Embedding: {embedding}")
        print()

    chunker = Chunker()
    text = "This is a long text. It consists of multiple sentences. The Chunker class will split it into individual sentences."
    sentences = chunker.chunk_text(text)
    print("Chunker Example:")
    for sentence in sentences:
        print(sentence)