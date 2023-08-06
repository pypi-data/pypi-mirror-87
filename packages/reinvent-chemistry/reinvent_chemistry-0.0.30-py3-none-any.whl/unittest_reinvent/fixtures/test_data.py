import numpy as np

SMILES_LIST = """
CC12NC1C1NCCCOC1C2N
CC1=COC2C3C(CN)C(=O)CC123
CC1Cc2c(cn3ncc(O)c23)O1
COC(=CCC(=O)O)C1CCCN1
CNC1(C)C2C(CN2C)C2(C)OC12
CCCCC1(N2CC2)C=COC1C
CCC=C1CCCC(=O)N1C=NN
C=C1C2NC3C(N)CC1(NC)CC23
CC1(O)C2NC2C23CC2CCNC13
CCC(C(C)OC)N(N)C(N)=O
C=NNC(C(CC)=NO)C(C)(C)C
C=CCCC(=C)C(=C)CC=O
CC=C(CO)C1CN(C=NOC)C1
C=C(OC)C1(OC)OCCN2CC21
CN=C(NOCC(N)=O)C1CCC1
C=C1CC(C)COCC(C)C(=C)O1
C=C1CNC2C(C1=O)C2(C)OC
CC(C)CCn1cc(CC=O)cn1
NS(=O)(=O)N1NCC2CN2C2CC21
NC(=O)C1C2C3CC3CC12O
CC(C)C(O)C1OCCC(=O)C1=O
C1=CC2C=CC(CC=NOCC2)O1
CC1CC2C(=NN1)C(C)CS2(=O)=O
C=C(CN1CC1)C(=C)C1CCN1C
CNC(=N)C1=CC(CNC=O)OC1
""".split("\n")

