import unittest

from rdkit.Chem.rdmolfiles import MolToSmiles

from reinvent_chemistry import Conversions
from reinvent_chemistry.library_design import AttachmentPoints
from reinvent_chemistry.library_design.bond_maker import BondMaker
from reinvent_chemistry.library_design.fragment_reactions import FragmentReactions


class TestBondMaker(unittest.TestCase):

    def setUp(self):
        self._bond_maker = BondMaker()
        self._attachments = AttachmentPoints()
        self._conversions = Conversions()
        self.reactions = FragmentReactions()
        self.expected_results = "CCCN(CCC)c1cccc2[nH]c(=Nc3c(C)cc(Br)cc3OC)n(C)c12"
        self.unlabeled_scaffold_A = "[*]N(c1cccc2[nH]c(=Nc3c(OC)cc(Br)cc3[*])n(C)c12)[*]"
        self.decorations_A = "*CCC|*C|*CCC"

    def test_join_randomized_scaffold_and_decorations(self):
        scaffold = self._attachments.add_attachment_point_numbers(self.unlabeled_scaffold_A, canonicalize=False)
        scaffold_mol = self._conversions.smile_to_mol(scaffold)
        scaffold = self._conversions.mol_to_random_smiles(scaffold_mol)

        molecule = self._bond_maker.join_scaffolds_and_decorations(scaffold, self.decorations_A)
        complete_smile = MolToSmiles(molecule, isomericSmiles=False, canonical=True)

        self.assertEqual(self.expected_results, complete_smile)
