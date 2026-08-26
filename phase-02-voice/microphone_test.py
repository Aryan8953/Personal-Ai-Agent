import speech_recognition as sr

recognizer = sr.Recognizer()

with sr.Microphone() as source:

    print("Adjusting for background noise...")
    recognizer.adjust_for_ambient_noise(source, duration=1)

    print("Listening...")
    audio = recognizer.listen(source)
print("Audio captured successfully!")