from taurus import Taurus
from communication import Communication

taurus = Taurus()
taurus_x = Taurus()
communication = Communication(taurus, taurus_x)

input()
