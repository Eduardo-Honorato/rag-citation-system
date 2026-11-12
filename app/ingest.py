#!/usr/bin/env python3
"""
ingest.py - Ingest documents and create FAISS index with embeddings.

Usage:
    python ingest.py --docs ./docs --output ./data

This script:
1. Reads all documents from the docs/ directory
2. Chunks them into manageable pieces
3. Generates embeddings using sentence-transformers
4. Saves embeddings and FAISS index to the output directory
"""

import argparse
import os
import sys
import json
import glob
from pathlib import Path

# PDF parsing
try:
    from pdfminer.high_level import extract_text
except ImportError:
    print("pdfminer.six not installed. Installing...")
    import subprocess
    subprocess.run([sys.executable, "-m", "pip", "install", "pdfminer.six"])
    from pdfminer.high_level import extract_text

from sentence_transformers import SentenceTransformer
import faiss
import numpy as np


def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file."""
    try:
        text = extract_text(str(pdf_path))
        return text
    except Exception as e:
        print(f"Warning: Could not extract text from {pdf_path}: {e}")
        return ""


def extract_text_from_txt(txt_path):
    """Extract text from a TXT file."""
    try:
        with open(txt_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        print(f"Warning: Could not read {txt_path}: {e}")
        return ""


def chunk_text(text, chunk_size=500, chunk_overlap=50):
    """Split text into chunks with overlap."""
    if not text:
        return []

    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = min(start + chunk_size, text_length)
        chunk = text[start:end]
        chunks.append(chunk)
        start += chunk_size - chunk_overlap

    return chunks


def ingest_documents(docs_dir, chunk_size=500, chunk_overlap=50):
    """Ingest all documents from a directory."""
    all_chunks = []
    doc_metadata = []

    # Find all supported files
    pdf_files = glob.glob(os.path.join(docs_dir, "*.pdf"))
    txt_files = glob.glob(os.path.join(docs_dir, "*.txt"))
    md_files = glob.glob(os.path.join(docs_dir, "*.md"))

    print(f"Found {len(pdf_files)} PDFs, {len(txt_files)} TXTs, {len(md_files)} MDs")

    # Process PDFs
    for pdf_path in pdf_files:
        print(f"Processing: {os.path.basename(pdf_path)}")
        text = extract_text_from_pdf(pdf_path)
        if text.strip():
            chunks = chunk_text(text, chunk_size, chunk_overlap)
            for i, chunk in enumerate(chunks):
                all_chunks.append(chunk)
                doc_metadata.append({
                    "source": os.path.basename(pdf_path),
                    "chunk_index": i,
                    "file": os.path.basename(pdf_path)
                })

    # Process TXT files
    for txt_path in txt_files:
        print(f"Processing: {os.path.basename(txt_path)}")
        text = extract_text_from_txt(txt_path)
        if text.strip():
            chunks = chunk_text(text, chunk_size, chunk_overlap)
            for i, chunk in enumerate(chunks):
                all_chunks.append(chunk)
                doc_metadata.append({
                    "source": os.path.basename(txt_path),
                    "chunk_index": i,
                    "file": os.path.basename(txt_path)
                })

    # Process MD files
    for md_path in md_files:
        print(f"Processing: {os.path.basename(md_path)}")
        text = extract_text_from_txt(md_path)
        if text.strip():
            chunks = chunk_text(text, chunk_size, chunk_overlap)
            for i, chunk in enumerate(chunks):
                all_chunks.append(chunk)
                doc_metadata.append({
                    "source": os.path.basename(md_path),
                    "chunk_index": i,
                    "file": os.path.basename(md_path)
                })

    print(f"Total chunks created: {len(all_chunks)}")
    return all_chunks, doc_metadata


def create_embeddings(chunks, model_name="all-MiniLM-L6-v2"):
    """Create embeddings for text chunks using sentence-transformers."""
    print(f"Loading model: {model_name}")
    model = SentenceTransformer(model_name)

    print("Generating embeddings...")
    embeddings = model.encode(chunks, show_progress_bar=True, convert_to_numpy=True)

    return embeddings


def build_faiss_index(embeddings):
    """Build a FAISS index for vector similarity search."""
    dimension = embeddings.shape[1]
    print(f"Building FAISS index with dimension {dimension}")

    # Use IndexFlatIP for inner product (cosine similarity with normalized vectors)
    index = faiss.IndexFlatIP(dimension)
    index.add(embeddings)

    return index


def save_index(index, embeddings, metadata, output_dir):
    """Save the FAISS index, embeddings, and metadata to disk."""
    os.makedirs(output_dir, exist_ok=True)

    # Save FAISS index
    index_path = os.path.join(output_dir, "faiss_index.bin")
    faiss.write_index(index, index_path)
    print(f"Saved FAISS index to {index_path}")

    # Save embeddings
    embeddings_path = os.path.join(output_dir, "embeddings.npy")
    np.save(embeddings_path, embeddings)
    print(f"Saved embeddings to {embeddings_path}")

    # Save metadata
    metadata_path = os.path.join(output_dir, "metadata.json")
    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)
    print(f"Saved metadata to {metadata_path}")


def main():
    parser = argparse.ArgumentParser(description="Ingest documents and create FAISS index")
    parser.add_argument("--docs", default="./docs", help="Directory containing documents to ingest")
    parser.add_argument("--output", default="./data", help="Output directory for index")
    parser.add_argument("--chunk-size", type=int, default=500, help="Chunck size in tokens")
    parser.add_argument("--chunk-overlap", type=int, default=50, help="Chunck overlap in tokens")
    parser.add_argument("--model", default="all-MiniLM-L6-v2", help="Sentence-transformers model name")

    args = parser.parse_args()

    print("=" * 60)
    print("RAG System - Document Ingestion")
    print("=" * 60)

    # Step 1: Ingest documents
    chunks, metadata = ingest_documents(
        args.docs,
        chunk_size=args.chunk_size,
        chunk_overlap=args.chunk_overlap
    )

    if not chunks:
        print("Warning: No chunks were created. Check your documents directory.")
        sys.exit(1)

    # Step 2: Create embeddings
    embeddings = create_embeddings(chunks, args.model)

    # Step 3: Build FAISS index
    index = build_faiss_index(embeddings)

    # Step 4: Save everything
    save_index(index, embeddings, metadata, args.output)

    print("=" * 60)
    print("Ingestion complete!")
    print(f"Documents processed: {len(metadata)}")
    print(f"Chunks created: {len(chunks)}")
    print(f"Index saved to: {args.output}")
    print("=" * 60)


if __name__ == "__main__":
    main()