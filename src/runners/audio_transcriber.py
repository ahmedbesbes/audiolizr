import bentoml
import whisper


class AudioTranscriber(bentoml.Runnable):
    SUPPORTED_RESOURCES = ("nvidia.com/gpu", "cpu")
    SUPPORTS_CPU_MULTI_THREADING = True

    def __init__(self):
        self.model = whisper.load_model("base")

    @bentoml.Runnable.method(batchable=False)
    def transcribe_audio(self, audio_path):
        transcription = self.model.transcribe(audio_path)
        print("audio successfully transcribed")
        return transcription
