from libs.file_mngt import *
from libs.parking import *
import argparse


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
                parkease.rmv_car(plate)
                print(f"Car with plate {plate} removed.")
        except Exception as e:
            print(e)

    if args.subscription:
        plate = args.subscription
        action = input(f"--check-- or --add-- a subscription for {plate} ? ")
        car = list(filter(lambda c: c.plate == plate, parkease.all_cars()))[0]
        if action == 'add':
            try:
                car.add_subscription()
                print("Subscription added.")
            except Exception as e:
                print(e)
        elif action == 'check':
            if car.sub is not None:
                print(car.sub)
            else:
                print("No active subscription.")

    if args.spaces:
        print(parkease)

    json_writer(parkease)


if __name__ == '__main__':
    # Définir le type personnalisé pour valider les valeurs
    def validate_two_values(value_list):
        try:
            state = value_list[0]
            plate = value_list[1]
            # Liste de choix acceptés pour la première valeur
            valid_choices = ["in", "out"]
            if state not in valid_choices:
                raise argparse.ArgumentTypeError(f'The first value must be one of the choices : {valid_choices}')
            return state, plate
        except (ValueError, IndexError):
            raise argparse.ArgumentTypeError(
                'Please provide two values: a predefined choice for the first (["in", "out"]), and a str for the second')

    parser = argparse.ArgumentParser(description='Parking manager')
    parser.add_argument('-m', '--management', nargs=2, type=str, help='First value, the state of the car: ["in", "out"], second value, the plate: str')
    parser.add_argument('-s', '--spaces', action='store_true', help='Show how many spaces are available')
    parser.add_argument('-sub', '--subscription', type=str, help='Check whether a car has an active subscription or adds a subscription to a car via its plate')
    args = parser.parse_args()



    if args.management and args.subscription:
        raise argparse.ArgumentTypeError('--management and --subscription are mutually exclusive')

    if args.management:
        try:
            validate_two_values(args.management)
        except argparse.ArgumentTypeError as e:
            parser.error(str(e))

    main(args)
