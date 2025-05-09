from django.test import TestCase
from .services import update_bets, update_promos

# Create your tests here.

class CalculateTestCase(TestCase):
    def test_from_services(self):
        update_bets()

class ScrapePromosTestCase(TestCase):
    def test_sportsbookreview(self):
        update_promos()