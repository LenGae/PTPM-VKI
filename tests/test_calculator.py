import unittest

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pages.calculator_page import CalculatorPage


class TestCalculator(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        opts = Options()
        opts.add_argument("--headless=new")
        cls.driver = webdriver.Chrome(options=opts)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def setUp(self):
        self.page = CalculatorPage(self.driver).open()

    def test_addition(self):
        self.page.compute(5, 3, 0)
        self.assertEqual(self.page.get_result(), "8")

    def test_addition_with_zero(self):
        self.page.compute(0, 7, 0)
        self.assertEqual(self.page.get_result(), "7")

    def test_addition_negative(self):
        self.page.compute(-5, -3, 0)
        self.assertEqual(self.page.get_result(), "-8")

    def test_subtraction(self):
        self.page.compute(10, 4, 1)
        self.assertEqual(self.page.get_result(), "6")

    def test_subtraction_negative_result(self):
        self.page.compute(3, 8, 1)
        self.assertEqual(self.page.get_result(), "-5")

    def test_multiplication(self):
        self.page.compute(6, 7, 2)
        self.assertEqual(self.page.get_result(), "42")

    def test_multiplication_by_zero(self):
        self.page.compute(100, 0, 2)
        self.assertEqual(self.page.get_result(), "0")

    def test_division(self):
        self.page.compute(20, 4, 3)
        self.assertEqual(self.page.get_result(), "5")

    def test_division_by_zero(self):
        self.page.compute(10, 0, 3)
        result = self.page.get_result()
        self.assertTrue(result == "" or "Infinity" in result or "error" in result.lower())

    def test_division_float(self):
        self.page.compute(7, 2, 3)
        self.assertEqual(self.page.get_result(), "3.5")

    def test_concatenation(self):
        self.page.compute("Hello", "World", 4)
        self.assertEqual(self.page.get_result(), "HelloWorld")


if __name__ == "__main__":
    unittest.main()