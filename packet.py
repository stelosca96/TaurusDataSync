import json

from digi.xbee.devices import RemoteXBeeDevice, XBeeDevice
from digi.xbee.models.address import XBee64BitAddress

PORT = "/dev/ttyUSB0"
BAUD_RATE = 115200

# TODO: togliere l'immissione esplicita degli
# indirizzi quando si chiamano le funzioni di send


class Communication:
    def __init__(self):
        self.__listener = dict()
        # self.device = XBeeDevice(PORT, BAUD_RATE)
        # self.device.open()
        # self.device.add_data_received_callback(self.receiver)

    # DIREZIONE: server --> bici
    @staticmethod
    def send(address, packet):
        self.device.send_data_async(RemoteXBeeDevice(
            self.device, XBee64BitAddress.from_hex_string(address)), packet.encode)

    @staticmethod
    def send_sync(address, packet):
        # aspetta l'ack, se scatta il
        # timeout e non riceve risposta
        # lancia una eccezione
        self.device.send_data(RemoteXBeeDevice(
            self.device, XBee64BitAddress.from_hex_string(address)), packet.encode)

    @staticmethod
    def send_broadcast(packet):
        self.device.send_data_broadcast(packet.encode)

    # DIREZIONE: bici --> server
    def receiver(self, packet):
        pass

    @property
    def listener(self):
        return self.__listener

    @listener.setter
    def listener(self, l):
        self.__listener.update({l.id: l})


class Packet:
    def __init__(self, content=list()):
        self.content = self.__filter(content)

    @property
    def decode(self):
        return self.content

    @property
    def encode(self):
        return ';'.join(map(str, self.content))

    @decode.setter
    # usato come la update()
    def decode(self, content):
        self.content = self.__filter(content)

    @property
    def jsonify(self):
        type = self.content[1]
        content = self.content[2:]
        content.reverse()

        with open('packet.json') as f:
            res = json.load(f)[str(type)]

        for key, _ in res.items():
            res[key] = str(content.pop())

        return json.dumps(res)

    def __filter(self, data):
        return data if type(data) is list else [i for i in data.values()]

    def __len__(self):
        return len(self.content)

    def __str__(self):
        # TODO: farlo meglio
        return str(self.content)
