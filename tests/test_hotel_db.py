import unittest
from hotel_db import get_hotels

class TestHotelDB(unittest.TestCase):
    def test_get_hotels_location(self):
        hotels = get_hotels(location="Goa")
        self.assertIsInstance(hotels, list)
        for hotel in hotels:
            self.assertEqual(hotel['location'], "Goa")

    def test_get_hotels_price_filter(self):
        hotels = get_hotels(max_price=2000)
        for hotel in hotels:
            self.assertLessEqual(hotel['price'], 2000)

if __name__ == '__main__':
    unittest.main()
