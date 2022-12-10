from ast import keyword
import bentoml
import yake


class KeywordExtractor(bentoml.Runnable):
    SUPPORTED_RESOURCES = ("nvidia.com/gpu", "cpu")
    SUPPORTS_CPU_MULTI_THREADING = False

    def __init__(self, **kwargs):
        self.keyword_extractor = yake.KeywordExtractor(**kwargs)

    @bentoml.Runnable.method(batchable=False)
    def extract_keywords(self, transcript):
        keywords = self.keyword_extractor.extract_keywords(transcript)
        print("keywords successfully extracted")
        output = {"keywords": keywords}
        return output
