from .packet import *

tunnel = Communication()


class Taurus:
    def __init__(self, id, address):
        self.address = address
        self.id = id

        # memorizzano i dati
        # TODO: inserire tutti e 13 i tipi
        self.mdata = Packet()
        self.msettings = Packet()
        tunnel.add_listener(self)

    def data(self):
        return self.mdata.decode()

    def setting(self):
        return self.msetting.decode()

    # DIREZIONE: server --> bici
    # TODO: aggiungere la send_sync
    def send(self, packet):
        tunnel.send(self.address, Packet(packet))

    def __str__(self):
        return self.id + ' -- ' + self.address
