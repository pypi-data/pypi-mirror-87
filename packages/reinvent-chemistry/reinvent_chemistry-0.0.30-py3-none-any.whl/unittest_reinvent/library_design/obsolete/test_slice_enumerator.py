import unittest

from reinvent_chemistry import Conversions
from reinvent_chemistry.library_design.dtos import FilteringConditionDTO
from reinvent_chemistry.library_design.enums import MolecularDescriptorsEnum, SliceTypeEnum
from reinvent_chemistry.library_design.obsolete import SliceEnumerator
from reinvent_chemistry.library_design.obsolete.slice_rules import SliceRules


class TestSliceEnumerator(unittest.TestCase):

    def setUp(self):
        descriptors_enum = MolecularDescriptorsEnum()
        slice_types = SliceTypeEnum()
        rules = SliceRules()
        smarts = rules.get_smarts_as_mols(slice_types.RECAP)
        scaffold_condition_1 = FilteringConditionDTO(descriptors_enum.RING_COUNT, min=1)
        scaffold_condition_2 = FilteringConditionDTO(descriptors_enum.MOLECULAR_WEIGHT, max=600)
        decoartion_condition_1 = FilteringConditionDTO(descriptors_enum.HYDROGEN_BOND_ACCEPTORS, max=3)
        decoartion_condition_2 = FilteringConditionDTO(descriptors_enum.HYDROGEN_BOND_DONORS, max=3)
        scaffold_conditions = [scaffold_condition_1, scaffold_condition_2]
        decoartion_conditions = [decoartion_condition_1, decoartion_condition_2]
        self._slice_enumerator = SliceEnumerator(smarts, scaffold_conditions, decoartion_conditions)
        self.chemistry = Conversions()

    def test_counting_slices_1(self):
        smile = "[*:0]CNCc1ccccc1"
        molecule = self.chemistry.smile_to_mol(smile)

        result = self._slice_enumerator.count(molecule)
        self.assertEqual(2, result)

    def test_counting_slices_2(self):
        smile = "[*:0]c1ccccc1CCNc2ccccc2C"
        molecule = self.chemistry.smile_to_mol(smile)

        result = self._slice_enumerator.count(molecule)
        self.assertEqual(1, result)

    def test_counting_slices_3(self):
        smile = "CCN"
        molecule = self.chemistry.smile_to_mol(smile)

        result = self._slice_enumerator.count(molecule)
        self.assertEqual(1, result)

    def test_enumeration_1(self):
        smile = "c1ccccc1CCCNC=Cc2ccccc2CCNCC"
        molecule = self.chemistry.smile_to_mol(smile)

        result = self._slice_enumerator.enumerate(molecule, 1)
        self.assertEqual(2, len(result))
