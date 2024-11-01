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
                parkease.add_car(Car(plate))
                print(f"Car with plate {plate} added.")
            else:
                parkease.rmv_car(plate)
                print(f"Car with plate {plate} removed.")
        except Exception as e:
            print(e)

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
            if not plate[0:3].isalpha() or not plate[3:].isnumeric() or len(plate) != 6:
                raise argparse.ArgumentTypeError('The second value must be a correct plate number (tree letters and tree numbers)')
            return state, plate
        except (ValueError, IndexError):
            raise argparse.ArgumentTypeError(
                'Please provide two values: a predefined choice for the first (["in", "out"]), and a str for the second')

    parser = argparse.ArgumentParser(description='Parking manager')
    parser.add_argument('-m', '--management', nargs=2, type=str, help='First value, the state of the car: ["in", "out"], second value, the plate: str')
    parser.add_argument('-s', '--spaces', action='store_true', help='Show how many spaces are available')
    args = parser.parse_args()

    if args.management:
        try:
            validate_two_values(args.management)
        except argparse.ArgumentTypeError as e:
            parser.error(str(e))

    main(args)
