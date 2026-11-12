# Sistema RAG com Citação - Instruções de Execução

## Estrutura do Projeto
```
meu-rag/
├── planejamento-rag-citacao.md  # Planejamento detalhado
├── requirements.txt               # Dependências Python
├── docs/                         # Pasta de documentos de entrada
├── data/                         # Índice FAISS e embeddings (gerado automaticamente)
└── app/
    ├── ingest.py                 # Script de ingestão de documentos
    ├── search.py                 # Script de busca semântica
    ├── generate.py               # Script de geração de respostas com citações
    └── app.py                    # Interface web Streamlit
```

## 1. Instalar Dependências

Execute este comando para instalar todas as dependências necessárias:

```powershell
pip install streamlit sentence-transformers faiss-cpu pdfminer.six python-dotenv
```

**Já instalado neste ambiente:**
- faiss-cpu 1.16.0
- streamlit 1.67.0
- sentence-transformers 6.3.0
- pdfminer.six (já incluso)
- python-dotenv (já incluso)

## 2. Preparar Documentos

Coloque seus documentos na pasta `docs/`. Formatos suportados:
- `.pdf` - Arquivos PDF
- `.txt` - Arquivos de texto simples
- `.md` - Markdown

**Exemplo:** Adicione um arquivo de teste:
```powershell
echo "Seu texto aqui" > C:\Users\eduar\meu-rag\docs\meu-doc.txt
```

## 3. Indexar Documentos

Execute o script de ingestão para processar os documentos e criar o índice FAISS:

```powershell
cd C:\Users\eduar\meu-rag
python app\ingest.py --docs ./docs --output ./data
```

**Parâmetros opcionais:**
- `--chunk-size`: Tamanho do chunk (padrão: 500)
- `--chunk-overlap`: Sobreposição entre chunks (padrão: 50)
- `--model`: Modelo sentence-transformers (padrão: all-MiniLM-L6-v2)

**Resultado:** Os arquivos serão criados em `./data/`:
- `faiss_index.bin` - Índice FAISS para busca vetorial
- `embeddings.npy` - Vetores de embeddings
- `metadata.json` - Metadados com informações de origem

## 4. Iniciar Interface Web

Execute o aplicativo Streamlit:

```powershell
cd C:\Users\eduar\meu-rag
& "C:\Users\eduar\AppData\Roaming\Python\Python314\Scripts\streamlit.exe" run "C:\Users\eduar\meu-rag\app\app.py"
```

**Ou simplesmente:**
```powershell
streamlit run app/app.py
```

O aplicativo será aberto em: **http://localhost:8501**

## 5. Usando a Interface

A interface Streamlit oferece as seguintes funcionalidades:

### Barra Lateral:
- **Pasta de documentos**: Defina o caminho (padrão: `docs/`)
- **Tamanho do chunk**: Ajuste o tamanho dos fragmentos de texto
- **Sobreposição do chunk**: Defina a sobreposagem entre chunks consecutivos
- **Indexar Documentos**: Processa todos os documentos da pasta e cria o índice
- **Reiniciar**: Limpa o estado atual

### Área Principal:
- **Buscar em documentos**: Digite sua pergunta e clique em "Buscar"
- **Resultados**: Visualize os chunks mais similares com arquivos de origem e scores de similaridade
- **Gerar Resposta**: Clique para gerar uma resposta fundamentada com citações das fontes

### Fluxo de Trabalho:

1. **Indexar**: Adicione documentos na pasta `docs/` e clique em "Indexar Documentos"
2. **Buscar**: Digite uma pergunta relacionada aos seus documentos
3. **Resultados**: Veja os chunks mais relevantes com scores de similaridade
4. **Gerar**: Clique em "Gerar Resposta" para obter uma resposta com citações formatadas

## 6. Exemplos

### Busca:
```
Query: "inteligência artificial"
Retorna: Chunks do documento teste.txt com score de similaridade 0.4857
```

### Geração de Resposta:
```
Query: "O que é RAG?"
Resposta: "Baseado nos documentos disponíveis, aqui está o que pude encontrar: [¹]..."
Citações: [1]: teste.txt (chunk 0)
```

## 7. Solução de Problemas

### Se aparecer erro de memória:
Reduza o `--chunk-size` nos parâmetros do ingestão.

### Se os documentos não serem encontrados:
- Verifique se a pasta `docs/` existe
- Certifique-se de que os arquivos têm extensões `.pdf`, `.txt` ou `.md`
- Verifique se os arquivos não estão corrompidos

### Se a busca retornar resultados irrelevantes:
- Ajuste o `--chunk-size` e `--chunk-overlap`
- Tente diferentes modelos sentence-transformers
- Aumente o número de resultados (`--k` na busca)

## Arquivos Importantes

- `app/ingest.py` - Processa e indexa documentos
- `app/search.py` - Busca no índice FAISS
- `app/generate.py` - Gera respostas com citações
- `app/app.py` - Interface Streamlit web
- `requirements.txt` - Dependências Python
- `planejamento-rag-citacao.md` - Planejamento detalhado