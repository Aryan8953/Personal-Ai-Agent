import wave

import pyaudio


FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024
RECORD_SECONDS = 5

OUTPUT_FILE = "test.wav"


audio = pyaudio.PyAudio()

stream = audio.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    frames_per_buffer=CHUNK
)

print("Recording... Speak now.")

frames = []

for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):

    data = stream.read(CHUNK)

    frames.append(data)


print("Recording finished.")

stream.stop_stream()
stream.close()

audio.terminate()


with wave.open(OUTPUT_FILE, "wb") as wave_file:

    wave_file.setnchannels(CHANNELS)
    wave_file.setsampwidth(audio.get_sample_size(FORMAT))
    wave_file.setframerate(RATE)
    wave_file.writeframes(b"".join(frames))


print(f"Saved recording to {OUTPUT_FILE}")