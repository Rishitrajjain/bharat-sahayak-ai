import speech_recognition as sr

def listen_for_income():

    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("Speak now...")
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio, language="hi-IN")
        return text

    except:
        return "Could not understand"