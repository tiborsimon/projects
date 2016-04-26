import unittest
from projects import main


class BasicFunctionalityTests(unittest.TestCase):
    def test__main_function_is_callable(self):
        main('')
