from datetime import datetime


class Ticket:
    def __init__(self, plaque="Inconnue", etage=0):
        self._plaque = plaque
        self._etage = etage
        self._arrive = None
        self._sortie = None

    @property
    def arrive(self):
        return self._arrive

    def enregistrer_arrive(self):  # probleme ici
        self._arrive = datetime.now()

    @property
    def sortie(self):
        return self._sortie

    def enregistrer_sortie(self):
        self._sortie = datetime.now()

    def calculer_duree_heure(self):
        return self.sortie.hour - self.arrive.hour  # bug ici

    def calculer_montant(self):
        duree = self.calculer_duree_heure()
        return duree * 2.30


class Etage:
    def __init__(self, id_etage=0, places=48):
        self._id_etage = id_etage
        self._places = places

    @property
    def nbr_places(self):
        return self._places


class Parking:
    def __init__(self, etage):
        pass

