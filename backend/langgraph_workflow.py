from langgraph.graph import StateGraph, END
from typing import TypedDict
from backend.web_search import tavily_search
from backend.decomposition import decompose_query
from backend.rag_pipeline import build_rag
from backend.router import handle_query

rag = build_rag()

PDF_KEYWORDS = [
    "documentation", "manual", "guide", "reference", "how to", "what is",
    "research", "paper", "document", "langchain", "pdf", "rag", "retriever",
    "vector store", "embedding","database","sql","truncate","alter","delete","update"
]

class GraphState(TypedDict):
    question: str
    answer: str
    sub_questions: list

def decompose_node(state):
    # ✅ Only decompose the ORIGINAL question once
    sub_questions = decompose_query(state["question"])
    return {"sub_questions": sub_questions}

def answer_node(state):
    if not state["sub_questions"]:
        answer = handle_query(state["question"])
        return {"answer": answer}

    answers = []
    for sq in state["sub_questions"]:
        if sq.strip():
            print(f"\nProcessing: {sq}")
            # ✅ Directly invoke RAG — NO decomposition here
            answer = handle_query(sq)
            answers.append(f"**{sq}**\n{answer}")

    return {"answer": "\n\n---\n\n".join(answers)}

def direct_answer(query):
    """Answer directly — RAG or web, NO decomposition"""
    if any(keyword in query.lower() for keyword in PDF_KEYWORDS):
        answer = rag.invoke({"question": query})
        if "could not find" in answer.lower():
            return tavily_search(query)
        return answer
    else:
        return tavily_search(query)

def build_graph():
    graph = StateGraph(GraphState)
    graph.add_node("decompose", decompose_node)
    graph.add_node("answer", answer_node)
    graph.set_entry_point("decompose")
    graph.add_edge("decompose", "answer")
    graph.add_edge("answer", END)
    return graph.compile()