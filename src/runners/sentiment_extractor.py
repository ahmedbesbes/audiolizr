import bentoml
from transformers import pipeline


class SentimentExtractor(bentoml.Runnable):
    def __init__(self):
        self.model = pipeline("sentiment-analysis")

    @bentoml.Runnable.method(batchable=False)
    def extract_sentiment(self, text):
        sentiment = self.model(text)
        return sentiment
