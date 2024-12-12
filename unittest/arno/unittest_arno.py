import unittest
from datetime import datetime, timedelta
from libs.parking import *

class TestTicket(unittest.TestCase):

    def test_ticket_initialization_with_defaults(self):
        plate = "ABC123"
        ticket = Ticket(plate)
        self.assertEqual(ticket._plate, plate)
        self.assertIsInstance(ticket.arrival, datetime)

    def test_ticket_initialization_with_custom_arrival(self):
        plate = "XYZ789"
        custom_arrival = datetime(2022, 12, 1, 10, 30)
        ticket = Ticket(plate, custom_arrival)
        self.assertEqual(ticket._plate, plate)
        self.assertEqual(ticket.arrival, custom_arrival)

    def test_ticket_to_dict(self):
        plate = "CAR456"
        custom_arrival = datetime(2023, 6, 1, 9, 0)
        ticket = Ticket(plate, custom_arrival)
        ticket_dict = ticket.to_dict()
        self.assertEqual(ticket_dict['plate'], plate)
        self.assertAlmostEqual(ticket_dict['arrival'], custom_arrival.timestamp(), delta=1)

    def test_ticket_from_dict(self):
        data = {
            'plate': "DEF789",
            'arrival': datetime(2023, 5, 1, 15, 0).timestamp()
        }
        ticket = Ticket.from_dict(data)
        self.assertEqual(ticket._plate, data['plate'])
        self.assertEqual(ticket.arrival, datetime.fromtimestamp(data['arrival']))

    def test_ticket_parked_time(self):
        plate = "TIMER123"
        custom_arrival = datetime.now() - timedelta(hours=2)
        ticket = Ticket(plate, custom_arrival)
        parked_time = ticket.parked_time
        self.assertGreaterEqual(parked_time.total_seconds(), 2 * 3600)

class TestCar(unittest.TestCase):

    def test_car_initialization_with_defaults(self):
        plate = "CAR001"
        car = Car(plate)
        self.assertEqual(car.plate, plate)
        self.assertEqual(car.tickets, [])
        self.assertIsNone(car.sub)

    def test_car_add_ticket(self):
        plate = "CAR002"
        car = Car(plate)
        car.add_ticket()
        self.assertEqual(len(car.tickets), 1)
        self.assertEqual(car.tickets[0]._plate, plate)

    def test_car_last_ticket(self):
        plate = "CAR003"
        car = Car(plate)
        car.add_ticket()
        self.assertEqual(car.last_ticket._plate, plate)

    def test_car_to_dict(self):
        plate = "CAR004"
        car = Car(plate)
        car.add_ticket()
        car_dict = car.to_dict()
        self.assertEqual(car_dict['plate'], plate)
        self.assertEqual(len(car_dict['tickets']), 1)
        self.assertEqual(car_dict['tickets'][0]['plate'], plate)

    def test_car_from_dict(self):
        data = {
            'plate': "CAR005",
            'tickets': [
                {
                    'plate': "CAR005",
                    'arrival': datetime(2023, 6, 1, 9, 0).timestamp()
                }
            ],
            'sub': None
        }
        car = Car.from_dict(data)
        self.assertEqual(car.plate, data['plate'])
        self.assertEqual(len(car.tickets), 1)
        self.assertEqual(car.tickets[0]._plate, data['tickets'][0]['plate'])

    def test_car_add_sub(self):
        plate = "CAR006"
        car = Car(plate)
        # Mocking Subscription and Payment to test the method
        car._sub = Subscription("CAR006", 6)
        self.assertRaises(ValueError, car.add_sub, 6)

    def test_car_extend_sub(self):
        plate = "CAR007"
        car = Car(plate)
        # Mocking an active subscription
        car._sub = Subscription("CAR007", 6)
        car.extend_sub(3)  # Should not raise an error with a valid subscription
        self.assertTrue(car._sub.is_active())  # Check if the subscription is extended

if __name__ == '__main__':
    unittest.main()



