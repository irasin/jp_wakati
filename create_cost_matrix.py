import os
import pickle
import logging
from collections import namedtuple


COST_MATRIX_PATH = 'cost_matrix.pkl' # コスト表の保存先
RAW_COST_MATRIX_PATH = 'dict/matrix.def' # コストを記録したソースファイル


logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
logging.root.setLevel(level=logging.INFO)


if os.path.exists(COST_MATRIX_PATH):
    # 構築済みのコスト表を読み込む
    logging.log(logging.INFO, 'Start loading preprocessed cost matrix ===>\n')
    with open(COST_MATRIX_PATH, 'rb') as f:
        cost_matrix = pickle.load(f)
    logging.log(logging.INFO, f'Preprocessed cost matrix loaded from {COST_MATRIX_PATH}\n')
else:
    # コスト表を構築する
    logging.log(logging.INFO, f'Start generateing cost matrix from {RAW_COST_MATRIX_PATH} ===>\n')
    with open(RAW_COST_MATRIX_PATH, encoding='utf-8') as f:
        data = f.read().split('\n')

    # コスト表 (シンプルなdictで実装する)
    cost_matrix = {}

    # ソースファイル各行を読み込み、単語ペアをキーとして、cost_matrixにインサートする
    for pair in data:
        try:
            left, right, cost = (int(i) for i in pair.split())
            cost_matrix[(left, right)] = cost
        except:
            ...

    # 構築済みのコスト表を保存する
    with open(COST_MATRIX_PATH, 'wb') as f:
        pickle.dump(cost_matrix, f)
    logging.log(logging.INFO, f'Cost matrix generated in {COST_MATRIX_PATH}\n')
