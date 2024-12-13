from ..my_datetime import *
import tkinter as tk

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

    @property
    def get_all_tickets(self):
        all_tickets = []
        for car in self._cars_in + self._cars_out:
            all_tickets += car.tickets
        return all_tickets

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

    @property
    def tickets(self):
        return self._tickets

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
    """Monthly car park subscription.

    Note: The `datetime` class is replaced here by its `MyDateTime` subclass,
    which includes the `add_months()` method.
    """

    def __init__(self, plate, length=1, start=None):
        """Initialize a new Subscription object.

        PRE:
            - `plate` (str): The license plate of the car. Must be a non-empty string.
            - `length` (int): The number of months for the subscription. Defaults to 1.
            - `start` (MyDateTime, optional): The start date of the subscription. Defaults to the current date and time.
        POST:
            - A `Subscription` object is initialized with the specified or default values.
        """
        self._plate = plate
        self._length = length  # in months
        self._start = MyDateTime.now() if start is None else start

    @property
    def start(self):
        """Get the start date of the subscription.

        POST:
            - Returns the start date as a `MyDateTime` object.
        """
        return self._start

    @property
    def end(self):
        """Get the end date of the subscription.

        POST:
            - Returns the end date as a `MyDateTime` object, calculated by adding `length` months to the start date.
        """
        return self._start.add_months(self._length)

    @classmethod
    def from_dict(cls, data):
        """Create a Subscription object from a dictionary.

        PRE:
            - `data` (dict): A dictionary containing key-value pairs for the subscription attributes:
                - `plate` (str): The license plate.
                - `length` (int): The duration in months.
                - `start` (int): The start date as a UNIX timestamp.
        POST:
            - Returns a `Subscription` object initialized with the dictionary values.
        """
        return cls(
            data['plate'],
            data['length'],
            MyDateTime.fromtimestamp(data['start'])
        )

    def to_dict(self):
        """Convert the Subscription object to a dictionary.

        POST:
            - Returns a dictionary representation of the Subscription object with the following keys:
                - `plate`: The license plate.
                - `length`: The duration in months.
                - `start`: The start date as a UNIX timestamp.
        """
        return {
            "plate": self._plate,
            "length": self._length,
            "start": self._start.timestamp()
        }

    def is_active(self):
        """Check if the subscription is currently active.

        POST:
            - Returns `True` if the current date and time are before the subscription's end date, otherwise `False`.
        """
        return datetime.now() < self.end

    def was_active(self, date):
        """Check if the subscription was active at a specific date.

        PRE:
            - `date` (datetime): The date to check.
        POST:
            - Returns `True` if the subscription was active at the specified date, otherwise `False`.
        """
        return self._start <= date < self.end

    def extend(self, length):
        """Extend the duration of the subscription.

        PRE:
            - `length` (int): The number of months to add to the subscription's duration.
        POST:
            - Increases the subscription's length by the specified number of months.
        """
        self._length += length

    def __str__(self):
        """Return a string representation of the Subscription object.

        POST:
            - Returns a formatted string containing the license plate, start date, and end date of the subscription.
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
        self._parking = parking
        self._vehicle_count_per_day = {}
        self._peak_hours = {}

    def add_data(self):
        tickets = self._parking.get_all_tickets
        for ticket in tickets:
            self.record_vehicle(ticket.arrival)

    def record_vehicle(self, arrival_time:datetime):
        date = arrival_time.date()
        if date not in self._vehicle_count_per_day:
            self._vehicle_count_per_day[date] = 0
        self._vehicle_count_per_day[date] += 1

        hour = arrival_time.hour
        if hour not in self._peak_hours:
            self._peak_hours[hour] = 0
        self._peak_hours[hour] += 1

    def get_daily_report(self):
        return self._vehicle_count_per_day , self._peak_hours

    def __str__(self):
        peak_days = []
        peak_hours = []

        max_day = max(self._vehicle_count_per_day.values())
        for day in self._vehicle_count_per_day.keys():
            if self._vehicle_count_per_day[day] == max_day:
                peak_days.append(day)

        max_hour = max(self._peak_hours.values())
        for hour in self._peak_hours.keys():
            if self._peak_hours[hour] == max_hour:
                peak_hours.append(hour)

        peak_days = map(lambda d: d.strftime('%A, %d %B %Y'), peak_days)
        peak_days = "\n".join(peak_days)

        peak_hours = map(lambda h: f"{h}h", peak_hours)
        peak_hours = "\n".join(peak_hours)

        return f"The busiest days for the parking lot are (with {max_day} cars):\n{peak_days}\nThe peak hours of the parking lot are (with {max_hour} cars):\n{peak_hours}"

class ParkEaseGUI:
    """
    Classe responsable de l'interface graphique pour le système de gestion de parking.

    Attributs :
        parking (Parking) : Instance du système de gestion de parking.
        fenetre (tk.Tk) : Fenêtre principale de l'application.
        largeur_fenetre (int) : Largeur de la fenêtre.
        hauteur_fenetre (int) : Hauteur de la fenêtre.
        champ_texte_manage (tk.Entry) : Champ de texte pour saisir une plaque.
        label_resultat (tk.Label) : Label pour afficher les résultats ou messages.
    """
    def __init__(self, parking):
        """
        Initialise l'interface graphique avec les composants nécessaires.

        PRE : Une instance de la classe Parking est disponible.
        POST : La fenêtre principale et les widgets de l'application sont initialisés et affichés.

        Args:
            parking (Parking) : Instance du système de gestion de parking.
        """
        self.parking = parking
        self.fenetre = tk.Tk()
        self.fenetre.title("ParkEase")
        self.fenetre.attributes("-fullscreen", False)
        self.largeur_fenetre = 1400
        self.hauteur_fenetre = 1050
        self.centrer_fenetre()
        self.creer_widgets()
        self.fenetre.mainloop()

    def centrer_fenetre(self):
        """
        Centre la fenêtre principale sur l'écran.

        PRE : Les dimensions de l'écran et de la fenêtre sont définies.
        POST : La fenêtre est centrée sur l'écran.
        """
        largeur_ecran = self.fenetre.winfo_screenwidth()
        hauteur_ecran = self.fenetre.winfo_screenheight()
        x = (largeur_ecran // 2) - (self.largeur_fenetre // 2)
        y = (hauteur_ecran // 2) - (self.hauteur_fenetre // 2)
        self.fenetre.geometry(f"{self.largeur_fenetre}x{self.hauteur_fenetre}+{x}+{y}")

    def creer_widgets(self):
        """
        Crée et organise tous les widgets de l'interface utilisateur avec une mise en page mise à jour.

        PRE : La fenêtre principale est initialisée.
        POST : Les widgets sont réorganisés avec les boutons à gauche et les résultats à droite.
        """
        # Cadre gauche pour les boutons et le champ texte
        frame_gauche = tk.Frame(self.fenetre)
        frame_gauche.grid(row=0, column=0, padx=10, pady=10, sticky="n")

        label = tk.Label(frame_gauche, text="Bienvenue dans le Parking ! \nVeuillez introduire votre plaque : ")
        label.pack(pady=10)

        fullscreen = tk.Button(frame_gauche, text="Fullscreen", command=self.toggle_fullscreen)
        fullscreen.pack(pady=5)

        self.champ_texte_manage = tk.Entry(frame_gauche, width=30)
        self.champ_texte_manage.pack(pady=5)

        bouton_in = tk.Button(frame_gauche, text="Entre", bg="blue", fg="white", width=20, height=2,
                              command=self.in_plate)
        bouton_in.pack(pady=5)

        bouton_out = tk.Button(frame_gauche, text="Sortie", bg="red", fg="white", width=20, height=2,
                               command=self.out_plate)
        bouton_out.pack(pady=5)

        bouton_space = tk.Button(frame_gauche, text="Espace", bg="black", fg="white", width=25, height=2,
                                 command=self.spaces)
        bouton_space.pack(pady=5)

        bouton_report = tk.Button(frame_gauche, text="Rapport", bg="green", fg="white", width=25, height=2,
                                  command=self.report)
        bouton_report.pack(pady=5)

        # Cadre droit pour les résultats
        frame_droit = tk.Frame(self.fenetre)
        frame_droit.grid(row=0, column=1, padx=10, pady=10, sticky="n")

        self.label_resultat = tk.Label(frame_droit, text="", fg="blue", justify="left", anchor="n", wraplength=300)
        self.label_resultat.pack(pady=10)

    def toggle_fullscreen(self):
        """
        Bascule entre le mode plein écran et le mode fenêtre normale.

        PRE : La fenêtre principale est initialisée.
        POST : L'état plein écran est inversé.
        """
        is_fullscreen = self.fenetre.attributes("-fullscreen")
        self.fenetre.attributes("-fullscreen", not is_fullscreen)

    def in_plate(self):
        """
        Récupère le texte saisi dans le champ de texte et ajoute la plaque au système de parking.
        Met à jour le label pour confirmer l'ajout.

        PRE : Une plaque valide est saisie dans le champ de texte.
        POST : La plaque est ajoutée au système de parking et un message de confirmation est affiché.
        """
        text = self.champ_texte_manage.get()
        try:
            self.parking.add_car(text)
            self.label_resultat.config(text=f"La plaque : {text} a bien été ajoutée")
        except ValueError as e:
            self.label_resultat.config(text=e)

    def out_plate(self):
        """
        Récupère le texte saisi dans le champ de texte et supprime la plaque du système de parking.
        Met à jour le label pour confirmer la suppression.

        PRE : Une plaque valide est saisie dans le champ de texte.
        POST : La plaque est supprimée du système de parking et un message de confirmation est affiché.
        """
        text = self.champ_texte_manage.get()
        try:
            self.parking.rmv_car(text)
            self.label_resultat.config(text=f"La plaque : {text} a bien été supprimée")
        except ValueError as e:
            self.label_resultat.config(text=e)

    def spaces(self):
        """
        Affiche les espaces disponibles dans le système de parking.
        Met à jour le label pour afficher cette information.

        PRE : Le système de parking est initialisé.
        POST : Les informations sur les espaces disponibles sont affichées.
        """
        self.label_resultat.config(text=str(self.parking))

    def report(self):
        """
        Génère un rapport sur le système de parking.
        Met à jour le label pour afficher les données du rapport.

        PRE : Le système de parking est initialisé.
        POST : Les données du rapport sont générées et affichées.
        """
        report = Report(self.parking)
        report.add_data()
        self.label_resultat.config(text=str(report))
