import unittest

import numpy.testing as npt

from reinvent_chemistry import Descriptors, Conversions
from unittest_reinvent.chemistry.fixtures import aspirin, celecoxib, dopamine, caffeine


class TestEqualityOfTwoCountsDescriptors(unittest.TestCase):

    def setUp(self):
        self.descriptors = Descriptors()
        self.chemistry = Conversions()
        smiles = [aspirin, celecoxib, caffeine, dopamine]
        self.mols = [self.chemistry.smile_to_mol(smi) for smi in smiles]

    def test_counts_fp_equal_default_params(self):
        parameters = {}
        fp_ori = self.descriptors.molecules_to_count_fingerprints_ori(self.mols, parameters)
        fp_alt = self.descriptors.molecules_to_count_fingerprints(self.mols, parameters)
        npt.assert_equal(fp_ori[0], fp_alt[0])
        npt.assert_equal(fp_ori, fp_alt)

    def test_counts_fp_equal_sas_params(self):
        parameters = dict(
            radius=3,
            size=4096,
            use_features=False,
        )
        fp_ori = self.descriptors.molecules_to_count_fingerprints_ori(self.mols, parameters)
        fp_alt = self.descriptors.molecules_to_count_fingerprints(self.mols, parameters)
        npt.assert_equal(fp_ori[0], fp_alt[0])
        npt.assert_equal(fp_ori, fp_alt)
