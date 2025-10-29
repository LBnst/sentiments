from transformers import pipeline

#modèle utilisé :
# https://huggingface.co/distilbert/distilbert-base-uncased-finetuned-sst-2-english

sentiment_model = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

def predict_sentiment(text: str):

    result = sentiment_model(text)[0]
    label = result["label"].lower()
    score = round(result["score"], 3)

    if "pos" in label:
        label = "positive"
    elif "neg" in label:
        label = "negative"
    else:
        label = "neutral"

    return {"sentiment_label": label, "sentiment_score": score}
