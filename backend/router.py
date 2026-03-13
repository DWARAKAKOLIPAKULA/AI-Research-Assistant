# from backend.rag_pipeline import build_rag
# from backend.web_search import tavily_search
# from backend.decomposition import decompose_query

# rag = build_rag()

# RAG_KEYWORDS = [
#     # document/research keywords
#     "documentation", "manual", "guide", "reference", "how to", "what is",
#     "research", "paper", "document", "langchain", "pdf", "rag", "retriever",
#     "vector store", "embedding","database","sql","truncate","alter","delete","update"
#     # git keywords
#     "git", "command", "commands", "branch", "commit", "merge", "push",
#     "pull", "clone", "rebase", "stash", "checkout",
#     # general
#     "explain", "describe", "tell", "show", "list", "define", "summarize"
# ]

# def is_rag_query(query):
#     return any(keyword in query.lower() for keyword in RAG_KEYWORDS)

# def handle_query(query):

#     if is_rag_query(query):
#         # ✅ Decompose into sub-questions and answer each via RAG
#         sub_questions = decompose_query(query)

#         if not sub_questions:
#             # fallback if decomposition returns nothing
#             return rag.invoke({"question": query})

#         answers = []
#         for sq in sub_questions:
#             if sq.strip():
#                 print(f"\nProcessing sub-question: {sq}")
#                 answer = rag.invoke({"question": sq})
#                 answers.append(f"Q: {sq}\nA: {answer}")

#         return "\n\n".join(answers)  # ✅ return combined answer

#     else:
#         # ✅ Web search for everything else
#         return tavily_search(query)

from backend import llm
from backend.rag_pipeline import build_rag
from backend.web_search import tavily_search

rag = build_rag()

PDF_KEYWORDS = [
    "git", "command", "commands", "branch", "commit", "merge", "push",
    "pull", "clone", "rebase", "stash", "checkout", "repository", "repo",
    "tag", "fetch", "diff", "log", "status", "init", "remote",
    "sql", "truncate", "alter", "delete", "insert", "update", "select",
    "database", "table", "query", "schema", "index"
]

def handle_query(query):
    if any(keyword in query.lower() for keyword in PDF_KEYWORDS):
        answer = rag.invoke({"question": query})
        if "could not find" in answer.lower():
            print(f"Not in PDF, searching web...")
            return tavily_search(query)
        return answer
    else:
        return tavily_search(query)
