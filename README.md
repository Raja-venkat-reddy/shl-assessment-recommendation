# shl-assessment-recommendation

SHL Assessment Recommendation Engine (Generative AI)

Overview

This project implements an AI-powered Assessment Recommendation Engine using SHL’s product catalog.
Given a job description, the system recommends the most relevant SHL assessments using semantic similarity and embeddings.

The solution demonstrates an end-to-end GenAI pipeline, including:
	•	Programmatic ingestion of SHL assessment data
	•	Embedding-based semantic search
	•	A recommendation engine
	•	A production-ready FastAPI backend

This project was developed as part of the SHL Research Intern – Generative AI assessment.

⸻

Architecture


Job Description
      ↓
Sentence Transformer (Embeddings)
      ↓
Cosine Similarity Search
      ↓
Top-K SHL Assessments
      ↓
FastAPI Response


Project Structure

shl-assessment-recommendation/
│
├── backend/
│   ├── app.py              # FastAPI application
│   ├── recommender.py      # Recommendation logic
│   └── schemas.py          # API request/response schemas
│
├── scripts/
│   ├── scrape_shl.py       # SHL catalog scraper
│   └── build_embeddings.py # Embedding generation
│
├── data/                   # Generated at runtime (gitignored)
│   ├── shl_catalog.json
│   ├── embeddings.npy
│   └── metadata.json
│
├── README.md
└── .gitignore


Data Ingestion (SHL Catalog Scraping)

The SHL assessment catalog is dynamically loaded via frontend pagination.
	•	The scraper programmatically ingests all publicly accessible Individual Test Solutions using:
	•	Catalog pagination
	•	Deep crawling of product pages
	•	Due to dynamic loading and variant-based assessments, not all logical variants have unique public URLs.
	•	The pipeline is designed to scale automatically if additional assessments are exposed.

The recommendation system is agnostic to catalog size and works for any number of assessments.

Embedding Strategy

	•	Model: sentence-transformers/all-MiniLM-L6-v2
	•	Each assessment is embedded using:
	•	Assessment name
	•	Description
	•	Test type (Knowledge / Personality)
	•	Job descriptions are embedded using the same model.
	•	Cosine similarity is used to rank assessments.

This enables semantic matching rather than keyword-based search.


Recommendation Logic

For a given job description:
	1.	Convert the text into an embedding
	2.	Compute similarity with all assessment embeddings
	3.	Rank assessments by relevance
	4.	Return the Top-K recommendations


API Specification

Endpoint
POST /recommend

Request Body
{
  "job_description": "We are hiring a Store Manager with leadership and retail experience",
  "top_k": 5
}

Response

{
  "recommendations": [
    {
      "name": "Store Manager 7.1 (Americas)",
      "url": "https://www.shl.com/products/...",
      "test_type": ["P", "K"],
      "score": 0.54
    }
  ]
}


Running the Project Locally

1. Install dependencies
pip install fastapi uvicorn sentence-transformers numpy tqdm beautifulsoup4 requests

2. Scrape SHL catalog
python scripts/scrape_shl.py

3. Build embeddings
python scripts/build_embeddings.py

4. Start the API
uvicorn backend.app:app --reload

Open Swagger UI:
http://127.0.0.1:8000/docs



Technologies Used
	•	Python
	•	FastAPI
	•	Sentence Transformers
	•	NumPy
	•	BeautifulSoup
	•	Requests
	•	Uvicorn

Author
Developed as part of the SHL Research Intern – Generative AI Assessment.


Final Notes

This project demonstrates:
	•	End-to-end GenAI system design
	•	Semantic recommendation engines
	•	Production-ready API development
	•	Practical handling of real-world dynamic data
