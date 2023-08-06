import unittest

from reinvent_chemistry import Conversions
from reinvent_chemistry.library_design.fragment_reactions import FragmentReactions
from unittest_reinvent.library_design.fixtures import FRAGMENT_REACTION_SUZUKI


class TestFragmentReactions(unittest.TestCase):

    def setUp(self):
        self.reactions = FragmentReactions()
        self._suzuki_reaction_dto_list = self.reactions.create_reactions_from_smirks(FRAGMENT_REACTION_SUZUKI)
        self.suzuki_positive_smile = "COc1c(-c2cnn(C3CCC(N(C)C(C)=O)CC3)c2)cnc2ccc(-c3ccncn3)nc12"
        self.suzuki_negative_smile = "c1ccccc1CCNc2ccccc2CCCCC(=O)c1ccccc1"
        self.suzuki_fragment = "[*:0]c1ccc2ncc(-c3cnn(C4CCC(N(C)C(C)=O)CC4)c3)c(OC)c2n1"
        self.chemistry = Conversions()

    def test_slicing_molecule_to_fragments(self):
        molecule = self.chemistry.smile_to_mol(self.suzuki_positive_smile)
        all_fragment_pairs = self.reactions.slice_molecule_to_fragments(molecule, self._suzuki_reaction_dto_list)
        smile_fragments = []
        for pair in all_fragment_pairs:
            smiles_pair = []

            for fragment in pair:
                smile = self.chemistry.mol_to_smiles(fragment)
                smiles_pair.append(smile)
            smile_fragments.append(tuple(smiles_pair))

        self.assertEqual("*c1cnc2ccc(-c3ccncn3)nc2c1OC", smile_fragments[0][0])
        self.assertEqual("*c1cnn(C2CCC(N(C)C(C)=O)CC2)c1", smile_fragments[0][1])
        self.assertEqual("*c1ccc2ncc(-c3cnn(C4CCC(N(C)C(C)=O)CC4)c3)c(OC)c2n1", smile_fragments[2][0])
        self.assertEqual("*c1ccncn1", smile_fragments[2][1])

    def test_slicing_wrong_molecule_to_fragments(self):
        molecule = self.chemistry.smile_to_mol(self.suzuki_negative_smile)
        all_fragment_pairs = self.reactions.slice_molecule_to_fragments(molecule, self._suzuki_reaction_dto_list)
        smile_fragments = []
        for pair in all_fragment_pairs:
            smiles_pair = []
            for fragment in pair:
                smile = self.chemistry.mol_to_smiles(fragment)
                smiles_pair.append(smile)
            smile_fragments.append(tuple(smiles_pair))
        self.assertEqual(0, len(smile_fragments))

    def test_slicing_suzuki_fragment(self):
        molecule = self.chemistry.smile_to_mol(self.suzuki_fragment)
        all_fragment_pairs = self.reactions.slice_molecule_to_fragments(molecule, self._suzuki_reaction_dto_list)
        smile_fragments = []
        for pair in all_fragment_pairs:
            smiles_pair = []
            for fragment in pair:
                smile = self.chemistry.mol_to_smiles(fragment)
                smiles_pair.append(smile)
            smile_fragments.append(tuple(smiles_pair))
        self.assertEqual(2, len(smile_fragments))
