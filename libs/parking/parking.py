from datetime import datetime


class Parking:
    def __init__(self, car=None, num_of_floors=4, spaces_per_floor=48):
        self._car = [] if car is None else car
        self._spaces = num_of_floors * spaces_per_floor

    def add_car(self, car):
        self._car.append(car)

    def rmv_car(self, car):
        self._car.remove(car)

    def av_spaces(self):
        return self._spaces - len(self._car)

    def __str__(self):
        return f"Il y a actuellement {self.av_spaces()} places libres."


class Ticket:
    def __init__(self, plate, arrival=None):
        self._plate = plate
        self._arrival = datetime.now() if arrival is None else arrival

    @property
    def arrival(self):
        return self._arrival

    @classmethod
    def from_dict(cls, data):
        return cls(
            data['plate'],
            datetime.fromtimestamp(data['arrival'])
        )

    def to_dict(self):
        return {
            "plate": self._plate,
            "arrival": self._arrival.timestamp()
        }

    def __str__(self):
        return f"Voiture : {self._plate}\n" \
               f"Arrivé : {self._arrival.strftime("%d/%m/%Y à %H:%M:%S")}\n-------------"


class Car:
    def __init__(self, plate, tickets=None):
        self._plate = plate
        self._tickets = [] if tickets is None else tickets

    @classmethod
    def from_dict(cls, data):
        return cls(
            data['plate'],
            list(map(lambda t: Ticket.from_dict(t), data['tickets']))
        )

    def to_dict(self):
        return {
            "plate": self._plate,
            "tickets": list(map(lambda t: t.to_dict(), self._tickets))
        }

    def entrance(self):
        self._tickets.append(Ticket(self._plate))

    def __str__(self):
        txt = f"Plate : {self._plate}\nTickets :\n"
        for ticket in self._tickets:
            txt += f"{ticket.__str__()}\n"
        return txt
