import bentoml
from bentoml.exceptions import BentoMLException
from pytube import YouTube


class VideoDownloader(bentoml.Runnable):
    SUPPORTED_RESOURCES = ("cpu",)
    SUPPORTS_CPU_MULTI_THREADING = True

    @bentoml.Runnable.method(batchable=False)
    def download_video(self, url):
        youtube = YouTube(url)

        if youtube.length > 360:
            raise BentoMLException(
                "The YouTube video you submitted is too long (exceeds 6 mins)",
            )

        path = youtube.streams.filter(only_audio=True)[0].download(
            filename="/tmp/output.mp4",
        )
        print("video successfully downloaded")
        return path
