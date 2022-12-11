import bentoml
import torch
from transformers import T5ForConditionalGeneration, T5Tokenizer
from nltk.tokenize import sent_tokenize


class TextSummarizer(bentoml.Runnable):
    SUPPORTED_RESOURCES = ("nvidia.com/gpu", "cpu")

    def __init__(self):
        self.model = T5ForConditionalGeneration.from_pretrained("t5-base")
        self.tokenizer = T5Tokenizer.from_pretrained("t5-base")
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.max_len = 512
        self.model.to(self.device)

    @staticmethod
    def postprocesstext(content):
        final = ""
        for sent in sent_tokenize(content):
            sent = sent.capitalize()
            final = final + " " + sent
        return final

    @bentoml.Runnable.method(batchable=False)
    def summarize(self, text):
        encoding = self.tokenizer.encode_plus(
            text,
            max_length=self.max_len,
            pad_to_max_length=False,
            truncation=True,
            return_tensors="pt",
        ).to(self.device)

        input_ids, attention_mask = encoding["input_ids"], encoding["attention_mask"]

        outs = self.model.generate(
            input_ids=input_ids,
            attention_mask=attention_mask,
            early_stopping=True,
            num_beams=3,
            num_return_sequences=1,
            no_repeat_ngram_size=2,
            min_length=75,
            max_length=300,
        )

        dec = [self.tokenizer.decode(ids, skip_special_tokens=True) for ids in outs]
        summary = dec[0]
        summary = TextSummarizer.postprocesstext(summary)
        output = {"summary": summary}
        return output
