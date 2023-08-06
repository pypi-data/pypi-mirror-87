import unittest

import unittest_reinvent.fixtures.test_data as tfv
from reinvent_chemistry.utils import get_indices_of_unique_smiles


class Test_utils_unique_smiles(unittest.TestCase):

    def test_unique_smiles_list(self):
        smiles = tfv.SMILES_LIST[1:-1]
        idxs = get_indices_of_unique_smiles(smiles)
        self.assertEqual(len(idxs), 25)
        self.assertEqual(smiles[idxs[0]], smiles[0])
        self.assertEqual(smiles[idxs[10]], smiles[10])

    def test_duplicate_smiles_list(self):
        smiles = tfv.REP_SMILES_LIST
        idxs = get_indices_of_unique_smiles(smiles)
        self.assertEqual(len(idxs), 2)
        self.assertEqual(smiles[idxs[0]], smiles[0])
        self.assertEqual(smiles[idxs[1]], smiles[15])

    def test_invalid_smiles_list(self):
        smiles = tfv.INVALID_SMILES_LIST
        idxs = get_indices_of_unique_smiles(smiles)
        self.assertEqual(len(idxs), 1)
        self.assertEqual(smiles[idxs[0]], smiles[0])

class Test_utils_unique_seqs(unittest.TestCase):

    def test_duplicate_seqs_list(self):
        seqs = tfv.REP_SMILES_LIST
        idxs = get_indices_of_unique_smiles(seqs)
        self.assertEqual(len(idxs), 2)
        self.assertEqual(seqs[idxs[0]], seqs[0])
        self.assertEqual(seqs[idxs[1]], seqs[15])

    def test_invalid_seqs_list(self):
        seqs = tfv.INVALID_SMILES_LIST
        idxs = get_indices_of_unique_smiles(seqs)
        self.assertEqual(len(idxs), 1)
        self.assertEqual(seqs[idxs[0]], seqs[0])


