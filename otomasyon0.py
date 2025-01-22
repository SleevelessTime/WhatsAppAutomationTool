############################################################################################
# Project: WhatsApp Automation Tool
# Author: Oğuzhan Cem Yücel
# Date: 2024-12-19
# Version: 1.0
# Description:
#   Automates message processing and command execution
#   for WhatsApp using Selenium.
############################################################################################

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from datetime import datetime
import time


class WhatsAppAutomation:

    def __init__(self):
        self.response_dict={
            "merhaba":"Merhaba! Sana nasıl yardımcı olabilirim? \n",
            "nasılsın":"İyiyim, teşekkür ederim! siz nasılsınız. \n",
            "teşekkürler":"Rica ederim! Yardım edebileceğim başka bir şey var mı? \n",
            "iyi misin": "Saçma sapan konuşma la. \n",
            "o kim şekerim": "o da benim şekerim \n"
        }
        self.service = Service("C:/tools/chromedriver-win64/chromedriver.exe")                                                                                                               # Chrome Driverın yolunu verdiğimiz yer.
        self.driver = webdriver.Chrome(service=self.service)
        self.last_message = None                                                                                                                                                             # Son mesajı saklamak için değişken.
        self.current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.help_message=(
            "------ YARDIM MENÜSÜ ------\n"
            "Mevcut komutlar:\n"
            "1. *exit*  - Programı sonlandırır.\n"
            "2. *help*  - Bu yardım mesajını görüntüler.\n"
            "3. *not* - not modu açma.\n"
            "4. *not bitti* - not modu kapatma.\n"
            "5. *gif* - Gif gönderme modu açma.\n"
            "6. *change chat* - Sohbet edilen kişiyi değiştirme.\n "
            )                                                                                                                                                                                # Yardım mesajı
        self.user_details=""                                                                                                                                                                 # Ulaşmak istediğimiz kişi adı

    def save_note_to_file(self, filename="Note.txt"):                                                                                                                                        # Not alma fonksiyonu
        """
        Bu fonksiyon, WhatsApp Web'deki mesajları takip ederek "Not bitti" mesajına kadar
        belirtilen dosyaya (varsayılan olarak "Note.txt") kaydeder. Yeni mesajları
        tekrar kaydetmemek için kontrol yapar.

        Mesajları HTML kaynak kodundan alır, analiz eder ve sırayla dosyaya yazar.
        "Not bitti" mesajı algılandığında işlem sonlanır. Hata durumunda işlem durdurulur.
        """
        with open(filename,"a",encoding="utf8") as file:

            while True:
                try:
                    html_source = self.driver.page_source                                                                                                                                    # HTML kaynağını al
                    soup = BeautifulSoup(html_source, 'html.parser')                                                                                                                         # HTML'i analiz et
                    message = soup.find_all('span', class_='_ao3e selectable-text copyable-text')                                                                                            # Mesajları bul

                    if message:
                        last_note = message[-1].text
                        if last_note.lower() == "not bitti":
                            file.write(self.current_time +"\n"+"\n")
                            print("Not kaydı tamamlandı.")
                            break
                        elif last_note != self.last_message:                                                                                                                                 # Aynı mesajı tekrar kaydetme
                            self.last_message = last_note
                            file.write(self.last_message + "\n")
                            print(f"Not eklendi: {self.last_message}")
                    time.sleep(2)
                except Exception as e:
                    print(f"Not modunda hata oluştu: {e}")
                    break

    def send_mesage(self,message):                                                                                                                                                           # Kullanıcıya yollamak istediğimiz mesajlar için fonksiyon
        """
        Bu fonksiyon, WhatsApp Web'de belirli bir kullanıcıya mesaj göndermek için kullanılır.
        1. Mesaj kutusu bulunur ve mesaj (`message`) yazılır.
        2. Mesaj kutusu dışındaki bir alana tıklanarak mesaj gönderilir.
        XPATH değerleri WhatsApp Web'in yapısına bağlıdır ve değişebilir.
        """
        wait = WebDriverWait(self.driver, 20)

        message_box =wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="main"]/footer/div[1]/div/span/div/div[2]/div[1]/div[2]/div[1]/p')))
        message_box.click()
        message_box.send_keys(message)

        free_click=wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="main"]/div[3]/div/div[2]/div[3]')))
        free_click.click()

    def auto_reply(self,message):
        response = self.response_dict.get(message.lower())
        self.send_mesage(response)

    def change_chat(self):
        """
        Bu fonksiyon, WhatsApp Web'de mevcut sohbeti değiştirmek için kullanılır.
        1. Kullanıcıdan yeni bir telefon numarası girmesi istenir ve kısa bir bekleme yapılır.
        2. Gelen son mesaj analiz edilerek yeni telefon numarası alınır.
        3. Sohbet arama alanı temizlenir, yeni numara yazılır ve ilgili sohbet açılır.

        Önemli Noktalar:
        - Gelen mesajın bir komut olmadığını kontrol eder.
        - XPATH değerleri WhatsApp Web'in yapısına bağlıdır ve değişebilir.
        """
        wait = WebDriverWait(self.driver, 10)
        self.send_mesage('Yeni telefon numarasını giriniz. \n')
        time.sleep(15)                                                                                                                                                                       # Yeni mesajın gelmesini beklemek için kısa bir duraklama

        html_source = self.driver.page_source
        soup = BeautifulSoup(html_source, 'html.parser')
        message = soup.find_all('span', class_='_ao3e selectable-text copyable-text')                                                                                                        # Gelen mesajları bul

        if message:
            new_number_message = message[-1].text                                                                                                                                            # Son gelen mesajı al
            if new_number_message != "change chat":                                                                                                                                          # Gelen mesajın komut olmadığını kontrol et
                chat_list_area = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="side"]/div[1]/div/div[2]/div[2]/div/div/p')))
                chat_list_area.click()
                chat_list_area.send_keys(Keys.CONTROL + "a")
                chat_list_area.send_keys(Keys.BACKSPACE)
                chat_list_area.send_keys(new_number_message)
                chat_list_area.send_keys(Keys.ENTER)
                print("Telefon numarası değiştirildi:", new_number_message)
            else:
                print("Hata: Yeni telefon numarası bekleniyor ancak 'change number' mesajı tekrar algılandı.")

    def send_GIF(self):
        """
        Bu fonksiyon, WhatsApp Web üzerinden bir GIF göndermek için kullanılır.
        1. Kullanıcıdan GIF için bir anahtar kelime girmesi istenir.
        2. GIF seçme ve arama paneli açılır, anahtar kelimeyle ilgili GIF aranır.
        3. Uygun bir GIF seçilerek gönderilir.

        Önemli Noktalar:
        - "gif" komutundan farklı bir mesaj geldiğinde anahtar kelime olarak kabul edilir.
        - XPATH değerleri WhatsApp Web'in yapısına bağlıdır ve değişebilir.
        """
        try:
            wait = WebDriverWait(self.driver, 20)
                                                                                                                                                                                             # Kullanıcıya GIF anahtar kelimesini girmesini iste
            GIF_keyword = None

            while not GIF_keyword:                                                                                                                                                           # Anahtar kelime gelene kadar bekle
                html_source = self.driver.page_source
                soup = BeautifulSoup(html_source, 'html.parser')
                messages = soup.find_all('span', class_='_ao3e selectable-text copyable-text')                                                                                               # Gelen mesajları bul

                if messages:
                    last_message = messages[-1].text
                    if last_message.lower() != "gif":                                                                                                                                        # "gif" komutundan farklı bir mesaj alındığında
                        GIF_keyword = last_message
                    else:
                        time.sleep(1)                                                                                                                                                        # Çok sık kontrol etmeyi önlemek için kısa bir bekleme süresi

                                                                                                                                                                                             # Anahtar kelime bulundu, işlemlere başla
            sticker_button = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="main"]/footer/div[1]/div/span/div/div[2]/div[1]/div[1]/button/span')))
            sticker_button.click()

            GIF_button = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="expressions-panel-container"]/span/div/ul/div[2]/div/div/div[2]/button')))
            GIF_button.click()

            GIF_search_area = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="expressions-panel-container"]/span/div/ul/div[1]/div[2]/div[2]/div[1]/label/div/input')))
            GIF_search_area.click()
            GIF_search_area.send_keys(GIF_keyword)
            GIF_search_area.send_keys(Keys.ENTER)

            time.sleep(3)

            GIF_selected = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="expressions-panel-container"]/span/div/ul/div[1]/div[2]/div[2]/div[2]/div/div/div[1]/div[1]/div/div/img')))
            GIF_selected.click()

            send_button = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="app"]/div/div[3]/div/div[2]/div[2]/span/div/div/div/div[2]/div/div[2]/div[2]/div/div')))
            send_button.click()

            print(f"GIF '{GIF_keyword}' başarıyla gönderildi.")
        except Exception as e:
            print(f"GIF gönderiminde hata oluştu: {e}")


    def start(self):
        """
        Bu fonksiyon, WhatsApp Web'e giriş yapıp belirli bir telefon numarasına ait sohbeti başlatır.
        1. WhatsApp Web'e gidilir ve giriş yöntemi telefon doğrulamasına alınır.
        2. Ülke kodu ve telefon numarası belirtilen alana girilir.
        3. Numara doğrulandıktan sonra, sohbet ekranında arama çubuğu kullanılarak ilgili kişi bulunur ve sohbet açılır.
        4. Sohbet açıldıktan sonra, gelen mesajları izlemek için `self.monitor_message()` çağrılır.

        Önemli Noktalar:
        - XPATH değerleri WhatsApp Web'in yapısına bağlıdır ve değişebilir.
        """
        self.driver.get("https://web.whatsapp.com/")

        phone_number="telefon numaran buraya yazılacak(ülke kodu ile)"

        wait = WebDriverWait(self.driver, 60)

        phone_number_selection= wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="app"]/div/div[2]/div[2]/div[1]/div/div/div[2]/div[1]/div[5]/span/div')))                    # Giriş Yöntemini qr koddan telefon doğrulamasına almak için XPATH'ını değişkene atadık.
        phone_number_selection.click()                                                                                                                                                       # Değişkene tıklanmasını sağladık.

        country_code_selection =wait.until(EC.visibility_of_element_located((By.XPATH,'//*[@id="app"]/div/div[2]/div[2]/div[1]/div/div/div[3]/div[1]/div[2]/div/div/div/form/input')))       # Ülke kodu yazma yerini XPATH'ını değişkene atadık.
        country_code_selection.click()                                                                                                                                                       # Ülke kodu metin kutusunun tıklamasını sağladık.
        country_code_selection.send_keys(Keys.CONTROL+"a")                                                                                                                                   # Ülke kodunun olduğu text boxun içindeki her şeyi seçtik.
        country_code_selection.send_keys(Keys.BACKSPACE)                                                                                                                                     # Ülke kodunun olduğu text boxun içindeki her şeyi sildik.
        country_code_selection.send_keys(phone_number)                                                                                                                                       # telefon numarası yazılacak yerin içine ülke kodlu bir şekilde değişkene atadığımız telefon numarsını girdik.


        next_button_for_verification= wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="app"]/div/div[2]/div[2]/div[1]/div/div/div[3]/div[3]/button/div/div')))               # telefon numarası yazıldıktan sonra ileri tuşunun XPATH'ını değişkene atadık.
        next_button_for_verification.click()                                                                                                                                                 # telefon numarası yazıldıktan sonra ileri tuşuna bastık.

        search_bar = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="side"]/div[1]/div/div[2]/div[2]/div/div/p')))                                                          # Arama çubuğunu XPATH'ini değişkene atadık.
        search_bar.click()                                                                                                                                                                   # Arama çubuğuna tıkladık.
        search_bar.send_keys(phone_number)                                                                                                                                                   # Arama kutusuna istediğimiz kişiyi yazıp aramak için text boxa atamasını yaptık.
        search_bar.send_keys(Keys.ENTER)                                                                                                                                                     # Enter tuşuna bastık.

        self.monitor_message()

    def monitor_message(self):
        """
        Bu fonksiyon, WhatsApp Web'deki gelen mesajları sürekli izler ve belirli komutlara göre işlem yapar.

        Fonksiyonun İşleyişi:
        1. HTML kaynağı alınarak gelen mesajlar analiz edilir.
        2. Son mesaj önceki mesajdan farklıysa işleme alınır:
           - `exit`: Sohbetten çıkılır ve "İyi Günler" mesajı gönderilir.
           - `help`: Kullanıcıya kullanılabilir komutlar gönderilir.
           - `not`: Not alma işlemi başlatılır.
           - `gif`: Belirtilen anahtar kelimeyle GIF gönderilir.
           - `change chat`: Sohbet değişikliği yapılır.
        3. Mesaj bulunmazsa veya başka bir mesaj gelirse döngü devam eder.

        Önemli Noktalar:
        - XPATH değerleri ve sınıf isimleri WhatsApp Web'in yapısına bağlıdır ve değişebilir.
        - Hata durumunda bir mesaj yazdırılır ve döngü sonlandırılır.
        """
        while True:
            try:
                html_source = self.driver.page_source                                                                                                                                        # Html kaynağını aldık
                soup =BeautifulSoup(html_source, 'html.parser')                                                                                                                              # BeatifulSoup ile HTML'i analiz ettik
                message = soup.find_all('span', class_='_ao3e selectable-text copyable-text')                                                                                                # Gelen mesajları bulduk.

                if message:                                                                                                                                                                  # Son yollanan mesajları alıyoruz.
                    last_message_text = message[-1].text

                    if last_message_text != self.last_message:
                        self.last_message = last_message_text
                        print("Yeni Mesaj:", self.last_message)

                    elif self.last_message.lower() =="exit":                                                                                                                            # mesaj ile çıkmak için yol ekledik ve tekrar başladığında başka mesaj yoksa tekrar algılamaması için ve daha güzel durması için bir mesaj ekledik.
                        self.send_mesage('iyi Günler \n')
                        break

                    elif self.last_message.lower() == "help":                                                                                                                           # Kullanıcı metotları öğrensin diye help metodu ekledik.
                        self.send_mesage(self.help_message)

                    elif self.last_message.lower() == "not":                                                                                                                            # Kullanıcı notlarını tutması için not metodu ekledik.
                        self.save_note_to_file()

                    elif self.last_message.lower() == "gif":
                        self.send_GIF()

                    elif self.last_message.lower() == "change chat":
                        self.change_chat()

                    elif self.last_message.lower() in self.response_dict:
                        self.auto_reply(self.last_message)

                    else:
                        time.sleep(3)

                else:
                    time.sleep(3)

            except Exception as e:
                    print(f"hata oluştu:{e}")
                    break


    def stop(self):                                                                                                                                                                          # otomasyonu durdurmak için kullanıyoruz.
        self.driver.quit()

if __name__ =="__main__":
    automation=WhatsAppAutomation ()
    automation.start()