from .communication import Communication
from .packet import *

class Taurus:
    def __init__(self):
        # self.REMOTE_DEVICE_ADDRESS = "0013A200418AE5A9" # ANTENNA CON ARDUINO NANO v1
        # self.REMOTE_DEVICE_ADDRESS = "0013A200418AE577" # ANTENNA CON ARDUINO UNO
        self.REMOTE_DEVICE_ADDRESS = "0012A200418AF52F"  # ANTENNA CON ARDUINO NANO v2 (cavo giallo)

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
