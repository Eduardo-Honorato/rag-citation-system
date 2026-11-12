# Planejamento do Sistema RAG com Citação

## Visão Geral
Sistema Retrieval-Augmented Generation (RAG - Geração Aumentada por Recuperação) que permite:
- Ingestão de documentos de várias fontes
- Indexação semântica usando embeddings
- Busca similaridade para recuperação de contexto
- Geração de respostas com citação de fontes

## Estrutura de Pastas
```
meu-rag/
├── docs/              # Documentos de entrada (PDFs, TXT, etc.)
├── data/              # Dados intermediários (embeddings, índices)
├── app/
│   ├── ingest.py      # Script de ingestão
│   ├── search.py      # Script de busca
│   ├── generate.py    # Script de geração com citações
│   └── app.py         # Interface Streamlit
├── requirements.txt   # Dependências Python
└── .streamlit/        # Configurações do Streamlit
```

## Passo a Passo

### Passo 1: Instalar Dependências
```
pip install streamlit sentence-transformers faiss-cpu
```

### Passo 2: Preparar Documentos
Colocar documentos na pasta `docs/`. Formatos suportados: PDF, TXT, MD.

### Passo 3: Executer Ingestão (ingest.py)
O script:
1. Lê todos os documentos da pasta `docs/`
2. Divide em chunks (tamanho configurable)
3. Gera embeddings usando sentence-transformers
4. Salva embeddings e índice FAISS em `data/`

### Passo 4: Buscar (search.py)
O script:
1. Recebe uma query do usuário
2. Gera embedding da query
3. Busca os k mais similares no índice FAISS
4. Retorna os chunks com suas fontes/orígem

### Passo 5: Gerar Resposta (generate.py)
O script:
1. Recebe a query e os chunks recuperados
2. Monta prompt com contexto + query
3. Usa um LLM (ou modelo local) para gerar resposta
4. Inclui citação das fontes usadas

### Passo 6: Interface Web (app.py)
Interface Streamlit que:
1. Permite upload de documentos
2. Exibe campo de busca
3. Mostra resultados da busca com fontes
4. Mostra resposta gerada com citações

### Passo 7: Testar e Validar
- Testar com diferentes tipos de documentos
- Verificar se as citações estão corretas
- Validar que a busca retorna resultados relevantes