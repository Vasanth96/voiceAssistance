import time
import speech_recognition as sr
from gtts import gTTS
import playsound
import os
import weathercom
import json
import webbrowser
from time import ctime

r = sr.Recognizer()

def voice_command_processor(ask=False):
    with sr.Microphone() as source:
        if(ask):
            audio_playback(ask)
        audio = r.listen(source,phrase_time_limit=3)
        text = ''
        try:
            text=r.recognize_google(audio)
        except sr.UnknownValueError as e:
            audio_playback("Sorry, I did not get that")
        except sr.RequestError as e:
            audio_playback("service is down")

        return text.lower()



def audio_playback(text):
    filename = "test.mp3"
    tts = gTTS(text=text, lang='en')
    tts.save(filename)
    playsound.playsound(filename)
    os.remove(filename)


def execute_voice_command(text):
    if "what are you" in text:
        audio_playback("i'm A  I voice assistance")
    if "your name" in text:
        audio_playback("My name is pi")
    if "what time is it" in text:
        audio_playback(ctime())

    if "thank you" in text:
        audio_playback("You are welcome")

    if "search" in text:
       search =voice_command_processor("What do you want to search for ?")
       url = 'https://google.com/search?q='+search
       webbrowser.get().open(url)
       audio_playback("Here is what i found"+search)

    if "what is the today's weather" in text:
        city = voice_command_processor("which city")
        humidity, temp, phrase = weatherReport(city)
        audio_playback("currently in " + city + "  temperature is " + str(temp)
                       + " degree celsius, " + "humidity is " + str(humidity) + " percent and sky is " + phrase)
        print("currently in " + city + "  temperature is " + str(temp)
              + "degree celsius, " + "humidity is " + str(humidity) + " percent and sky is " + phrase)
    if 'exit' in text:
        audio_playback("thank you")
        exit()


def weatherReport(city):
    weatherDetails = weathercom.getCityWeatherDetails(city)
    print(weatherDetails)
    humidity = json.loads(weatherDetails)["vt1observation"]["humidity"]
    temp = json.loads(weatherDetails)["vt1observation"]["temperature"]
    phrase = json.loads(weatherDetails)["vt1observation"]["phrase"]
    return humidity, temp, phrase

time.sleep(1)
audio_playback("How can i help you?")
while 1:
    command = voice_command_processor()
    print(command)
    execute_voice_command(command)
