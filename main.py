from libs import parking
import argparse

def main(args):
    pass

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Parking manager')
    parser.add_argument('-p', '--plate', type=str, help='Plate number', required=True)
    parser.add_argument('-s', '--state', type=str, choices=['in', 'out'], help='Status of the car: in/out', required=True)
    args = parser.parse_args()

    main(args)
