class SettingsPacket:
    def __init__(self):
        # sogno di mettere tutti i parametri in una 
        # lista(forse meglio dizionario, da python 3.6 mantengono l'ordine) todo: verificare il compilatore per il tinker
        # cosi' da alleggerire il metodo encode e update
        # vedi sotto
        
        # todo: convertire quale conviene
        # a Parameter()
        # es. syncronized lo lascerei a parte
        
        self.lista = list()
        
        self.bike = 0
        self.type = 0
        self.synchronized = False
        
        # NON MODIFICABILI DA REMOTO, SOLO A SCOPO INFORMATIVO
        self.log = False
        self.video = False  # decice se avviare il modulo video
        self.ant = False
        self.ant_running = False  # è crashata l'ant?? Questo flag dovrebbe dirlo
        self.video_running = False  # è craschato il video?? Questo flag dovrebbe dirlo
        self.powermeter_running = False  # Indica se il powermeter ha trasmesso dei dati
        self.heartrate_running = False
        self.speed_running = False
        
        # MODIFICABILI DA REMOTO
        self.average_power_time = -1  # Tempo su cui viene calcolata la potenza media. Default 3s
        self.led_mode = 0  # Modalità funzionamento LED. 0 -> spenti
        self.circumference = -1  # Circonferenza della ruota. Default 1.450
        self.csv = False  # Decide se avviare o fermare la registrazione su file csv
        self.timer = 0  # indica se il timer è avviato o in pausa
        
        # IMPOSTAZIONI DEL POWERMETER
        self.calibration = False  # Indica se il powermeter è in attesa di calibrazione
        self.calibration_value = -1  # Valore della calibrazione del powermeter. Default 500
        
        # REGISTRAZIONE VIDEO ON BOARD
        self.video_record = False  # La implementiamo veramente???

    def encode(self):
        return ';'.join(map(str,self.lista)
        
        '''
        return str(self.bike) + ";" + str(self.type) + ";" + \
               bool2str(self.log) + ";" + bool2str(self.video) + ";" + bool2str(self.ant) + ";" + \
               bool2str(self.video_running) + ";" + bool2str(self.powermeter_running) + ";" +\
               bool2str(self.heartrate_running) + ";" + bool2str(self.speed_running) + ";" + \
               str(self.average_power_time) + ";" + str(self.led_mode) + ";" + str(self.circumference) + ";" +\
               bool2str(self.csv) + ";" + str(self.timer) + ";" + bool2str(self.calibration) + ";" +\
               str(self.calibration_value) + ";" + bool2str(self.video_record) + ";" + bool2str(self.video_running)'''

    def update(self, mex):
        parts = mex.split(";")
        
        for index, value in enumerate(parts):
            self.lista[index].value = value
       
        '''
        self.log = parts[2]
        self.video = parts[3]
        self.ant = parts[4]
        self.video_running = parts[5]
        self.powermeter_running = parts[6]
        self.heartrate_running = parts[7]
        self.speed_running = parts[8]
        self.average_power_time = parts[9]
        self.led_mode = parts[10]
        self.circumference = parts[11]
        self.csv = parts[12]
        self.timer = parts[13]
        self.calibration = parts[14]
        self.calibration_value = parts[15]
        self.video_record = parts[16]
        self.video_running = parts[17]
        '''
                        
        self.synchronized = True
        
        # per continuare ad accedere in modo diretto 
        # dizionario, costanti, oppure?
        print(self.synchronized, self.video_record)
        print(self.circumference)
        print("SINCRONIZZAZIONE AVVENUTA")

    def __len__(self):
        return len(self.encode())

    
class Parameter:
    __init__(self, method=int()):
        # bool sono inizializzati a False
        # gli int a 0, voledo si può aggiungere un
        # paramtro per inizializzarli a un valore
        self.value = method
    
    def get_value(self):
        return self.value
    
    def __str__(self):
        # per adesso lascio il passaggio del parametro 
        # self.value, si puo' incorporare il metodo
        # a questa classe e aumentare l'astrazione
        return str(int(self.value)) if isinstance(self.value, bool) else str(self.value)
    
                        
                        
# volendo si possono togliere
def bool2str(variable):
    # si può evitare passando per int()
    # vale quello scritto per str2bool
    if variable:
        return "1"
    else:
        return "0"


def str2bool(variable):
    # questo gia' lo fa il metodo bool() equivalente di str()
    # bool(0) => False, bool(!=0) => True
    if variable == "1":
        return True
    else:
        return False

     
