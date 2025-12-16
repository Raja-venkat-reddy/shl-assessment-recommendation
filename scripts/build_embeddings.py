import json
import numpy as np
from sentence_transformers import SentenceTransformer
from tqdm import tqdm
import os

CATALOG_PATH = "data/shl_catalog.json"
EMBEDDINGS_PATH = "data/embeddings.npy"
METADATA_PATH = "data/metadata.json"

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


def main():
    print("📦 Loading SHL catalog...")
    with open(CATALOG_PATH, "r", encoding="utf-8") as f:
        catalog = json.load(f)

    print(f"✅ Loaded {len(catalog)} assessments")

    print("🤖 Loading embedding model...")
    model = SentenceTransformer(MODEL_NAME)

    texts = []
    metadata = []

    for item in catalog:
        text = (
            f"{item['name']}. "
            f"{item['description']}. "
            f"Test Type: {' '.join(item['test_type'])}"
        )
        texts.append(text)
        metadata.append(item)

    print("🔢 Creating embeddings...")
    embeddings = model.encode(
        texts,
        convert_to_numpy=True,
        normalize_embeddings=True,
        show_progress_bar=True
    )

    print("💾 Saving outputs...")
    np.save(EMBEDDINGS_PATH, embeddings)

    with open(METADATA_PATH, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)

    print("✅ Embeddings created successfully")
    print(f"📁 {EMBEDDINGS_PATH}")
    print(f"📁 {METADATA_PATH}")


if __name__ == "__main__":
    main()