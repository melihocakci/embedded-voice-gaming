import speech_recognition as sr
import subprocess

# obtain audio from the microphone
r = sr.Recognizer()
with sr.Microphone() as source:

    while True:
        print("Recording...")
        audio = r.record(source, duration=4)

        try:
            result = r.recognize_google(audio, language="tr-TR")
            print(result)

            if 'sol' in result.lower():
                subprocess.run(['xdotool', 'key', 'Left'])
            elif 'sağ' in result.lower():
                subprocess.run(['xdotool', 'key', 'Right'])
            elif 'aşağı' in result.lower():
                subprocess.run(['xdotool', 'key', 'Down'])
            elif 'yukarı' in result.lower():
                subprocess.run(['xdotool', 'key', 'Up'])
                

#            num = re.findall('\d+', result)[0]
#            print(num)
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print(
                "Could not request results from Google Speech Recognition service; {0}".format(e))
