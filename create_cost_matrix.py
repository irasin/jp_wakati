import os
import pickle
import logging
from collections import namedtuple


COST_MATRIX_PATH = 'cost_matrix.pkl'
RAW_COST_MATRIX_PATH = 'dict/matrix.def'


logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
logging.root.setLevel(level=logging.INFO)


if os.path.exists(COST_MATRIX_PATH):
    logging.log(logging.INFO, 'Start loading preprocessed cost matrix ===>\n')
    with open(COST_MATRIX_PATH, 'rb') as f:
        cost_matrix = pickle.load(f)
    logging.log(logging.INFO, f'Preprocessed cost matrix loaded from {COST_MATRIX_PATH}')
else:
    logging.log(logging.INFO, f'Start generateing cost matrix from {RAW_COST_MATRIX_PATH} ===>\n')
    with open(RAW_COST_MATRIX_PATH) as f:
        data = f.read().split('\n')

    cost_matrix = {}
    for pair in data:
        try:
            left, right, cost = (int(i) for i in pair.split())
            cost_matrix[(left, right)] = cost
        except:
            ...

    with open(COST_MATRIX_PATH, 'wb') as f:
        pickle.dump(cost_matrix, f)
    logging.log(logging.INFO, f'Cost matrix generated in {COST_MATRIX_PATH}')
