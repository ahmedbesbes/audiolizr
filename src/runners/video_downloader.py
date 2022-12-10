import bentoml
from pytube import YouTube


class VideoDownloader(bentoml.Runnable):
    SUPPORTED_RESOURCES = ("cpu",)
    SUPPORTS_CPU_MULTI_THREADING = False

    @bentoml.Runnable.method(batchable=False)
    def download_video(self, url):
        youtube = YouTube(url)
        path = youtube.streams.filter(only_audio=True)[0].download(
            filename="/tmp/output.mp4",
        )
        print("video successfully downloaded")
        return path
