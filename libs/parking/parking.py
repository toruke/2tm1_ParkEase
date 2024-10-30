from datetime import datetime


class Parking:
    def __init__(self, num_of_floors=4):
        self._floor = []
        for i in range(num_of_floors):
            self._floor.append(Floor(i))

    def add_floor(self, floor):
        self._floor.append(floor)

    def av_spaces_parking(self):
        spaces = 0
        for floor in self._floor:
            spaces += floor.av_spaces_floor()
        return spaces

    def __str__(self):
        return f"Il y a actuellement {self.av_spaces_parking()} places libres."


class Floor:
    def __init__(self, id_floor, spaces=48):
        self._id = id_floor
        self._spaces = spaces
        self._car = []

    def add_car(self, car):
        self._car.append(car)

    def rmv_car(self, car):
        self._car.remove(car)

    def av_spaces_floor(self): # available spaces
        return self._spaces - len(self._car)


class Ticket:
    def __init__(self, plate, floor):
        self._plate = plate
        self._floor = floor
        self._arrival = datetime.now()

    @property
    def arrival(self):
        return self._arrival

    def __str__(self):
        return f"Voiture : {self._plate}\nEtage : {self._floor}\n" \
               f"Arriver : {self._arrival.hour} Heures\n-------------"


class Car:
    def __init__(self, plate):
        self._plate = plate
        self._tickets = []

    def entrance(self, floor): # jsp encore comment faire cette partie
        self._tickets.append(Ticket(self._plate, floor))
