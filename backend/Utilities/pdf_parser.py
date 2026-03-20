# utilities/pdf_parser.py
import sys
from pathlib import Path

# Add parent directory to path so we can import config
sys.path.insert(0, str(Path(__file__).parent.parent))

import fitz  # PyMuPDF
from typing import List, Dict
import re


class PDFParser:
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
    
    def extract_text(self, pdf_path: Path) -> List[Dict]:
        """
        Extract text from PDF and return list of chunks with metadata.
        Each chunk contains: text, source, page, chunk_index
        """
        doc = fitz.open(pdf_path)
        chunks = []
        
        for page_num, page in enumerate(doc):
            text = page.get_text().strip()
            
            if not text:
                continue
            
            # Split into paragraphs (double newline)
            paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
            
            # Further split long paragraphs into chunks
            page_chunks = self._chunk_paragraphs(paragraphs)
            
            for idx, chunk_text in enumerate(page_chunks):
                chunks.append({
                    "text": chunk_text,
                    "metadata": {
                        "source": pdf_path.name,
                        "page": page_num + 1,  # 1-based for humans
                        "chunk_index": idx
                    }
                })
        
        doc.close()
        return chunks
    
    def _chunk_paragraphs(self, paragraphs: List[str]) -> List[str]:
        """
        Combine paragraphs into chunks of ~chunk_size characters with overlap.
        """
        chunks = []
        current_chunk = []
        current_length = 0
        
        for para in paragraphs:
            para_len = len(para)
            
            # If single paragraph exceeds chunk_size, split it
            if para_len > self.chunk_size:
                # First, flush any pending content
                if current_chunk:
                    chunks.append(" ".join(current_chunk))
                    # Keep overlap for next chunk
                    overlap_text = " ".join(current_chunk)[-self.chunk_overlap:]
                    current_chunk = [overlap_text] if len(overlap_text) > 10 else []
                    current_length = sum(len(c) for c in current_chunk)
                
                # Split long paragraph by sentences
                sentences = re.split(r'(?<=[.!?])\s+', para)
                for sent in sentences:
                    if current_length + len(sent) > self.chunk_size:
                        if current_chunk:
                            chunks.append(" ".join(current_chunk))
                        # Start new chunk with overlap
                        overlap = " ".join(current_chunk)[-self.chunk_overlap:] if current_chunk else ""
                        current_chunk = [overlap, sent] if overlap else [sent]
                        current_length = sum(len(c) for c in current_chunk)
                    else:
                        current_chunk.append(sent)
                        current_length += len(sent) + 1
            
            # Normal paragraph that fits
            elif current_length + para_len > self.chunk_size:
                # Flush current chunk
                chunks.append(" ".join(current_chunk))
                # Start new chunk with overlap from previous
                overlap_text = " ".join(current_chunk)[-self.chunk_overlap:]
                current_chunk = [overlap_text, para] if len(overlap_text) > 10 else [para]
                current_length = sum(len(c) for c in current_chunk)
            else:
                current_chunk.append(para)
                current_length += para_len + 1
        
        # Don't forget last chunk
        if current_chunk:
            final_text = " ".join(current_chunk)
            if final_text.strip():
                chunks.append(final_text)
        
        return chunks


# Quick test function
def test_parser():
    from config import PDF_DIR

    parser = PDFParser(chunk_size=500, chunk_overlap=50)
    
    # Check for PDFs
    pdf_files = list(PDF_DIR.glob("*.pdf"))
    if not pdf_files:
        print(f"No PDFs found in {PDF_DIR}")
        print("Please copy your travel_agency_content.pdf there")
        return
    
    for pdf_path in pdf_files:
        print(f"\n{'='*50}")
        print(f"Processing: {pdf_path.name}")
        print(f"{'='*50}")
        
        chunks = parser.extract_text(pdf_path)
        
        print(f"Total chunks: {len(chunks)}")
        print(f"\nFirst 3 chunks:\n")
        
        for i, chunk in enumerate(chunks[:3]):
            print(f"--- Chunk {i+1} (Page {chunk['metadata']['page']}) ---")
            print(chunk['text'][:200] + "..." if len(chunk['text']) > 200 else chunk['text'])
            print(f"Length: {len(chunk['text'])} chars\n")


if __name__ == "__main__":
    test_parser()