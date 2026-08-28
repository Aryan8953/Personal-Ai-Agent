import speech_recognition as sr
import webrtcvad


vad = webrtcvad.Vad(2)

recognizer = sr.Recognizer()


def detect_speech():

    with sr.Microphone(sample_rate=16000) as source:

        print("Listening for speech...")
        print("Say something.")

        while True:

            audio = recognizer.listen(
                source,
                phrase_time_limit=1
            )

            raw_audio = audio.get_raw_data(
                convert_rate=16000,
                convert_width=2
            )

            # WebRTC VAD requires 10, 20, or 30 ms frames.
            frame_size = int(
                16000 * 0.03 * 2
            )

            for start in range(
                0,
                len(raw_audio),
                frame_size
            ):

                frame = raw_audio[
                    start:start + frame_size
                ]

                if len(frame) != frame_size:
                    continue

                if vad.is_speech(
                    frame,
                    16000
                ):

                    print("Speech detected!")
                    return


if __name__ == "__main__":

    detect_speech()
    