SMILES_LIST_2 = """
CCCCN(C(=O)CSc1nnc(-c2ccco2)n1C1CC1)c1c(N)n(Cc2ccccc2)c(=O)[nH]c1=O
C1(c2ccc(Br)cc2)CCN(Cc2c[nH]c3ccccc23)CC1
Cc1cccc(N=c2[nH]c(NCCCN3CCOCC3)c(N=c3cc[nH]c4cc(Cl)ccc34)s2)c1
CC(=O)NC1(C(=O)NC(CCCN=C(N)N)C(=O)NC(CC2CCC2)C(=O)O)C(C)CC(C)C1
O=C(c1cccnc1-c1ccsc1)N1CCC(N2C(=O)OCc3ccccc32)CC1
Cc1[nH]c2ccccc2c1Cc1cc(C(N)=NO)ccc1Cl
O=C(O)c1cccc(NCC2CCCCN2C(=O)Cc2ccc(Cl)c(Cl)c2)c1
O=C(NCCCC(CCCCN1CCC(c2ccccc2)CC1)NC1CCCC1)C1CCCO1
O=C(CCc1ccc(O)c(O)c1)NCC1CCN(Cc2ccccc2)CC1
Cc1ccc2c(c1)-c1cc(C(F)(F)C(F)(F)F)nn1CCO2
CC(NC(=O)Nc1ccccc1Br)C1CCN(C(=O)OCC(C)C)CC1
N=c1[nH]nc(CCCCCCc2n[nH]c(=Nc3ccccc3)s2)s1
O=C(CNC(=O)OCc1ccccc1)NC(Cc1ccc(Cl)cc1)C(=O)CN1CCN(c2ncccn2)CC1
NCCCN1N=C(CCC(=O)c2ccc(O)cc2)c2ccccc2N(Cc2ccc3cc4c(cc3c2)CCC4)C1=O
COC(=O)C=Cc1cc(Cl)ccc1OCc1cc(C)c(-c2ccccc2OC)n1C
Cc1ccc(CC(=O)Nc2ccc(NC(=O)C(C)Cc3ccccc3)cc2)cc1
Cc1ccc(S(=O)(=O)Oc2ccc(C=NNC(=O)CC[N+](=O)[O-])cc2)cc1
NC(=O)CC12CC3CC(CC(C3)C1)C2
COc1ccccc1C1C(C(C)=O)=C(C)N2CCSC21
COc1ccc(S(=O)(=O)N(CC(C)C)CC(O)C(Cc2ccccc2)NC(=O)C2CCOC2)cc1
CSc1cccc(N=c2[nH]c(-c3cccc(O)c3)cs2)c1
CN(N=Cc1ccccc1Cl)c1nc(=NCCCN=C(N)N)nc(N=c2cc[nH]cc2)[nH]1
C=C(C)CN1CC2(CCC(c3nnc(C)n4ccnc34)C2)CCCC1=O
CCCC(=O)OCCc1c2ccccc2cc2ccccc12
CN(C)C(=O)c1cc(N=c2nc(-c3cnc4ccccn34)c(Cl)c[nH]2)ccc1-c1cncs1
CC(NC(=O)Nc1ccccc1Br)C1CCN(C(=O)OCC(C)C)CC1
N=c1[nH]nc(CCCCCCc2n[nH]c(=Nc3ccccc3)s2)s1
O=C(CNC(=O)OCc1ccccc1)NC(Cc1ccc(Cl)cc1)C(=O)CN1CCN(c2ncccn2)CC1
NCCCN1N=C(CCC(=O)c2ccc(O)cc2)c2ccccc2N(Cc2ccc3cc4c(cc3c2)CCC4)C1=O
COC(=O)C=Cc1cc(Cl)ccc1OCc1cc(C)c(-c2ccccc2OC)n1C
Cc1ccc(CC(=O)Nc2ccc(NC(=O)C(C)Cc3ccccc3)cc2)cc1
Cc1ccc(S(=O)(=O)Oc2ccc(C=NNC(=O)CC[N+](=O)[O-])cc2)cc1
NC(=O)CC12CC3CC(CC(C3)C1)C2
COc1ccccc1C1C(C(C)=O)=C(C)N2CCSC21
COc1ccc(S(=O)(=O)N(CC(C)C)CC(O)C(Cc2ccccc2)NC(=O)C2CCOC2)cc1
CSc1cccc(N=c2[nH]c(-c3cccc(O)c3)cs2)c1
CN(N=Cc1ccccc1Cl)c1nc(=NCCCN=C(N)N)nc(N=c2cc[nH]cc2)[nH]1
C=C(C)CN1CC2(CCC(c3nnc(C)n4ccnc34)C2)CCCC1=O
CCCC(=O)OCCc1c2ccccc2cc2ccccc12
CN(C)C(=O)c1cc(N=c2nc(-c3cnc4ccccn34)c(Cl)c[nH]2)ccc1-c1cncs1
""".split("\n")

REP_SMILES_LIST = ["CCCCN(C(=O)CSc1nnc(-c2ccco2)n1C1CC1)c1c(N)n(Cc2ccccc2)c(=O)[nH]c1=O"] * 15 + [
    "C1(c2ccc(Br)cc2)CCN(Cc2c[nH]c3ccccc23)CC1"] * 10

INVALID_SMILES_LIST = ["INVALID"] * 25

LIKELIHOODLIST = np.array(
    [20.0, 20.0, 19.0, 19.0, 18.0, 18.0, 20.0, 21.0, 21.0, 20.0, 17.0, 16.0, 15.0, 14.0, 13.0, 12.0, 20.0, 21.0,
     22.0, 23.0, 24.0, 25.0, 26.0, 27.0, 20.0, 17.0, 16.0, 15.0, 14.0, 13.0, 12.0, 20.0, 21.0, 22.0, 23.0, 24.0,
     25.0, 26.0, 27.0, 20.0], dtype=np.float32)
REP_LIKELIHOOD = np.array(
    [15.0, 15.0, 15.0, 15.0, 15.0, 15.0, 15.0, 15.0, 15.0, 15.0, 15.0, 15.0, 15.0, 15.0, 15.0, 10.0, 10.0, 10.0,
     10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0], dtype=np.float32)

SIMPLE_TOKENS = {t: i for i, t in enumerate(['$', '^', '(', ')', '1', '2', '3', '=', 'C', 'N', 'O', 'S', 'c', 'n'])}


