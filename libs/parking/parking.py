from datetime import datetime


class ParkingFull(Exception):
    pass

class Parking:
    """ Represents an entire parking lot, including the available spaces and the cars it contains.
    It stores also the cars that already been in one time.
    """

    def __init__(self, cars_in=None, cars_out=None, spaces=None, num_of_floors=4, spaces_per_floor=48):
        """Initializes a new Parking object.

        PRE:
            - cars_in and cars_out are lists of Car objects or None (default: empty list).
            - spaces is an integer specifying the total number of spaces, or None (default: calculated from num_of_floors and spaces_per_floor).
            - num_of_floors and spaces_per_floor are positive integers.
        POST: The parking lot is initialized with the specified or default values.
        RAISE: ValueError if num_of_floors or spaces_per_floor is not positive.
        """
        if num_of_floors <= 0 or spaces_per_floor <= 0:
            raise ValueError('num_of_floors and spaces_per_floor must be positive integers.')
        self._cars_in = [] if cars_in is None else cars_in
        self._cars_out = [] if cars_out is None else cars_out
        self._spaces = num_of_floors * spaces_per_floor if spaces is None else spaces

    @classmethod
    def from_dict(cls, data):
        """ Transform a dictionary into a Parking object.

        PRE: data is a dictionary with key-value pairs.
        POST: The parking lot is initialized with the specified or default values.
        """
        return cls(
            list(map(lambda c: Car.from_dict(c), data['cars_in'])),
            list(map(lambda c: Car.from_dict(c), data['cars_out'])),
            data['spaces']
        )

    def to_dict(self):
        """ Transform a Parking object to a dictionary.

        PRE: None.
        POST: The parking lot is initialized with the specified or default values.
        """
        return {
            'cars_in': list(map(lambda c: c.to_dict(), self._cars_in)),
            'cars_out': list(map(lambda c: c.to_dict(), self._cars_out)),
            'spaces': self._spaces
        }

    def add_car(self, plate):
        """ Adds a car to the parking lot and adds a new Ticket object to the car.

        PRE: The plate of the car that is to be added.
        POST: Adds the Car object to the parking lot and create a new Ticket object to the car.
        RAISE:
            - ParkingFull if there are no available spaces (av_spaces() returns 0).
            - ValueError if car already exists in the parking lot.
        """
        if self.av_spaces() == 0:
            raise ParkingFull("There are no available spaces in the parking lot.")
        if plate in list(map(lambda c: c.plate, self._cars_in)):
            raise ValueError(f'Car with plate {plate} already exists.')

        car = Car(plate)
        if plate in list(map(lambda c: c.plate, self._cars_out)):
            car = list(filter(lambda c: c.plate == plate, self._cars_out))[0]
            self._cars_out.remove(car)

        car.add_ticket()
        self._cars_in.append(car)

    def rmv_car(self, plate):
        """ Removes a car from the parking lot.

        PRE: The plate of the car that is to be removed.
        POST: Removes the car from the parking lot.
        RAISE: ValueError if a car with the corresponding plate does not exist in the parking lot.
        """
        if plate not in list(map(lambda c: c.plate, self._cars_in)):
            raise ValueError(f'Car with plate {plate} does not exist.')
        car = list(filter(lambda c: c.plate == plate, self._cars_in))[0]
        self._cars_in.remove(car)
        self._cars_out.append(car)

    def av_spaces(self):
        """ Returns the total number of spaces available in the parking lot.

        PRE: None.
        POST: The number of spaces available.
        """
        return self._spaces - len(self._cars_in)

    def __str__(self):
        """ Returns a string representation of the Parking object.

        PRE: None.
        POST: The string representation of the Parking object.
        """
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
        return f"Car : {self._plate}\n" \
               f"Arrival : {self._arrival.strftime("%d/%m/%Y à %H:%M:%S")}\n-------------"


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

class Subscription:
    def __init__(self, plate):
        self._plate = plate
        self._start = datetime.now()

        try:
            self._end = self._start.replace(year=self._start.year + 1)
        except ValueError:
            self._end = self._start.replace(year=self._start.year + 1, month=3, day=1)

    def __str__(self):
        return f"Plate : {self._plate}\nStart : {self._start.strftime("%d/%m/%Y à %H:%M:%S")}\nEnd : {self._end.strftime("%d/%m/%Y à %H:%M:%S")}"
