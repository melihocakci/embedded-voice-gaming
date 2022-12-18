#!/usr/bin/env python3

# NOTE: this example requires PyAudio because it uses the Microphone class

import speech_recognition as sr
from threading import Thread
from queue import Queue  # Python 3 import
import subprocess
import time
import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(17, GPIO.OUT)
GPIO.setup(27, GPIO.OUT)


r = sr.Recognizer()
audio_queue = Queue()


def recognize_worker():
    # this runs in a background thread
    while True:
        time.sleep(0.2)
        audio = audio_queue.get()  # retrieve the next audio processing job from the main thread
        if audio is None:
            break  # stop processing if the main thread is done

        GPIO.output(27, GPIO.HIGH)
        print("processing...")
        # received audio data, now we'll recognize it using Google Speech Recognition
        try:
            # for testing purposes, we're just using the default API key
            # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
            # instead of `r.recognize_google(audio)`
            result = r.recognize_google(audio, language="tr-TR")
            result = result.lower()

            if 'sol' in result:
                subprocess.run(['xdotool', 'key', 'Left'])
            elif 'sağ' in result:
                subprocess.run(['xdotool', 'key', 'Right'])
            elif 'aşağı' in result:
                subprocess.run(['xdotool', 'key', 'Down'])
            elif 'yukarı' in result:
                subprocess.run(['xdotool', 'key', 'Up'])
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print(
                "Could not request results from Google Speech Recognition service; {0}".format(e))

        audio_queue.task_done()  # mark the audio processing job as completed in the queue
        GPIO.output(27, GPIO.LOW)


# start a new thread to recognize audio, while this thread focuses on listening
recognize_thread = Thread(target=recognize_worker)
recognize_thread.daemon = True
recognize_thread.start()
with sr.Microphone() as source:
    try:
        while True:  # repeatedly listen for phrases and put the resulting audio on the audio processing job queue
            GPIO.output(17, GPIO.HIGH)
            try:
                print('listening...')
                rec = r.listen(source, timeout=1, phrase_time_limit=10)
                audio_queue.put(rec)
            except sr.WaitTimeoutError:
                print('timeout reached')
            GPIO.output(17, GPIO.LOW)
            time.sleep(1)
    except KeyboardInterrupt:  # allow Ctrl + C to shut down the program
        pass

GPIO.output(17, GPIO.LOW)
GPIO.output(27, GPIO.LOW)
audio_queue.join()  # block until all current audio processing jobs are done
audio_queue.put(None)  # tell the recognize_thread to stop
recognize_thread.join()  # wait for the recognize_thread to actually stop
