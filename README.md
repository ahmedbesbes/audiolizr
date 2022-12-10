# audiolizr
---

This repo shows how to build and deploy a BentoML service that performs that transcribes Youtube videos and extracts the following metadata from them: 
- keywords and topics
- named entities: people's name, products, organizations, etc.
- sentiment analysis score

<img src="./images/audiolizr.png">

#### What's used under the hood?

pytube to download youtube audio
whisper to transcribe audio data
Yake to extract keywords
spaCy to extract named entities
transformers to perform sentiment analysis

