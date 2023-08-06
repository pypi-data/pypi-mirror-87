from typing import List, Dict, Tuple

from rdkit.Chem import AllChem, Mol
from rdkit.Chem.Lipinski import RingCount
from rdkit.Chem.rdChemReactions import ChemicalReaction
from rdkit.Chem.rdchem import Atom, AtomKekulizeException
from rdkit.Chem.rdmolops import FragmentOnBonds, GetMolFrags

from reinvent_chemistry import Conversions
from reinvent_chemistry.library_design.dtos import ReactionDTO
from reinvent_chemistry.tokens import TransformationTokens


class Reactions:
    def __init__(self):
        self._conversions = Conversions()
        self._tokens = TransformationTokens()

    def create_reactions_from_smarts(self, smarts: List[str]) -> List[ChemicalReaction]:
        reactions = [AllChem.ReactionFromSmarts(smirks) for smirks in smarts]
        return reactions

    def create_reaction_from_smirk(self, smirks: str) -> ReactionDTO:
        reaction = ReactionDTO(smirks, AllChem.ReactionFromSmarts(smirks))
        return reaction

    def create_reactions_from_smirks(self, smirks: List[str]) -> List[ReactionDTO]:
        reactions = [self.create_reaction_from_smirk(smirk) for smirk in smirks]
        return reactions

    def slice_molecule_to_fragments(self, molecule: Mol, chemical_reactions: List[ChemicalReaction]) -> List[Tuple[Mol]]:
        """
        This method applies a list of chemical reactions on a molecule and
        decomposes the input molecule to complementary fragments.
        :param molecule:
        :param chemical_reactions:
        :return: Different slicing combinations are returned.
        """
        neighbor_map = self._create_neighbor_map(molecule)
        reagent_pairs = self.apply_reactions_on_molecule(molecule, chemical_reactions)
        # for pair in reagent_pairs:
        #     print(len(pair))
        #     for reagent in pair:
        #         smiles = self._conversions.mol_to_smiles(reagent)
        #         print(smiles)
        #     print('*'*80)
        all_fragments = []
        try:
            for reagent_pair in reagent_pairs:
                list_of_atom_pairs = self._find_bonds_targeted_by_reaction(reagent_pair, neighbor_map)
                bonds_to_cut = self._find_indices_of_target_bonds(molecule, list_of_atom_pairs)

                if len(bonds_to_cut) == 1:
                    reaction_fragments = self._create_fragments(molecule, bonds_to_cut)
                    all_fragments.append(reaction_fragments)
        except AtomKekulizeException as ex:
            print(f"failed scaffold: {self._conversions.mol_to_smiles(molecule)}")
            raise(ex)
        return all_fragments

    def apply_reactions_on_molecule(self, molecule: Mol, reactions: List[ChemicalReaction]) -> List[Tuple[Mol]]:
        """Build list of possible splits of a molecule given multiple reactions."""
        reactants = []
        for reaction in reactions:
            outcomes = reaction.RunReactant(molecule, 0)
            acceptable_pairs = self._filter_pairs_with_no_ring_count_change(molecule, outcomes)
            reactants.extend(acceptable_pairs)
        return reactants

    def _filter_pairs_with_no_ring_count_change(self, molecule: Mol, reagent_pair: Tuple[Tuple[Mol]]) -> List[Tuple[Mol]]:
        molecule_rings = RingCount(molecule)
        acceptable_pairs = []
        for pair in reagent_pair:
            if not self._detect_ring_break(molecule_rings, pair):
                acceptable_pairs.append(pair)
        return acceptable_pairs

    def _detect_ring_break(self, molecule_ring_count: int, pair: Tuple[Mol]) -> bool:
        reagent_rings = 0
        for reagent in pair:
            reagent_smiles = self._conversions.mol_to_smiles(reagent)
            reagent_mol = self._conversions.smile_to_mol(reagent_smiles)
            try:
                reagent_rings = reagent_rings + RingCount(reagent_mol)
            except:
                return True
        return molecule_ring_count != reagent_rings

    def apply_reaction_on_molecule(self, molecule: Mol, reaction: ChemicalReaction) -> List[Tuple[Mol]]:
        """Build list of possible splits of a molecule given a single reaction."""
        reactants = reaction.RunReactant(molecule, 0)
        return list(reactants)

    def _get_neighbor_ids_for_atom(self, atom: Atom) -> List[int]:
        neighbours = atom.GetNeighbors()
        indices = [neighbor.GetIdx() for neighbor in neighbours]
        neighbor_indxs = [idx for idx in indices]
        return neighbor_indxs

    def _create_neighbor_map(self, molecule: Mol) -> Dict[int, List[int]]:
        atoms = molecule.GetAtoms()
        interaction_map = {atom.GetIdx(): self._get_neighbor_ids_for_atom(atom) for atom in atoms}
        return interaction_map

    def _create_neighbor_map_for_reactant(self, reactant: Mol) -> Dict[int, List[int]]:
        interaction_map = {}

        for atom in reactant.GetAtoms():
            if atom.HasProp("react_atom_idx"):
                neighbor_indxs = self._get_original_ids_from_reactant(atom)
                interaction_map[int(atom.GetProp("react_atom_idx"))] = neighbor_indxs

        return interaction_map

    def _get_original_ids_from_reactant(self, atom: Atom) -> List[int]:
        neighbours = atom.GetNeighbors()
        indices = [int(neighbor.GetProp("react_atom_idx")) for neighbor in neighbours if
                   neighbor.HasProp("react_atom_idx")]
        neighbor_indxs = [idx for idx in indices]

        return neighbor_indxs

    def _indentify_mismatching_indices(self, original: Dict, derived: Dict) -> List[Tuple]:

        def is_a_mismatch(original_points: [], derived_points: []):
            original_points.sort()
            derived_points.sort()
            return original_points != derived_points

        mismatching_indices = []

        for key in derived.keys():
            if is_a_mismatch(original.get(key), derived.get(key)):
                differences = list(set(original.get(key)) - set(derived.get(key)))
                for difference in differences:
                    pair = (key, difference)
                    mismatching_indices.append(tuple(sorted(pair)))

        return mismatching_indices

    def _find_indices_of_target_bonds(self, molecule: Mol, list_of_atom_pairs: List[Tuple[int]]) -> List[int]:
        list_of_atom_pairs = list(set(list_of_atom_pairs))
        bonds_to_cut = [molecule.GetBondBetweenAtoms(pair[0], pair[1]).GetIdx() for pair in list_of_atom_pairs]
        return bonds_to_cut

    def _create_fragments(self, molecule: Mol, bonds_to_cut: List[int]) -> Tuple[Mol]:

        attachment_point_idxs = [(i, i) for i in range(len(bonds_to_cut))]
        cut_mol = FragmentOnBonds(molecule, bondIndices=bonds_to_cut, dummyLabels=attachment_point_idxs)

        for atom in cut_mol.GetAtoms():
            if atom.GetSymbol() == self._tokens.ATTACHMENT_POINT_TOKEN:
                num = atom.GetIsotope()
                atom.SetIsotope(0)
                atom.SetProp("molAtomMapNumber", str(num))
        cut_mol.UpdatePropertyCache()
        fragments = GetMolFrags(cut_mol, asMols=True, sanitizeFrags=True)

        return fragments

    def _find_bonds_targeted_by_reaction(self, reagent_pair: Tuple[Mol], neighbor_map: Dict) -> List[Tuple[int]]:
        atom_pairs = []
        for reagent in reagent_pair:
            reactant_map = self._create_neighbor_map_for_reactant(reagent)
            atom_pair = self._indentify_mismatching_indices(neighbor_map, reactant_map)
            atom_pairs.extend(atom_pair)
        return atom_pairs
