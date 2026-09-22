import unittest
from main import calculate_triangle


class TestCalculateTriangle(unittest.TestCase):
    def test_non_numeric_input_returns_error_marker(self):
        result, coords = calculate_triangle("abc", "5", "5")
        self.assertEqual(result, "")
        self.assertEqual(coords, [(-2, -2), (-2, -2), (-2, -2)])

    def test_none_input_returns_error_marker(self):
        result, _ = calculate_triangle(None, 3, 4)
        self.assertEqual(result, "")

    def test_zero_side_returns_not_a_triangle(self):
        result, coords = calculate_triangle(0, 3, 4)
        self.assertEqual(result, "не треугольник")
        self.assertEqual(coords, [(-1, -1), (-1, -1), (-1, -1)])

    def test_negative_side_returns_not_a_triangle(self):
        result, _ = calculate_triangle(-3, 4, 5)
        self.assertEqual(result, "не треугольник")

    def test_degenerate_triangle_is_rejected(self):
        result, _ = calculate_triangle(1, 2, 3)
        self.assertEqual(result, "не треугольник")

    def test_equilateral_triangle(self):
        result, _ = calculate_triangle(5, 5, 5)
        self.assertEqual(result, "равносторонний")

    def test_isosceles_triangle(self):
        result, _ = calculate_triangle(5, 5, 6)
        self.assertEqual(result, "равнобедренный")

    def test_scalene_triangle(self):
        result, _ = calculate_triangle(3, 4, 5)
        self.assertEqual(result, "разносторонний")

    def test_string_numbers_are_accepted(self):
        result, _ = calculate_triangle("3", "4", "5")
        self.assertEqual(result, "разносторонний")

    def test_returns_tuple_of_type_and_coordinates(self):
        result = calculate_triangle(3, 4, 5)
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[1], list)
        self.assertEqual(len(result[1]), 3)

    def test_coordinates_are_integers(self):
        _, coords = calculate_triangle(3, 4, 5)
        for x, y in coords:
            self.assertIsInstance(x, int)
            self.assertIsInstance(y, int)

    def test_first_vertex_at_origin_offset(self):
        _, coords = calculate_triangle(3, 4, 5)
        self.assertEqual(coords[0], (5, 5))

    def test_coordinates_fit_canvas(self):
        _, coords = calculate_triangle(1000, 1000, 1000)
        for x, y in coords:
            self.assertLessEqual(x, 100)
            self.assertLessEqual(y, 100)


if __name__ == "__main__":
    unittest.main()