import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()  # Load environment variables from .env file

def load_llm():

    model = ChatGroq(model="llama-3.1-8b-instant", temperature=0.7)

    return model

