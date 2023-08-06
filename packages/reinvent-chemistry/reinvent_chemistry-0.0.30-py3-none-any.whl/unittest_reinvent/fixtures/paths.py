import os
import json

project_root = os.path.dirname(__file__)
with open(os.path.join(project_root, '../../configs/config.json'), 'r') as f:
    config = json.load(f)

MAIN_TEST_PATH = config["MAIN_TEST_PATH"]
ROCS_SIMILARITY_TEST_DATA = "/projects/mai/software/reinvent_data/non_user/test_data/datasets/reference.sdf"
ROCS_MULTI_SIMILARITY_TEST_DATA = "/projects/mai/software/reinvent_data/non_user/test_data/datasets/reference_multiple_mols.sdf"
ROCS_SHAPE_QUERY = "/projects/mai/software/reinvent_data/non_user/test_data/datasets/shape_query.sq"
ROCS_SHAPE_QUERY_2 = "/projects/mai/software/reinvent_data/non_user/test_data/datasets/negative_shape_query.sq"
ROCS_SHAPE_QUERY_3 = "/projects/mai/software/reinvent_data/non_user/test_data/datasets/rocs_bug.sq"
ROCS_SHAPE_QUERY_CFF = "/projects/mai/software/reinvent_data/non_user/test_data/datasets/rocs_phA_rings_only_mod.sq"
ROCS_SHAPE_QUERY_BATCH = '/projects/mai/software/reinvent_data/non_user/test_data/datasets/batch_shape_query.sq'
ROCS_CUSTOM_CFF = "/projects/mai/software/reinvent_data/non_user/test_data/datasets/implicit_MD_mod.cff"
SCIKIT_REGRESSION_PATH = "/projects/mai/software/reinvent_data/non_user/test_data/predictive_models/GLK_svm_ecfp6c_reg_190122.pkl"
SCIKIT_MODEL_PATH_CDK9 = "/projects/mai/software/reinvent_data/non_user/test_data/predictive_models/CDK9_best.pkl"
ACTIVITY_CLASSIFICATION = "/projects/mai/software/reinvent_data/non_user/test_data/predictive_models/MAT2A_svm_ecfp6_c_class.pkl"
PRIOR_PATH = "/projects/mai/software/reinvent_data/non_user/test_data/agents/isac_diverse/Prior.ckpt"
SMILES_SET_PATH = "/projects/mai/software/reinvent_data/non_user/test_data/datasets/test_set.smi"
RANDOM_PRIOR_PATH = "/projects/mai/software/reinvent_data/non_user/test_data/agents/chembl/random.prior"
CANNONICAL_PRIOR_PATH = "/projects/mai/software/reinvent_data/non_user/test_data/agents/chembl/canonical.prior"
SAS_MODEL_PATH = "/projects/mai/software/reinvent_data/non_user/test_data/predictive_models/SA_score_prediction.pkl"

# component specific
AZDOCK_ENV_PATH = config["COMPONENT_SPECIFIC"]["AZDOCK"]["AZDOCK_ENV_PATH"]
AZDOCK_DOCKER_SCRIPT_PATH = config["COMPONENT_SPECIFIC"]["AZDOCK"]["AZDOCK_DOCKER_SCRIPT_PATH"]
AZDOCK_DEBUG = config["COMPONENT_SPECIFIC"]["AZDOCK"]["AZDOCK_DEBUG"]
AZDOCK_UNITTEST_JSON = project_root + "/../scoring_tests/unittest_data/azdock_OpenEye.json"
AZDOCK_UNITTEST_OE_RECEPTOR_PATH = project_root + "/../scoring_tests/unittest_data/azdock_OpenEye_receptor.oeb"
AZDOCK_UNITTEST_REFERENCE_LIGAND_DPATH = project_root + "/../scoring_tests/unittest_data/azdock_ligand_PU8.sdf"
