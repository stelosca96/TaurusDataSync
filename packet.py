import json


class Packet:
    def __init__(self, data=list()):
        self.content = data

    def encode(self):
        return ';'.join(map(str, self.content))

    def decode(self, data):
        self.content = [field for field in data]
        return self.content

    def jsonify(self):
        type = self.content[1]
        content = self.content[2:]
        content.reverse()

        with open('packet.json') as f:
            res = json.load(f)[str(type)]

        for key, _ in res.items():
            res[key] = str(content.pop())

        return json.dumps(res)

    def __len__(self):
        return len(self.content)

    def __str__(self):
        # TODO: farlo meglio
        return str(self.content)




''''
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
'''