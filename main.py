# from backend.ingestion import ingest_pdf
# from backend.rag_pipeline import build_rag
# from backend.router import handle_query

# pdf_path = "git commands.pdf"

# ingest_pdf(pdf_path)

# rag = build_rag()

# query = input("Ask your question: ")

# answer = handle_query(query)  # returns a plain string



# print("\nAnswer:")
# print(answer)  # ✅ plain string, not response["answer"]

from backend.ingestion import ingest_pdf
from backend.langgraph_workflow import build_graph
import os
import shutil

pdf_path = "git commands.pdf"

if os.path.exists("vectorstore/faiss_index"):
    shutil.rmtree("vectorstore/faiss_index")
    print("Cleared old vector store")

ingest_pdf(pdf_path)

graph = build_graph()

print("\n🤖 AI Research Assistant Ready!")
print("Type 'exit' or 'quit' to stop.\n")

while True:
    query = input("You: ").strip()

    if not query:
        print("Assistant: Please enter a question.\n")
        continue

    # ✅ Use lower() for comparison but check against lowercase strings
    query_lower = query.lower()

    if query_lower in ["introduce", "introduce yourself", "who are you?", 
                        "what can you do?", "inaugurate", "presentation", 
                        "self introduction"]:
        print("Assistant: Hello! I am your AI Research Assistant. I can help you answer questions based on the content of the PDF you provided. Just ask me anything related to the document, and I'll do my best to assist you!\n")
        continue

    if query_lower in ["hi", "hello", "hey", "greetings", "help", 
                        "start", "new", "reset", "whats up"]:
        print("Assistant: Hello! How can I help you today?\n")
        continue

    if query_lower in ["exit", "quit", "bye"]:
        print("Assistant: Goodbye! Have a great day! 👋")
        break

    try:
        result = graph.invoke({
            "question": query,
            "answer": "",
            "sub_questions": []
        })
        print(f"\nAssistant: {result['answer']}\n")

    except Exception as e:
        print(f"\nAssistant: Sorry, something went wrong: {str(e)}\n")

    print("-" * 60)