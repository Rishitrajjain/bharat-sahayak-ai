import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Load schemes database
with open("schemes.json","r") as f:
    schemes = json.load(f)

# Prepare searchable text
texts = []

for s in schemes:
    text = f"""
    Scheme: {s['name']}
    Description: {s['description']}
    Benefit: {s['benefit']}
    Occupation: {s['occupation']}
    """
    texts.append(text)

# Create embeddings
embeddings = model.encode(texts)

dimension = embeddings.shape[1]

# Build FAISS index
index = faiss.IndexFlatL2(dimension)

index.add(np.array(embeddings))


# --------------------------
# Retrieve Schemes
# --------------------------

def retrieve_schemes(query, k=5):

    query_embedding = model.encode([query])

    distances, indices = index.search(query_embedding, k)

    results = []

    for i in indices[0]:
        results.append(schemes[i])

    return results