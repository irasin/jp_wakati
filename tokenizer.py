import sys
from collections import defaultdict
from create_trie import trie
from create_cost_matrix import cost_matrix

# 特殊なエントリーとして、BOSとEOSを定義する
# [表層形、ID、コスト、長さ]の形式
# BOS: Begin Of Sentence
# EOS: End Of Sentence
_BOS_ENTRY = ['BOS', 0, 0, 1]
_EOS_ENTRY = ['EOS', 0, 0, 1]


# 共通接頭辞検索
# いわゆる辞書引くの関数
# 検索ワードの長さに比例した計算量なので、非常に早い
# 例えば、くるまを検索すると、下記のようになる
# >>> res = common_prefix_search(trie, 'くるま')
# >>> for i in res:
# ...     print(i)
# ...
# ['く', 11, 9106, 1]
# ['く', 776, 11108, 1]
# ['く', 993, 13513, 1]
# ['く', 565, 11108, 1]
# ['く', 899, 11782, 1]
# ['くる', 772, 9531, 2]
# ['くる', 563, 9531, 2]
# ['くる', 897, 10291, 2]
# ['くるま', 764, 8390, 3]
# ['くるま', 776, 9281, 3]
# >>>
def common_prefix_search(trie, key):
    res = []
    if 'value' in trie:
        res += trie['value']
    if key:
        first, rest = key[0], key[1:]
        if first in trie:
            res += common_prefix_search(trie[first], rest)

    return res

# ビタビアルゴリズムで使用する接続コストを計算する関数
# 左ノードと右ノードを受け取り、ノード間の接続コストと右ノードの単語生起コストの和を返す
def connect_cost(left_node, right_node):
    id_pair = (left_node['entry'][1], right_node['entry'][1])
    return cost_matrix[id_pair] + right_node['entry'][2]

# ビタビアルゴリズムのフォワード計算
# 順方向にラティスを構築する
def forward(sentence):
    # ラティスの最初にBOS_nodeを定義する
    # Nodeはdictとして定義、下記四つのキーを持つ
    # {'begin': i, 'next': [], 'entry': [], 'cost': j}
    # begin: i番目の位置/BOS_nodeからの距離
    # next: 次に接続ノードのリスト
    # entry: 単語エントリー
    # cost: BOS_nodeから現在ノードまでのパスの最小コスト
    BOS_node = {'begin': -1, 'next': [], 'entry': _BOS_ENTRY, 'cost': 0}

    # end_node_listは各位置に終わるノードのリストの結果を保存するdictである
    end_node_list = defaultdict(list)
    # 初期化として、最初にBOS_nodeを入れる
    end_node_list[0].append(BOS_node)

    # 入力文の先頭から最後までループ
    for i in range(0, len(sentence) + 1):
        # 文の最後じゃない場合、共通接頭辞検索を行う
        if i < len(sentence):
            common_prefix_search_results = common_prefix_search(trie, sentence[i:])
        # 文の最後まで行ったら、[_EOS_ENTRY]を入れる
        else:
            common_prefix_search_results = [_EOS_ENTRY]

        # 共通接頭辞検索の結果の単語を解析する
        for res in common_prefix_search_results:
            # 各右ノードのパスは無限大(システム最大値)で初期化する
            right_node = {'begin': i, 'next': [], 'entry': res, 'cost': sys.maxsize}
            # 最小パスコストをマイナス無限大で初期化する
            min_cost = -sys.maxsize
            # 最小パスコストを取得した左ノードのリスト
            min_left_nodes = []

            # 計算済みのi番目で終わる左ノードから、新しい右ノードへのコスト最小のパスを決定
            # 最小パスコストを取得した左ノードをmin_left_nodesに保存
            for left_node in end_node_list[i]:
                cost = left_node['cost'] + connect_cost(left_node, right_node)

                if min_cost == -sys.maxsize or cost < min_cost:
                    min_cost = cost
                    min_left_nodes = [left_node]
                elif cost == min_cost:
                    min_left_nodes.append(left_node)

            # min_left_nodesが空でなければ
            # 各右ノードの'cost'の値を最小パスコストに変更する
            # それぞれの左ノードの'next'フィルドに現在の右ノードの情報を追加する
            if min_left_nodes:
                for left_node in min_left_nodes:
                    right_node['cost'] = min_cost
                    left_node['next'].append(right_node)

            # end_node_listに現在の右ノードが存在するかどうかを確認する
            # なければ、end_node_listに追加する
            end_nodes = end_node_list[i + res[3]]
            if not right_node in end_nodes:
                end_nodes.append(right_node)

    # 解析終了後、BOS_nodeがラティス構造となり、これを返せば良い
    return BOS_node

# ビタビアルゴリズムのバックワード計算
# 逆方向に構築済みのラティスから、最小コストのパスを返す
def backward(node):
    results = []
    if node['entry'][0] == 'EOS':
        return [['EOS']]
    for next_node in node['next']:
        for res in backward(next_node):
            results.append([node['entry'][0]] + res)

    return results

# ビタビアルゴリズムを用いて形態素解析を行う関数
def tokenize(sentence):
    lattice = forward(sentence)
    res = backward(lattice)
    res = set(tuple(i) for i in res)

    return '\n'.join('/'.join(sentence[1: -1]) for sentence in res)

