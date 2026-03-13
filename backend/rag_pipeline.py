from backend.retriever import get_retriever
from backend.llm import load_llm
from backend.reranker import rerank_documents
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

def build_rag():
    retriever = get_retriever()
    llm = load_llm()

    template = """
You are an AI research assistant.

Answer the question using ONLY the context below.

If the answer is not present in the context, say:
"I could not find this information in the provided documents."

Context:
{context}

Question:
{question}

Answer clearly and concisely.
"""
    prompt = ChatPromptTemplate.from_template(template)

    # ✅ Explicitly extract the string before passing to retriever
    extract_question = RunnableLambda(lambda x: x["question"])

    def retrieve_and_rerank(question):
        docs = retriever.invoke(question)
        reranked = rerank_documents(question, docs, top_k=3)
        return "\n\n".join([doc.page_content for doc in reranked])
    
    rerank_step = RunnableLambda(retrieve_and_rerank)

    rag_pipeline = (
        {
            "context": extract_question | retriever,  # ✅ string goes into retriever
            "question": extract_question              # ✅ string goes into prompt
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    return rag_pipeline