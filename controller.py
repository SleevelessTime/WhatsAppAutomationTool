############################################################################################
# Project: WhatsApp Automation Controller
# Author: Oğuzhan Cem Yücel
# Date: 2024-12-19
# Version: 1.0
# Description:
#   This Python script is a controller for automating 
#   WhatsApp operations using the WhatsappAppAutomation class.
#   The script provides a command-line interface that allows users to 
#   start or stop the automation and gracefully manage its state.
############################################################################################


from otomasyon0 import WhatsAppAutomation


def control():
    print("Whatsapp otomasyonu basltmak icin 'Start' komutunu girin. Cikmak icin 'Exit' komutunu girin.  ")

    automation = None

    while True:
        command =input("Bir komut girin: ")
        if command.lower() =="start":
            if automation is None:
                print("Whatsapp otomasyonu baslatiliyor ...")
                automation = WhatsAppAutomation()
                automation.start()
            else:
                print("Otomasyon zaten çalişiyor.")
        
        elif command.lower() == "exit":
            if automation is not None:
                print("Otomasyon durduruluyor ...")
                automation.stop()
                automation = None
            else:
                print("Otomasyon zaten Durdurulmuş.")
            break

        else:
            print("Geçersiz komut !")

if __name__ == "__main__":
    control()