import speech_recognition as sr


recognizer = sr.Recognizer()


def listen():

    with sr.Microphone() as source:

        print("Adjusting for background noise...")
        recognizer.adjust_for_ambient_noise(source, duration=1)

        print("Listening...")

        audio = recognizer.listen(source)

    print("Processing speech...")

    try:

        text = recognizer.recognize_google(audio)

        return text

    except sr.UnknownValueError:

        print("I couldn't understand the audio.")
        return None

    except sr.RequestError as error:

        print(f"Speech recognition service error: {error}")
        return None


if __name__ == "__main__":

    result = listen()

    if result:
        print(f"You said: {result}")