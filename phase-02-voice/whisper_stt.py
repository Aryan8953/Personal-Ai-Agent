from faster_whisper import WhisperModel


MODEL_SIZE = "base"


print("Loading Whisper model...")

model = WhisperModel(
    MODEL_SIZE,
    device="cpu",
    compute_type="int8"
)

print("Whisper loaded.")


def transcribe(audio_file):

    segments, info = model.transcribe(audio_file)

    text = ""

    for segment in segments:
        text += segment.text

    return text.strip()


if __name__ == "__main__":

    result = transcribe("test.wav")

    print("Transcription:")
    print(result)          