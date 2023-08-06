import unittest

from reinvent_chemistry import Conversions, MolecularTransformations
from reinvent_chemistry.library_design import AttachmentPoints
from reinvent_chemistry.library_design.fragment_reactions import FragmentReactions


class TestMolecularTransformations(unittest.TestCase):

    def setUp(self):
        self._transformation = MolecularTransformations()
        self._attachments = AttachmentPoints()
        self.chemistry = Conversions()
        self.reactions = FragmentReactions()
        self.decorations_A = '*OCC|*N1CCOCC1|*C'
        self.expected_results = "CCOC(=O)c1c(NC(=O)c2cccc(S(=O)(=O)N3CCOCC3)c2)sc(C)c1C"
        self.labeled_scaffold_A = "[*:0]C(=O)c1c(NC(=O)c2cccc(S(=O)(=O)[*:2])c2)sc([*:1])c1C"

    def test_join_labeled_scaffold_and_decorations(self):
        molecule = self._transformation.join_scaffolds_and_decorations(self.labeled_scaffold_A, self.decorations_A)
        complete_smile = self.chemistry.mol_to_smiles(molecule)

        self.assertEqual(self.expected_results, complete_smile)

    def test_get_attachment_points(self):
        result = self._attachments.get_attachment_points(self.labeled_scaffold_A)
        self.assertEqual([0, 2, 1], result)

    def test_add_attachment_point_numbers(self):
        relabeled = self._attachments.add_attachment_point_numbers(self.labeled_scaffold_A)
        result = self._attachments.get_attachment_points(relabeled)
        self.assertEqual([0, 1, 2], result)

    def test_remove_attachment_point_numbers(self):
        result = self._attachments.remove_attachment_point_numbers(self.labeled_scaffold_A)
        molecule = self._transformation.join_scaffolds_and_decorations(result, self.decorations_A)
        complete_smile = self.chemistry.mol_to_smiles(molecule)
        self.assertEqual(self.expected_results, complete_smile)
        self.assertEqual("[*]C(=O)c1c(NC(=O)c2cccc(S(=O)(=O)[*])c2)sc([*])c1C", result)

