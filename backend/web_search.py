# from googlesearch import search
# import requests
# from bs4 import BeautifulSoup

# def web_search_answer(query):
#     results = []
#     for url in search(query, num_results=3):
#         try:
#             res = requests.get(url, timeout=5)
#             soup = BeautifulSoup(res.text, "html.parser")
#             paragraphs = soup.find_all("p")
#             text = " ".join(p.get_text() for p in paragraphs[:3])
#             if text.strip():
#                 results.append(f"Source: {url}\n{text.strip()}\n")
#         except:
#             results.append(f"Source: {url}\n(Could not fetch content)\n")

#     return "\n".join(results) if results else "No results found."

import os
from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv()

client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))  # ✅ pass key explicitly

def tavily_search(query):
    try:
        response = client.search(
            query=query,
            search_depth="advanced",
            max_results=3
        )

        results = []
        for r in response["results"]:
            results.append(r["content"])

        return "\n\n".join(results) if results else "No results found."

    except Exception as e:
        return f"Web search failed: {str(e)}" 