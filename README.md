### Legenda

#### CAMPI PACCHETT0

    0.  "destinatario"    0 -> Taurus | 1 -> TaurusX  
    1.  "tipo"            0 >> 13
    2.  "contenuto"       varia in base al tipo di pacchetto   

#### TIPO DI PACCHETTO

    #0  -> DATI
    #1  -> IMPOSTAZIONI SALVATE SU TAURUS
    #3  -> CALIBRAZIONE POWERMETER
    #4  -> IMPOSTAZIONE CIRCONFERENZA
    #5  -> RESET (Distanza, Timer)
    #6  -> REGISTRAZIONE VIDEO
    #7  -> CALIBRAZIONE CAMBIO
    #8  -> MESSAGGI SU SCHERMO
    #9  -> LED
    #10 -> GESTIONE RASPBERRY
    #11 -> UPDATE SETTINGS REQUEST
    #13 -> PACCHETTO 13

#### CONTENUTO TIPO 0

    "heartrate"
    "power"
    "cadence"
    "distance"
    "speed"
    "time"
    "gear"

#### CONTENUTO TIPO 1

**Non modificabili**

    "log"
    "video"
    "ant"
    "ant_running"
    "video_running"
    "powermeter_running"
    "heartrate_running"
    "speed_running"

**Modificabili da remoto**

    "average_power_time"
    "led_mode"
    "circumference"
    "csv
    "timer"

**Impostazioni del powermeter**

    "calibration"
    "calibration_value"

**Registrazione video onboard**

    "video_record"    

#### PORTA USB

    dmesg | grep tty

#### INDIRIZZI ANTENNE

    arduino nano v2 (cavo giallo) -> "0013A200418AF52F"
    ardiuno nano v1 (due cavi)    -> "0013A200418AE5A9"
    arduino uno                   -> "0013A200418AE577"
