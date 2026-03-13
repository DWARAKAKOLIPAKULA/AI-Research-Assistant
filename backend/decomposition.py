from backend.llm import load_llm
from langchain_core.prompts import ChatPromptTemplate

llm = load_llm()

def decompose_query(query):
    prompt = ChatPromptTemplate.from_template("""
You are an AI assistant that breaks complex questions into simpler sub-questions.

Break the following question into 1-2 simple sub-questions.
Return ONLY the sub-questions, one per line, no numbering, no bullets, no extra text.

Question: {query}

Sub-questions:
""")
    # ✅ removed "1." from prompt — curly braces in numbered lists break LangChain templates

    chain = prompt | llm

    response = chain.invoke({"query": query})

    # ✅ Extract text from AIMessage
    text = response.content.strip()

    # ✅ Clean up and split into list
    sub_questions = [q.strip() for q in text.split("\n") if q.strip()]

    print(f"\nDecomposed into {len(sub_questions)} sub-questions:")
    for sq in sub_questions:
        print(f"  → {sq}")

    return sub_questions