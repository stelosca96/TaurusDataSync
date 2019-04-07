from .packet import *

tunnel = Communication()


class Taurus:
    def __init__(self, id, address):
        self.address = address
        self.id = id

        # inserisce l'istanza corrente
        # nei listener dell'antenna
        # del server
        tunnel.listener = self

        # memorizzano i dati sottoforma
        # di pacchetti ricevuti dalla bici
        self.__data = Packet()
        self.__settings = Packet()

        # TODO: inserire gli altri pacchetti


    @property
    def data(self):
        return self.__data.decode

    @property
    def setting(self):
        return self.__setting.decode

    # TODO: inserire gli altri pacchetti

    # DIREZIONE: server --> bici
    # TODO: aggiungere la send_sync
    def send(self, packet):
        tunnel.send(self.address, Packet(packet))

    def __str__(self):
        return self.id + ' -- ' + self.address
