from libs.parking import *
import argparse


def main(args):
    parking = Parking()

    if args.spaces:
        print(parking)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Parking manager')
    parser.add_argument('-p', '--plate', type=str, help='Plate number.', required=True)
    parser.add_argument('-s', '--state', type=str, choices=['in', 'out'], help='Status of the car: in/out.')
    parser.add_argument('--spaces', action='store_true', help='Show how many spaces are available.')
    args = parser.parse_args()

    main(args)
