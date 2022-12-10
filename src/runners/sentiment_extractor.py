import bentoml
from transformers import pipeline


class SentimentExtractor(bentoml.Runnable):
    SUPPORTED_RESOURCES = ("nvidia.com/gpu", "cpu")
    SUPPORTS_CPU_MULTI_THREADING = False

    def __init__(self):
        self.model = pipeline("sentiment-analysis")

    @bentoml.Runnable.method(batchable=False)
    def extract_sentiment(self, text):
        sentiment = self.model(text)
        output = {"sentiment": sentiment}
        return output
