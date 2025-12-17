import numpy as np
import json
from sentence_transformers import SentenceTransformer
from typing import List, Dict

EMBEDDINGS_PATH = "data/embeddings.npy"
METADATA_PATH = "data/metadata.json"

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


class AssessmentRecommender:
    def __init__(self):
        print("📦 Loading embeddings...")
        self.embeddings = np.load(EMBEDDINGS_PATH)

        print("📦 Loading metadata...")
        with open(METADATA_PATH, "r", encoding="utf-8") as f:
            self.metadata = json.load(f)

        print("🤖 Loading embedding model...")
        self.model = SentenceTransformer(MODEL_NAME)

        assert len(self.embeddings) == len(self.metadata)
        print(f"✅ Ready with {len(self.metadata)} assessments")

    def recommend(
        self,
        job_description: str,
        top_k: int = 10
    ) -> List[Dict]:
        """
        Recommend top_k SHL assessments for a given job description
        """

        # Step 1: Embed job description
        query_embedding = self.model.encode(
            job_description,
            normalize_embeddings=True
        )

        # Step 2: Cosine similarity
        scores = np.dot(self.embeddings, query_embedding)

        # Step 3: Rank
        top_indices = np.argsort(scores)[::-1][:top_k]

        # Step 4: Build response
        recommendations = []
        for idx in top_indices:
            item = self.metadata[idx]
            recommendations.append({
                "name": item["name"],
                "url": item["url"],
                "test_type": item["test_type"],
                "score": float(scores[idx])
            })

        return recommendations