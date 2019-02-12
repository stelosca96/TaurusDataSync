from digi.xbee.devices import XBeeDevice
from digi.xbee.devices import RemoteXBeeDevice
from digi.xbee.models.address import XBee64BitAddress

from taurus import Taurus

PORT = "COM5"
BAUD_RATE = 115200
REMOTE_DEVICE_ADDRESS = "0013A200418AE577"


class Communication:

    def __init__(self, taurus: Taurus, taurus_x: Taurus):
        self.xbee_state = False

        self.taurus = taurus
        self.taurus_x = taurus_x

        print("INIT COMMUNICATION")
        self.device = XBeeDevice(PORT, BAUD_RATE)
        try:
            self.device.open()
            self.remote_device = RemoteXBeeDevice(self.device, XBee64BitAddress.from_hex_string(REMOTE_DEVICE_ADDRESS))
            self.device.add_data_received_callback(self.receiver)
            self.xbee_state = True
        except:
            self.xbee_state = False
            print("XBEE non collegato")

    def send(self, data):
        mex = data.encode()
        print("Data:\n", mex, "\nSize: ", data.__len__())
        if self.xbee_state:
            self.device.send_data_async(self.remote_device, mex)
        # data.decode(mex)

    def send_sync(self, data):
        mex = data.encode()
        print("Data:\n", mex, "\nSize: ", data.__len__())
        if self.xbee_state:
            try:
                self.device.send_data(self.remote_device, mex)
                return True
            except:
                print("Pacchetto non ricevuto dal destinatario")
                return False

    def send_broadcast(self, data):
        mex = data.encode()
        print("Data:\n", mex, "\nSize: ", data.__len__())
        if self.xbee_state:
            self.device.send_data_broadcast(self.remote_device, mex)

    def receiver(self, xbee_message):
        mex = xbee_message.data.decode()
        print("From %s >> %s" % (xbee_message.remote_device.get_64bit_addr(), mex))
        self.direct_to_bike(mex)

    def direct_to_bike(self, mex):
        if mex[0] == "0":
            self.taurus.new_mex(mex, mex[2])
        if mex[0] == "1":
            self.taurus_x.new_mex(mex, mex[2])
