from gtts import gTTS
import os

def speak(text):

    tts = gTTS(text=text, lang="hi")

    tts.save("speech.mp3")

    os.system("start speech.mp3")