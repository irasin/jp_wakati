# 日本語分かち書き

このrepoはpythonを用いて日本語の分かち書きを行うビタビアルゴリズム およびMecabの利用方法を説明する。

本repoの構成は以下のようである。

```
├ README.md .. 説明
│
├ dict ..単語辞書、ID、コストの定義ファイル
│
├ create_cost_matrix.py ..単語連接コスト表を生成するファイル
│
├ create_trie.py ..トライ木を生成するファイル
│
├ tokenize.py ..ビタビアルゴリズムを実装するファイル
│
├ test.py ..分かち書きの実行例
|
├ test_mecab.py ..MeCabを用いた分かち書きの実行例
```

------

## Pythonで分かち書き

------

### Requirement

Python3.6+ (miniconda/anaconda recommended!)

### Usage

1. このrepoをローカルにcloneまたはdownloadする

```
git clone https://github.com/irasin/jp_wakati
cd jp_wakati
```

2. サンプル`test.py`を実行する

```bash
python test.py
```

3. MeCabをインストールできたら、MeCabの実行例`test_mecab.py`を実行する

```bash
python test_mecab.py
```
MeCabのインストールは一番下を参照

### データの説明

`dict/*.csv`は品詞ごとに単語をまとめたipadic辞書である。

具体的に、各単語は以下のような形式で表現される。

```
表層形,左文脈ID,右文脈ID,コスト,品詞,品詞細分類1,品詞細分類2,品詞細分類3,活用型,活用形,原形,読み,発音
```

例として、以下のようになっている。

```
いそがしい,120,120,6078,形容詞,自立,*,*,形容詞・イ段,基本形,いそがしい,イソガシイ,イソガシイ
いそがし,128,128,6080,形容詞,自立,*,*,形容詞・イ段,文語基本形,いそがしい,イソガシ,イソガシ
いそがしから,136,136,6079,形容詞,自立,*,*,形容詞・イ段,未然ヌ接続,いそがしい,イソガシカラ,イソガシカラ
いそがしかろ,132,132,6079,形容詞,自立,*,*,形容詞・イ段,未然ウ接続,いそがしい,イソガシカロ,イソガシカロ
いそがしかっ,148,148,6078,形容詞,自立,*,*,形容詞・イ段,連用タ接続,いそがしい,イソガシカッ,イソガシカッ
いそがしく,152,152,6078,形容詞,自立,*,*,形容詞・イ段,連用テ接続,いそがしい,イソガシク,イソガシク
いそがしくっ,152,152,6079,形容詞,自立,*,*,形容詞・イ段,連用テ接続,いそがしい,イソガシクッ,イソガシクッ
いそがしゅう,144,144,6079,形容詞,自立,*,*,形容詞・イ段,連用ゴザイ接続,いそがしい,イソガシュウ,イソガシュウ
いそがしゅぅ,144,144,6079,形容詞,自立,*,*,形容詞・イ段,連用ゴザイ接続,いそがしい,イソガシュゥ,イソガシュゥ
いそがしき,124,124,6079,形容詞,自立,*,*,形容詞・イ段,体言接続,いそがしい,イソガシキ,イソガシキ
いそがしけれ,108,108,6079,形容詞,自立,*,*,形容詞・イ段,仮定形,いそがしい,イソガシケレ,イソガシケレ
いそがしかれ,140,140,6079,形容詞,自立,*,*,形容詞・イ段,命令ｅ,いそがしい,イソガシカレ,イソガシカレ
いそがしけりゃ,112,112,6079,形容詞,自立,*,*,形容詞・イ段,仮定縮約１,いそがしい,イソガシケリャ,イソガシケリャ
いそがしきゃ,116,116,6079,形容詞,自立,*,*,形容詞・イ段,仮定縮約２,いそがしい,イソガシキャ,イソガシキャ
いそがし,104,104,6080,形容詞,自立,*,*,形容詞・イ段,ガル接続,いそがしい,イソガシ,イソガシ
```

今回の実装に当たって、利用する項目は`表層形,左文脈ID,コスト`の三つである。

1. 表層形とは、活用や表記揺れなどを考慮した、文中において文字列として実際に出現する形式である。
2. 左文脈IDと右文脈IDは等しいため、一方のみを利用すればよい。左文脈IDは整数の0から1315までの1316種類存在する。各IDに対応する定義は`dict/left-id.def`で定義されている。例として、以下のようになっている。

