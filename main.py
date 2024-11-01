from libs.file_mngt import *
from libs.parking import *
import argparse


def main(args):
    parking = Parking()
    car1 = Car('jsf-620')
    car1.entrance(parking)
    car2 = Car('zny-017')
    car2.entrance(parking)

    with open('data/data.json', 'w', encoding="utf-8") as f:
        json.dump(parking.to_dict(), f, ensure_ascii=False, indent=4)

    with open('data/data.json', 'r', encoding="utf-8") as f:
        data = json.load(f)
        print(Parking.from_dict(data))

    if args.spaces:
        print(parking)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Parking manager')
    parser.add_argument('-p', '--plate', type=str, help='Plate number.')
    parser.add_argument('-s', '--state', type=str, choices=['in', 'out'], help='Status of the car: in/out.')
    parser.add_argument('--spaces', action='store_true', help='Show how many spaces are available.')
    args = parser.parse_args()

    main(args)
