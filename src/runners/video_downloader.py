import bentoml
from pytube import YouTube


class VideoDownloader(bentoml.Runnable):
    @bentoml.Runnable.method(batchable=False)
    def download_video(self, url):
        youtube = YouTube(url)
        path = youtube.streams.filter(only_audio=True)[0].download(
            filename="/Users/ahmedbesbes/Desktop/output.mp4"
        )
        print("video successfully downloaded")
        return path
