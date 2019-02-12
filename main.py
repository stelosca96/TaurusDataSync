from taurus import Taurus
from communication import Communication

taurus = Taurus()
taurus_x = Taurus()
communication = Communication(taurus, taurus_x)

print(taurus.set_circumference(1.46))
# input()


def print_data():
    print("DATA:")
    print("Timer: ", taurus.get_timer())
    print("HR: ", taurus.get_heartrate())
    print("Power: ", taurus.get_power())
    print("Cad: ", taurus.get_cadence())
    print("Speed: ", taurus.get_speed())
    print("Distance: ", taurus.get_distance())


def print_settings():
    print("SETTINGS:")
    print("Sincronizzato: ", taurus.synchronized())
    print("Stato Ant: ", taurus.get_ant_state())
    print("Stato Video: ", taurus.get_ant_state())
    print("Stato Log: ", taurus.get_ant_state())
    print("Timer: ", taurus.get_timer_state())
    print("Led: ", taurus.get_led_mode())
    print("Richiesta di calibrazione: ", taurus.get_calibration_request())
    print("Valore calibrazione: ", taurus.get_calibration_value())
    print("Sto registrando il video: ", taurus.get_video_record_state())
    print("Tempo potenza media: ", taurus.get_average_power_time())
    print("Circonferenza ruota: ", taurus.get_circumference())
    print("Ho ricevuto dei dati dal powermeter: ", taurus.get_powemeter_running())
    print("Ho ricevuto dei dati dal sensore di velocità: ", taurus.get_speed_running())
    print("Ho ricevuto dei dati dalla fascia cardio: ", taurus.get_heartrate_running())
    print("Ho ricevuto dei dati dalla fascia cardio: ", taurus.get_heartrate_running())
    print("Il video sta funzionando: ", taurus.get_video_running())
    print("L'ant sta funzionando: ", taurus.get_ant_running())


choice = ""
while choice != "q":
    print("Taurus Data Sync")
    print("1) Ricezione")
    print("2) Trasmissione")
    choice = input()
    if choice == "1":
        while choice != "q":
            print("RICEZIONE: ")
            print("1) Dati")
            print("2) Settings")
            choice = input()
            if choice == "1":
                while choice != "q":
                    print_data()
                    print("Premere un tasto qualsiasi per aggiornare...")
                    print("q) Ritorna")
                    choice = input()
                choice = ""
            elif choice == "2":
                print_settings()
    elif choice == "2":
        while choice != "q":
            print("TRASMISSIONE: ")
            print("3) Calibrazione Powermeter")
            print("4) Impostazione circonferenza")
            print("5) Reset(Distanza, Timer)")
            print("6) Avvia/Ferma registrazione video")
            print("8) Messaggi su schermi")
            print("11) Richiesta UPDATE settings")
            choice = input()
            if choice == "3":
                val = input("Vuoi mettere un valore fisso(0 per ricerca automatica): ")
                if val != "0":
                    taurus.set_calibration(val)
                else:
                    taurus.set_calibration()
            elif choice == "4":
                dim = input("Dimensione circonferenza: ")
                taurus.set_circumference(dim)
            elif choice == "5":
                print("Non ancora implementato")
            elif choice == "6":
                print("Non ancora implementato")
            elif choice == "7":
                print("Non ancora implementato")
            elif choice == "8":
                print("Non ancora implementato")
            elif choice == "9":
                print("Non ancora implementato")
            elif choice == "10":
                print("Non ancora implementato")
            elif choice == "11":
                print("Non ancora implementato")

            # TIPI PACCHHETI
            # 0 -> DATI
            # 1 -> IMPOSTAZIONI SALVATE SU TAURUS
            # 3 -> CALIBRAZIONE POWERMETER
            # 4 -> IMPOSTAZIONE CIRCONFERENZA
            # 5 -> RESET (Distanza, Timer)
            # 6 -> REGISTRAZIONE VIDEO
            # 7 -> CALIBRAZIONE CAMBIO
            # 8 -> MESSAGGI SU SCHERMO
            # 9 -> LED
            # 10 -> GESTIONE RASPBERRY
            # 11 -> UPDATE SETTINGS REQUEST
