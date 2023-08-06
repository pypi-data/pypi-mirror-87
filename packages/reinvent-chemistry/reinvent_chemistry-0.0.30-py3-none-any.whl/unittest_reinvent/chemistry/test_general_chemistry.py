import unittest

from reinvent_chemistry import Conversions
from unittest_reinvent.chemistry.fixtures import smiles_collection, mols_collection, invalid, aspirin


class Test_general_chemistry(unittest.TestCase):

    def setUp(self):
        self.chemistry = Conversions()
        self.smiles = smiles_collection
        self.mols = mols_collection

    def test_smiles_to_mols_and_indices(self):
        mols, indices = self.chemistry.smiles_to_mols_and_indices(self.smiles)

        self.assertEqual(len(mols), 2)
        self.assertEqual(len(indices), 2)

    def test_mols_to_fingerprints(self):
        fps = self.chemistry.mols_to_fingerprints(self.mols)

        self.assertEqual(len(fps), 2)

    def test_smiles_to_mols(self):
        mols = self.chemistry.smiles_to_mols(self.smiles)

        self.assertEqual(len(mols), 2)

    def test_smiles_to_fingerprints(self):
        fps = self.chemistry.smiles_to_fingerprints(self.smiles)

        self.assertEqual(len(fps), 2)

    def test_smile_to_mol_not_none(self):
        mol = self.chemistry.smile_to_mol(aspirin)

        self.assertIsNotNone(mol)

    def test_smile_to_mol_none(self):
        mol = self.chemistry.smile_to_mol(invalid)

        self.assertIsNone(mol)

    def test_mols_to_smiles(self):
        mols = self.chemistry.smiles_to_mols(self.smiles)
        smiles = self.chemistry.mols_to_smiles(mols)

        self.assertEqual(self.smiles[:2], smiles)
