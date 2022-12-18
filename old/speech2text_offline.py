import speech_recognition as sr
import time
import subprocess


def mycallbackk(recognizer, audio):
    _ = 0
    # try:
    #     result = recognizer.recognize_google(audio, language='en-US')
    #     print(result)

    #     result = result.lower()

    #     if 'sol' in result:
    #         subprocess.run(['xdotool', 'key', 'Left'])
    #     elif 'sağ' in result:
    #         subprocess.run(['xdotool', 'key', 'Right'])
    #     elif 'aşağı' in result:
    #         subprocess.run(['xdotool', 'key', 'Down'])
    #     elif 'yukarı' in result:
    #         subprocess.run(['xdotool', 'key', 'Up'])

    # except sr.UnknownValueError:
    #     print("Google Speech Recognition could not understand audio")
    # except sr.RequestError as e:
    #     print(
    #         "Could not request results from Google Speech Recognition service; {0}".format(e))


r = sr.Recognizer()
mymic = sr.Microphone()
with mymic as mysource:
    # we only need to calibrate once, before we start listening
    r.adjust_for_ambient_noise(mysource)

# start listening in the background (note that we don't have to do this inside a `with` statement)
stop_listening = r.listen_in_background(mymic, mycallbackk)
# `stop_listening` is now a function that, when called, stops background listening
while True:
    time.sleep(5)
    # calling this function requests that the background listener stop listening
    stop_listening(wait_for_stop=False)
