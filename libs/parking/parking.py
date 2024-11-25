from ..my_datetime import *

# car park rates in euros
PRICE_PER_HOUR = 2
PRICE_PER_DAY = 12
PRICE_PER_MONTH = 100


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

    @property
    def all_cars(self):
        return self._cars_in + self._cars_out

    @classmethod
    def from_dict(cls, data):
        """ Transforms a dictionary into a Parking object.

        PRE: data is a dictionary with key-value pairs.
        POST: The parking lot is initialized with the specified or default values.
        """
        return cls(
            list(map(lambda c: Car.from_dict(c), data['cars_in'])),
            list(map(lambda c: Car.from_dict(c), data['cars_out'])),
            data['spaces']
        )

    def to_dict(self):
        """ Transforms a Parking object to a dictionary.

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

        if plate in list(map(lambda c: c.plate, self._cars_out)):
            car = list(filter(lambda c: c.plate == plate, self._cars_out))[0]
            self._cars_out.remove(car)
        else:
            car = Car(plate)

        if not car.sub.is_active():
            car.add_ticket()
        self._cars_in.append(car)

    def rmv_car(self, plate):
        """ Removes a car from the parking lot.

        PRE: The plate of the car that is to be removed.
        POST: Removes the car from the parking lot.
        RAISE: ValueError if a car with the corresponding plate does not exist in the parking lot.
        """
        if plate not in list(map(lambda c: c.plate, self._cars_in)):
            raise ValueError(f"Car with plate {plate} isn't in the parking lot.")
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
        """ Initializes a new Ticket object.

            PRE:
                -The plate of the car (must be a non-empty string).
                -`arrival` must be a datetime object.
            POST: A Ticket object is initialized with the specified or default values.
            RAISE:
                -ValueError if the plate is not a non-empty string.
                -ValueError if the arrival is not a datetime object
        """
        self._plate = plate
        self._arrival = datetime.now() if arrival is None else arrival

    @property
    def arrival(self):
        return self._arrival

    @classmethod
    def from_dict(cls, data):
        """ Transforms a dictionary into a Ticket object.

            PRE: data is a dictionary with key-value pairs.
            POST: The Ticket object is initialized with the specified or default values.
        """
        return cls(
            data['plate'],
            datetime.fromtimestamp(data['arrival'])
        )

    def to_dict(self):
        """ Transforms a Ticket object to a dictionary.

            PRE: None.
            POST: The dictionary representation of the Ticket object.
        """
        return {
            "plate": self._plate,
            "arrival": self._arrival.timestamp()
        }

    def __str__(self):
        """ Returns a string representation of the Ticket object.

            PRE: None.
            POST: The string representation of the Ticket object.
        """
        return f"Car : {self._plate}\n" \
               f"Arrival : {self._arrival.strftime("%d/%m/%Y à %H:%M:%S")}\n-------------"


class Car:
    def __init__(self, plate, tickets=None, sub=None):
        """Initializes a new Car object.

               PRE:
                   - The plate of the car (must be a non-empty string).
                   - A list of Ticket objects associated with the car or None (default: empty list).
                   - The subscription associated with the car (default None).
               POST: A Car object is initialized with the specified or default values.
               RAISE:
                   - TypeError if plate is not a string or tickets is not a list.
                   - ValueError if plate is an empty string.
        """
        self._plate = plate
        self._tickets = [] if tickets is None else tickets
        self._sub = sub

    @property
    def plate(self):
        return self._plate

    @property
    def sub(self):
        return self._sub

    @classmethod
    def from_dict(cls, data):
        """ Transforms a dictionary into a Car object.

            PRE: data is a dictionary with key-value pairs.
            POST: The Car object is initialized with the specified or default values.
        """
        return cls(
            data['plate'],
            list(map(lambda t: Ticket.from_dict(t), data['tickets'])),
            None if data['sub'] is None else Subscription.from_dict(data['sub'])
        )

    def to_dict(self):
        """ Transforms a Car object to a dictionary.

                PRE: None.
                POST: The Car object is initialized with the specified or default values.
        """
        return {
            "plate": self._plate,
            "tickets": list(map(lambda t: t.to_dict(), self._tickets)),
            "sub": None if self._sub is None else self._sub.to_dict()
        }

    def add_ticket(self):
        """ Adds a ticket to the car object.

            PRE: The car must have a valid plate number (non-empty string).
            POST: A new Ticket object is created with the car's plate and added to the tickets list.
            RAISE: ValueError: If the car's plate is invalid (e.g., None or empty string).
        """
        self._tickets.append(Ticket(self._plate))

    def add_sub(self, length):  # in months
        """ Adds a subscription to the car object.

            PRE:
                -The car may or may not already have a subscription.
                -`length` is an integer representing the subscription duration in months.
            POST:
                -A new subscription is added to the car if there is no active subscription.
                -If there is an active subscription, a ValueError is raised.
            RAISE:
                -ValueError if the `length` is not a positive integer.
                -ValueError if the car already has an active subscription.

        """
        if self._sub is None or not self._sub.is_active():
            self._sub = Subscription(self._plate, length)
        else:
            raise ValueError(f'This car already has a subscription that ends on {self._sub.end.strftime("%d/%m/%Y")}.')

    def extend_sub(self, length):   # in months
        """ Extends the car's subscription to the specified length.

            PRE:
                -The car must have an existing subscription.
                -`length` is an integer representing the subscription duration in months.
            POST:
                -Extends the car's subscription to the specified length.
            RAISE:
                -ValueError if `length` is not a positive integer.
                -AttributeError if there is no active subscription to extend.
        """
        self._sub.extend(length)

    def __str__(self):
        """ Returns a string representation of the Car object.

            PRE: None.
            POST: The string representation of the Car object.
        """
        txt = f"Plate : {self._plate}\nTickets :\n"
        for ticket in self._tickets:
            txt += f"{ticket.__str__()}\n"
        return txt


class Subscription:
    """ Monthly car park subscription.

    !!! Note that here the datetime class is replaced by its MyDateTime subclass, which has the add_months() method.
    """
    def __init__(self, plate, length=1, start=None):
        """Initialize a new Subscription object.

            PRE:
                - The plate of the car (must be a non-empty string).
                - The number of months for the subscription
                - The start of they object subscription
            POST: a Subscribe object are initialized with the specified or default values.
        """
        self._plate = plate
        self._length = length  # in months
        self._start = MyDateTime.now() if start is None else start

    @property
    def start(self):
        return self._start

    @property
    def end(self):
        return self._start.add_months(self._length)

    @classmethod
    def from_dict(cls, data):
        """ Transforms a dictionary into a Subscription Object.

            PRE: data is a dictionary with key-value pairs.
            POST: the dictionary object is initialized with the specified or default values.
        """
        return cls(
            data['plate'],
            data['length'],
            MyDateTime.fromtimestamp(data['start'])
        )

    def to_dict(self):
        """ Transforms a Subscription object to a dictionary

            PRE: None.
            POST: The dictionary representation of the Subscription object.
        """
        return {
            "plate": self._plate,
            "length": self._length,
            "start": self._start.timestamp()
        }

    def is_active(self):
        """ Check if the Subscription is still available

            PRE: None.
            POST: return true false if the Subscription time is still available
        """
        return datetime.now() < self.end

    def extend(self, length):   # in months
        """ Increase the time of the subscription.

            PRE: length is an int
            POST: add time to the property length
        """
        self._length += length

    def __str__(self):
        """ Returns a string representation of the Subscription object.

            PRE: None.
            POST: The string representation of the Subscription object
        """
        return f"Plate : {self._plate}\nStart : {self._start.strftime("%d/%m/%Y à %H:%M:%S")}\nEnd : {self.end.strftime("%d/%m/%Y à %H:%M:%S")}"


class Payment:
    pass

