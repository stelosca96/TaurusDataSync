import json
import logging

from digi.xbee.devices import RemoteXBeeDevice, XBeeDevice
from digi.xbee.exception import (InvalidOperatingModeException,
                                 InvalidPacketException, TimeoutException)
from digi.xbee.models.address import XBee64BitAddress
from serial.serialutil import SerialException
from abc import abstractmethod


log = logging.getLogger(__name__)

PORT = '/dev/ttyUSB0'
BAUD_RATE = 115200


# NOTE: ogni nuovo pacchetto
# che deve essere mandato al
# frontend deve avere la sua costante
class Const:
    @property
    def DATA(self):
        return '0'

    @property
    def STATE(self):
        return '1'


# Constanti per il identificare i pacchetti
CONST = Const()


# questa classe si interfaccia in con
# le funzioni di basso livello
# dello xbee e si occupa i mandare
# e ricevere raw_message formati da
# stringhe del tipo {};{};{};{}
class _Transmitter:
    def __init__(self):
        self.device = self.__open_device(PORT, BAUD_RATE)

    def __del__(self):
        if self.device is not None and self.device.is_open():
            log.debug('Device ({}) close'.format(self.device.get_64bit_addr()))
            self.device.close()

    def __open_device(self, port, baud_rate):
        device = XBeeDevice(port, baud_rate)
        try:
            device.open()
            device.add_data_received_callback(self.receiver)
            log.info('Device ({}) connected\n'.format(device.get_64bit_addr()))
            return device
        except (InvalidOperatingModeException, SerialException):
            log.error('Nessuna antenna trovata')

    @property
    def address(self):
        return self.device.get_64bit_addr()

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
        # lancia l'eccezione
        try:
            self.device.send_data(RemoteXBeeDevice(
                self.device, XBee64BitAddress.from_hex_string(address)), packet.encode)
        except (TimeoutException, InvalidPacketException):
            log.error('ACK send_sync non ricevuto\n')

    def send_broadcast(self, packet):
        self.device.send_data_broadcast(packet.encode)

    # DIREZIONE: bici --> server
    def receiver(self, xbee_message):
        if xbee_message != '':
            raw = xbee_message.data.decode()
            packet = Packet(raw)
            log.debug('Received packet: {}'.format(packet))
            self.manage_packet(packet)

    @abstractmethod
    def manage_packet(self, packet):
        pass


# SERVER mode del transmitter
class Server(_Transmitter):
    def __init__(self):
        super().__init__()
        self.__listener = dict()

    @property
    def listener(self):
        return self.__listener

    @listener.setter
    def listener(self, l):
        self.__listener.update({l.code: l})

    # DIREZIONE: bici --> server
    def manage_packet(self, packet):
        dest = self.listener.get(packet.dest)
        dest.receive(packet)


# CLIENT mode del transmitter
class Client(_Transmitter):
    def __init__(self):
        super().__init__()
        self.__bike = None

    @property
    def bike(self):
        return self.__bike

    @bike.setter
    def bike(self, b):
        self.__bike = b

    # DIREZIONE: server --> bici
    def manage_packet(self, packet):
        self.bike.receive(packet)


# questa classe crea dei pacchetti
# contenitori sottoforma di liste
# e fornisce metodi per facilitare la
# comunicazione con il frontend
class Packet:
    def __init__(self, content=tuple()):
        self.__content = self.__decode(content)

    def __len__(self):
        return len(self.content)

    def __str__(self):
        return str(self.content)

    @classmethod
    def __decode(cls, data):
        # se viene passato un dict, una lista o una
        # stringa cruda la trasforma in tupla
        if isinstance(data, (list, tuple)):
            res = data
        elif isinstance(data, dict):
            res = [i for i in data.values()]
        else:
            res = data.split(';')
        return tuple(res)

    @property
    def content(self):
        return self.__content

    @content.setter
    def content(self, content):
        self.__content = self.__decode(content)

    @property
    def dest(self):
        return self.content[0] if len(self) > 0 else None

    @property
    def tipo(self):
        return self.content[1] if len(self) > 0 else None

    @property
    def encode(self):
        return ';'.join(map(str, self.content))

    @property
    def jsonify(self):
        content = list(self.content[:])
        content.reverse()

        with open('pyxbee/packets.json') as f:
            res = json.load(f)[str(self.tipo)]

        for key, _ in res.items():
            res[key] = content.pop()
        return json.dumps(res)


# classe genitore per la modalita' server e client
class _SuperBike:
    def __init__(self, code, address, transmitter):
        self.__address = address
        self.__code = code
        self.__transmitter = transmitter

    @property
    def transmitter(self):
        return self.__transmitter

    @property
    def code(self):
        return self.__code

    @property
    def address(self):
        return self.__address

    @abstractmethod
    def receive(self, packet):
        pass

    # DIREZIONE: server --> bici

    def send(self, packet):
        self.transmitter.send(self.address, Packet(packet))


# questa classe prende instaza dell'antenna in
# modalita' CLIENT, conserva i pacchetti
# ricevuti in __memoize e si occupa
# dell'invio di pacchetti verso il SERVER (marta)
#
# code --> codice con cui viene identif. nei pacchetti
# address --> indirizzo dell'antenna server
# client --> instanza dell'antenna client
class Bike(_SuperBike):
    def __init__(self, code, address, client, sensors):
        super().__init__(code, address, client)

        # memorizza le instanze dei valori utili
        self.__sensors = sensors

        # inserisce l'instanza corrente
        # come client dell'antenna
        self.transmitter.bike = self

        # memorizza i pacchetti ricevuti
        self.__memoize = list()

    def __len__(self):
        return len(self.__memoize)

    def __str__(self):
        return '{} -- {}'.format(self.code, self.transmitter.address)

    @property
    def packets(self):
        return self.__memoize

    # DIREZIONE: bici -> server
    @property
    def send_data(self, data):
        data.update({'dest': self.code, 'type': CONST.DATA})
        self.send(data)

    @property
    def send_state(self, state):
        state.update({'dest': self.code, 'type': CONST.STATE})
        self.send(state)

    # TODO: Inserire gli altri pacchetti

    # DIREZIONE: server --> bici
    def receive(self, packet):
        self.__memoize.append(packet)


# questa classe prende instaza dell'antenna in
# modalita' SERVER, conserva i pacchetti
# ricevuti in __memoize e si occupa
# dell'invio di pacchetti verso il CLIENT (bici)
#
# code --> codice con cui viene identif. nei pacchetti
# address --> indirizzo dell'antenna client
# server --> instanza dell'antenna server
class Taurus(_SuperBike):
    def __init__(self, code, address, server):
        super().__init__(code, address, server)

        # inserisce l'istanza corrente
        # nei listener dell'antenna del server
        self.transmitter.listener = self

        # colleziona i pacchetti mandati al frontend
        # per visualizzarli al reload della pagina con
        # soluzione di continuita'
        self.__history = list()

        # memorizza un pacchetto
        # ricevuto per ogni tipo
        self.__memoize = dict()

    def __str__(self):
        return '{} -- {}'.format(self.code, self.address)

    @property
    def history(self):
        return self.__history

    @property
    def data(self):
        data = self.__memoize.get(CONST.DATA)
        jdata = data.jsonify if data != None else {}
        self.__history.append(jdata)
        return jdata

    @property
    def state(self):
        state = self.__memoize.get(CONST.STATE)
        return state.jsonify if state != None else {}

    # TODO: Inserire gli altri pacchetti

    # DIREZIONE: bici --> server
    def receive(self, packet):
        tipo = packet.content[1]
        self.__memoize.update({tipo: packet})
