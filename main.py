# main du projet Park Ease
from datetime import datetime
from multiprocessing.managers import Token


class Ticket:
    def __init__(self, plaque="Inconnue", etage=0):
        self._plaque = plaque
        self._etage = etage
        self.arrive = None
        self.sortie = None

    def arrive(self):
        self.arrive = datetime.now()

    def sortie(self):
        self.sortie = datetime.now()

    def calculer_duree(self):
        return self.sortie.hour - self.arrive.hour  #bug ici

    def calculer_montant(self):
        duree = self.calculer_duree()
        return duree * 2.30

class Etage:
    def __init__(self,id_etage=0,places=48):
        self._id_etage = id_etage
        self._places = places

    @property
    def nbr_places(self):
        return self._places

class Parking:
    def __init__(self,etage):
        pass

