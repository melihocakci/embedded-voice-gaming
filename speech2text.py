import speech_recognition as sr
import regex as re

# obtain audio from the microphone
r = sr.Recognizer()
with sr.Microphone() as source:
    

# # recognize speech using Google Speech Recognition
# try:
#     # for testing purposes, we're just using the default API key
#     # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
#     # instead of `r.recognize_google(audio)`
#     print("Google Speech Recognition thinks you said in English: -  " +
#           r.recognize_google(audio, language="en-US"))
# except sr.UnknownValueError:
#     print("Google Speech Recognition could not understand audio")
# except sr.RequestError as e:
#     print(
#         "Could not request results from Google Speech Recognition service; {0}".format(e))

    while True:
        input("press enter\n")
        print("Say something!")
        audio = r.record(source, duration=3)

        try:
            result = r.recognize_google(audio, language="tr-TR")
            print("Google Speech Recognition thinks you said in Turkish: -  " + result)
            
            num = re.findall('\d+', result)[0]
            print(num)   
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
