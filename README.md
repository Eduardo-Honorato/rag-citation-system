# Sistema RAG com Citações

## Apresentação

Este projeto implementa um sistema completo de Retrieval-Augmented Generation (RAG - Geração Aumentada por Recuperação) utilizando Streamlit como interface web. O sistema permite o upload e processamento de documentos, indexação semântica utilizando FAISS e geração de respostas com citações das fontes origem.

O sistema foi desenvolvido para proporcionar buscas semânticas em documentos pessoais ou corporativos, retornando respostas fundamentadas com referências diretas aos trechos relevantes encontrados nos documentos originais.

## Arquitetura do Sistema

O sistema consiste em três componentes principais:

1. **Módulo de Ingestão (ingest.py)**
   - Leitura de documentos nos formatos PDF, TXT e MD
   - Extração de texto usando pdfminer.six e leitura padrão
   - Divisão do texto em chunks com tamanho e sobreposição configuráveis
   - Geração de embeddings utilizando modelo Sentence-Transformers (all-MiniLM-L6-v2 por padrão)
   - Salvamento de embeddings e metadados em formato numpy e JSON

2. **Módulo de Indexação e Busca (search.py)**
   - Criação de índice FAISS (IndexFlatIP) para busca de similaridade por produto interno
   - Geração de embedding para queries do usuário
   - Busca de top-k chunks mais similares usando index.search()
   - Retorno de resultados com scores de similaridade e índices dos chunks

3. **Módulo de Geração de Resposta (generate.py)**
   - Construção de prompt utilizando os chunks recuperados como contexto
   - Geração de resposta fundamentada apenas nos documentos fornecidos
   - Criação de estrutura de citações com identificadores, fontes e números de chunk
   - Resposta simulada para demonstração ou integração com LLM real em produção

## fluxo de trabalho

1. **Upload e Processamento**
   - Uploader documentos → Ingestão (botão "Indexar Documentos")
   - O sistema lê os documentos da pasta especificada
   - Textos são extraídos e divididos em chunks gerenciáveis
   - Embeddings são gerados para cada chunk
   - Índice FAISS é construído e salvo

2. **Busca Semântica**
   - Usuário digita uma pergunta no campo de busca
   - Embedding da query é gerado utilizando o mesmo modelo
   - Índice FAISS é pesquisado para encontrar os k chunks mais similares
   - Resultados são exibidos com scores de similaridade

3. **Geração de Resposta**
   - Usuário clica em "Gerar Resposta com Citação"
   - Response é gerada baseada nos chunks recuperados
   - Fontes são listadas com identificadores, nomes dos arquivos e números de chunk

## Instalação

### Pré-requisitos

- Python 3.8 ou superior
- Pip (gerenciador de pacotes Python)

### Passo a passo

1. **Clonar o repositório** (ou baixar os arquivos do projeto)

2. **Criar ambiente virtual** (recomendado)

   ```bash
   python -m venv .venv
   ```

3. **Ativar o ambiente virtual**

   - No Windows:
     ```
     .venv\Scripts\activate
     ```

   - No macOS/Linux:
     ```
     source .venv/bin/activate
     ```

4. **Instalar dependências**

   ```bash
   pip install -r requirements.txt
   ```

   As dependências principais incluem:
   - **streamlit**: Framework para interfaces web interativas em Python
   - **faiss-cpu**: Facebook AI Similarity Search para indexação e busca vetorial
   - **sentence-transformers**: Modelos de embeddings para transformação de texto em vetores
   - **pdfminer.six**: Extração de texto de arquivos PDF
   - **numpy**: Operações numéricas para processamento de embeddings

5. **Executar o aplicativo**

   ```bash
   streamlit run app/app.py
   ```

   O aplicativo será disponibilizado em: http://localhost:8501

## Utilização

### Interface

Ao iniciar o aplicativo, será apresentada uma barra lateral à esquerda com as seguintes funcionalidades:

- **Área de logo 3D animada** no topo da sidebar
- **Pastas de documentos**: Campo de texto para especificar o diretório contendo os documentos a serem indexados (padrão: "docs")
- **Configurações de indexação**:
  - Tamanho do chunk: Define o tamanho dos fragmentos de texto (padrão: 500, faixa: 100-1000)
  - Sobreposição do chunk: Define a sobreposência entre chunks consecutivos (padrão: 50, faixa: 0-200)
- **Botão "Indexar Documentos"**: Processa todos os documentos da pasta especificada
- **Chips de status**: Indicam se o índice foi construído e quantos documentos foram processados

### Área Principal

Após o índice ser construído, a área principal exibirá:

- **Status ativo**: Indica que o sistema está pronto para buscas
- **Campo de busca**: Digite sua pergunta para buscar nos documentos indexados
- **Seletor de resultados**: Número de resultados a retornar (1-10, padrão: 4)
- **Botão "Buscar"**: Executa a busca semântica
- **Expansores de resultados**: Cada resultado mostra o arquivo, score de similaridade e preview do conteúdo
- **Citações**: Informações sobre os trechos selecionados com numeração
- **Botão "Gerar Resposta com Citação"**: Gera uma resposta fundamentada nos documentos encontrados

### Passos para uso típico

1. Coloque seus documentos (PDF, TXT, MD) na pasta especificada ou informe o caminho
2. Clique em "Indexar Documentos" na barra lateral
3. Aguarde o processamento - o sistema extrairá texto, gerará embeddings e construirá o índice FAISS
4. Digite sua pergunta no campo de busca
5. Ajuste o número de resultados desejados
6. Clique em "Buscar" para encontrar chunks relevantes
7. Clique em "Gerar Resposta com Citação" para obter uma resposta com fontes citadas

## Estrutura de Arquivos

```
rag-citation-system/
├── app/
│   ├── app.py              # Interface principal Streamlit
│   ├── ingest.py          # Módulo de ingestão e processamento de documentos
│   ├── search.py          # Módulo de busca semântica com FAISS
│   └── generate.py        # Módulo de geração de resposta com citações
├── data/                  # Pasta para índices gerados (faiss_index.bin, embeddings.npy, metadata.json)
├── docs/                  # Pasta para documentos de origem (PDFs, TXTs, MDs)
├── .gitignore            # Arquivo para ignorar arquivos de cache e ambientes virtuais
├── requirements.txt       # Dependências Python
└── README.md              # Documentação do projeto
```

## Requisitos

Consulte o arquivo `requirements.txt` para a lista completa de dependências. Os pacotes essenciais são:

- streamlit >= 1.28.0
- faiss-cpu >= 1.7.0
- sentence-transformers >= 2.2.0
- pdfminer.six >= 20231117
- numpy >= 1.24.0

## Contribuição

Contribuições são bem-vindas! Para contribuir:

1. Faça um fork do repositório
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas alterações (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## Licença

Este projeto está licenciado sob a licença MIT - consulte o arquivo LICENSE para obter mais detalhes.

## Contato

**Desenvolvedor**: Eduardo Honorato

Para mais informações, acesse o repositório oficial ou abra uma issue no GitHub.

---

Sistema RAG com Citação - Interface Streamlit para busca semântica com fontes