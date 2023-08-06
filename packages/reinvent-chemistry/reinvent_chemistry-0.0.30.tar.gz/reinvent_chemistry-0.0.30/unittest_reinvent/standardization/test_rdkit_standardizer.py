import unittest

from dacite import from_dict

from reinvent_chemistry import Conversions
from reinvent_chemistry.enums import FilterTypesEnum
from reinvent_chemistry.standardization.filter_configuration import FilterConfiguration
from reinvent_chemistry.standardization.rdkit_standardizer import RDKitStandardizer


class MockLogger:
    def log_message(self, message):
        print(message)


class TestRDKitStandardizer_PositiveOutcome(unittest.TestCase):

    def setUp(self):
        self.chemistry = Conversions()
        filter_types = FilterTypesEnum()
        logger = MockLogger()
        raw_config = {"name": filter_types.DEFAULT, "parameters": {"max_heavy_atoms": 50}}
        config = from_dict(data_class=FilterConfiguration, data=raw_config)
        filter_configs = [config]
        self.standardizer = RDKitStandardizer(filter_configs, logger)

        self.compound_1 = "CCOC(=O)c1c(NC(=O)c2cccc(S(=O)(=O)N3CCOCC3)c2)sc(C)c1C"

    def test_standardizer_1(self):
        result = self.standardizer.apply_filter(self.compound_1)

        self.assertEqual(self.compound_1, result)


class TestRDKitStandardizer_NegativeOutcome(unittest.TestCase):

    def setUp(self):
        self.chemistry = Conversions()
        filter_types = FilterTypesEnum()
        logger = MockLogger()
        raw_config = {"name": filter_types.DEFAULT, "parameters": {"max_heavy_atoms": 10}}
        config = from_dict(data_class=FilterConfiguration, data=raw_config)
        filter_configs = [config]
        self.standardizer = RDKitStandardizer(filter_configs, logger)

        self.compound_1 = "CCOC(=O)c1c(NC(=O)c2cccc(S(=O)(=O)N3CCOCC3)c2)sc(C)c1C"

    def test_standardizer_1(self):
        result = self.standardizer.apply_filter(self.compound_1)

        self.assertEqual(None, result)


class TestRDKitStandardizer_NoConfig(unittest.TestCase):

    def setUp(self):
        self.chemistry = Conversions()
        logger = MockLogger()
        filter_configs = []
        self.standardizer = RDKitStandardizer(filter_configs, logger)

        self.compound_1 = "CCOC(=O)c1c(NC(=O)c2cccc(S(=O)(=O)N3CCOCC3)c2)sc(C)c1C"

    def test_standardizer_1(self):
        result = self.standardizer.apply_filter(self.compound_1)

        self.assertEqual(self.compound_1, result)


class TestRDKitStandardizer_AliphaticFilterPositive(unittest.TestCase):

    def setUp(self):
        self.chemistry = Conversions()
        filter_types = FilterTypesEnum()
        logger = MockLogger()
        raw_config = {"name": filter_types.ALIPHATIC_CHAIN_FILTER, "parameters": {}}
        config = from_dict(data_class=FilterConfiguration, data=raw_config)
        filter_configs = [config]
        self.standardizer = RDKitStandardizer(filter_configs, logger)

        self.compound_1 = "CCCCc1ccccc1"

    def test_standardizer_1(self):
        result = self.standardizer.apply_filter(self.compound_1)

        self.assertEqual(self.compound_1, result)


class TestRDKitStandardizer_AliphaticFilterNegative(unittest.TestCase):

    def setUp(self):
        self.chemistry = Conversions()
        filter_types = FilterTypesEnum()
        logger = MockLogger()
        raw_config = {"name": filter_types.ALIPHATIC_CHAIN_FILTER, "parameters": {}}
        config = from_dict(data_class=FilterConfiguration, data=raw_config)
        filter_configs = [config]
        self.standardizer = RDKitStandardizer(filter_configs, logger)

        self.compound_1 = "CCCCCc1ccccc1"

    def test_standardizer_1(self):
        result = self.standardizer.apply_filter(self.compound_1)

        self.assertEqual(None, result)