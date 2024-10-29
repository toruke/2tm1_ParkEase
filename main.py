# main du projet Park Ease
class Ticket:
    def __init__(self, plaque, arrive, sortie, etage):
        self._plaque = plaque
        self._arrive = arrive
        self._sortie = sortie
        self._etage = etage

    def calculer_duree(self):
        return self._sortie - self._arrive

    def calculer_montant(self):
        duree = self.calculer_duree()
        return duree * 2.30

class Etage:
    def __init__(self,id_etage,places=48):
        self._id_etage = id_etage
        self._places = places
    @property
    def nbr_places(self):
        return self._places

class Parking:
    def __init__(self,etage):
        pass
