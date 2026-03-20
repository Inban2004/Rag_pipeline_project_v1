# database/chroma_store.py

import sys
from pathlib import Path

# Add parent directory to path so we can import config
sys.path.insert(0, str(Path(__file__).parent.parent))


import chromadb
from chromadb.config import Settings
from typing import List, Dict, Optional
from config import CHROMA_DIR, COLLECTION_NAME, EMBEDDING_MODEL, OLLAMA_HOST
import requests


class ChromaStore:
    def __init__(self):
        # Persistent client (saves to disk)
        self.client = chromadb.PersistentClient(
            path=str(CHROMA_DIR),
            settings=Settings(
                anonymized_telemetry=False,  # Disable tracking
                allow_reset=True  # Allow deleting collections
            )
        )
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name=COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"}  # Similarity metric
        )
        
        self.ollama_host = OLLAMA_HOST
        self.embed_model = EMBEDDING_MODEL
    
    def _get_embedding(self, text: str) -> List[float]:
        """Get embedding from Ollama for single text."""
        response = requests.post(
            f"{self.ollama_host}/api/embeddings",
            json={
                "model": self.embed_model,
                "prompt": text
            }
        )
        response.raise_for_status()
        return response.json()["embedding"]
    
    def _get_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """Get embeddings for multiple texts (batch)."""
        # Ollama embeddings API doesn't natively batch, so we loop
        # For production, consider parallel requests
        embeddings = []
        for text in texts:
            emb = self._get_embedding(text)
            embeddings.append(emb)
        return embeddings
    
    def add_documents(self, chunks: List[Dict]) -> int:
        """
        Add chunks to ChromaDB.
        chunks: List of {"text": str, "metadata": dict}
        Returns: Number of documents added
        """
        if not chunks:
            return 0
        
        # Prepare data
        texts = [c["text"] for c in chunks]
        metadatas = [c["metadata"] for c in chunks]
        ids = [f"{m['source']}_p{m['page']}_c{m['chunk_index']}" 
               for m in metadatas]
        
        # Get embeddings via Ollama
        print(f"Generating embeddings for {len(texts)} chunks...")
        embeddings = self._get_embeddings_batch(texts)
        
        # Add to Chroma
        self.collection.add(
            embeddings=embeddings,
            documents=texts,
            metadatas=metadatas,
            ids=ids
        )
        
        return len(chunks)
    
    def query(self, query_text: str, n_results: int = 3) -> Dict:
        """
        Query the database with natural language.
        Returns: Chroma query results with documents, metadatas, distances
        """
        # Embed the query
        query_embedding = self._get_embedding(query_text)
        
        # Search
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            include=["documents", "metadatas", "distances"]
        )
        
        return results
    
    def get_stats(self) -> Dict:
        """Get collection statistics."""
        count = self.collection.count()
        return {
            "collection_name": COLLECTION_NAME,
            "total_documents": count,
            "chroma_dir": str(CHROMA_DIR)
        }
    
    def reset(self):
        """Delete all data (use with caution)."""
        self.client.delete_collection(COLLECTION_NAME)
        self.collection = self.client.get_or_create_collection(
            name=COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"}
        )
        return {"status": "reset", "collection": COLLECTION_NAME}
    
    def reset_db(self, verbose: bool = True):
        """Reset entire database - deletes all collections and data."""
        if verbose:
            print("=" * 50)
            print("RESETTING DATABASE")
            print("=" * 50)
            print(f"Deleting collection: {COLLECTION_NAME}")
        
        self.client.delete_collection(COLLECTION_NAME)
        
        if verbose:
            print(f"Creating new collection: {COLLECTION_NAME}")
        
        self.collection = self.client.get_or_create_collection(
            name=COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"}
        )
        
        result = {"status": "reset", "collection": COLLECTION_NAME, "documents_deleted": True}
        
        if verbose:
            print("Database reset complete!")
            print("=" * 50)
        
        return result
    
    def remove_by_source(self, source_name: str, verbose: bool = True) -> int:
        """Remove all chunks from a specific PDF/source."""
        if verbose:
            print(f"Finding chunks from: {source_name}")
        
        all_ids = self.collection.get(include=[])["ids"]
        ids_to_delete = [id for id in all_ids if id.startswith(f"{source_name}_")]
        
        if not ids_to_delete:
            if verbose:
                print(f"No chunks found for source: {source_name}")
            return 0
        
        if verbose:
            print(f"Found {len(ids_to_delete)} chunks to delete")
        
        self.collection.delete(ids=ids_to_delete)
        
        if verbose:
            print(f"Deleted {len(ids_to_delete)} chunks from {source_name}")
        
        return len(ids_to_delete)
    
    def list_sources(self) -> List[str]:
        """Get list of all unique PDF sources in the database."""
        all_metadatas = self.collection.get(include=["metadatas"])["metadatas"]
        sources = set()
        for meta in all_metadatas:
            if meta and "source" in meta:
                sources.add(meta["source"])
        return sorted(list(sources))
    
    def get_detailed_stats(self, verbose: bool = True) -> Dict:
        """Get detailed database statistics."""
        sources = self.list_sources()
        total = self.collection.count()
        
        stats = {
            "collection_name": COLLECTION_NAME,
            "total_chunks": total,
            "chroma_dir": str(CHROMA_DIR),
            "sources": []
        }
        
        for source in sources:
            all_ids = self.collection.get(include=[])["ids"]
            count = len([id for id in all_ids if id.startswith(f"{source}_")])
            stats["sources"].append({
                "name": source,
                "chunk_count": count
            })
        
        if verbose:
            print("=" * 50)
            print("DATABASE STATUS")
            print("=" * 50)
            print(f"Total chunks: {total}")
            print(f"Unique sources: {len(sources)}")
            for src in stats["sources"]:
                print(f"  - {src['name']}: {src['chunk_count']} chunks")
            print("=" * 50)
        
        return stats
    
    def rebuild_from_pdfs(self, pdf_paths: List[Path], verbose: bool = True) -> Dict:
        """Reset DB and ingest specific PDFs."""
        from Utilities.pdf_parser import PDFParser
        
        if verbose:
            print("=" * 50)
            print("REBUILDING DATABASE")
            print("=" * 50)
            print(f"Found {len(pdf_paths)} PDF(s) to ingest")
        
        self.reset_db(verbose=False)
        
        parser = PDFParser()
        total_added = 0
        
        for pdf_path in pdf_paths:
            if verbose:
                print(f"\nProcessing: {pdf_path.name}")
            
            if not pdf_path.exists():
                if verbose:
                    print(f"  [ERROR] File not found: {pdf_path}")
                continue
            
            chunks = parser.extract_text(pdf_path)
            
            if not chunks:
                if verbose:
                    print(f"  [WARNING] No text extracted from {pdf_path.name}")
                continue
            
            if verbose:
                print(f"  Extracted {len(chunks)} chunks")
                print(f"  Generating embeddings...")
            
            added = self.add_documents(chunks)
            total_added += added
            
            if verbose:
                print(f"  Added {added} chunks to database")
        
        final_stats = self.get_detailed_stats(verbose=False)
        
        if verbose:
            print("\n" + "=" * 50)
            print("REBUILD COMPLETE")
            print("=" * 50)
            print(f"Total chunks added: {total_added}")
            print(f"Sources: {len(final_stats['sources'])}")
            for src in final_stats['sources']:
                print(f"  - {src['name']}: {src['chunk_count']} chunks")
            print("=" * 50)
        
        return {
            "status": "rebuilt",
            "total_chunks": total_added,
            "sources": final_stats["sources"]
        }


