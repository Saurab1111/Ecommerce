from transformers import pipeline
from statistics import mean
from collections import Counter
from ..models import Reviews, ReviewAnalysis

# Load once (VERY IMPORTANT)
sentiment_pipeline = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english"
)

def analyze_reviews(product):
    reviews = Reviews.objects.filter(product=product)

    if not reviews.exists():
        return None

    ratings = []
    sentiments = []
    word_counter = Counter()

    for r in reviews:
        ratings.append(r.rating)

        # Sentiment prediction
        result = sentiment_pipeline(r.review[:512])[0]
        sentiments.append(result["label"])

        # Collect words for pros / cons
        words = r.review.lower().split()
        word_counter.update(words)

    avg_rating = round(mean(ratings), 2)

    positive = sentiments.count("POSITIVE")
    negative = sentiments.count("NEGATIVE")

    if positive > negative:
        overall_sentiment = "Positive"
    elif negative > positive:
        overall_sentiment = "Negative"
    else:
        overall_sentiment = "Neutral"

    common_words = [w for w, _ in word_counter.most_common(20)]
    pros = ", ".join(common_words[:5])
    cons = ", ".join(common_words[-5:])

    summary = (
        f"Based on {len(reviews)} reviews, the overall customer sentiment "
        f"towards this product is {overall_sentiment.lower()}."
    )

    analysis, _ = ReviewAnalysis.objects.update_or_create(
        product=product,
        defaults={
            "average_rating": avg_rating,
            "overall_sentiment": overall_sentiment,
            "review_summary": summary,
            "pros": pros,
            "cons": cons,
            "total_reviews": reviews.count(),
        }
    )

    return analysis
