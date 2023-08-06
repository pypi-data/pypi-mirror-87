import unittest

from rdkit.Chem.rdmolfiles import MolToSmiles

from reinvent_chemistry import Conversions
from reinvent_chemistry.library_design import AttachmentPoints, BondMaker
from reinvent_chemistry.library_design.fragment_reactions import FragmentReactions


class TestAttachmentPoints(unittest.TestCase):

    def setUp(self):
        self._attachment_points = AttachmentPoints()
        self._bond_maker = BondMaker()
        self.chemistry = Conversions()
        self.reactions = FragmentReactions()
        self.decorations_A = '*OCC|*N1CCOCC1|*C'
        self.expected_results = "CCOC(=O)c1c(NC(=O)c2cccc(S(=O)(=O)N3CCOCC3)c2)sc(C)c1C"
        self.labeled_scaffold_A = "[*:0]C(=O)c1c(NC(=O)c2cccc(S(=O)(=O)[*:2])c2)sc([*:1])c1C"

    def test_get_attachment_points(self):
        result = self._attachment_points.get_attachment_points(self.labeled_scaffold_A)
        self.assertEqual([0, 2, 1], result)

    def test_add_attachment_point_numbers(self):
        relabeled = self._attachment_points.add_attachment_point_numbers(self.labeled_scaffold_A)
        result = self._attachment_points.get_attachment_points(relabeled)
        self.assertEqual([0, 1, 2], result)

    def test_remove_attachment_point_numbers(self):
        result = self._attachment_points.remove_attachment_point_numbers(self.labeled_scaffold_A)
        self.assertEqual("[*]C(=O)c1c(NC(=O)c2cccc(S(=O)(=O)[*])c2)sc([*])c1C", result)

    def test_remove_attachment_point_numbers_from_mol(self):
        molecule = self.chemistry.smile_to_mol(self.labeled_scaffold_A)
        mol_result = self._attachment_points.remove_attachment_point_numbers_from_mol(molecule)
        result_no_brackets = MolToSmiles(mol_result, isomericSmiles=False, canonical=True)
        result = self._attachment_points.add_brackets_to_attachment_points(result_no_brackets)
        self.assertEqual("[*]C(=O)c1c(NC(=O)c2cccc(S([*])(=O)=O)c2)sc([*])c1C", result)

    def test_add_brackets_to_attachment_points(self):
        result = self._attachment_points.add_brackets_to_attachment_points(self.decorations_A)
        self.assertEqual('[*]OCC|[*]N1CCOCC1|[*]C', result)

    def test_add_first_attachment_point_number(self):
        result = self._attachment_points.add_first_attachment_point_number('[*]OCC[*]c1ccccc1', 0)
        self.assertEqual('[*:0]OCC[*]c1ccccc1', result)

    def test_get_attachment_points_for_molecule(self):
        molecule = self.chemistry.smile_to_mol(self.labeled_scaffold_A)
        result = self._attachment_points.get_attachment_points_for_molecule(molecule)
        self.assertEqual([0, 2, 1], result)