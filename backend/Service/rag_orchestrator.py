# service/rag_orchestrator.py
import sys
from pathlib import Path

# Add parent directory to path so we can import config
sys.path.insert(0, str(Path(__file__).parent.parent))

from typing import Dict, List
from Database.chroma_store import ChromaStore
from Service.generation_service import GenerationService
from Service.embedding_service import EmbeddingService
from config import TOP_K_RESULTS


class RAGOrchestrator:
    """
    The brain of the RAG pipeline.
    Coordinates: Embed query → Retrieve from Chroma → Generate answer.
    """
    
    def __init__(self):
        self.chroma = ChromaStore()
        self.embedder = EmbeddingService()
        self.generator = GenerationService()
        self.top_k = TOP_K_RESULTS
    
    def answer(self, question: str) -> Dict:
        """
        End-to-end RAG: question → answer with sources.
        """
        print(f"\n🔍 Processing question: '{question}'")
        
        # Step 1: Embed the question
        print("  1. Embedding query...")
        query_embedding = self.embedder.embed_query(question)
        
        # Step 2: Retrieve relevant chunks
        print(f"  2. Retrieving top {self.top_k} chunks from Chroma...")
        results = self.chroma.collection.query(
            query_embeddings=[query_embedding],
            n_results=self.top_k,
            include=["documents", "metadatas", "distances"]
        )
        
        # Extract results (Chroma returns lists of lists)
        chunks = results["documents"][0]
        metadatas = results["metadatas"][0]
        distances = results["distances"][0]
        
        if not chunks:
            return {
                "answer": "I don't have any relevant documents to answer this question.",
                "sources": [],
                "chunks_used": 0,
                "confidence": "none"
            }
        
        print(f"     Found {len(chunks)} relevant chunks")
        for i, (chunk, dist) in enumerate(zip(chunks, distances)):
            print(f"     [{i+1}] Distance: {dist:.4f} | {metadatas[i]['source']} p{metadatas[i]['page']}")
        
        # Step 3: Generate answer with context
        print("  3. Generating answer with LLM...")
        generation_result = self.generator.generate_with_context(
            question=question,
            context_chunks=chunks,
            metadatas=metadatas
        )
        
        # Add retrieval metadata
        generation_result["retrieval_confidence"] = {
            "best_distance": min(distances),
            "avg_distance": sum(distances) / len(distances)
        }
        
        return generation_result
    
    def ingest_pdf(self, pdf_path: str) -> Dict:
        """
        Helper: Parse PDF and add to Chroma.
        """
        from Utilities.pdf_parser import PDFParser
        from pathlib import Path
        
        parser = PDFParser()
        path = Path(pdf_path)
        
        if not path.exists():
            return {"error": f"File not found: {pdf_path}"}
        
        print(f"\n📄 Ingesting: {path.name}")
        chunks = parser.extract_text(path)
        
        if not chunks:
            return {"error": "No text extracted from PDF"}
        
        # Use ChromaStore's add_documents (which uses embedding service internally)
        added = self.chroma.add_documents(chunks)
        
        return {
            "file": path.name,
            "chunks_added": added,
            "total_docs_in_db": self.chroma.get_stats()["total_documents"]
        }
    
    def get_stats(self) -> Dict:
        """Quick stats about the RAG system."""
        return {
            "chroma_stats": self.chroma.get_stats(),
            "embedding_model": self.embedder.model,
            "llm_model": self.generator.model,
            "top_k_retrieval": self.top_k
        }


# Full pipeline test
def test_rag_pipeline():
    orchestrator = RAGOrchestrator()
    
    # Show stats
    print("="*50)
    print("RAG System Stats:")
    print("="*50)
    stats = orchestrator.get_stats()
    print(f"Documents in DB: {stats['chroma_stats']['total_documents']}")
    print(f"Embedding model: {stats['embedding_model']}")
    print(f"LLM model: {stats['llm_model']}")
    
    # Test query
    print("\n" + "="*50)
    print("Testing RAG Query")
    print("="*50)
    
    question = "What services does AlfaOverseas offer?"
    result = orchestrator.answer(question)
    
    print("\n" + "="*50)
    print("RESULT:")
    print("="*50)
    print(f"Answer: {result['answer']}")
    print(f"Sources: {', '.join(result['sources'])}")
    print(f"Confidence score: {result['retrieval_confidence']['best_distance']:.4f}")


if __name__ == "__main__":
    test_rag_pipeline()