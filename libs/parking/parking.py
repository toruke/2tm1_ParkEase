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
        self._plate = plate
        self._arrival = datetime.now() if arrival is None else arrival
        """ Initializes a new Ticket object.
                
            PRE:
                -The plate of the car (must be a non-empty string).
                -`arrival` must be a datetime object.
            POST: A Ticket object is initialized with the specified or default values.
            RAISE:
                -ValueError if the plate is not a non-empty string.
                -ValueError if the arrival is not a datetime object
        """

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
        self._plate = plate
        self._tickets = [] if tickets is None else tickets
        self._sub = sub
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
        self._tickets.append(Ticket(self._plate))
        """ Adds a ticket to the car object.

                PRE: The car must have a valid plate number (non-empty string).
                POST: A new Ticket object is created with the car's plate and added to the tickets list.
                RAISE: ValueError: If the car's plate is invalid (e.g., None or empty string).   
        """

    def add_sub(self, length):  # in months
        if self._sub is None or not self._sub.is_active():
            self._sub = Subscription(self._plate, length)
        else:
            raise ValueError(f'This car already has a subscription that ends on {self._sub.end.strftime("%d/%m/%Y")}.')
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

    def extend_sub(self, length):   # in months
        self._sub.extend(length)
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

    def __str__(self):
        txt = f"Plate : {self._plate}\nTickets :\n"
        for ticket in self._tickets:
            txt += f"{ticket.__str__()}\n"
        """ Returns a string representation of the Car object.

                PRE: None.
                POST: The string representation of the Car object.
        """
        return txt


class Subscription:
    """ Monthly car park subscription.

    !!! Note that here the datetime class is replaced by its MyDateTime subclass, which has the add_months() method.
    """
    def __init__(self, plate, length=1, start=None):
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
        return cls(
            data['plate'],
            data['length'],
            MyDateTime.fromtimestamp(data['start'])
        )

    def to_dict(self):
        return {
            "plate": self._plate,
            "length": self._length,
            "start": self._start.timestamp()
        }

    def is_active(self):
        return datetime.now() < self.end

    def extend(self, length):   # in months
        self._length += length

    def __str__(self):
        return f"Plate : {self._plate}\nStart : {self._start.strftime("%d/%m/%Y à %H:%M:%S")}\nEnd : {self.end.strftime("%d/%m/%Y à %H:%M:%S")}"


class Payment:
    pass


class Report:
    """ Classe pour générer des rapports détaillés sur l'occupation du parking """

    def __init__(self, parking):
        """Initialisation du rapport avec l'objet Parking."""
        self.parking = parking
        self.vehicle_count_per_day = {}
        self.peak_hours = []
        # Plages horaires définies pour les heures de pointe
        self.peak_time_ranges = [(7, 9), (17, 19)]
        self.peak_hour_count = {range_str: 0 for range_str in self.peak_time_ranges}

    def record_vehicle(self, arrival_time):
        date = arrival_time.date()
        if date not in self.vehicle_count_per_day:
            self.vehicle_count_per_day[date] = 0
        self.vehicle_count_per_day[date] += 1

        self._detect_peak_hours(arrival_time)

    def _detect_peak_hours(self, arrival_time):
        for start_hour, end_hour in self.peak_time_ranges:
            if start_hour <= arrival_time.hour < end_hour:
                self.peak_hour_count[(start_hour, end_hour)] += 1

    def get_daily_report(self):
        return self.vehicle_count_per_day

    def get_peak_hours(self):
        peak_hours_report = []
        for time_range, count in self.peak_hour_count.items():
            peak_hours_report.append(f"Plage {time_range[0]}h-{time_range[1]}h : {count} véhicules")
        return peak_hours_report

    def display_report(self):
        print("Rapport quotidien du parking:")
        for date, count in self.vehicle_count_per_day.items():
            print(f"{date}: {count} véhicules")

        print("\nHeures de pointe:")
        peak_hours = self.get_peak_hours()
        for report in peak_hours:
            print(report)
