import unittest
from src.utils.stringUtils import extractVoltFromName
import datetime as dt
from src.appConfig import getConfig


class TestStringUtils(unittest.TestCase):
    appConfig = None

    def test_fsc(self) -> None:
        """tests extract voltage level from fsc name
        """
        elemType = 'FSC'
        elemName = '400KV-APL-MUNDRA-SAMI-1 FSC@ SAMI'
        elemVoltLvl = extractVoltFromName(elemType, elemName)
        # print(elemVoltLvl)
        self.assertTrue(elemVoltLvl == '400KV')

    def test_acTransLineCkt(self) -> None:
        """tests extract voltage level from acTransLineCkt name
        """
        elemType = 'AC_TRANSMISSION_LINE_CIRCUIT'
        elemName = '132KV-BINA-MP-MORWA-1'
        elemVoltLvl = extractVoltFromName(elemType, elemName)
        # print(elemVoltLvl)
        self.assertTrue(elemVoltLvl == '132KV')

    def test_hvdcLineCkt(self) -> None:
        """tests extract voltage level from hvdcLineCkt name
        """
        elemType = 'HVDC_LINE_CIRCUIT'
        elemName = 'HVDC400KV-Vindyachal(PS)-RIHAND-1'
        elemVoltLvl = extractVoltFromName(elemType, elemName)
        # print(elemVoltLvl)
        self.assertTrue(elemVoltLvl == '400KV')

    def test_busReactor(self) -> None:
        """tests extract voltage level from busReactor name
        """
        elemType = 'BUS REACTOR'
        elemName = 'AKOLA (2) - 765KV B/R 1'
        elemVoltLvl = extractVoltFromName(elemType, elemName)
        # print(elemVoltLvl)
        self.assertTrue(elemVoltLvl == '765KV')

    def test_lineReactor(self) -> None:
        """tests extract voltage level from lineReactor name
        """
        elemType = 'LINE_REACTOR'
        elemName = '400KV-AKOLA-AURANGABAD-2 L/R@ AKOLA - 400KV'
        elemVoltLvl = extractVoltFromName(elemType, elemName)
        # print(elemVoltLvl)
        self.assertTrue(elemVoltLvl == '400KV')

    def test_transformer(self) -> None:
        """tests extract voltage level from transformer name
        """
        elemType = 'TRANSFORMER'
        elemName = '1200KV/400KV BINA-ICT-1'
        elemVoltLvl = extractVoltFromName(elemType, elemName)
        # print(elemVoltLvl)
        self.assertTrue(elemVoltLvl == '1200KV/400KV')
