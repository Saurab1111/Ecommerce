📦 Product Review Analysis System (Hugging Face – Offline)
📌 Overview

This project extends an e-commerce backend by adding an AI-powered product review analysis system. It analyzes user reviews using a pretrained Hugging Face Transformer model to generate actionable insights such as overall sentiment, average rating, review summary, pros, and cons for each product.

The solution runs fully locally, requires no external API keys, and is designed for enterprise-style scalability and explainability.

🎯 Problem Statement

E-commerce platforms often collect large volumes of textual reviews, but raw reviews alone do not provide quick insights. Manually reading reviews to understand customer sentiment, strengths, and weaknesses of a product is inefficient.

This system automates:

Review aggregation

Sentiment analysis

Insight generation at the product level

🧠 AI Solution Approach
1️⃣ Review Collection

Users submit reviews with ratings for products

Reviews are stored as raw inputs in the database

2️⃣ Sentiment Analysis (AI Layer)

Each review text is passed through a pretrained Hugging Face Transformer model:

distilbert-base-uncased-finetuned-sst-2-english


The model classifies reviews as POSITIVE or NEGATIVE

Runs locally using transformers and torch

3️⃣ Aggregation & Insight Generation

Average rating is computed from all review ratings

Overall sentiment is derived from aggregated model predictions

Common keywords are extracted to infer pros and cons

A concise review summary is generated

4️⃣ Persistence

All derived insights are stored in a dedicated ReviewAnalysis model

Analysis can be re-run at any time as reviews change

🏗️ Architecture (Conceptual)
User Reviews
     ↓
Hugging Face Sentiment Model (Offline)
     ↓
Aggregation Logic
     ↓
Product-Level Insights (Stored in DB)

🧩 Tech Stack

Backend: Django, Django REST Framework

AI / ML: Hugging Face Transformers, PyTorch

Model: DistilBERT (Sentiment Analysis)

Database: PostgreSQL / MySQL / SQLite

Deployment Ready: Docker, AWS

No External APIs Required

🚀 How to Run Locally
✅ Prerequisites

Python 3.9+

Git

Virtual environment (recommended)

1️⃣ Clone the Repository
git clone https://github.com/Saurab1111/Ecommerce.git
cd your-repo-name

2️⃣ Create & Activate Virtual Environment

Windows

python -m venv venv
venv\Scripts\activate


macOS / Linux

python3 -m venv venv
source venv/bin/activate

3️⃣ Install Dependencies
pip install -r requirements.txt


This will also install:

torch

transformers

4️⃣ Run Migrations
python manage.py makemigrations
python manage.py migrate

5️⃣ Start the Server
python manage.py runserver


Server runs at:

http://127.0.0.1:8000/

🔌 API Endpoints
➕ Add Review
POST /<product-slug>/reviews/

{
  "user": "saurabh",
  "review": "Battery life is excellent and performance is smooth",
  "rating": 5
}

📊 Trigger Review Analysis
POST /<product-slug>/reviews/analyze/

📥 Analysis Response
{
  "product": "iPhone 15",
  "average_rating": 4.5,
  "overall_sentiment": "Positive",
  "review_summary": "Based on 12 reviews, customers generally feel positive about this product.",
  "pros": "battery, performance, camera",
  "cons": "price",
  "total_reviews": 12
}

🧪 What Was Tested

Review creation and persistence

Sentiment inference using Hugging Face model

Aggregation logic correctness

End-to-end API execution

Database storage of derived insights