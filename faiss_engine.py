# faiss_engine.py
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Load model globally once
model = SentenceTransformer("all-MiniLM-L6-v2")

def build_faiss_index(job_descriptions):
    if not job_descriptions:
        raise ValueError("Job descriptions list is empty.")

    embeddings = model.encode(job_descriptions)
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(np.array(embeddings))
    return index, embeddings


def find_top_matches(resume_text, job_descriptions, top_k=3):

    if not job_descriptions:
        return []
     
    # Step 1: Embed all JDs and build index
    index, jd_embeddings = build_faiss_index(job_descriptions)

    # Step 2: Embed the resume
    resume_embedding = model.encode([resume_text])

    # Step 3: Search
    distances, indices = index.search(np.array(resume_embedding), top_k)

    # Step 4: Return results
    matches = []
    for i, dist in zip(indices[0], distances[0]):
        matches.append({
            "job_description": job_descriptions[i],
            "score": float(np.exp(-dist))  # Converts distance into a similarity score (0 to 1)
        })
    return matches
