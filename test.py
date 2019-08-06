from tokenizer import tokenize


print('このひとことで元気になった ==>')
print(tokenize('このひとことで元気になった'))
print()

print('私は東京工業大学修士一年の学生です ==>')
print(tokenize('私は東京工業大学修士一年の学生です'))
print()

print('これは辞書のみを利用したシンプルな形態素解析器です ==>')
print(tokenize('これは辞書のみを利用したシンプルな形態素解析器です'))
