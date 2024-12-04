from ..my_datetime import *

# car park rates in euros
PRICE_PER_HOUR = 2
PRICE_PER_DAY = 12
PRICE_PER_MONTH = 100
# Define the alert threshold (10% of places remaining)
ALERT_THRESHOLD = 0.1


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

        # If the car park is almost full, send an alert
        if self.av_spaces() / self._spaces <= ALERT_THRESHOLD:
            self.send_alert()

        if plate in list(map(lambda c: c.plate, self._cars_out)):
            car = list(filter(lambda c: c.plate == plate, self._cars_out))[0]
            self._cars_out.remove(car)
        else:
            car = Car(plate)

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
        return car.last_ticket.parked_time, car.checkout(), car.sub

    def new_car(self, plate):
        new_car = Car(plate)
        self._cars_out.append(new_car)
        return new_car

    def av_spaces(self):
        """ Returns the total number of spaces available in the parking lot.

        PRE: None.
        POST: The number of spaces available.
        """
        return self._spaces - len(self._cars_in)

    def send_alert(self):
        print(f"Alert: The car park is almost full! There are only {self.av_spaces()} spaces available.")

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

    @property
    def parked_time(self):
        return datetime.now() - self._arrival

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
               f"Arrival : {self._arrival.strftime('%d/%m/%Y à %H:%M:%S')}\n-------------"


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

    @property
    def last_ticket(self):
        return self._tickets[-1]

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
        """
        self._tickets.append(Ticket(self._plate))

    def add_sub(self, length):  # in months
        """ Adds a subscription to the car object.

            PRE:
                -The car may or may not already have a subscription.
                -`length` is an integer representing the subscription duration in months.
            POST:
                -A new subscription is added to the car if there is no active subscription.
            RAISE:
                -ValueError if the car already has an active subscription.

        """
        if self._sub is None or not self._sub.is_active():
            self._sub = Subscription(self._plate, length)
            return Payment(self).sub_price(length)
        else:
            raise ValueError(f'This car already has a subscription that ends on {self._sub.end.strftime("%d/%m/%Y")}.')

    def extend_sub(self, length):   # in months
        """ Extends the car's subscription to the specified length.

            PRE:
                -The car must have an existing subscription.
                -`length` is an integer representing the subscription duration in months.
            POST:
                -Extends the car's subscription to the specified length.
        """
        self._sub.extend(length)
        return Payment(self).sub_price(length)

    def checkout(self):
        return Payment(self).amount_due()

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
        """ Check if the Subscription is active.

            PRE: None.
            POST: return true false if the Subscription is active.
        """
        return datetime.now() < self.end

    def was_active(self, date):
        """ Check if the Subscription was active at the specified date.

            PRE: date is a datetime.
            POST: return true if the Subscription was active at the specified date.
        """
        return date < self.end

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
        return f"Plate : {self._plate}\nStart : {self._start.strftime('%d/%m/%Y à %H:%M:%S')}\nEnd : {self.end.strftime('%d/%m/%Y à %H:%M:%S')}"


class Payment:
    def __init__(self, car):
        self._car = car

    def sub_price(self, length):
        return length * PRICE_PER_MONTH

    def amount_due(self):
        ticket = self._car.last_ticket
        sub = self._car.sub
        if sub is not None and sub.was_active(ticket.arrival):
            return 0
        hours = int(ticket.parked_time.seconds / 3600)
        days = ticket.parked_time.days
        switch_tariff = int(PRICE_PER_DAY / PRICE_PER_HOUR)
        if hours > switch_tariff:
            hours -= switch_tariff
            days += 1
        amount_for_days = days * PRICE_PER_DAY
        amount_for_hours = hours * PRICE_PER_HOUR
        return amount_for_days + amount_for_hours


class Report:
    """ Class for generating detailed reports on car park occupancy """

    def __init__(self, parking):
        """ Initialise the relationship with the Parking object. """
        self.parking = parking
        self.vehicle_count_per_day = {}
        self.peak_hours = []
        # Time slots defined for peak periods
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
            peak_hours_report.append(f"Range {time_range[0]}h-{time_range[1]}h : {count} cars.")
        return peak_hours_report

    def display_report(self):
        print("Daily car park report:")
        for date, count in self.vehicle_count_per_day.items():
            print(f"{date}: {count} cars")

        print("\nPeak times:")
        peak_hours = self.get_peak_hours()
        for report in peak_hours:
            print(report)

    def __str__(self):

        pass

class Gui:
    def __init__(self):
        """crée une instance qui permet d'encoder un nombre indéfinit de plaque
            PRE:
            POST:
        """

        pass

    """Ancien fonction de gui
    import tkinter as tk
from tkinter import simpledialog, messagebox

def gui():

    # Créer la fenêtre principale
    fenetre = tk.Tk()
    fenetre.title("ParkEase")
    fenetre.attributes("-fullscreen", False)

    # Ajouter un label
    label = tk.Label(fenetre, text="Bienvenue dans le Parking ! \n Veuillez introduire votre plaque : ")
    label.pack()

    # Définir la taille de la fenêtre
    largeur_fenetre = 1400
    hauteur_fenetre = 1050

    # Obtenir les dimensions de l'écran
    largeur_ecran = fenetre.winfo_screenwidth()
    hauteur_ecran = fenetre.winfo_screenheight()

    # Calculer les coordonnées pour centrer la fenêtre
    x = (largeur_ecran // 2) - (largeur_fenetre // 2)
    y = (hauteur_ecran // 2) - (hauteur_fenetre // 2)

    # Appliquer la géométrie pour centrer
    fenetre.geometry(f"{largeur_fenetre}x{hauteur_fenetre}+{x}+{y}")

    # Ajouter un bouton
    def on_click():
        if fenetre.attributes("-fullscreen"):
            fenetre.attributes("-fullscreen", False)
        else:
            fenetre.attributes("-fullscreen", True)

    def valider():
        texte = champ_texte.get()
        label_resultat.config(text=f"la plaque : {texte} a bien été ajouter")

    # Premier bouton
    bouton1 = tk.Button(fenetre, text="Mode plein écran", command=on_click, bg="red", fg="white")
    bouton1.pack(pady=10)  # Placer le bouton avec un espacement vertical
    bouton1.place(x=50, y=50, width=200, height=100)

    # Champ de saisie
    champ_texte = tk.Entry(fenetre)
    champ_texte.pack(pady=10)

    # Bouton de validation
    bouton = tk.Button(
        fenetre, text="Valider", command=valider, bg="red", fg="white", width=20, height=2
    )
    bouton.pack(pady=10)

    # Label pour afficher le résultat
    label_resultat = tk.Label(fenetre, text="", fg="blue")
    label_resultat.pack(pady=10)

    # Lancer la boucle principale
    fenetre.mainloop()

    """