```
0 BOS/EOS,*,*,*,*,*,BOS/EOS
1 その他,間投,*,*,*,*,*
2 フィラー,*,*,*,*,*,*
3 感動詞,*,*,*,*,*,*
4 記号,アルファベット,*,*,*,*,*
5 記号,一般,*,*,*,*,*
6 記号,括弧開,*,*,*,*,BOS/EOS
7 記号,括弧閉,*,*,*,*,BOS/EOS
8 記号,句点,*,*,*,*,BOS/EOS
9 記号,空白,*,*,*,*,*
10 記号,読点,*,*,*,*,*
11 形容詞,自立,*,*,形容詞・アウオ段,ガル接続,*
12 形容詞,自立,*,*,形容詞・アウオ段,ガル接続,無い
13 形容詞,自立,*,*,形容詞・アウオ段,仮定形,*
14 形容詞,自立,*,*,形容詞・アウオ段,仮定形,無い
15 形容詞,自立,*,*,形容詞・アウオ段,仮定縮約１,*
16 形容詞,自立,*,*,形容詞・アウオ段,仮定縮約１,無い
17 形容詞,自立,*,*,形容詞・アウオ段,仮定縮約２,*
18 形容詞,自立,*,*,形容詞・アウオ段,仮定縮約２,無い
19 形容詞,自立,*,*,形容詞・アウオ段,基本形,*
20 形容詞,自立,*,*,形容詞・アウオ段,基本形,無い
21 形容詞,自立,*,*,形容詞・アウオ段,体言接続,*
22 形容詞,自立,*,*,形容詞・アウオ段,体言接続,無い
23 形容詞,自立,*,*,形容詞・アウオ段,文語基本形,*
24 形容詞,自立,*,*,形容詞・アウオ段,文語基本形,無い
25 形容詞,自立,*,*,形容詞・アウオ段,未然ウ接続,*
26 形容詞,自立,*,*,形容詞・アウオ段,未然ウ接続,無い
27 形容詞,自立,*,*,形容詞・アウオ段,未然ヌ接続,*
28 形容詞,自立,*,*,形容詞・アウオ段,未然ヌ接続,無い
```

3. コストには、単語生起コストと単語連接コストの２種類が存在する。`表層形,左文脈ID,コスト`の`コスト`は単語生起コストを表し、コストが高ければ、この単語が日本語の文脈に出現する確率が低いことを意味する。一方、単語連接コストは異なる品詞の繋がりやすさを表し、`dict/matrix def`で定義される。例として、以下のようになっている。

```
0 0 -434
0 1 1
0 2 -1630
0 3 -1671
0 4 24
0 5 111
0 6 -2752
0 7 -589
0 8 -589
0 9 -294
0 10 -155
0 11 475
0 12 945
0 13 -467
0 14 -155
0 15 -461
0 16 -148
0 17 -461
0 18 -148
0 19 -2409
0 20 -3230
0 21 -558
0 22 -246
0 23 -510
0 24 -198
0 25 -461
0 26 -148
0 27 -462
```

------

### ビタビアルゴリズムの実装

1. 前処理として、`create_trie.py`と`create_cost_matrix.py`によって、解析用のトライ木とコスト表を生成する。
2. `tokenize.py`はビタビアルゴリズム実装する。BOSノードから、`forward`でラティスを構築して、`backward`で最小コスト経路を出力する。

PS: 未知語処理などは一切していないため、辞書にない単語が存在すると、解析できない。



# MeCabの利用

## MeCabのインストール

### Macユーザー

0. ターミナルを開く。

1. homebrewをインストールする。

```bash
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```

2. Mecab本体と辞書をインストールする。

```bash
brew install mecab mecab-ipadic
```

3. PythonからMeCabを利用できるようにする。

```bash
brew install swig
pip install mecab-python3
```

### Windowsユーザー

1. MeCabの公式HPにて、下記のバージョンをダウンロードし、インストールする。

   Binary package for MS-Windows

   - mecab-0.996.exe:[ダウンロード](https://drive.google.com/uc?export=download&id=0B4y35FiV1wh7WElGUGt6ejlpVXc)
   - Windows 版には コンパイル済みの IPA 辞書が含まれています

   **インストール際に、文字コードはUTF-8を選ぶ！！！！！！！！**

2. PythonからMeCabを利用できるようにする。Anaconda Promptで下記のコマンドを入力する。

   ```
   pip install mecab-python-windows
   ```

   

   

   
