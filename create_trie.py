import os
import glob
import pickle
import logging
from collections import namedtuple


TRIE_PATH = 'trie.pkl'
DICT_CSV_PATH = 'dict/*.csv'


logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
logging.root.setLevel(level=logging.INFO)


entry = namedtuple('Entry', ['surface', 'id', 'cost', 'length'])


def insert(trie, key, value):
    if key:
        first, rest = key[0], key[1:]
        if first not in trie:
            trie[first] = {}
        insert(trie[first], rest, value)
    else:
        if not 'value' in trie:
            trie['value'] = []
        trie['value'].append(value)


if os.path.exists(TRIE_PATH):
    logging.log(logging.INFO, 'Start loading preprocessed trie ===>\n')
    with open(TRIE_PATH, 'rb') as f:
        trie = pickle.load(f)
    logging.log(logging.INFO, f'Preprocessed trie loaded from {TRIE_PATH}')
else:
    logging.log(logging.INFO, 'Start generateing dict_entries from dict/*.csv ===>\n')
    dict_entries = []
    df_path_list = glob.glob(DICT_CSV_PATH)
    for file_path in df_path_list:
        with open(file_path, 'r') as f:
            data = f.read().split('\n')
        for line in data:
            try:
                surface, id, _, cost, *feature = line.split(',')
                dict_entries.append(entry(surface, int(id), int(cost), len(surface)))
            except:
                ...
        logging.log(logging.INFO, f'{file_path} handled')

    dict_entries = sorted(dict_entries, key=lambda x: x.surface)

    trie = {}

    for e in dict_entries:
        insert(trie, e.surface, [e.surface, e.id, e.cost, e.length])

    with open(TRIE_PATH, 'wb') as f:
        pickle.dump(trie, f)
    logging.log(logging.INFO, f'Trie generated in {TRIE_PATH}')
