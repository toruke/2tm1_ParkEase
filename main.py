# main du projet Park Ease
class Parking:
    def __init__(self,place=192):#peut-être pas néssesaire une class pour sa
        self._place = place

    @property
    def place(self):#à améliorer Suivi des places
        return self._place

    def sortie(self):#la gestion des sorties
        if self._place > 0 :
            self._place -= 1
        else:
            return print("no more place in the parking")#envoie d'un message d'alert ici

    def entre(self):#la gestion des entrée
        if self._place < 192:
            self._place += 1

    def rapport(self):#a revoir
        pass
    def __str__(self):
        return f"il reste : {self._place} place"
      
parkEase = Parking()
print(parkEase)
