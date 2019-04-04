class SettingsPacket:
    def __init__(self):
        self.lista = list()
        # TODO: lettura lista da json
        self.synchronized = False

    def encode(self):
        return ';'.join(map(str, self.lista))

    def update(self, mex):
        parts = mex.split(';')

        for index, value in enumerate(parts):
            self.lista[index].value = value

    def __len__(self):
        return len(self.lista())


class DataPacket:
    def __init__(self, heartrate=-1, power=-1, cadence=-1, speed=-1, distance=-1, timer=-1, gear=-1):
        self.bike = 0
        self.type = 0
        self.hr = heartrate
        self.power = power
        self.cad = cadence
        self.distance = distance
        self.speed = speed
        self.timer = timer
        self.gear = gear

    def to_str(self):
        timer = "Time: " + str(self.timer) + "s\n"
        hr = "Heart Rate: " + str(self.hr) + "bpm\n"
        power = "Power: " + str(self.power) + "W\n"
        cadence = "Cadence: " + str(self.cad) + "rpm\n"
        speed = "Speed: " + str(self.speed) + "km/h\n"
        distance = "Distance: " + str(self.distance) + "km\n"
        gear = "Gear: " + str(self.gear) + "\n"
        return timer + hr + power + cadence + speed + distance + gear

    def to_json(self):
        data = {
            "time": float(self.timer),
            "heartrate": int(self.hr),
            "power": int(self.power),
            "cadence": int(self.cad),
            "speed": int(self.speed),
            "distance": int(self.distance),
            "gear": int(self.gear),
        }
        return json.dumps(data)

    def __len__(self):
        return len(self.encode())

    def encode(self):
        return str(self.bike) + ";" + str(self.type) + ";" + str(self.hr) + ";"
        + str(self.power) + ";" + str(self.cad) + ";" + \
            str(self.distance) + ";" + str(self.speed) + ";"
        + str(round(self.timer, 2)) + ";" + str(self.gear)

    def decode(self, data):
        parts = data.split(";")
        self.bike = parts[0]
        self.type = parts[1]
        self.hr = parts[2]
        self.power = parts[3]
        self.cad = parts[4]
        self.distance = parts[5]
        self.speed = parts[6]
        self.timer = parts[7]
        self.gear = parts[8]
        # print(self.hr, self.timer)


class MexPacket:
    def __init__(self, mex="", priority=4, time_m=5):
        self.bike = 0
        self.type = 8
        self.mex_send = mex
        self.priority = priority
        self.time_m = time_m
        self.mex1 = ""
        self.time1 = 0
        self.mex2 = ""
        self.time2 = 0

        if self.__len__() > 255:
            # Alza un'eccezione se le dimensioni dei messaggi
            raise ValueError('Dimensioni pacchetto superate')
            # sono troppo lunghe, probabilmente non avremo mai questo problema perchè a schermo c'è spazio per
            #  visualizzare meno roba ancora

    def to_str(self):
        mex1 = "Mex1: " + self.mex1 + \
            " Durata: " + str(self.time1) + "\n"
        mex2 = "Mex2: " + self.mex2 + \
            " Durata: " + str(self.time2) + "\n"
        return mex1 + mex2

    def __len__(self):
        return len(self.encode())

    def encode(self):
        return str(self.bike) + ";" + str(self.type) + ";" + self.mex_send + ";" + str(self.priority) + ";" + \
            str(self.time_m)

    def decode(self, data):
        parts = data.split(";")
        self.bike = parts[0]
        self.type = parts[1]
        self.mex1 = parts[2]
        self.time1 = int(parts[3])
        self.mex2 = parts[4]
        self.time2 = int(parts[5])
        # print(self.to_str())
        # print(self.hr, self.timer)


class Taurus:
    def __init__(self):
        self.data = DataPacket()
        self.settings = SettingsPacket()
        self.mex = MexPacket()
        # print(self.settings.encode())
        # print(self.settings.__len__())
        # self.settings.update(self.settings.encode())
        # self.i = 0

    def synchronized(self):
        return self.settings.synchronized

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

    def get_log_state(self):
        return self.settings.log

    def get_ant_state(self):
        return self.settings.ant

    def get_ant_running(self):
        return self.settings.ant_running

    def get_video_state(self):
        return self.settings.video

    def get_video_running(self):
        return self.settings.video_running

    def get_powemeter_running(self):
        return self.settings.powermeter_running

    def get_speed_running(self):
        return self.settings.speed_running

    def get_heartrate_running(self):
        return self.settings.heartrate_running

    def get_average_power_time(self):
        return self.settings.average_power_time

    def get_led_mode(self):
        state = self.settings.led_mode
        if state == "0":
            return "Spenti"
        elif state == "1":
            return "Tricolore statico"

    def get_circumference(self):
        return self.settings.circumference

    def get_csv_state(self):
        return self.settings.csv

    def get_timer_state(self):
        state = self.settings.timer
        if state == "0":
            return "Stoppato"
        elif state == "1":
            return "Avviato"
        elif state == "2":
            return "Autopausa"

    def get_antilope(self):
        return self.settings.antilope

    def get_calibration_request(self):
        return self.settings.calibration

    def get_calibration_value(self):
        return self.settings.calibration_value

    def get_video_record_state(self):
        return self.settings.video_record

    def get_message(self, riga):
        if riga == 1:
            return self.mex.mex1, self.mex.time1
        else:
            return self.mex.mex2, self.mex.time2

    def new_mex(self, mex, mex_type):
        # print(mex_type)
        if mex_type == "0":
            self.data.decode(mex)
            # print(self.i)
            # self.i += 1
            # print("New data: ", self.data.timer)
        if mex_type == "1":
            self.settings.update(mex)
        if mex_type == "8":
            self.mex.decode(mex)

    def set_circumference(self, value):
        if float(value) >= 2:
            print("Errore: dimensione ruota troppo grande!!")
            return False
        if float(value) <= 1:
            print("Errore: dimensione ruota troppo piccola!!")
            return False
        mex = str(self.settings.bike) + ";4;" + str(value)
        print(mex)
        return Communication.send_sync(self.REMOTE_DEVICE_ADDRESS, mex)

    def set_calibration(self, value=-1):
        if int(value) > 0:
            mex = str(self.settings.bike) + ";3;0;" + str(value)
        else:
            mex = str(self.settings.bike) + ";3;1;" + str(value)
        print(mex)
        return Communication.send_sync(self.REMOTE_DEVICE_ADDRESS, mex)

    def set_message(self, string, time=7, priority=4):
        packet = MexPacket(string, priority, time)
        try:
            mex = packet.encode()
        except ValueError as err:
            print(err.args)
            return False
        print(mex)
        return Communication.send_sync(self.REMOTE_DEVICE_ADDRESS, mex)

    def reset_timer_distance(self):
        mex = str(self.settings.bike) + ";5"
        return Communication.send_sync(self.REMOTE_DEVICE_ADDRESS, mex)

    def settings_request(self):
        mex = str(self.settings.bike) + ";11"
        return Communication.send_sync(self.REMOTE_DEVICE_ADDRESS, mex)

    def set_video_record(self, state):
        if state:
            s = "1"
        else:
            s = "0"
        mex = str(self.settings.bike) + ";6;" + s
        return Communication.send_sync(self.REMOTE_DEVICE_ADDRESS, mex)

    def set_antilope(self, state):
        if state:
            s = "1"
        else:
            s = "0"
        mex = str(self.settings.bike) + ";13;" + s
        return Communication.send_sync(self.REMOTE_DEVICE_ADDRESS, mex)

    def get_data_json(self):
        return self.data.to_json()
