from .packet import *

# TODO: farlo meglio
DATA = '0'
SETTING = '1'


# avvio trasmissione xbee
transmiter = Transmitter()


# questa classe istazia l'antenna
# della bici corrispondente e conserva
# i dati trasmetti sottoforma di Packet,
# si occupa anche dell'invio di
# pacchetti verso l'antenna server
class Taurus:
    def __init__(self, id, address):
        self.address = address
        self.id = id

        # inserisce l'istanza corrente
        # nei listener dell'antenna
        # del server
        transmiter.listener = self

        # memorizza i dati sottoforma
        # di pacchetti ricevuti dalla bici
        self.__memoize = dict()

    @property
    def data(self):
        return self.__memoize.get(DATA).jsonify

    @property
    def setting(self):
        return self.__memoize.get(SETTING).jsonify

    # TODO: inserire gli altri pacchetti

    # DIREZIONE: server --> bici
    # TODO: aggiungere la send_sync
    def send(self, packet):
        transmiter.send(self.address, Packet(packet))

    def receive(self, packet):
        type = packet.content[1]
        self.__memoize.update({type: packet})

    def __str__(self):
        return self.id + ' -- ' + self.address
