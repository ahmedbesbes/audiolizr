import io
import asyncio
import bentoml
from bentoml.io import JSON, File
from runners.video_downloder import VideoDownloader
from runners.audio_transcriber import AudioTranscriber
from runners.keyword_extractor import KeywordExtractor
from runners.entity_extractor import EntityExtractor
from runners.sentiment_extractor import SentimentExtractor


runner_video_downloader = bentoml.Runner(
    VideoDownloader,
    name="video_downloader",
)
runner_audio_transcriber = bentoml.Runner(
    AudioTranscriber,
    name="audio_transcriber",
)
runner_keyword_extractor = bentoml.Runner(
    KeywordExtractor,
    name="keyword_extractor",
)
runner_entity_extractor = bentoml.Runner(
    EntityExtractor,
    name="entity_extractor",
)
runner_sentiment_extractor = bentoml.Runner(
    SentimentExtractor,
    name="sentiment_extractor",
)

svc = bentoml.Service(
    "speech_to_text_pipeline",
    runners=[
        runner_video_downloader,
        runner_audio_transcriber,
        runner_keyword_extractor,
        runner_entity_extractor,
        runner_sentiment_extractor,
    ],
)


@svc.api(input=JSON(), output=JSON())
async def process_youtube_url(input_data):
    url = input_data.get("youtube_video_url", None)

    path = runner_video_downloader.download_video.run(url)
    transcript = runner_audio_transcriber.transcribe_audio.run(path)
    transcript_text = transcript["text"]

    results = await asyncio.gather(
        runner_keyword_extractor.extract_keywords.async_run(transcript_text),
        runner_entity_extractor.extract_entities.async_run(transcript_text),
        runner_sentiment_extractor.extract_sentiment.async_run(transcript_text),
    )
    return results


@svc.api(input=File(), output=JSON())
async def process_uploaded_file(input_file: io.BytesIO):
    path = f"/Users/ahmedbesbes/Desktop/audio.mp4"
    with open(path, "wb") as f:
        f.write(input_file.read())

    transcript = runner_audio_transcriber.transcribe_audio.run(path)
    transcript_text = transcript["text"]

    results = await asyncio.gather(
        runner_keyword_extractor.extract_keywords.async_run(transcript_text),
        runner_entity_extractor.extract_entities.async_run(transcript_text),
        runner_sentiment_extractor.extract_sentiment.async_run(transcript_text),
    )
    return results
