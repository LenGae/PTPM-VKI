import unittest
from converter import Converter


class TestConverterPositiveLarge(unittest.TestCase):
    def test_exact_boundary_100_7(self):
        self.assertEqual(Converter.do(100.7), 1000)

    def test_above_boundary_100_8(self):
        self.assertEqual(Converter.do(100.8), 1000)

    def test_large_value_500(self):
        self.assertEqual(Converter.do(500.0), 1000)

    def test_very_large_value_999999(self):
        self.assertEqual(Converter.do(999999.9), 1000)


class TestConverterPositiveRange(unittest.TestCase):
    def test_just_below_boundary_100_6(self):
        self.assertEqual(Converter.do(100.6), 100)

    def test_mid_value_50_5(self):
        self.assertEqual(Converter.do(50.5), 50)

    def test_small_positive_0_1(self):
        self.assertEqual(Converter.do(0.1), 0)

    def test_value_1_0(self):
        self.assertEqual(Converter.do(1.0), 1)

    def test_value_99_9(self):
        self.assertEqual(Converter.do(99.9), 99)

    def test_value_65_7(self):
        self.assertEqual(Converter.do(65.7), 65)


class TestConverterZero(unittest.TestCase):
    def test_zero_raises_value_error(self):
        with self.assertRaises(ValueError):
            Converter.do(0.0)

    def test_zero_int_raises_value_error(self):
        with self.assertRaises(ValueError):
            Converter.do(0)


class TestConverterNegativeRange(unittest.TestCase):
    def test_small_negative_minus_0_1(self):
        self.assertEqual(Converter.do(-0.1), -5)

    def test_value_minus_1_0(self):
        self.assertEqual(Converter.do(-1.0), -1 - 5)

    def test_value_minus_10_5(self):
        self.assertEqual(Converter.do(-10.5), -10 - 5)

    def test_value_minus_15_3(self):
        self.assertEqual(Converter.do(-15.3), -15 - 5)

    def test_boundary_minus_30_4(self):
        self.assertEqual(Converter.do(-30.4), -30 - 5)

    def test_value_minus_29_9(self):
        self.assertEqual(Converter.do(-29.9), -29 - 5)


class TestConverterNegativeLarge(unittest.TestCase):
    def test_exact_boundary_minus_30_5(self):
        self.assertEqual(Converter.do(-30.5), -2000)

    def test_below_boundary_minus_30_6(self):
        self.assertEqual(Converter.do(-30.6), -2000)

    def test_value_minus_100(self):
        self.assertEqual(Converter.do(-100.0), -2000)

    def test_value_minus_94_5(self):
        self.assertEqual(Converter.do(-94.5), -2000)

    def test_very_large_negative(self):
        self.assertEqual(Converter.do(-999999.9), -2000)


if __name__ == "__main__":
    unittest.main()
