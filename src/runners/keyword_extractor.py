from ast import keyword
import bentoml
from keybert import KeyBERT


class KeywordExtractor(bentoml.Runnable):
    def __init__(self):
        self.keybert_model = KeyBERT()

    @bentoml.Runnable.method(batchable=False)
    def extract_keywords(self, transcript, **kwargs):
        keywords = self.keybert_model.extract_keywords(transcript, **kwargs)
        print("keywords successfully extracted")
        return keywords
