class MexPacket:
    def __init__(self, mex="", time=7, riga=2):
        self.bike = 0
        self.type = 8
        self.riga = riga
        if riga == 1:
            self.mex1 = mex
            self.time1 = time
            self.mex2 = ""
            self.time2 = 0
        else:
            self.mex2 = mex  # ABBIAMO DUE RIGHE, POTREMMO RISERVARNE UNA AI MESSAGGI DEL SISTEMA E UNA USARLA NOI
            self.time2 = time
            self.mex1 = ""
            self.time1 = 0
        if self.__len__() > 255:
            raise ValueError('Dimensioni pacchetto superate')  #  Alza un'eccezione se le dimensioni dei messaggi
            # sono troppo lunghe, probabilmente non avremo mai questo problema perchè a schermo c'è spazio per
            #  visualizzare meno roba ancora

    def to_str(self):
        mex1 = "Mex1: " + self.mex1 + " Durata: " + str(self.time1) + "\n"
        mex2 = "Mex2: " + self.mex2 + " Durata: " + str(self.time2) + "\n"
        return mex1 + mex2

    def __len__(self):
        return len(self.encode())

    def encode(self):
        if self.riga == 1:
            return str(self.bike) + ";" + str(self.type) + ";" + str(self.riga) + ";" + self.mex1 + ";" + str(self.time1)
        else:
            return str(self.bike) + ";" + str(self.type) + ";" + str(self.riga) + ";" + self.mex2 + ";" + str(self.time2)

    def decode(self, data):
        parts = data.split(";")
        self.bike = parts[0]
        self.type = parts[1]
        self.mex1 = parts[2]
        self.time1 = int(parts[3])
        self.mex2 = parts[4]
        self.time2 = int(parts[5])
        print(self.to_str())
        # print(self.hr, self.timer)
