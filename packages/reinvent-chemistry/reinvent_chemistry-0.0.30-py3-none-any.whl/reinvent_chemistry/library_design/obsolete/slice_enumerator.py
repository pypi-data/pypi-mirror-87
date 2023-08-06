import itertools
from typing import List

from rdkit.Chem.rdchem import Mol
from rdkit.Chem.rdmolops import GetMolFrags, FragmentOnBonds

from reinvent_chemistry import TransformationTokens
from reinvent_chemistry.library_design import FragmentFilter
from reinvent_chemistry.library_design.dtos import FilteringConditionDTO
from reinvent_chemistry.library_design.obsolete.sliced_molecule import SlicedMol


#TODO: Maybe Remove - This is Obsolete
class SliceEnumerator:

    def __init__(self, slice_smarts: List[Mol], scaffold_conditions: List[FilteringConditionDTO] = None,
                 decoration_conditions: List[FilteringConditionDTO] = None):
        """
        Class to enumerate slicings given certain conditions.
        :param slice_smarts: A list of SMARTS rules to cut molecules (see SLICE_SMARTS for an example).
        :param scaffold_conditions: Conditions to use when filtering scaffolds obtained from slicing molecules (see FragmentFilter).
        :param decoration_conditions: Conditions to use when filtering decorations obtained from slicing molecules.
        """
        self._tockens = TransformationTokens()
        self._slice_smarts = slice_smarts
        self._scaffold_filter = FragmentFilter(scaffold_conditions)
        self._decoration_filter = FragmentFilter(decoration_conditions)

    def count(self, mol: Mol):
        """
        Count the number of possible slicings in a given molecule.
        :param mol: Molecule to check.
        :return : An integer with the number of possible cuts.
        """
        return len(self._get_matches(mol))

    def enumerate(self, mol: Mol, cuts):
        """
        Enumerates all possible combination of slicings of a molecule given a number of cuts.
        :param mol: A mol object with the molecule to slice.
        :param cuts: The number of cuts to perform.
        :return : A list with all the possible (scaffold, decorations) pairs as SlicedMol objects.
        """
        matches = self._get_matches(mol)
        sliced_mols = set()
        for atom_pairs_to_cut in itertools.combinations(matches, cuts):
            to_cut_bonds = list(sorted(mol.GetBondBetweenAtoms(aidx, oaidx).GetIdx()
                                       for aidx, oaidx in atom_pairs_to_cut))
            attachment_point_idxs = [(i, i) for i in range(len(to_cut_bonds))]
            cut_mol = FragmentOnBonds(mol, bondIndices=to_cut_bonds, dummyLabels=attachment_point_idxs)
            for atom in cut_mol.GetAtoms():
                if atom.GetSymbol() == self._tockens.ATTACHMENT_POINT_TOKEN:
                    num = atom.GetIsotope()
                    atom.SetIsotope(0)
                    atom.SetProp("molAtomMapNumber", str(num))

            cut_mol.UpdatePropertyCache()
            fragments = GetMolFrags(cut_mol, asMols=True, sanitizeFrags=True)

            # detect whether there is one fragment with as many attachment points as cuts (scaffold)
            # the rest are decorations
            if cuts == 1:
                sliced_mols.add(SlicedMol(fragments[0], [fragments[1]]))
                sliced_mols.add(SlicedMol(fragments[1], [fragments[0]]))
            else:
                scaffold = None
                decorations = []
                for frag in fragments:
                    num_att = len(
                        [atom for atom in frag.GetAtoms() if atom.GetSymbol() == self._tockens.ATTACHMENT_POINT_TOKEN])
                    if num_att == cuts and not scaffold:
                        scaffold = frag
                    else:
                        decorations.append(frag)
                if scaffold:
                    sliced_mols.add(SlicedMol(scaffold, decorations))

        return list(filter(self._filter, sliced_mols))

    def _filter(self, sliced_mol):
        return self._scaffold_filter.filter(sliced_mol.scaffold) \
               and all(self._decoration_filter.filter(dec) for dec in sliced_mol.decorations.values())

    def _get_matches(self, mol: Mol):
        matches = set()
        for smarts in self._slice_smarts:
            matches |= set(tuple(sorted(match)) for match in mol.GetSubstructMatches(smarts))
        return list(matches)
