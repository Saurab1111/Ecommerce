AI-Powered Product Review Insights
Overview

This project is a backend system that analyzes product reviews using Natural Language Processing (NLP) to generate actionable insights such as overall sentiment, average ratings, review summaries, pros, and cons.

The application is built using Django REST Framework and Hugging Face Transformers, and is designed to run fully offline without any paid APIs or cloud dependencies.

Key Features

Analyze customer reviews using Transformer-based NLP models

Generate overall product sentiment and rating insights

Create short summaries from multiple reviews

RESTful APIs for review ingestion and analysis

JWT-based authentication for secure API access

Runs completely offline using local database and models

Tech Stack

Backend: Python, Django, Django REST Framework

Authentication: JWT (SimpleJWT)

Database: SQLite (default Django database)

NLP / AI: Hugging Face Transformers

Model Used: distilbert-base-uncased-finetuned-sst-2-english

Architecture
Client → Django REST API → NLP Model (Transformers) → Aggregation Logic → JSON Response

Setup & Run Locally (Offline)
1. Clone the Repository
git clone https://github.com/Saurab1111/Ecommerce.git
cd Ecommerce

2. Create Virtual Environment
python -m venv venv
source venv/bin/activate      # macOS / Linux
venv\Scripts\activate         # Windows

3. Install Dependencies
pip install -r requirements.txt

4. Run Database Migrations
python manage.py makemigrations
python manage.py migrate

5. Create Superuser (for authentication)
python manage.py createsuperuser

6. Start Development Server
python manage.py runserver


The application will run at:

http://127.0.0.1:8000/

Authentication (JWT)

This project uses SimpleJWT for authentication.

Obtain Access Token
POST /api/token/


Request Body

{
  "username": "your_username",
  "password": "your_password"
}

Use Token in API Requests

Add the token in the request header:

Authorization: Bearer <access_token>

API Endpoints
Add Product Review
POST /reviews/
Authorization: Bearer <token>

{
  "user": "john_doe",
  "review": "The product quality is good and delivery was fast.",
  "rating": 5
}

Analyze Reviews
POST /reviews/analyze/
Authorization: Bearer <token>


Sample Response

{
  "overall_sentiment": "Positive",
  "average_rating": 4.5,
  "review_summary": "Users liked the product quality and fast delivery.",
  "pros": "Good quality, fast delivery",
  "cons": "None",
  "total_reviews": 10
}

Notes

The NLP models are loaded locally using Hugging Face Transformers.

No external APIs or cloud services are required to run this project.

Authentication and database configuration are optimized for local development.

Future Improvements

Replace SQLite with PostgreSQL for production use

Add caching for faster inference

Extend summarization using retrieval-based techniques (RAG)

Deploy using cloud services

Author

Saurabh Keskar

License

This project is for learning and demonstration purposes.




or a cloud-ready architecture note

Just say the word.
