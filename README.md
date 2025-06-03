<div align="center">

# 💬 SpeechTree 🌲 <!-- omit in toc -->

Represent speech text with simple-but-rich tree structure, Convert from/to popular TTS formats.  
様々な TTS をつなぐ、シンプルかつリッチな木構造の音声テキスト。

</div>

```python
ojt = openjtalk.run_frontend("相互運用性って良いよね。")
tree = parse_ojt_features(ojt)
vv = parse_as_voicevox(tree)  # Use it for speech synthesis by VOICEVOX API 🎉
graph = parse_as_graph(tree)  # Beautiful graph, see below ✨️
```

[graph]

# ParseOJT
Parser of Open JTalk text-processing output (NJD features).

```mermaid
graph TD;
    A["Open JTalk NJD features"] --> B["Utterance"];
    B --> C["VOICEVOX AccentPhrases"];
    B --> D["visual graph"];
```

## Dev
### All-in Check
```bash
## check-and-fix
uv run mypy . && uv run ruff check --fix && uv run ruff format && uv run typos && uv run pytest
```

### All-in Static Program Analysis
```bash
# check-only
uv run mypy . && uv run ruff check && uv run ruff format --check && uv run typos

## check-and-fix
uv run mypy . && uv run ruff check --fix && uv run ruff format && uv run typos
```

### Design Docs
Open JTalk `make_label()` 系（NJD のパーサーとその出力表現）が内部でどんな処理をしているか、web 上に情報がほぼない。  
NJD パーサーとその出力表現を、よりモダンな言語で実装して整理する必要がある。  

フルコンテキストラベルは情報が不足している。表層形の情報を意図的に落としているため、単語と音素の対応が取れない。  
editable な TTS をつくるにはフルコンテキストラベルは役不足であり、新しい規格が必要である。  

Open JTalk `make_label()` 系は NJDNode を JPCommonNode へ変換しており、この時点で表層形の情報を意図的に落としている。  
つまり、`make_label()` 系のモダン再実装をしても情報不足は解決しない。  

そのため、`make_label()` 系の現行挙動を理解したうえで、表層形を保持するスーパーセット的なパーサー・出力表現を新しく提案する必要がある。  

作りたいものは「editable な音声合成における、テキスト処理の最終出力表現」である。  
テキストに話者性はないので、この表現にも話者性は持たせない。そのため音の長さや高さは不要。  
基本的に話者非依存である「発音」「アクセント」「記号イントネーション（！や？）」が合成向けに重要。  
テキスト処理の中間出力でなく最終出力であるため、短単位の自動結合や品詞を用いた自動アクセント推定は完了した前提。そのため品詞や活用は不要。  
また editable にするため、発音やアクセントの修正が必要。そのためには大元となる表層形とその対応付けが必要。じゃないと「何が間違っているか」の「何が」を特定できない。  
前段では「辞書表層形とテキストの一致検索 & 最適系列選択」が基礎となって発音が与えられると想定する（例: MeCab）ため、辞書の「語/ワード」が基準ユニット。  
ワードに表層形と発音がくっつく形。発音はモーラ列へ一意に変換できるので、モーラ列として保持される。  

音声合成が目的であって、テキスト分析が目的ではないことに注意。  
なので表層形は大事だが、基本形は重要ではない。  

TTS が前提であるため、エンドユーザーは文字的に音を指定する。  
より具体的には、発音を（音素や単音でなく）カタカナで指定する。  
これは一般的な日本人の感覚では仮名が音の原子であるため。  
そのため日本人が発音として受け入れられるカタカナ表記は全てカバーするのが好ましい。  
カタカナと音素の対応が 1:1 かはわからない。レアなカタカナ表記（例: ヴャ）が標準的なカタカナ表記（ビャ）と同じ音素という可能性もある。その辺は個人差がデカくて標準化困難かもしれない。  
この点も考えると、モーラと音素が別レイヤーなのも一理がある。  
マッピングを設定値として外に出すのも手。ひとまずは OJT 準拠とする。  
なお、もっと細かくしたいなら単音を音素の下に置けば良い。異音をきっちり分けられる。が、現行で音素→単音を適切に推定する手法は寡聞にして知らない。  

