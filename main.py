# backend/main.py
from fastapi import FastAPI, Query
from sentence_transformers import SentenceTransformer
import faiss
import pandas as pd
import numpy as np
import os

app = FastAPI()

# ----- Load Model -----
model_path = os.path.join(os.path.dirname(__file__), "sustain_reco_model")
model = SentenceTransformer(model_path)

# ----- Load FAISS Index -----
faiss_index_path = os.path.join(os.path.dirname(__file__), "faiss_index2.bin")
index = faiss.read_index(faiss_index_path)

# ----- Load Product Catalog -----
catalog_path = os.path.join(os.path.dirname(__file__), "catalog_indexed.csv")
catalog = pd.read_csv(catalog_path)

@app.get("/")
def home():
    return {"message": "Sustainable Recommendation API running!"}

@app.get("/recommendations")
def recommend(query: str = Query(..., description="Search query"), top_k: int = 5):
    """
    Get top_k recommendations based on a search query.
    Example: /recommendations?query=eco-friendly bottle&top_k=5
    """

    if not query.strip():
        return {"results": [], "message": "Empty query provided."}

    # Convert query to embedding
    query_emb = model.encode([query], convert_to_numpy=True)

    # Search FAISS
    distances, indices = index.search(query_emb.astype('float32'), top_k)

    results = []
    for idx, score in zip(indices[0], distances[0]):
        if idx == -1:
            continue  # Skip invalid results

        product = catalog.iloc[idx].to_dict()

        # Convert NaN/inf to None for JSON safety
        product = {k: (None if isinstance(v, float) and (np.isnan(v) or np.isinf(v)) else v) 
                   for k, v in product.items()}

        # Calculate similarity score (normalized)
        similarity = None
        if not (np.isnan(score) or np.isinf(score)):
            similarity = float(np.exp(-score))  # Better similarity representation

        product['similarity'] = similarity
        results.append(product)

    if not results:
        return {"results": [], "message": "No similar products found."}

    return {"results": results}
