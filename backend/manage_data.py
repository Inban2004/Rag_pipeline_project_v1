#!/usr/bin/env python3
"""
Database Management CLI for AlfaOverseas RAG System

Usage:
    python manage_data.py --status              Show current database status
    python manage_data.py --reset                Reset (clear) entire database
    python manage_data.py --rebuild             Rebuild from all PDFs in data/pdfs/
    python manage_data.py --add <pdf_file>      Add specific PDF(s)
    python manage_data.py --remove <source>     Remove PDF by source name
    python manage_data.py --query <question>    Test query

Examples:
    python manage_data.py --status
    python manage_data.py --reset
    python manage_data.py --rebuild
    python manage_data.py --add data/pdfs/my_document.pdf
    python manage_data.py --remove my_document.pdf
    python manage_data.py --query "What services do you offer?"
"""

import sys
from pathlib import Path
import argparse

sys.path.insert(0, str(Path(__file__).parent))

from Database.chroma_store import ChromaStore
from config import PDF_DIR


def status(store: ChromaStore):
    """Show database status."""
    store.get_detailed_stats(verbose=True)


def reset(store: ChromaStore):
    """Reset entire database."""
    confirm = input("Are you sure you want to RESET the database? (yes/no): ")
    if confirm.lower() == "yes":
        store.reset_db(verbose=True)
    else:
        print("Reset cancelled.")


def rebuild(store: ChromaStore):
    """Rebuild database from all PDFs in data/pdfs/."""
    pdf_files = list(PDF_DIR.glob("*.pdf"))
    
    if not pdf_files:
        print(f"\nNo PDFs found in {PDF_DIR}")
        print("Please add PDF files to data/pdfs/ first.")
        return
    
    print(f"\nFound {len(pdf_files)} PDF(s) in {PDF_DIR}:")
    for f in pdf_files:
        print(f"  - {f.name}")
    
    confirm = input("\nProceed with rebuild? (yes/no): ")
    if confirm.lower() == "yes":
        store.rebuild_from_pdfs(pdf_files, verbose=True)
    else:
        print("Rebuild cancelled.")


def add_pdf(store: ChromaStore, pdf_path: str):
    """Add specific PDF(s) to database."""
    path = Path(pdf_path)
    
    if not path.exists():
        print(f"[ERROR] File not found: {pdf_path}")
        return
    
    if path.is_dir():
        pdf_files = list(path.glob("*.pdf"))
        if not pdf_files:
            print(f"[ERROR] No PDFs found in directory: {pdf_path}")
            return
        print(f"\nFound {len(pdf_files)} PDF(s):")
        for f in pdf_files:
            print(f"  - {f.name}")
        confirm = input("\nAdd all PDFs? (yes/no): ")
        if confirm.lower() == "yes":
            for pdf in pdf_files:
                print(f"\n--- Processing: {pdf.name} ---")
                store.rebuild_from_pdfs([pdf], verbose=True)
    else:
        if not path.suffix.lower() == ".pdf":
            print(f"[WARNING] File does not have .pdf extension: {pdf_path}")
        
        print(f"\n--- Processing: {path.name} ---")
        store.rebuild_from_pdfs([path], verbose=True)


def remove_source(store: ChromaStore, source_name: str):
    """Remove PDF by source name."""
    sources = store.list_sources()
    
    if source_name not in sources:
        print(f"\n[ERROR] Source not found: {source_name}")
        print("\nAvailable sources:")
        for src in sources:
            print(f"  - {src}")
        return
    
    print(f"\nRemoving all chunks from: {source_name}")
    confirm = input("Are you sure? (yes/no): ")
    
    if confirm.lower() == "yes":
        deleted = store.remove_by_source(source_name, verbose=True)
        print(f"\nDeleted {deleted} chunks from {source_name}")
    else:
        print("Remove cancelled.")


def test_query(store: ChromaStore, question: str):
    """Test a query against the database."""
    print(f"\n--- Testing Query ---")
    print(f"Question: {question}")
    print("-" * 50)
    
    results = store.query(question, n_results=3)
    
    if not results["documents"][0]:
        print("No results found.")
        return
    
    print(f"\nTop {len(results['documents'][0])} results:\n")
    for i, (doc, meta, dist) in enumerate(zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0]
    )):
        print(f"--- Result {i+1} (similarity: {1-dist:.4f}) ---")
        print(f"Source: {meta['source']}, Page {meta['page']}")
        print(f"Content: {doc[:300]}{'...' if len(doc) > 300 else ''}")
        print()


def list_pdfs():
    """List available PDFs in data/pdfs/."""
    pdf_files = list(PDF_DIR.glob("*.pdf"))
    
    print(f"\nPDFs in {PDF_DIR}:")
    if pdf_files:
        for f in pdf_files:
            size_kb = f.stat().st_size / 1024
            print(f"  - {f.name} ({size_kb:.1f} KB)")
    else:
        print("  (empty)")
    
    return pdf_files


def main():
    parser = argparse.ArgumentParser(
        description="Database Management CLI for AlfaOverseas RAG System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    parser.add_argument("--status", action="store_true", help="Show database status")
    parser.add_argument("--reset", action="store_true", help="Reset (clear) entire database")
    parser.add_argument("--rebuild", action="store_true", help="Rebuild from all PDFs in data/pdfs/")
    parser.add_argument("--add", metavar="PDF", help="Add PDF file or directory")
    parser.add_argument("--remove", metavar="SOURCE", help="Remove PDF by source name")
    parser.add_argument("--query", metavar="TEXT", help="Test a query")
    parser.add_argument("--list", action="store_true", help="List PDFs in data/pdfs/")
    
    args = parser.parse_args()
    
    if not any(vars(args).values()):
        parser.print_help()
        print("\n" + "=" * 50)
        print("Quick Reference:")
        print("=" * 50)
        list_pdfs()
        store = ChromaStore()
        sources = store.list_sources()
        print(f"\nDatabase contains {store.collection.count()} chunks from:")
        for src in sources:
            print(f"  - {src}")
        return
    
    store = ChromaStore()
    
    if args.status:
        status(store)
    elif args.reset:
        reset(store)
    elif args.rebuild:
        rebuild(store)
    elif args.add:
        add_pdf(store, args.add)
    elif args.remove:
        remove_source(store, args.remove)
    elif args.query:
        test_query(store, args.query)
    elif args.list:
        list_pdfs()


if __name__ == "__main__":
    main()
