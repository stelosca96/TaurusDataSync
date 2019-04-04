from digi.xbee.devices import RemoteXBeeDevice
from digi.xbee.models.address import XBee64BitAddress
from digi.xbee.devices import XBeeDevice

import json


PORT = "/dev/ttyUSB0"
BAUD_RATE = 115200

# TODO: togliere l'immissione esplicita degli
# indirizzi quando si chiamano le funzioni di send


class Communication:
    def __init__(self):
        self.listener = dict()
        #self.device = XBeeDevice(PORT, BAUD_RATE)
        # self.device.open()
        # self.device.add_data_received_callback(self.receiver)

    # DIREZIONE: server --> bici
    @staticmethod
    def send(address, packet):
        self.device.send_data_async(RemoteXBeeDevice(
            self.device, XBee64BitAddress.from_hex_string(address)), packet.encode())

    @staticmethod
    def send_sync(address, packet):
        # aspetta l'ack, se scatta il
        # timeout e non riceve risposta
        # lancia una eccezione
        self.device.send_data(RemoteXBeeDevice(
            self.device, XBee64BitAddress.from_hex_string(address)), packet.encode())

    @staticmethod
    def send_broadcast(packet):
        self.device.send_data_broadcast(packet.encode())

    # DIREZIONE: bici --> server
    def receiver(self, packet):
        pass

    def add_listener(self, l):
        self.listener.update({l.id: l})


class Packet:
    def __init__(self, content=list()):
        self.content = self.update(content)

    def encode(self):
        return ';'.join(map(str, self.content))

    def decode(self):
        return self.content

    def update(self, new):
        self.content = new if type(new) is list else [i for i in new.values()]
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
