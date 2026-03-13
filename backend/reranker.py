from sentence_transformers import CrossEncoder

reranker = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')

def rerank_documents(query, docs, top_k=5):
    # Create pairs of query and documents for scoring
    pairs = [(query, doc.page_content) for doc in docs]
    
    # Get relevance scores for each pair
    scores = reranker.predict(pairs)
    
    # Combine documents with their scores and sort by score
    scored_docs = list(zip(docs, scores))
    scored_docs.sort(key=lambda x: x[1], reverse=True)
    
    reranked_docs = [doc for doc, score in scored_docs[:top_k]]
    
    # Return the top_k documents based on relevance scores
    return reranked_docs