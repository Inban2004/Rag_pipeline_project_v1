# service/embedding_service.py
import sys
from pathlib import Path

# Add parent directory to path so we can import config
sys.path.insert(0, str(Path(__file__).parent.parent))


import requests
from typing import List, Union
from config import OLLAMA_HOST, EMBEDDING_MODEL


class EmbeddingService:
    """Clean wrapper for Ollama embedding API."""
    
    def __init__(self, model: str = EMBEDDING_MODEL, host: str = OLLAMA_HOST):
        self.model = model
        self.host = host
        self.endpoint = f"{host}/api/embeddings"
    
    def embed(self, text: str) -> List[float]:
        """
        Embed single text string.
        Returns: List of 768 floats (for nomic-embed-text)
        """
        response = requests.post(
            self.endpoint,
            json={"model": self.model, "prompt": text},
            timeout=30
        )
        response.raise_for_status()
        return response.json()["embedding"]
    
    def embed_batch(self, texts: List[str], show_progress: bool = True) -> List[List[float]]:
        """
        Embed multiple texts sequentially.
        For production: add threading/async here.
        """
        embeddings = []
        
        for i, text in enumerate(texts):
            if show_progress:
                print(f"  Embedding {i+1}/{len(texts)}...", end="\r")
            emb = self.embed(text)
            embeddings.append(emb)
        
        if show_progress:
            print(f"  Embedded {len(texts)} chunks complete.   ")
        
        return embeddings
    
    def embed_query(self, query: str) -> List[float]:
        """Special method for query embedding (same as embed, semantic clarity)."""
        return self.embed(query)


# Test
def test_embedding_service():
    service = EmbeddingService()
    
    # Single embed
    print("Testing single embed...")
    vec = service.embed("AlfaOverseas travel agency")
    print(f"Vector length: {len(vec)}")
    print(f"First 5 values: {vec[:5]}")
    
    # Batch embed
    print("\nTesting batch embed...")
    texts = [
        "Flight booking services",
        "Hotel reservations",
        "Adventure trekking packages"
    ]
    batch = service.embed_batch(texts)
    print(f"Batch result: {len(batch)} vectors, each length {len(batch[0])}")


if __name__ == "__main__":
    test_embedding_service()