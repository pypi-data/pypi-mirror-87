from typing import List

from rdkit.Chem.rdchem import Mol
from rdkit.Chem.rdmolfiles import MolFromSmarts

from reinvent_chemistry.library_design.enums import SliceTypeEnum


class SliceRules:
    def __init__(self):
        self._slice_types = SliceTypeEnum()
        self._rules = {
            self._slice_types.COMPLETE: [
                "[*]!@-[*]"
            ],
            self._slice_types.RECAP: [
                "[C;$(C=O)]!@-N",  # amides and urea
                "[C;$(C=O)]!@-O",  # esters
                "C!@-[N;!$(NC=O)]",  # amines
                "C!@-[O;!$(NC=O)]",  # ether
                "[CX3]!@=[CX3]",  # olefin
                "[N+X4]!@-C",  # quaternary nitrogen
                "n!@-C",  # aromatic N - aliphatic C
                "[$([NR][CR]=O)]!@-C",  # lactam nitrogen - aliphatic carbon
                "c!@-c",  # aromatic C - aromatic C
                "N!@-[$(S(=O)=O)]"  # sulphonamides
            ]
        }

    def get_smarts(self, slice_type: str) -> List[str]:
        return self._rules.get(slice_type)

    def get_smarts_as_mols(self, slice_type: str) -> List[Mol]:
        smarts = self.get_smarts(slice_type)
        mols = [MolFromSmarts(smart) for smart in smarts]
        return mols
