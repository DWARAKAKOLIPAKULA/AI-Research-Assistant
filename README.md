# AI Research Assistant

## Overview

This is an **AI-powered research assistant** built with LangChain, LangGraph, and RAG techniques. Processes PDFs, builds FAISS vector store, handles complex queries via decomposition → routing → RAG/web search.

**Current: LangGraph workflow** on PDFs like `sql handwritten notes.pdf`, `git commands.pdf`.

## Detailed Implementation (Step-by-Step)

### 1. PDF Ingestion (`backend/ingestion.py`)
```
PyPDFLoader(pdf_path) → RecursiveCharacterTextSplitter(1000/200) → 
HuggingFaceEmbeddings(all-MiniLM-L6-v2) → FAISS.from_documents() → save_local("vector_store")
```
- Loads PDF text, chunks with overlap, embeds, stores locally.

### 2. Retriever Setup (`backend/retriever.py`)
```
FAISS.load_local("vector_store", embeddings) → as_retriever(k=5)
```
- Loads index for similarity search.

### 3. LLM (`backend/llm.py`)
```
ChatGroq(model="llama-3.1-8b-instant", temperature=0.7)
```
- Primary model; env: `GROQ_API_KEY`.

### 4. RAG Pipeline (`backend/rag_pipeline.py`)
```
{question} → retriever → rerank_documents(top_k=5) → 
prompt|llm|StrOutputParser()
```
- **Reranker** (`backend/reranker.py`): CrossEncoder('ms-marco-MiniLM-L-6-v2') scores query-doc pairs, sorts top 5.
- Prompt: "Answer using ONLY context or 'could not find'".
- Returns concise string.

### 5. Query Router (`backend/router.py`)
```
if PDF_KEYWORDS (git/sql terms) in query.lower():
  rag.invoke(query)
  if "could not find": tavily_search(query)
else:
  tavily_search(query)
```
- Keywords: git commands, SQL ops (truncate/alter/etc.).

### 6. Decomposition (`backend/decomposition.py`)
```
Prompt → llm → split("\n") → [2-4 clean sub-questions]
```
- e.g., "SQL JOINs?" → ["What is INNER JOIN?", "What is LEFT JOIN?", ...]

### 7. Web Search (`backend/web_search.py`)
```
TavilyClient.search(query, depth="advanced", max_results=3) → "\n\n".join(contents)
```
- Requires `TAVILY_API_KEY`; fallback for non-PDF topics.

### 8. LangGraph Workflow (`backend/langgraph_workflow.py`)
```
StateGraph(GraphState: question/answer/sub_questions)
decompose_node → answer_node (handle_query each sub) → END
```
- Entry: Original question → decompose → for each sub: router/rag/web → join answers.

### 9. Main Entry (`main.py`)
```
ingest_pdf(pdf_path)
graph = build_graph()
result = graph.invoke({"question": input()})
print(result["answer"])
```

**Full Flow**: User query → decompose → subs → router (rag/web per sub) → formatted answer.

## Architecture Diagram (ASCII)

```
┌──────────────┐
│   PDF Input  │
└──────┬───────┘
       ↓
┌──────────────┐
│   Ingestion  │  ← PyPDF/Split/Embed/FAISS
│ (vector_store)│
└──────┬───────┘
       │
┌──────────────┐
│  User Query  │
└──────┬───────┘
       ↓
┌──────────────┐
│  LangGraph   │
└──────┬───────┘
       ↓
┌──────────────┐
│  Decompose   │  ← Query → 2-4 Sub-questions
└──────┬───────┘
       ↓
     ┌──────────────┐
     │ For Each Sub │
     └──────┬───────┘
            ↓
     ┌──────────────┐
     │   Router     │
     └──────┬───────┘
    /              \
   ↓                ↓
RAG                Web
(Store+Rerank+LLM)  Search
   │                │    ↑
   └──────┬───────┘    │ "No info"
          ↓            │
   ┌──────────────┐   │
   │  handle_query │◄──┘
   └──────┬───────┘
          ↓
┌──────────────┐
│ Join Answers │
└──────┬───────┘
       ↓
┌──────────────┐
│ Final Output │
└──────────────┘
```

**Notes**: 
- Router uses PDF_KEYWORDS for RAG vs Tavily.
- Fallback `direct_answer` (no decompose) defined but unused.
- Mermaid version above for GitHub/VSCode preview.


- **PDF Ingestion**: Extract text, chunk, embed, and store in local FAISS vector store.
- **Query Decomposition**: Break down complex questions.
- **Smart Routing**: RAG for internal docs, web search (DuckDuckGo/Google) for fresh info.
- **Agentic Workflow**: LangGraph orchestrates retrieval, decomposition, routing.
- **Local Setup**: Runs offline (except LLM API keys and optional web search).

## Quick Start

### 1. Clone & Setup Environment

```bash
# Create virtual environment (recommended)
python -m venv venv
venv\\Scripts\\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

### 2. Set Environment Variables

Create `.env`:

```
GROQ_API_KEY=your_groq_key_here
TAVILY_API_KEY=your_tavily_key_here  # For web search
# OPENAI_API_KEY=... (alt LLM)
# PINECONE_API_KEY=... (opt)
```

Auto-loaded via `dotenv`.

### 3. Ingest PDF

Place your PDF (e.g., `your_notes.pdf`) in root, then run:

```bash
python main.py
```

It auto-ingests `sql handwritten notes.pdf` (edit `main.py` for others).

### 4. Query

After ingestion:
```
Ask your question: What are JOIN types in SQL?
```

**Sample Output**:
```
Answer: [Structured response with sub-questions, RAG/web results]
```

## Project Structure

```
AI RESEARCH ASSISTANT/
├── main.py                 # Entry point: ingest + query loop
├── requirements.txt        # Dependencies
├── vector_store/           # FAISS index (auto-created)
├── backend/
│   ├── ingestion.py     # 1. PDF→FAISS
│   ├── retriever.py     # 2. Load retriever
│   ├── llm.py           # 3. Groq Llama
│   ├── rag_pipeline.py  # 4. RAG + rerank
│   ├── router.py        # 5. rag/web route
│   ├── decomposition.py # 6. Query→subs
│   ├── reranker.py      # CrossEncoder rerank
│   ├── web_search.py    # 7. Tavily
│   └── langgraph_workflow.py # 8. Graph
└── *.pdf                # Docs: git/sql notes
```

## Development

- Edit `pdf_path` in `main.py`.
- Switch workflows: Comment/uncomment imports in `main.py`.
- Vector store regenerates on ingestion.
- Test: `python main.py`

## Troubleshooting

- **No vector store**: Run ingestion first.
- **LLM errors**: Check API keys in `.env`.
- **Embeddings slow**: Uses `all-MiniLM-L6-v2`; GPU optional via Torch.
- **Windows paths**: Use `\\` or raw strings.

## Future Enhancements

- Multi-PDF support.
- UI (Streamlit/Gradio).
- Advanced agents/tools.


