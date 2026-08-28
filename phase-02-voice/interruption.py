import threading
import tempfile
import wave
from pathlib import Path

import speech_recognition as sr
import webrtcvad


class MicrophoneMonitor:

    def __init__(self, whisper_model):

        self.recognizer = sr.Recognizer()
        self.vad = webrtcvad.Vad(2)

        self.whisper_model = whisper_model

        self.stop_event = threading.Event()

        self.monitor_thread = None

        self.interrupted_audio = None
        self.interrupted_text = None

    # ==========================================
    # Check speech ratio
    # ==========================================

    def _speech_ratio(self, audio):

        raw_audio = audio.get_raw_data(
            convert_rate=16000,
            convert_width=2
        )

        frame_size = int(
            16000 * 0.03 * 2
        )

        speech_frames = 0
        total_frames = 0

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

            total_frames += 1

            if self.vad.is_speech(
                frame,
                16000
            ):

                speech_frames += 1

        if total_frames == 0:
            return 0.0

        return speech_frames / total_frames

    # ==========================================
    # Whisper
    # ==========================================

    def _transcribe(self, audio):

        if audio is None:
            return None

        raw_audio = audio.get_raw_data(
            convert_rate=16000,
            convert_width=2
        )

        temp_file = tempfile.NamedTemporaryFile(
            suffix=".wav",
            delete=False
        )

        temp_path = Path(
            temp_file.name
        )

        temp_file.close()

        try:

            with wave.open(
                str(temp_path),
                "wb"
            ) as wav_file:

                wav_file.setnchannels(1)
                wav_file.setsampwidth(2)
                wav_file.setframerate(16000)

                wav_file.writeframes(
                    raw_audio
                )

            segments, info = (
                self.whisper_model.transcribe(
                    str(temp_path),

                    language="en",

                    temperature=0.0,

                    condition_on_previous_text=False,

                    vad_filter=True
                )
            )

            texts = []

            for segment in segments:

                if segment.no_speech_prob > 0.60:
                    continue

                if segment.avg_logprob < -1.2:
                    continue

                text = segment.text.strip()

                if text:
                    texts.append(text)

            if not texts:
                return None

            return " ".join(texts).strip()

        except Exception as error:

            print(
                f"\nWhisper error: {error}"
            )

            return None

        finally:

            try:
                temp_path.unlink()

            except PermissionError:
                pass

    # ==========================================
    # Monitor
    # ==========================================

    def _monitor(self):

        try:

            with sr.Microphone(
                sample_rate=16000
            ) as source:

                print(
                    "\n🎤 Interruption monitor active"
                )

                # Give microphone a moment
                # to initialize.

                self.recognizer.adjust_for_ambient_noise(
                    source,
                    duration=0.3
                )

                while not self.stop_event.is_set():

                    # --------------------------
                    # Wait for possible speech
                    # --------------------------

                    try:

                        audio = self.recognizer.listen(
                            source,
                            timeout=0.5,
                            phrase_time_limit=1
                        )

                    except sr.WaitTimeoutError:

                        continue


                    ratio = self._speech_ratio(
                        audio
                    )


                    if ratio < 0.25:

                        continue


                    print(
                        "\nPossible user speech..."
                    )


                    # --------------------------
                    # Whisper
                    # --------------------------

                    text = self._transcribe(
                        audio
                    )


                    if not text:

                        print(
                            "Speech not confirmed."
                        )

                        continue


                    print(
                        f"\n🛑 User interruption: "
                        f"{text}"
                    )


                    self.interrupted_audio = audio
                    self.interrupted_text = text

                    self.stop_event.set()

                    return

        except Exception as error:

            print(
                f"\nMonitor error: {error}"
            )

    # ==========================================
    # Start
    # ==========================================

    def start(self):

        self.stop_event.clear()

        self.interrupted_audio = None
        self.interrupted_text = None

        self.monitor_thread = threading.Thread(
            target=self._monitor,
            daemon=True
        )

        self.monitor_thread.start()

    # ==========================================
    # Stop
    # ==========================================

    def stop(self):

        self.stop_event.set()

        if (
            self.monitor_thread
            and self.monitor_thread.is_alive()
        ):

            self.monitor_thread.join(
                timeout=1
            )

    # ==========================================
    # State
    # ==========================================

    def interrupted(self):

        return self.stop_event.is_set()

    def get_audio(self):

        return self.interrupted_audio

    def get_text(self):

        return self.interrupted_text