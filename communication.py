from digi.xbee.devices import RemoteXBeeDevice
from digi.xbee.models.address import XBee64BitAddress
from digi.xbee.devices import XBeeDevice
# from taurus import Taurus

PORT = "COM5"
BAUD_RATE = 115200


class Communication:
    xbee_state = False
    device = None

    def __init__(self, taurus, taurus_x):
        self.taurus = taurus
        self.taurus_x = taurus_x

        print("INIT COMMUNICATION")
        Communication.device = XBeeDevice(PORT, BAUD_RATE)
        try:
            Communication.device.open()
            Communication.device.add_data_received_callback(self.receiver)
            Communication.xbee_state = True
        except:
            Communication.xbee_state = False
            print("XBEE non collegato")

    @staticmethod
    def send(address, mex):
        print("Data:\n", mex, "\nSize: ", mex.__len__())
        if Communication.xbee_state:
            remote_device = RemoteXBeeDevice(Communication.device, XBee64BitAddress.from_hex_string(address))
            Communication.device.send_data_async(remote_device, mex)
        # data.decode(mex)

    @staticmethod
    def send_sync(address, mex):
        print("Data: ", mex, "\nSize: ", mex.__len__())
        if Communication.xbee_state:
            remote_device = RemoteXBeeDevice(Communication.device, XBee64BitAddress.from_hex_string(address))

            try:
                Communication.device.send_data(remote_device, mex)
                return True
            except:
                print("Pacchetto non ricevuto dal destinatario")
                return False
        return False

    @staticmethod
    def send_broadcast(data):
        mex = data.encode()
        print("Data: ", mex, "\nSize: ", data.__len__())
        if Communication.xbee_state:
            Communication.device.send_data_broadcast(mex)

    def receiver(self, xbee_message):
        mex = xbee_message.data.decode()
        print("From %s >> %s" % (xbee_message.remote_device.get_64bit_addr(), mex))
        self.direct_to_bike(mex)

    def direct_to_bike(self, mex):
        if mex[0] == "0":
            self.taurus.new_mex(mex, mex[2])
        if mex[0] == "1":
            self.taurus_x.new_mex(mex, mex[2])
