from app.models import User
import os
import unittest

from app.service import calculate_based_on_category


class CategoryCalculationsTests(unittest.TestCase):
    """regular category"""

    def test_regular_category_min_charge(self):
        output = calculate_based_on_category("regular", 2)
        self.assertEqual(output, 4)

    def test_regular_category_max_charge(self):
        output = calculate_based_on_category("regular", 3)
        self.assertEqual(output, 3.5)

    def test_regular_category_max_charge_part_two(self):
        output = calculate_based_on_category("regular", 5)
        self.assertEqual(output, 6.5)

    """novels category"""

    def test_novels_category_min_charge(self):
        output = calculate_based_on_category("novels", 3)
        self.assertEqual(output, 13.5)

    def test_novels_category_max_charge(self):
        output = calculate_based_on_category("novels", 4)
        self.assertEqual(output, 6)

    def test_novels_category_max_charge_part_two(self):
        output = calculate_based_on_category("novels", 10)
        self.assertEqual(output, 15)

    """fiction category"""

    def test_fiction_category_charge(self):
        output = calculate_based_on_category("fiction", 2)
        self.assertEqual(output, 6)

    def test_fiction_category_charge_part_two(self):
        output = calculate_based_on_category("fiction", 10)
        self.assertEqual(output, 30)
