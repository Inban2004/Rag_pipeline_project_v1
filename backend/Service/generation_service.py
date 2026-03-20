# service/generation_service.py

import sys
from pathlib import Path

# Add parent directory to path so we can import config
sys.path.insert(0, str(Path(__file__).parent.parent))

import requests
from typing import List, Dict
from config import OLLAMA_HOST, LLM_MODEL


class GenerationService:
    """Wrapper for Ollama text generation (qwen2.5:3b)."""
    
    def __init__(self, model: str = LLM_MODEL, host: str = OLLAMA_HOST):
        self.model = model
        self.host = host
        self.endpoint = f"{host}/api/generate"
    
    def generate(
        self,
        prompt: str,
        system: str = None,
        temperature: float = 0.7,
        max_tokens: int = 500
    ) -> str:
        """
        Generate text from prompt.
        
        Args:
            prompt: The main prompt
            system: Optional system message (instructions)
            temperature: 0.0=factual, 1.0=creative
            max_tokens: Limit response length
        """
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens
            }
        }
        
        if system:
            payload["system"] = system
        
        response = requests.post(self.endpoint, json=payload, timeout=60)
        response.raise_for_status()
        return response.json()["response"]
    
    def generate_with_context(
        self,
        question: str,
        context_chunks: List[str],
        metadatas: List[Dict] = None
    ) -> Dict:
        """
        RAG-specific generation: builds prompt from retrieved chunks.
        Returns: dict with answer and debug info
        """
        # Build context string
        context = "\n\n---\n\n".join([
            f"[Document {i+1}]: {chunk}" 
            for i, chunk in enumerate(context_chunks)
        ])

        # Check if we have relevant context
        has_context = len(context_chunks) > 0 and any(chunk.strip() for chunk in context_chunks)
        
        # RAG prompt template
        if has_context:
            prompt = f"""You are a helpful assistant for AlfaOverseas, a travel and visa consultancy service.

CONTEXT FROM OUR DOCUMENTS:
{context}

QUESTION: {question}

INSTRUCTIONS:
- Answer questions about our services, visa processes, travel planning, pricing, requirements ONLY using the context above
- For greetings (like "hi", "hello", "how are you", "hey"), respond warmly and briefly as a helpful assistant
- If the question cannot be answered from the provided context, respond with exactly: "I don't have enough information to answer that. Please try asking about our visa services, travel planning, or related topics."
- NEVER make up information not in the context above
- Keep responses concise and helpful

ANSWER:"""
        else:
            prompt = f"""You are a helpful assistant for AlfaOverseas, a travel and visa consultancy service.

GREETING/QUESTION: {question}

INSTRUCTIONS:
- For greetings, respond warmly and briefly as a helpful assistant
- If asked about specific services, pricing, visa details, or anything requiring specific information, respond with exactly: "I don't have enough information to answer that. Please try asking about our visa services, travel planning, or related topics."
- Keep responses brief and professional

ANSWER:"""
        
        answer = self.generate(
            prompt=prompt,
            system="You are AlfaOverseas assistant. Be helpful, brief, and professional. Only use information from provided context.",
            temperature=0.3,
            max_tokens=300
        )
        
        # Build sources for citation
        sources = []
        if metadatas and has_context:
            for meta in metadatas:
                sources.append(f"{meta.get('source', 'Unknown')}, Page {meta.get('page', '?')}")
        
        return {
            "answer": answer.strip(),
            "sources": list(set(sources)),
            "chunks_used": len(context_chunks) if has_context else 0
        }


# Test
def test_generation_service():
    service = GenerationService()
    
    # Simple generation
    print("Test 1: Simple generation")
    response = service.generate(
        "What is the capital of France?",
        temperature=0.1
    )
    print(f"Answer: {response}\n")
    
    # RAG-style with context
    print("Test 2: RAG with context")
    fake_chunks = [
        "AlfaOverseas offers flight bookings, hotel reservations, and complete itinerary planning.",
        "Adventure packages include trekking, scuba diving, and wildlife safaris."
    ]
    fake_metas = [
        {"source": "brochure.pdf", "page": 1},
        {"source": "brochure.pdf", "page": 2}
    ]
    
    result = service.generate_with_context(
        question="What adventure activities are available?",
        context_chunks=fake_chunks,
        metadatas=fake_metas
    )
    
    print(f"Answer: {result['answer']}")
    print(f"Sources: {result['sources']}")
    print(f"Chunks used: {result['chunks_used']}")


if __name__ == "__main__":
    test_generation_service()