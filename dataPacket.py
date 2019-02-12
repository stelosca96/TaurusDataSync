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

    def __len__(self):
        return len(self.encode())

    def encode(self):
        return str(self.bike) + ";" + str(self.type) + ";" + str(self.hr) + ";" +\
               str(self.power) + ";" + str(self.cad) + ";" + str(self.distance) + ";" + str(self.speed) + ";" + \
               str(round(self.timer, 2)) + ";" + str(self.gear)

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
        print(self.hr, self.timer)
