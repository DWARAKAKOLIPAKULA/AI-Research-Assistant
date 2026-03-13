from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings 

def get_retriever():

    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    vector_store = FAISS.load_local("vector_store", embeddings, allow_dangerous_deserialization=True)

    retriever = vector_store.as_retriever(search_kwargs={"k": 5})
    return retriever

