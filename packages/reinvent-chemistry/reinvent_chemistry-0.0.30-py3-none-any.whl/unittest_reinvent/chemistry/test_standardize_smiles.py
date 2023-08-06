import unittest

from reinvent_chemistry.input_standardization import Standardizer
from unittest_reinvent.chemistry.fixtures import aspirin, celecoxib


class Test_standardize_smiles(unittest.TestCase):

    def setUp(self):
        self.standardizer = Standardizer()
        self.smiles_string = "CC(C)(Cc1ccc(cc1)Cl)NC(=O)[C@H](CCC(=O)O)NC(=O)c2ccc(cc2)c3ccc(cc3)Cl"

    def test_standardize_long_aliphatic_molecule(self):
        molecule = self.standardizer.standardize_smiles(self.smiles_string)

        self.assertIsNone(molecule)

    def test_standardize_normal_molecule_1(self):
        molecule = self.standardizer.standardize_smiles(celecoxib)

        self.assertIsNotNone(molecule)

    def test_standardize_normal_molecule_2(self):
        molecule = self.standardizer.standardize_smiles(aspirin)

        self.assertIsNotNone(molecule)

