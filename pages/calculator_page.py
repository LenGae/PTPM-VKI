from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CalculatorPage:
    URL = "https://testsheepnz.github.io/BasicCalculator.html"

    _FIRST_NUMBER = (By.ID, "number1Field")
    _SECOND_NUMBER = (By.ID, "number2Field")
    _OPERATOR = (By.ID, "selectOperationDropdown")
    _RESULT = (By.ID, "numberAnswerField")
    _CALCULATE_BTN = (By.ID, "calculateButton")
    _CLEAR_BTN = (By.ID, "clearButton")

    def __init__(self, driver):
        self.driver = driver

    def open(self):
        self.driver.get(self.URL)
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self._FIRST_NUMBER)
        )
        return self

    def enter_first_number(self, value):
        field = self.driver.find_element(*self._FIRST_NUMBER)
        field.clear()
        field.send_keys(str(value))
        return self

    def enter_second_number(self, value):
        field = self.driver.find_element(*self._SECOND_NUMBER)
        field.clear()
        field.send_keys(str(value))
        return self

    def select_operation(self, op_value):
        dropdown = Select(self.driver.find_element(*self._OPERATOR))
        dropdown.select_by_value(str(op_value))
        return self

    def click_calculate(self):
        self.driver.find_element(*self._CALCULATE_BTN).click()
        return self

    def get_result(self):
        return self.driver.find_element(*self._RESULT).get_attribute("value")

    def compute(self, first, second, op_value):
        return (
            self.enter_first_number(first)
            .enter_second_number(second)
            .select_operation(op_value)
            .click_calculate()
        )