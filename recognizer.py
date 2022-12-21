import speech_recognition as sr
from threading import Thread
from queue import Queue
import subprocess
import time
import RPi.GPIO as GPIO


# LEDler için GPIO hazırlığı
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(17, GPIO.OUT) # Ses kaydı için LED
GPIO.setup(27, GPIO.OUT) # Ses işlenmesi için LED


def recognize_worker(): # Ses tanıma kodu
    # Bu kod arkaplandaki bir threadde çalışmaktadır.
    while True:
        time.sleep(0.2)
        audio = audio_queue.get()  # Ana thread üzerinden sıradaki işlenecek sesi al
        if audio is None:
            break  # Eğer bir ses kaydedilmemişse ana thread durmuştur ve bu thread de sonlandırılır.

        GPIO.output(27, GPIO.HIGH) # İşleme LEDini yak
        print("processing...")
        # Google'ın ses tanıma kütüphanesini kullanarak kaydedilen sesi tanımaya çalışıyoruz.
        try:
            result = r.recognize_google(audio, language="tr-TR")
            result = result.lower() # Kaydedilen seste söylenilen kelime result adlı
                                    # değişkende küçük harflerle saklanılır.

            # Gelen ses aşağıdaki kelimelerden birini içeriyorsa ona uygun komut oluşturulur.
            if 'sol' in result:
                print('pressing left button')
                subprocess.run(['xdotool', 'key', 'Left'])
            elif 'sağ' in result:
                print('pressing right button')
                subprocess.run(['xdotool', 'key', 'Right'])
            elif 'aşağı' in result:
                print('pressing down button')
                subprocess.run(['xdotool', 'key', 'Down'])
            elif 'yukarı' in result:
                print('pressing up button')
                subprocess.run(['xdotool', 'key', 'Up'])
        except sr.UnknownValueError:
            # Ses tanınamadıysa bu hata mesajı gösterilir.
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            # Bir sebepten dolayı Google Ses Tanıma servisine erişilemiyorsa bu hata mesajı gösterilir.
            print(
                "Could not request results from Google Speech Recognition service; {0}".format(e))

        audio_queue.task_done()  # Sırada işlenen bu ses dosyasını tamamlandı olarak işaretle.
        GPIO.output(27, GPIO.LOW) # Ses işleme bittikten sonra LED söndürülür.


# Ses tanıyıcıyı ve ses sırasını yaratıyoruz.
r = sr.Recognizer()
audio_queue = Queue()

# Sistemin gecikmesini azaltmak amacıyla ses tanımayı farklı bir thread üzerinde
# çalıştırmalıyız, böylece bu ana thread sesi kaydetmeye odaklanabilmektedir.
recognize_thread = Thread(target=recognize_worker) # Yukarıda yazmış olduğumuz fonksiyonu threade atıyoruz.
recognize_thread.daemon = True
recognize_thread.start()

# Ses tanıma değişkenine kaynak olarak cihazın mikrofonunu kullanmasını söylüyoruz.
with sr.Microphone() as source:
    try:
        while True:  # Durmadan mikrofondan gelen sesi dinliyoruz ve bir ses gelirse bunu ses tanıma sırasına sokuyoruz.
            GPIO.output(17, GPIO.HIGH)  # Ses kaydetme LEDini yakıyoruz.
            try:
                print('listening...')
                # Mikrofondan bir ses bekliyoruz.
                rec = r.listen(source, timeout=1, phrase_time_limit=10)
                # Ses kaydını ses tanıma sırasına sokuyoruz.
                audio_queue.put(rec)
            except sr.WaitTimeoutError:
                print('timeout reached')
            GPIO.output(17, GPIO.LOW)  # Ses kaydetme LEDini söndürüyoruz
            time.sleep(1)
    except KeyboardInterrupt:  # Klavyede "Ctrl + C" tuşlarına basıldığında programın sonlandırılmasını sağlıyoruz.
        pass

# Programın çalışması bittiğinde LEDleri söndürüyoruz.
GPIO.output(17, GPIO.LOW)
GPIO.output(27, GPIO.LOW)
audio_queue.join()  # Bütün ses tanıma işlemleri bitene kadar bekliyoruz.
audio_queue.put(None)  # Ses tanıma threadini durdurmaya başlıyoruz.
recognize_thread.join()  # Ses tanıma thredinin durdurulmasını bekliyoruz.
