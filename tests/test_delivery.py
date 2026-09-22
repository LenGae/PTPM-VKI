import unittest
import datetime
from Delivery import calculate_delivery_cost


class TestDeliveryCost(unittest.TestCase):
    def test_returns_error_for_negative_weight(self):
        cost, date = calculate_delivery_cost(-1, 100, "обычный")
        self.assertEqual(cost, -1)
        self.assertEqual(date, "0000-00-00")

    def test_returns_error_for_too_heavy_package(self):
        cost, _ = calculate_delivery_cost(51.0, 100, "обычный")
        self.assertEqual(cost, -1)

    def test_returns_error_for_zero_distance(self):
        cost, _ = calculate_delivery_cost(1.0, 0, "обычный")
        self.assertEqual(cost, -1)

    def test_returns_error_for_invalid_package_type(self):
        cost, _ = calculate_delivery_cost(1.0, 100, "неизвестный")
        self.assertEqual(cost, -1)

    def test_base_cost_for_light_package(self):
        cost, _ = calculate_delivery_cost(1.0, 100, "обычный")
        self.assertEqual(cost, 700)

    def test_distance_scales_cost_linearly(self):
        cost1, _ = calculate_delivery_cost(1.0, 100, "обычный")
        cost2, _ = calculate_delivery_cost(1.0, 200, "обычный")
        self.assertEqual(cost2 - cost1, 500)

    def test_medium_weight_applies_1_2_coefficient(self):
        # 700 * 1.2 = 840
        cost, _ = calculate_delivery_cost(10.0, 100, "обычный")
        self.assertEqual(cost, 840)

    def test_heavy_weight_applies_1_5_coefficient(self):
        # 700 * 1.5 = 1050
        cost, _ = calculate_delivery_cost(25.0, 100, "обычный")
        self.assertEqual(cost, 1050)

    def test_fragile_package_adds_300(self):
        cost, _ = calculate_delivery_cost(1.0, 100, "хрупкий")
        self.assertEqual(cost, 700 + 300)

    def test_dangerous_package_adds_1000(self):
        cost, _ = calculate_delivery_cost(1.0, 100, "опасный")
        self.assertEqual(cost, 700 + 1000)

    def test_express_should_cost_more_than_regular(self):
        cost_regular, _ = calculate_delivery_cost(1.0, 100, "обычный", False)
        cost_express, _ = calculate_delivery_cost(1.0, 100, "обычный", True)
        self.assertGreater(cost_express, cost_regular,
                           "Экспресс должен быть дороже обычной доставки")

    def test_delivery_date_for_short_distance(self):
        _, date = calculate_delivery_cost(1.0, 100, "обычный")
        expected = (datetime.date(2026, 9, 3) + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        self.assertEqual(date, expected)

    def test_express_short_distance_still_delivers_in_one_day(self):
        _, date = calculate_delivery_cost(1.0, 100, "обычный", True)
        expected = (datetime.date(2026, 9, 3) + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        self.assertEqual(date, expected,
                         "Экспресс не может приехать в день отправки")

    def test_returns_tuple_of_cost_and_date(self):
        result = calculate_delivery_cost(1.0, 100, "обычный")
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)


if __name__ == "__main__":
    unittest.main()