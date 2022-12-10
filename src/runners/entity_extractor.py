import bentoml
import spacy


class EntityExtractor(bentoml.Runnable):
    SUPPORTED_RESOURCES = ("cpu",)
    SUPPORTS_CPU_MULTI_THREADING = False

    def __init__(self):
        self.model = spacy.load("en_core_web_md")

    @bentoml.Runnable.method(batchable=False)
    def extract_entities(self, text):
        doc = self.model(text)
        entities = []
        for ent in doc.ents:
            entity = {
                "entity_text": ent.text,
                "entity_label": ent.label_,
                "start": ent.start_char,
                "end": ent.end_char,
            }
            entities.append(entity)

        output = {"entities": entities}
        return output
