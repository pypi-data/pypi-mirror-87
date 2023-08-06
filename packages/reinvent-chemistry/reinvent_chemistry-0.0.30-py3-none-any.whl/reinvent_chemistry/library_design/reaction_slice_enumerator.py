from typing import List, Tuple, Set

from rdkit.Chem.rdChemReactions import ChemicalReaction
from rdkit.Chem.rdchem import Mol

from reinvent_chemistry import TransformationTokens
from reinvent_chemistry.library_design import FragmentFilter
from reinvent_chemistry.library_design.dtos import FilteringConditionDTO
from reinvent_chemistry.library_design.obsolete.reactions import Reactions
from reinvent_chemistry.library_design.obsolete.sliced_molecule import SlicedMol


class ReactionSliceEnumerator:

    def __init__(self, chemical_reactions: List[ChemicalReaction],
                 scaffold_conditions: List[FilteringConditionDTO],
                 decoration_conditions: List[FilteringConditionDTO]):
        """
        Class to enumerate slicings given certain conditions.
        :param chemical_reactions: A list of ChemicalReaction objects.
        :param scaffold_conditions: Conditions to use when filtering scaffolds obtained from slicing molecules (see FragmentFilter).
        :param decoration_conditions: Conditions to use when filtering decorations obtained from slicing molecules.
        """
        self._tockens = TransformationTokens()
        self._chemical_reactions = chemical_reactions
        self._scaffold_filter = FragmentFilter(scaffold_conditions)
        self._decoration_filter = FragmentFilter(decoration_conditions)
        self._reactions = Reactions()

    def enumerate(self, molecule: Mol, cuts: int) -> List[SlicedMol]:
        """
        Enumerates all possible combination of slicings of a molecule given a number of cuts.
        :param molecule: A mol object with the molecule to slice.
        :param cuts: The number of cuts to perform.
        :return : A list with all the possible (scaffold, decorations) pairs as SlicedMol objects.
        """
        sliced_mols = set()
        for cut in range(1, cuts + 1):
            if cut == 1:
                fragment_pairs = self._reactions.slice_molecule_to_fragments(molecule, self._chemical_reactions)
                for pair in fragment_pairs:
                    for indx, _ in enumerate(pair):
                        decorations = self._select_all_except(pair, indx)
                        sliced_mols.add(SlicedMol(pair[indx], decorations))
            else:
                for slice in sliced_mols:
                    to_add = self._scaffold_slicing(slice, cut)
                    sliced_mols = sliced_mols.union(to_add)

        return list(filter(self._filter, sliced_mols))

    def _scaffold_slicing(self, slice: SlicedMol, cut: int) -> Set[SlicedMol]:
        to_add = set()
        if slice.decorations_count() == cut - 1:
            fragment_pairs = self._reactions.slice_molecule_to_fragments(slice.scaffold, self._chemical_reactions)
            for pair in fragment_pairs:
                sliced_mol = self._identify_scaffold(pair, cut, slice)
                if sliced_mol:
                    to_add.add(sliced_mol)
        return to_add

    def _select_all_except(self, fragments: Tuple[Mol], to_exclude: int) -> List:
        return [fragment for indx, fragment in enumerate(fragments) if indx != to_exclude]

    def _filter(self, sliced_mol: SlicedMol) -> bool:
        return self._scaffold_filter.filter(sliced_mol.scaffold) \
               and all(self._decoration_filter.filter(dec) for dec in sliced_mol.decorations.values())

    def _identify_scaffold(self, pair: Tuple[Mol], cuts: int, original_sliced_mol: SlicedMol) -> SlicedMol:
        decorations = []
        scaffold = None
        sliced_mol = None
        for frag in pair:
            num_att = len(
                [atom for atom in frag.GetAtoms() if atom.GetSymbol() == self._tockens.ATTACHMENT_POINT_TOKEN])
            # detect whether there is one fragment with as many attachment points as cuts (scaffold)
            # the rest are decorations
            if num_att == cuts and not scaffold:
                scaffold = frag
            else:
                decorations.append(frag)
        if scaffold:
            sliced_mol = SlicedMol(scaffold, decorations)
            sliced_mol.add_decorations(original_sliced_mol.decorations)
        return sliced_mol
