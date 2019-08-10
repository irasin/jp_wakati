import MeCab


m = MeCab.Tagger()


def tokenize_mecab(sentence):
    res = m.parseToNode(sentence).next
    out = []
    while res:
        out.append(res.surface)
        res = res.next
    return '/'.join(out[:-1])



print('このひとことで元気になった ==>')
print(tokenize_mecab('このひとことで元気になった'))
print()

print('私は東京工業大学修士一年の学生です ==>')
print(tokenize_mecab('私は東京工業大学修士一年の学生です'))
print()

print('これは辞書のみを利用したシンプルな形態素解析器です ==>')
print(tokenize_mecab('これは辞書のみを利用したシンプルな形態素解析器です'))
print()

print('君の膵臓をたべたい ==>')
print(tokenize_mecab('君の膵臓をたべたい'))
print()
