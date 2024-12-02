from libs.file_mngt import *
from libs.parking import *
import argparse
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

def my_input(query, choices=None, numeric=False, my_min=None, my_max=None):
    """Prompt the user for input with optional numeric range and validation.

    PRE:
        - `query` is a string to display as a prompt.
        - If `numeric` is True:
            - `my_min` and `my_max` must be provided and define the acceptable numeric range (inclusive).
        - If `numeric` is False:
            - `choices` must be provided and define a list of valid response options.
    POST:
        - Returns the user's response as an integer if `numeric` is True.
        - Returns the user's response as a string if `numeric` is False.
        - If 'q' is entered, the program terminates with a status code of 0.
    """
    query += " (--q-- to quit): "
    response = input(query)

    def my_condition():
        if numeric:
            return not (response.isnumeric() and my_min <= int(response) <= my_max)
        else:
            return response not in choices

    while my_condition() and response != 'q':
        if numeric:
            print(f"Please enter a number between {my_min} and {my_max}.")
        else:
            print(f"Please enter a valid response: {choices}")
        response = input(query)
    if response == 'q':
        exit(0)
    return int(response) if numeric else response


def main(args):
    if json_reader():
        parkease = Parking().from_dict(json_reader())
    else:
        parkease = Parking()

    if args.management:
        state, plate = args.management
        try:
            if state == 'in':
                parkease.add_car(plate)
                print(f"Car with plate {plate} added.")
            else:
                parked_time, amount_due, sub = parkease.rmv_car(plate)
                sub_msg = f"Your subscription ends on {sub.end.strftime('%d/%m/%Y')}.\n" if sub is not None else ""
                print(f"Car with plate {plate} removed.\nYou are staying {parked_time.days} days and {int(parked_time.seconds / 3600)} hours.\n{sub_msg}The amount to be paid is €{amount_due}.")
        except Exception as e:
            print(e)

    if args.subscription:
        plate = args.subscription
        action = my_input(f"--check-- or --add-- a subscription for '{plate}'?", ['add', 'check', 'q'])

        car = list(filter(lambda c: c.plate == plate, parkease.all_cars))[0]
        if action == 'add':
            def my_length():
                return my_input(
                    f"For how many months? [{PRICE_PER_MONTH}€/month] (max=24)",
                    numeric=True,
                    my_min=1,
                    my_max=24
                    )

            if car.sub is not None and car.sub.is_active():
                extend = my_input("A subscription is already active. Would you like to extend it? yes or no", ['yes', 'no'])
                if extend == 'yes':
                    car.extend_sub(my_length())
            else:
                try:
                    car.add_sub(my_length())
                    print("Subscription added.")
                except Exception as e:
                    print(e)

        else:
            if car.sub is not None:
                print(car.sub)
            else:
                print("No active subscription.")

    if args.spaces:
        print(parkease)

    if args.report:
        print("Ajouter Class Report ici")

    json_writer(parkease)


if __name__ == '__main__':
    def validate_two_values(value_list):
        try:
            state = value_list[0]
            plate = value_list[1]

            valid_choices = ["in", "out"]
            if state not in valid_choices:
                raise argparse.ArgumentTypeError(f'The first value must be one of the choices : {valid_choices}')
            return state, plate
        except (ValueError, IndexError):
            raise argparse.ArgumentTypeError(
                'Please provide two values: a predefined choice for the first (["in", "out"]), and a str for the second')

    parser = argparse.ArgumentParser(prog='main.py', description='Parking manager')
    parser.add_argument('-m', '--management', nargs=2, type=str, help='First value, the state of the car you want to manage: ["in", "out"], second value, his plate: str')
    parser.add_argument('-s', '--spaces', action='store_true', help='Show how many spaces are available.')
    parser.add_argument('-sub', '--subscription', type=str, help='Requires the plate number of the car for which you want to manipulate the subscription.')
    parser.add_argument('-r', '--report', action='store_true', help='Generates a report showing the current state of the parking lot at the time the command is executed.')
    args = parser.parse_args()



    if args.management and args.subscription:
        raise argparse.ArgumentTypeError('--management and --subscription are mutually exclusive')

    if args.management:
        try:
            validate_two_values(args.management)
        except argparse.ArgumentTypeError as e:
            parser.error(str(e))

    main(args)
    gui()