型は str で自由にして、validator でチェックするというのも手。そうすれば validator の rule を設定値で変えられる。  
tree を合成に利用するときはどうせ合成器に合わせて converter を書くので、その時にその合成器に合わせた validator を掛ければ良い。

class TreeManager (かオシャレに Gardener) を用意して、そこに validator や replacer をもたせるのは有り。  
Tree 自体はコンテナ規格なのが大事で、独自のプログラムで Tree を作ってもらうのは一向に構わない。  
dict からのコンバーターを用意しても良い。  

音素一覧やモーラ音素マッピングを SpeechTree 仕様に入れると、これより広い値を取れなくなる。  
今のフルコンテキストラベルが表層形やモーラ種別に不足があるのと同じ構図になる（表層形は種別というより属性ごとないのでちょっと違うけど）。  
そのため standard validator/mapper だけ用意して、仕様としては任意にしておくのがまるそう。Mecab のなんでもつけれるのと似た感じ。  

OJT から取り込む情報とその根拠:
  - string: 読み上げたい書き文字テキストであり、原文の情報として必要。
  - pron: 読み上げるときの音の種類であり、主要な音声情報として必要。なお、string から簡単にはわからない。
  - acc: 読み上げるときの音の高さであり、主要な音声情報として必要。なお、string から簡単にはわからない。
  - chain_flag: アクセント句化の指示であり、アクセント句への構造化に必要。なお、最終的にはフラグ値としては不要。

#### History
- 着想 ver1：「フルコンテキストラベルがまどろっこしい」
- 着想 ver2：「`make_label()` の処理内容がぱっと見でわからなすぎる」
- 着想 ver3：「フルコンテキストラベルは情報が不足してる気がする」
- 着想 ver4：「JPCommon への変換時に情報落としすぎている」
- 着想 ver5：「もう少しリッチな中間表現が TTS には必要なのでは？」

#### Notes
木構造 tree  
音声的  
個別モーラのピッチは持たず、アクセント句のみ。  
→ voice 一般（∋ 歌声）ではなく、speech 寄り。  

# speech_tree = sorted(list(set(MR_CV.keys())))
# voicevox = sorted(list(set(map(lambda s: s[0], vv_mapping))))
# ojt_vv_diff_phonemes = ['ウゥ', 'キィ', 'ギィ', 'クァ', 'クィ', 'クゥ', 'クェ', 'クォ', 'グァ', 'グィ', 'グゥ', 'グェ', 'グォ', 'ヂェ', 'ヂャ', 'ヂュ', 'ヂョ', 'テェ', 'デェ', 'ニィ', 'ヒィ', 'ビィ', 'ピィ', 'ミィ', 'リィ', ]
# diff_s = list(filter(lambda s: s[0] in ojt_vv_diff_phonemes, vv_mapping))
# ojt_vv_diff_sets = [('リィ', 'ry', 'i'), ('ミィ', 'my', 'i'), ('ピィ', 'py', 'i'), ('ビィ', 'by', 'i'), ('ヒィ', 'hy', 'i'), ('ニィ', 'ny', 'i'), ('デェ', 'dy', 'e'), ('テェ', 'ty', 'e'), ('グォ', 'gw', 'o'), ('グェ', 'gw', 'e'), ('グゥ', 'gw', 'u'), ('グィ', 'gw', 'i'), ('クォ', 'kw', 'o'), ('クェ', 'kw', 'e'), ('クゥ', 'kw', 'u'), ('クィ', 'kw', 'i'), ('ギィ', 'gy', 'i'), ('キィ', 'ky', 'i'), ('ウゥ', 'w', 'u'), ('ヂョ', 'j', 'o'), ('ヂュ', 'j', 'u'), ('ヂャ', 'j', 'a'), ('ヂェ', 'j', 'e'), ('グァ', 'gw', 'a'), ('クァ', 'kw', 'a')]
