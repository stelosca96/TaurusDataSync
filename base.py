import json
import logging

from digi.xbee.devices import RemoteXBeeDevice, XBeeDevice
from digi.xbee.exception import (InvalidOperatingModeException,
                                 InvalidPacketException, TimeoutException)
from digi.xbee.models.address import XBee64BitAddress
from serial.serialutil import SerialException

log = logging.getLogger(__name__)

PORT = "/dev/ttyUSB0"
BAUD_RATE = 115200
# NOTE: ogni nuovo pacchetto
# che deve essere mandato al
# frontend deve avere la sua costante


class Const:
    @property
    def DATA(self):
        return '0'

    @property
    def SETTING(self):
        return '1'


# questa classe si interfaccia con
# le funzioni di basso livello
# dello xbee e si occupa i mandare
# e ricevere raw_message formati da
# stringhe del tipo {};{};{};{}
class Server:
    def __init__(self):
        self.__listener = dict()
        self.device = self.__open_device(PORT, BAUD_RATE)

    @property
    def listener(self):
        return self.__listener

    @listener.setter
    def listener(self, l):
        self.__listener.update({l.id: l})

    # DIREZIONE: server --> bici
    def send(self, address, packet):
        try:
            self.device.send_data_async(RemoteXBeeDevice(
                self.device, XBee64BitAddress.from_hex_string(address)), packet.encode)
        except (TimeoutException, InvalidPacketException):
            log.error('Dispositivo ({}) non trovato\n'.format(address))

    def send_sync(self, address, packet):
        # aspetta l'ack, se scatta il
        # timeout e non riceve risposta
        # lancia una eccezione
        try:
            self.device.send_data(RemoteXBeeDevice(
                self.device, XBee64BitAddress.from_hex_string(address)), packet.encode)
        except (TimeoutException, InvalidPacketException):
            log.error('ACK send_sync non ricevuto\n')

    def send_broadcast(self, packet):
        self.device.send_data_broadcast(packet.encode)

    # DIREZIONE: bici --> server
    def receiver(self, xbee_message):
        # per gestire il pacchetto vuoto
        if xbee_message != '':
            raw = xbee_message.data.decode()
            packet = Packet(raw)
            log.debug('Received packet: {}'.format(packet))
            dest = self.listener.get(packet.content[0])
            dest.receive(packet)

    def __open_device(self, port, baud_rate):
        device = XBeeDevice(port, baud_rate)
        try:
            device.open()
            device.add_data_received_callback(self.receiver)
            log.info('Antenna ({}) collegata\n'.format(device.get_64bit_addr()))
            return device
        except (InvalidOperatingModeException, SerialException):
            log.error('Nessuna antenna trovata')

    def __del__(self):
        if self.device is not None and self.device.is_open():
            log.debug('Device ({}) close'.format(self.device.get_64bit_addr()))
            self.device.close()


# questa classe crea dei pacchetti
# contenitori sottoforma di liste
# e fornisce metodi per facilitare la
# comunicazione con il frontend
class Packet:
    def __init__(self, content=list()):
        self.__content = self.__decode(content)

    @property
    def content(self):
        return self.__content

    @content.setter
    def content(self, content):
        self.__content = self.__decode(content)

    @property
    def encode(self):
        return ';'.join(map(str, self.content))

    @property
    def jsonify(self):
        type = self.content[1]
        content = self.content[:]
        content.reverse()

        with open('pyxbee/packets.json') as f:
            res = json.load(f)[str(type)]

        for key, _ in res.items():
            res[key] = content.pop()
        return json.dumps(res)

    def __decode(self, data):
        # se viene passato un dict o una
        # stringa cruda la trasforma in lista
        if isinstance(data, list):
            res = data
        elif isinstance(data, dict):
            res = [i for i in data.values()]
        else:
            res = data.split(';')
        return res

    def __len__(self):
        return len(self.content)

    def __str__(self):
        return str(self.content)


# questa classe istazia l'antenna
# della bici corrispondente e conserva
# i dati trasmetti sottoforma di Packet,
# si occupa anche dell'invio di
# pacchetti verso l'antenna server
#
# id --> codice con cui viene identif. nei pacchetti
# address --> indirizzo dell'antenna
class Taurus:
    def __init__(self, id, address, transmitter):
        self.address = address
        self.id = id

        # inserisce l'istanza corrente
        # nei listener dell'antenna del server
        transmitter.listener = self

        # Constanti per il dizionario dei pacchetti
        CONST = Const()

        # memorizza i dati sottoforma
        # di pacchetti ricevuti
        self.__memoize = dict()

    @property
    def data(self):
        data = self.__memoize.get(CONST.DATA)
        return data.jsonify if data != None else {}

    @property
    def settings(self):
        settings = self.__memoize.get(CONST.SETTING)
        return settings.jsonify if settings != None else {}

    # TODO: Inserire gli altri pacchetti

    # DIREZIONE: server --> bici
    def send(self, packet):
        transmitter.send(self.address, Packet(packet))

    def receive(self, packet):
        type = packet.content[1]
        self.__memoize.update({type: packet})

    def __str__(self):
        return self.id + ' -- ' + self.address
