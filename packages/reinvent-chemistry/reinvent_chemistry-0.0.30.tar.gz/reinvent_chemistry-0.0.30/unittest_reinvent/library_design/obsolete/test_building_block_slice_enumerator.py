import unittest

from reinvent_chemistry import Conversions
from reinvent_chemistry.library_design.dtos import FilteringConditionDTO
from reinvent_chemistry.library_design.enums import MolecularDescriptorsEnum
from reinvent_chemistry.library_design.obsolete import BuildingBlockReactions, BuildingBlockSliceEnumerator
from reinvent_chemistry.library_design.obsolete.reaction_slice_enumerator import ReactionSliceEnumerator
from unittest_reinvent.library_design.fixtures import REACTION_SUZUKI, SUZUKI_NEGISHI_REDUCTIVE_AMINATION


class TestSingleBuildingBlockSliceEnumerator(unittest.TestCase):

    def setUp(self):
        self.chemistry = Conversions()
        self.reactions = BuildingBlockReactions()
        self._suzuki_reactions = self.reactions.create_reactions_from_smirks(REACTION_SUZUKI)
        self.suzuki_positive_smile = "COc1c(-c2cnn(C3CCC(N(C)C(C)=O)CC3)c2)cnc2ccc(-c3ccncn3)nc12"
        self.suzuki_positive_molecule = self.chemistry.smile_to_mol(self.suzuki_positive_smile)

        scaffold_conditions = []
        decoartion_conditions = []
        self._slice_enumerator = BuildingBlockSliceEnumerator(self._suzuki_reactions, scaffold_conditions,
                                                         decoartion_conditions)

    def test_enumeration_slcing_1(self):
        result = self._slice_enumerator.enumerate(self.suzuki_positive_molecule, 1)

        self.assertEqual(4, len(result))

    def test_enumeration_slicing_2(self):
        result = self._slice_enumerator.enumerate(self.suzuki_positive_molecule, 2)

        self.assertEqual(6, len(result))


class TestMultipleBuildingBlockSliceEnumerator(unittest.TestCase):

    def setUp(self):
        self.chemistry = Conversions()
        self.reactions = BuildingBlockReactions()
        self._suzuki_reactions = self.reactions.create_reactions_from_smirks(SUZUKI_NEGISHI_REDUCTIVE_AMINATION)
        self.positive_smile = "COc1c(-c2cnn(C(NCC)CCCCCC3CCC(N(C)C(C)=O)CC3)c2)cnc2ccc(-c3ccncn3)nc12"

        self.positive_molecule = self.chemistry.smile_to_mol(self.positive_smile)

        scaffold_conditions = []
        decoartion_conditions = []
        self._slice_enumerator = BuildingBlockSliceEnumerator(self._suzuki_reactions, scaffold_conditions,
                                                         decoartion_conditions)

    def test_enumeration_slicing_1(self):
        result = self._slice_enumerator.enumerate(self.positive_molecule, 1)

        self.assertEqual(16, len(result))

    def test_enumeration_slicing_2(self):
        result = self._slice_enumerator.enumerate(self.positive_molecule, 2)

        self.assertEqual(73, len(result))

    def test_enumeration_slicing_3(self):
        result = self._slice_enumerator.enumerate(self.positive_molecule, 3)

        self.assertEqual(133, len(result))


class TestBuildingBlockSliceEnumeratorWithFilters(unittest.TestCase):

    def setUp(self):
        self.chemistry = Conversions()
        self.reactions = BuildingBlockReactions()
        self._suzuki_reactions = self.reactions.create_reactions_from_smarts(SUZUKI_NEGISHI_REDUCTIVE_AMINATION)
        self.positive_smile = "COc1c(-c2cnn(C(NCC)CCCCCC3CCC(N(C)C(C)=O)CC3)c2)cnc2ccc(-c3ccncn3)nc12"

        self.positive_molecule = self.chemistry.smile_to_mol(self.positive_smile)
        descriptors_enum = MolecularDescriptorsEnum()

        scaffold_condition_1 = FilteringConditionDTO(descriptors_enum.RING_COUNT, min=1)
        scaffold_condition_2 = FilteringConditionDTO(descriptors_enum.MOLECULAR_WEIGHT, max=600)
        decoartion_condition_1 = FilteringConditionDTO(descriptors_enum.HYDROGEN_BOND_ACCEPTORS, max=3)
        decoartion_condition_2 = FilteringConditionDTO(descriptors_enum.HYDROGEN_BOND_DONORS, max=3)
        scaffold_conditions = [scaffold_condition_1, scaffold_condition_2]
        decoartion_conditions = [decoartion_condition_1, decoartion_condition_2]
        self._slice_enumerator = ReactionSliceEnumerator(self._suzuki_reactions, scaffold_conditions,
                                                         decoartion_conditions)

    def test_enumeration_slicing_1(self):
        result = self._slice_enumerator.enumerate(self.positive_molecule, 1)

        self.assertEqual(7, len(result))

    def test_enumeration_slicing_2(self):
        result = self._slice_enumerator.enumerate(self.positive_molecule, 2)

        self.assertEqual(29, len(result))

    def test_enumeration_slicing_3(self):
        result = self._slice_enumerator.enumerate(self.positive_molecule, 3)

        self.assertEqual(59, len(result))

