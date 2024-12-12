import unittest
from datetime import timedelta
from libs.parking  import *


class TestSubscription(unittest.TestCase):
    def test_initialization(self):
        """Test de l'initialisation de Subscription."""
        start_date = MyDateTime.now()
        subscription = Subscription(plate="123ABC", length=3, start=start_date)

        self.assertEqual(subscription._plate, "123ABC")
        self.assertEqual(subscription._length, 3)
        self.assertEqual(subscription._start, start_date)

    def test_default_start(self):
        """Test du démarrage par défaut."""
        subscription = Subscription(plate="123ABC")
        now = MyDateTime.now()

        self.assertAlmostEqual(subscription._start.timestamp(), now.timestamp(), delta=1)

    def test_end_date(self):
        """Test de la date de fin."""
        start_date = MyDateTime.now()
        subscription = Subscription(plate="123ABC", length=3, start=start_date)

        expected_end = start_date.add_months(3)
        self.assertEqual(subscription.end, expected_end)

    def test_is_active(self):
        """Test si l'abonnement est actif."""
        start_date = MyDateTime.now()
        subscription = Subscription(plate="123ABC", length=1, start=start_date)

        self.assertTrue(subscription.is_active())

    def test_was_active(self):
        """Test si l'abonnement était actif à une date donnée."""
        start_date = MyDateTime.now()
        subscription = Subscription(plate="123ABC", length=1, start=start_date)
        test_date = start_date + timedelta(days=15)

        self.assertTrue(subscription.was_active(test_date))

    def test_extend(self):
        """Test de l'extension de l'abonnement."""
        subscription = Subscription(plate="123ABC", length=1)
        subscription.extend(2)

        self.assertEqual(subscription._length, 3)

    def test_from_dict(self):
        """Test de la méthode from_dict."""
        data = {
            "plate": "123ABC",
            "length": 2,
            "start": MyDateTime.now().timestamp()
        }
        subscription = Subscription.from_dict(data)

        self.assertEqual(subscription._plate, data["plate"])
        self.assertEqual(subscription._length, data["length"])
        self.assertEqual(subscription._start.timestamp(), data["start"])

    def test_to_dict(self):
        """Test de la méthode to_dict."""
        start_date = MyDateTime.now()
        subscription = Subscription(plate="123ABC", length=2, start=start_date)
        result = subscription.to_dict()

        self.assertEqual(result["plate"], "123ABC")
        self.assertEqual(result["length"], 2)
        self.assertEqual(result["start"], start_date.timestamp())

    def test_str_representation(self):
        """Test de la représentation en chaîne de caractères."""
        start_date = MyDateTime.now()
        subscription = Subscription(plate="123ABC", length=2, start=start_date)
        end_date = subscription.end
        expected_str = f"Plate : 123ABC\nStart : {start_date.strftime('%d/%m/%Y à %H:%M:%S')}\nEnd : {end_date.strftime('%d/%m/%Y à %H:%M:%S')}"

        self.assertEqual(str(subscription), expected_str)


if __name__ == "__main__":
    unittest.main()
