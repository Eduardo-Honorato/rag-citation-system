# RAG System with Citations

A Streamlit-based Retrieval-Augmented Generation (RAG) system that enables semantic document search with source citations. The system allows users to upload documents, index them using FAISS vector search, and query them to get answers with proper source references.

## 📋 Project Overview

This project implements a complete RAG (Retrieval-Augmented Generation) pipeline:

1. **Document Ingestion** - Upload and process PDF, TXT, and MD files
2. **Text Chunking** - Split documents into manageable chunks with configurable overlap
3. **Embedding Generation** - Create vector embeddings using Sentence-Transformers
4. **Vector Indexing** - Build FAISS index for fast similarity search
5. **Semantic Search** - Find relevant document chunks based on query semantics
6. **Response Generation** - Generate answers with proper source citations

## ✨ Features

- **📁 Document Support**: PDF, TXT, and MD file formats
- **🔍 Semantic Search**: Vector-based similarity search using FAISS
- **📄 Source Citations**: Each answer includes source document references
- **🎨 Modern UI**: Dark mode interface with animated visual elements
- **⚡ Fast Indexing**: Optimized document processing pipeline
- **🔒 Local-First**: All processing happens locally - no API keys required

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Git (optional, for version control)

### 1. Clone or Download

```bash
git clone https://github.com/Eduardo-Honorato/rag-citation-system.git
cd rag-citation-system
```

### 2. Create Virtual Environment

```bash
# Using venv (recommended)
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
streamlit run app/app.py
```

The app will be available at `http://localhost:8501`

## 📦 Project Structure

```
rag-citation-system/
├── app/
│   ├── app.py              # Main Streamlit application
│   ├── ingest.py          # Document ingestion and embedding
│   ├── search.py          # FAISS search functionality
│   └── generate.py        # Response generation with citations
├── data/                   # Generated index files (added to .gitignore)
├── docs/                   # Source documents directory
├── .gitignore             # Git ignore rules
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation
```

## 🛠️ Requirements

See `requirements.txt` for the full list of dependencies, but the key packages include:

- **streamlit**: Web interface framework
- **faiss-cpu**: Facebook AI Similarity Search for vector indexing
- **sentence-transformers**: Sentence embedding model (all-MiniLM-L6-v2 by default)
- **pdfminer.six**: PDF text extraction
- **numpy**: Numerical operations
- **json**: Metadata handling

## 📚 How It Works

### Ingestion Flow

1. User uploads documents (PDF, TXT, MD) via the sidebar
2. System extracts text from each document
3. Text is split into chunks with configurable size and overlap
4. Sentence-transformers model generates embeddings for each chunk
5. FAISS index is built for fast similarity search
6. Index and metadata are saved to `./data/` directory

### Search Flow

1. User enters a query in the search box
2. Query embedding is generated using the same model
3. FAISS index searches for top-k similar chunks
4. Retrieved chunks are used as context for response generation
5. Response is generated with proper source citations

### Response Generation

1. Retrieved chunks provide contextual information
2. LLM (or simulated response) generates answer based on context
3. Source citations are formatted and displayed
4. Answer includes references to original document chunks

## 🔧 Configuration

### Adjustable Parameters (via Sidebar)

- **Tamanho do chunk**: Size of text chunks (default: 500)
- **Sobreposição do chunk**: Overlap between consecutive chunks (default: 50)
- **Número de resultados**: How many search results to return (default: 4)

### Default Model

The system uses `all-MiniLM-L6-v2` from Sentence-Transformers, which provides good quality embeddings with fast inference. This model converts text to 384-dimensional vectors.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📧 Contact

**Eduardo Honorato** - [GitHub Profile](https://github.com/Eduardo-Honorato)

Project Link: [https://github.com/Eduardo-Honorato/rag-citation-system](https://github.com/Eduardo-Honorato/rag-citation-system)

---

**Generated with** [Claude Code](https://claude.com/claude-code)