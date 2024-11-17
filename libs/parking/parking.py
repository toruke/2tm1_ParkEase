from datetime import datetime


class Parking:
    """ Represents an entire parking lot, including the available spaces and the cars it contains.

    Attributes:
        cars (list of Car): A list of Car objects currently parked in the parking lot.
        spaces (int): The total number of parking spaces available in the parking lot.
        num_of_floors (int): Number of floors in the parking lot (default is 4).
        spaces_per_floor (int): Number of spaces per floor in the parking lot (default is 48).

    PRE:
        - cars is a list of Car objects or None (default: empty list).
        - spaces is an integer specifying the total number of spaces, or None (default: calculated from num_of_floors and spaces_per_floor).
        - num_of_floors and spaces_per_floor are positive integers.

    POST: The parking lot is initialized with the specified or default values.

    RAISE: ValueError if num_of_floors or spaces_per_floor is not positive.
    """

    def __init__(self, cars=None, spaces=None, num_of_floors=4, spaces_per_floor=48):
        if num_of_floors <= 0 or spaces_per_floor <= 0:
            raise ValueError('num_of_floors and spaces_per_floor must be positive integers.')
        self._cars = [] if cars is None else cars
        self._spaces = num_of_floors * spaces_per_floor if spaces is None else spaces

    @classmethod
    def from_dict(cls, data):
        """ Transform a dictionary into a Parking object.

        PRE: data is a dictionary with key-value pairs.
        POST: The parking lot is initialized with the specified or default values.
        """
        return cls(
            list(map(lambda c: Car.from_dict(c), data['cars'])),
            data['spaces']
        )

    def to_dict(self):
        """ Transform a Parking object to a dictionary.

        POST: A dictionary with key-value pairs.
        """
        return {
            'cars': list(map(lambda c: c.to_dict(), self._cars)),
            'spaces': self._spaces
        }

    def add_car(self, car):
        """ Adds a car to the parking lot and adds a new Ticket object to the car.

        PRE: A Car object.
        POST: None.
        RAISE: ValueError if car already exists in the parking lot.
        """
        if car.plate in list(map(lambda c: c.plate, self._cars)):
            raise ValueError(f'Car with plate {car.plate} already exists')
        car.add_ticket()
        self._cars.append(car)

    def rmv_car(self, plate):
        if plate not in list(map(lambda c: c.plate, self._cars)):
            raise ValueError(f'Car with plate {plate} does not exist')
        car = list(filter(lambda c: c.plate == plate, self._cars))[0]
        self._cars.remove(car)

    def av_spaces(self):
        return self._spaces - len(self._cars)

    def __str__(self):
        return f"There is {self.av_spaces()} spaces available."


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

    @property
    def plate(self):
        return self._plate

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

    def add_ticket(self):
        self._tickets.append(Ticket(self._plate))

    def __str__(self):
        txt = f"Plate : {self._plate}\nTickets :\n"
        for ticket in self._tickets:
            txt += f"{ticket.__str__()}\n"
        return txt
