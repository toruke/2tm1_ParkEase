import unittest
from libs.parking import *


class TestParking(unittest.TestCase):
    def setUp(self):
        self.parking = Parking(num_of_floors=2, spaces_per_floor=10)

    def test_av_spaces(self):
        self.assertEqual(self.parking.av_spaces(), 20, 'Test av_spaces function')

    def test_add_car(self):
        plate = 'ABC123'
        self.parking.add_car(plate)
        self.assertEqual(self.parking.av_spaces(), 19, 'Test av_spaces function')
        self.assertEqual(len(self.parking._cars_in), 1, 'Test add_car function')
        self.assertEqual(self.parking._cars_in[0].plate, plate, 'Test add_car function')

    def test_add_car_full(self):
        for i in range(20):
            self.parking.add_car(f"CAR{i}")
        with self.assertRaises(ParkingFull):
            self.parking.add_car("FULL")

    def test_add_car_dup(self):
        plate = 'DUP'
        self.parking.add_car(plate)
        with self.assertRaises(ValueError):
            self.parking.add_car(plate)

    def test_rmv_car(self):
        plate = 'ABC123'
        self.parking.add_car(plate)
        self.parking.rmv_car(plate)
        self.assertEqual(self.parking.av_spaces(), 20, 'Test rmv_car function')
        self.assertEqual(len(self.parking._cars_out), 1, 'Test rmv_car function')
        self.assertEqual(self.parking._cars_out[0].plate, plate, 'Test rmv_car function')

    def test_rmv_car_doesnt_exist(self):
        with self.assertRaises(ValueError):
            self.parking.rmv_car("DOESNT_EXIST")

    def test_to_dict(self):
        self.assertDictEqual(Parking().to_dict(), {'cars_in': [], 'cars_out': [], 'spaces': 192}, "Conversion d'un parking vide en dict.")

    def test_from_dict(self):
        data = {
            'cars_in': [{'plate': 'CARIN', 'tickets': [], 'sub': None}],
            'cars_out': [{'plate': 'CAROUT', 'tickets': [], 'sub': None}],
            'spaces': 30
        }
        parking = Parking.from_dict(data)
        self.assertEqual(parking._spaces, 30)
        self.assertEqual(len(parking._cars_in), 1)
        self.assertEqual(parking._cars_in[0].plate, 'CARIN')
        self.assertEqual(len(parking._cars_out), 1)
        self.assertEqual(parking._cars_out[0].plate, 'CAROUT')


if __name__ == '__main__':
    unittest.main()
