import unittest

from reinvent_chemistry import Conversions
from reinvent_chemistry.library_design import FragmentFilter
from reinvent_chemistry.library_design.dtos import FilteringConditionDTO
from reinvent_chemistry.library_design.enums import MolecularDescriptorsEnum


class TestFragmentFilter(unittest.TestCase):

    def setUp(self):
        descriptors_enum = MolecularDescriptorsEnum()
        condition_1 = FilteringConditionDTO(descriptors_enum.RING_COUNT, equals=1)
        condition_2 = FilteringConditionDTO(descriptors_enum.CLOGP, min=1)
        conditions = [condition_1, condition_2]
        self.filter = FragmentFilter(conditions)
        self.chemistry = Conversions()

    def test_compliant_with_conditions(self):
        smile = "[*:0]CNCc1ccccc1"
        molecule = self.chemistry.smile_to_mol(smile)

        result = self.filter.filter(molecule)
        self.assertTrue(result)

    def test_non_compliant_with_conditions(self):
        smile = "[*:0]c1ccccc1CCNc2ccccc2C"
        molecule = self.chemistry.smile_to_mol(smile)

        result = self.filter.filter(molecule)
        self.assertFalse(result)

    def test_non_compliant_with_ring_count(self):
        smile = "CNCCC"
        molecule = self.chemistry.smile_to_mol(smile)

        result = self.filter.filter(molecule)
        self.assertFalse(result)
