from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
from model import predict_sentiment
from es import index_sentiment

from es import test_connection
test_connection()


app = FastAPI(title="Service d'analyse de sentiment")

class TextRequest(BaseModel):
    author: str | None = "unknown"
    source: str | None = "twitter"
    message: str


#analyse manuelle + indexation
@app.post("/analyze")
def analyze_text(data: TextRequest):
    prediction = predict_sentiment(data.message)

    doc = {
        "author": data.author,
        "source": data.source,
        "message": data.message,
        "sentiment_label": prediction["sentiment_label"],
        "sentiment_score": prediction["sentiment_score"],
        "created_at": datetime.utcnow().isoformat()
    }

    response = index_sentiment("product_sentiment", doc)

    if response:
        return {"status": "indexed", **doc}
    else:
        return {"status": "error", **doc}


#process du csv
@app.post("/bulk_import")
def bulk_import():
    import pandas as pd
    from datetime import datetime

    df = pd.read_csv("clean_dataset.csv")

    for _, row in df.iterrows():
        result = predict_sentiment(row["message"])
        doc = {
            "author": row["author"],
            "source": row["source"],
            "message": row["message"],
            "sentiment_label": result["sentiment_label"],
            "sentiment_score": result["sentiment_score"],
            "created_at": datetime.utcnow().isoformat()
        }
        index_sentiment("product_sentiment", doc)

    return {"status": "imported", "count": len(df)}

