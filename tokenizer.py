import sys
from collections import defaultdict
from create_trie import trie
from create_cost_matrix import cost_matrix

_BOS_ENTRY = ['BOS', 0, 0, 1, 'BOS']
_EOS_ENTRY = ['EOS', 0, 0, 1, 'EOS']


def common_prefix_search(trie, key):
    res = []
    if 'value' in trie:
        res += trie['value']
    if key:
        first, rest = key[0], key[1:]
        if first in trie:
            res += common_prefix_search(trie[first], rest)

    return res

def cost_minimum(left_node, right_node):
    id_pair = (left_node['entry'][1], right_node['entry'][1])
    return cost_matrix[id_pair] + right_node['entry'][2]

def forward(sentence):
    BOS_node = {'begin': -1, 'next': [], 'entry': _BOS_ENTRY, 'cost': sys.maxsize}
    end_node_list = defaultdict(list)
    end_node_list[0].append(BOS_node)

    for i in range(0, len(sentence) + 1):
        if i < len(sentence):
            common_prefix_search_results = common_prefix_search(trie, sentence[i:])
        else:
            common_prefix_search_results = [_EOS_ENTRY]

        for res in common_prefix_search_results:
            right_node = {'begin': i, 'next': [], 'entry': res, 'cost': 0}
            min_cost = -sys.maxsize
            min_left_nodes = []

            for left_node in end_node_list[i]:
                cost = left_node['cost'] + cost_minimum(left_node, right_node)

                if min_cost == -sys.maxsize or cost < min_cost:
                    min_cost = cost
                    min_left_nodes = [left_node]
                elif cost == min_cost:
                    min_left_nodes.append(left_node)

            if min_left_nodes:
                for left_node in min_left_nodes:
                    right_node['cost'] = min_cost
                    left_node['next'].append(right_node)

            end_nodes = end_node_list[i + res[3]]
            if not right_node in end_nodes:
                end_nodes.append(right_node)

    return BOS_node

def backward(node):
    results = []
    if node['entry'][0] == 'EOS':
        return [['EOS']]
    for next_node in node['next']:
        for res in backward(next_node):
            results.append([node['entry'][0]] + res)

    return results

def tokenize(sentence):
    lattice = forward(sentence)
    res = backward(lattice)

    return '\n'.join('/'.join(sentence[1: -1]) for sentence in res)
