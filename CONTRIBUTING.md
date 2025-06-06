# 貢献者ガイド

SpeechTree はオープンソースプロジェクトです。  
本ガイドは開発方針・開発用コマンドなど、コントリビュータの皆さんの一助となる情報を提供します。  

## 目次
SpeechTree の方針は以下をご参照ください：

- [開発ガバナンス](#開発ガバナンス)
- [チェック](#チェック)

コントリビュータの目的に応じたガイドは以下をご参照ください：

- [環境構築](#環境構築)

開発にあたって頻繁に利用されるコマンドは以下をご参照ください：

- [依存ライブラリをインストールする](#依存ライブラリをインストールする)
- [チェックを一括実行する](#チェックを一括実行する)

## 開発ガバナンス

SpeechTree はコミュニティの皆さんからの機能要望・バグ報告・質問を GitHub Issues で受け付けています。

## 環境構築

`Python 3.12` を用いて開発されています。  

パッケージ管理ツールに [uv](https://docs.astral.sh/uv/) を採用しています。  
uv のインストール方法は[公式ドキュメント](https://docs.astral.sh/uv/getting-started/installation/)をご参照ください。  

### 依存ライブラリをインストールする
```bash
# 実行・開発環境をインストールする
uv sync --all-groups

# git hook をインストールする
uv run pre-commit install -t pre-push
```

## チェック
様々な自動チェックを採用しています。  
目的は安全性・可読性・開発速度の向上です。  

### チェックを一括実行する
```bash
## 一括でチェックのみをおこなう
uv run mypy . && uv run ruff check && uv run ruff format --check && uv run typos && uv run pytest

## 一括でチェックと可能な範囲の自動修正をおこなう
uv run mypy . && uv run ruff check --fix && uv run ruff format && uv run typos && uv run pytest
```

### 静的解析

自動での型検査・リント・整形・タイポ検査を採用しています。  

#### 型検査

自動型検査を採用しています。  
目的は安全性の向上であり、チェッカーには `mypy` を採用しています。

型検査の実行は "[チェックを一括実行する](#チェックを一括実行する)" をご参照ください。型検査の設定は `pyproject.toml` で管理されています。  

#### リント

自動リントを採用しています。  
目的は安全性の向上であり、リンターには `ruff` を採用しています。

リントの実行は "[チェックを一括実行する](#チェックを一括実行する)" をご参照ください。リントの設定は `pyproject.toml` で管理されています。  

#### 整形

自動整形を採用しています。  
目的は可読性の向上であり、フォーマッタには `ruff` を採用しています。

整形の実行は "[チェックを一括実行する](#チェックを一括実行する)" をご参照ください。整形の設定は `pyproject.toml` で管理されています。  

#### タイポ検査

自動タイポ検査を採用しています。  
目的は可読性の向上であり、チェッカーには `typos` を採用しています。

タイポ検査の実行は "[チェックを一括実行する](#チェックを一括実行する)" をご参照ください。タイポ検査の設定は `pyproject.toml` で管理されています。  

### テスト

自動テストを採用しています。 
目的は安全性の向上であり、ランナーには `pytest` を採用しています。

テストの実行は "[チェックを一括実行する](#チェックを一括実行する)" をご参照ください。テストの設定は `pyproject.toml` で管理されています。  