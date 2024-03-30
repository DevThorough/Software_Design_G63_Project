from pricing import fuelPrice
import unittest

## Test pricing function
## def fuelPrice(gallons, hasHistory, state):

class TestPricingFunction(unittest.TestCase):
    def test_price(self):
        #Test prices when gallons >= 0
        self.assertAlmostEqual(fuelPrice(5,1,'TX'), 5*3.50+5)
        self.assertAlmostEqual(fuelPrice(10000,True,'AZ'), 10000*3.50+15)
        self.assertAlmostEqual(fuelPrice(5,False,'XYZ'), 5*3.99+15)

    def test_values(self):
        self.assertRaises(ValueError, fuelPrice, -4, 1, 'TX')
        self.assertRaises(ValueError, fuelPrice, -4, -1, 'TX')
