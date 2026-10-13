import unittest
from calculator import TriangleCalculator


class TestTriangleCalculatorUnit(unittest.TestCase):

    def test_equilateral(self):
        t, err, coords = TriangleCalculator.determine_type(3, 3, 3)
        self.assertEqual(t, "равносторонний")
        self.assertIsNone(err)
        self.assertEqual(len(coords), 3)

    def test_isosceles(self):
        t, err, _ = TriangleCalculator.determine_type(5, 5, 6)
        self.assertEqual(t, "равнобедренный")
        self.assertIsNone(err)

    def test_scalene(self):
        t, err, _ = TriangleCalculator.determine_type(3, 4, 5)
        self.assertEqual(t, "разносторонний")
        self.assertIsNone(err)

    def test_non_positive(self):
        t, err, coords = TriangleCalculator.determine_type(-1, 2, 3)
        self.assertEqual(t, "не треугольник")
        self.assertIsNotNone(err)
        self.assertEqual(coords[0], (-1, -1))

    def test_non_numeric(self):
        t, err, coords = TriangleCalculator.determine_type("a", "b", "c")
        self.assertEqual(t, "")
        self.assertIsNotNone(err)
        self.assertEqual(coords[0], (-2, -2))