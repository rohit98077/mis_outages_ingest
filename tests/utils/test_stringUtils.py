import unittest
from src.utils.stringUtils import extractVoltFromName
import datetime as dt
from src.appConfig import getConfig


class TestStringUtils(unittest.TestCase):
    appConfig = None

    def test_run(self) -> None:
        """tests the function that extracts voltage level from element name
        """
        elementType = 'TRANSFORMER'
        elementName = '765KV/400KV KHANDWA-STERLITE-ICT-2'
        elementVoltLevel = extractVoltFromName(elementType, elementName)
        self.assertTrue(elementVoltLevel == '765KV/400KV')
