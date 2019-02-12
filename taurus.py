from dataPacket import DataPacket


class Taurus:
    def __init__(self):
        self.data = DataPacket()

    def get_heartrate(self):
        return self.data.hr

    def get_power(self):
        return self.data.power

    def get_cadence(self):
        return self.data.cad

    def get_distance(self):
        return self.data.distance

    def get_speed(self):
        return self.data.speed

    def get_timer(self):
        return self.data.timer

    def get_gear(self):
        return self.data.gear

    def new_mex(self, mex, mex_type):
        print(mex_type)
        if mex_type == "0":
            self.data.decode(mex)
            print("New data: ", self.data.timer)
        # TIPI PACCHHETI
        # 0 -> DATI
        # 1 -> IMPOSTAZIONI SALVATE SU TAURUS
