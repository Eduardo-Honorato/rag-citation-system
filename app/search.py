#!/usr/bin/env python3
"""
search.py - Search the FAISS index for similar documents.

Usage:
    python search.py --query "sua pergunta aqui" --data ./data --k 4

This script:
1. Loads the FAISS index and metadata from the data directory
2. Generates an embedding for the query
3. Searches for the k most similar chunks
4. Returns the results with source information
"""

import argparse
import json
import os
import numpy as np
from pathlib import Path

from sentence_transformers import SentenceTransformer

import faiss


def load_index(data_dir):
    """Load the FAISS index, embeddings, and metadata from disk."""
    index_path = os.path.join(data_dir, "faiss_index.bin")
    embeddings_path = os.path.join(data_dir, "embeddings.npy")
    metadata_path = os.path.join(data_dir, "metadata.json")

    if not os.path.exists(index_path):
        raise FileNotFoundError(f"FAISS index not found at {index_path}")
    if not os.path.exists(embeddings_path):
        raise FileNotFoundError(f"Embeddings not found at {embeddings_path}")
    if not os.path.exists(metadata_path):
        raise FileNotFoundError(f"Metadata not found at {metadata_path}")

    # Load FAISS index
    index = faiss.read_index(index_path)

    # Load embeddings
    embeddings = np.load(embeddings_path)

    # Load metadata
    with open(metadata_path, "r", encoding="utf-8") as f:
        metadata = json.load(f)

    return index, embeddings, metadata


def search(query, data_dir, k=4, model_name="all-MiniLM-L6-v2"):
    """Search for the k most similar chunks to the query."""
    # Load index and metadata
    index, embeddings, metadata = load_index(data_dir)

    # Generate query embedding
    print(f"Generating embedding for query: '{query[:50]}...'")
    model = SentenceTransformer(model_name)
    query_embedding = model.encode([query], convert_to_numpy=True)

    # Normalize query embedding for inner product similarity
    faiss.normalize_L2(query_embedding)

    # Search
    print(f"Searching top {k} results...")
    scores, indices = index.search(query_embedding, k)

    # Format results
    results = []
    for score, idx in zip(scores[0], indices[0]):
        if idx < len(metadata):
            result = metadata[idx]
            result["similarity_score"] = float(score)
            # Text will be loaded separately or shown from source
            results.append(result)

    return results, indices, scores


def main():
    parser = argparse.ArgumentParser(description="Search RAG index for similar documents")
    parser.add_argument("--query", required=True, help="Search query")
    parser.add_argument("--data", default="./data", help="Directory containing the FAISS index")
    parser.add_argument("--k", type=int, default=4, help="Number of results to return")
    parser.add_argument("--model", default="all-MiniLM-L6-v2", help="Sentence-transformers model name")

    args = parser.parse_args()

    print("=" * 60)
    print("RAG System - Document Search")
    print("=" * 60)

    # Load chunks from the first result's context
    # We need to also load the original chunks - they're not stored in metadata alone
    # Let's re-read them from the source documents or store them differently

    # Search
    results, indices, scores = search(args.query, args.data, k=args.k, model_name=args.model)

    print(f"\nQuery: {args.query}")
    print(f"\nTop {len(results)} results:\n")

    for i, result in enumerate(results):
        print(f"--- Result {i+1} ---")
        print(f"Arquivo: {result.get('source', 'N/A')}")
        print(f"Similaridade: {result.get('similarity_score', 'N/A'):.4f}")
        print(f"Texto: {result.get('text', '')[:200]}...")
        print()

    print("=" * 60)


if __name__ == "__main__":
    main()