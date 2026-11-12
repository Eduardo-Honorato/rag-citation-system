#!/usr/bin/env python3
"""
generate.py - Generate a response with citations based on retrieved chunks.

Usage:
    python generate.py --query "sua pergunta" --chunks "chunk1, chunk2" --metadata "./data/metadata.json"

This script:
1. Takes a user query and retrieved chunks
2. Constructs a prompt with context and citation requirements
3. Generates a response using a LLM (or template for demo)
4. Includes proper citations from the source documents
"""

import argparse
import json
import os
from pathlib import Path


def load_metadata(data_dir):
    """Load metadata from the data directory."""
    metadata_path = os.path.join(data_dir, "metadata.json")
    if os.path.exists(metadata_path):
        with open(metadata_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def generate_response(query, chunks, metadata, model_name="claude-3-5-sonnet"):
    """
    Generate a response with citations based on the query and retrieved chunks.

    In a production setup, this would use an LLM API. For this demo, we'll
    construct a formatted response with proper citations.
    """
    # Build the context from chunks with citations
    context_parts = []
    citations = []

    for i, chunk_info in enumerate(chunks):
        source = chunk_info.get("source", "desconhecido")
        chunk_idx = chunk_info.get("chunk_index", i)
        text = chunk_info.get("text", "")

        # Add to context
        context_parts.append(f"[Trecho {i+1} - {source}]: {text}")

        # Track citation
        citations.append({
            "id": i + 1,
            "source": source,
            "chunk": chunk_idx
        })

    context = "\n\n".join(context_parts)

    # Construct the prompt for the LLM
    prompt = f"""Você é um assistente que responde perguntas baseado exclusivamente em documentos fornecidos.

IMPORTANTE: Você deve responder apenas baseado nos trechos abaixo e deve citar as fontes usando o formato [¹], [²], etc. correspondente à ordem dos trechos.

CONTEXTO DOS DOCUMENTOS:
{context}

PERGUNTA DO USUÁRIO: {query}

INSTRUÇÕES:
1. Responda à pergunta baseado apenas no contexto acima
2. Cite as fontes usando números entre colchetes, ex: [¹], [²]
3. Se a informação não estiver nos documentos, declare que não tem informação nos documentos disponíveis
4. Não alucine ou use conhecimento externo

SUA RESPOSTA:"""

    # Simulated response - in production, this would call an LLM
    response = generate_simulated_response(query, context, citations)

    return response, citations


def generate_simulated_response(query, context, citations):
    """Generate a simulated response for demonstration purposes."""
    # Check if we have any meaningful context
    if not context.strip():
        return "Não encontrei informações relevantes nos documentos fornecidos para responder à sua pergunta."

    # Simple extraction: return the most relevant part with citation
    # In a real system, this would use an LLM to generate a proper answer

    # For demo, just return a summary indicating what was found
    sources_list = ", ".join([f"[^{c['id']}^{c['source']}]" for c in citations])

    return f"""Baseado nos documentos disponíveis, aqui está o que pude encontrar:

{sources_list}

A resposta seria gerada por um modelo de linguagem (como Claude ou GPT-4) que teria acesso ao contexto acima e geraria uma resposta fundamentada com as devidas citações."""

def main():
    parser = argparse.ArgumentParser(description="Generate response with citations")
    parser.add_argument("--query", required=True, help="User query")
    parser.add_argument("--data", default="./data", help="Directory containing metadata")
    parser.add_argument("--chunks", type=int, default=4, help="Number of chunks to use")
    parser.add_argument("--model", default="claude-3-5-sonnet", help="LLM model name")

    args = parser.parse_args()

    print("=" * 60)
    print("RAG System - Response Generation")
    print("=" * 60)

    # Load metadata
    metadata = load_metadata(args.data)
    print(f"Loaded {len(metadata)} metadata entries")

    # Query
    query = args.query
    print(f"\nQuery: {query}")

    # In a real system, we would search first, then generate
    # For this demo, we'll use all metadata entries as "retrieved chunks"
    chunks = metadata[:args.chunks]

    # Generate response
    response, citations = generate_response(query, chunks, metadata, args.model)

    print(f"\nGenerated Response:")
    print("-" * 60)
    print(response)
    print("-" * 60)

    print(f"\nCitations:")
    for cite in citations:
        print(f"  {cite['id']}: {cite['source']} (chunk {cite['chunk']})")

    print("=" * 60)


if __name__ == "__main__":
    main()