# Test function
def test_chroma():
    from Utilities.pdf_parser import PDFParser
    from config import PDF_DIR
    
    store = ChromaStore()
    parser = PDFParser()
    
    # Check current stats
    print("Before ingestion:", store.get_stats())
    
    # Find PDFs
    pdf_files = list(PDF_DIR.glob("*.pdf"))
    if not pdf_files:
        print("No PDFs found!")
        return
    
    # Ingest
    total = 0
    for pdf_path in pdf_files:
        print(f"\nProcessing {pdf_path.name}...")
        chunks = parser.extract_text(pdf_path)
        added = store.add_documents(chunks)
        total += added
        print(f"Added {added} chunks")
    
    print(f"\nTotal added: {total}")
    print("After ingestion:", store.get_stats())
    
    # Test query
    print("\n" + "="*50)
    print("Testing query: 'What services does AlfaOverseas offer?'")
    print("="*50)
    
    results = store.query("What services does AlfaOverseas offer?", n_results=2)
    
    for i, (doc, meta, dist) in enumerate(zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0]
    )):
        print(f"\n--- Result {i+1} (distance: {dist:.4f}) ---")
        print(f"Source: {meta['source']}, Page {meta['page']}")
        print(doc[:300] + "..." if len(doc) > 300 else doc)


if __name__ == "__main__":
    test_chroma()