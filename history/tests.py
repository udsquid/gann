###
### django libraries
###
from django.test import TestCase
from django.test.client import Client


###
### ??? test cases
###
class SimpleTests(TestCase):
    def test_simple_add(self):
        self.assertEqual(1+2, 3)
