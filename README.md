# AI司令塔ナレッジ

開発現場で「困った！」と思った時に、AIへの最適なプロンプトを即座に発行できるナレッジベース。さらに、世界中の最新AIトレンドを自動で収集し、それを「実務で使える戦術」に変換して毎日更新する仕組み。

## 機能

- 🔍 **キーワード検索**: シチュエーション、プロンプト、タグから検索
- 🏷️ **タグフィルタリング**: 複数タグで絞り込み
- ✨ **プロンプト発行**: 変数を埋め込んだ完成形プロンプトを生成
- 🚀 **推奨AI表示**: 各戦術に最適なAIモデルを推奨
- 🔥 **NEWマーク**: 3日以内の新しいナレッジを強調表示
- 📰 **ソース表示**: 元になったニュースのリンクを表示

## セットアップ

### 1. リポジトリをクローン

```bash
git clone https://github.com/your-org/ai-code.git
cd ai-code
```

### 2. 仮想環境を作成

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. 依存ライブラリをインストール

```bash
pip install -r requirements.txt
```

### 4. 環境変数を設定

```bash
cp .env.example .env
# .envファイルを編集してAPIキーを設定
```

### 5. アプリを起動

```bash
streamlit run app.py
```

## 自動更新機能

GitHub Actionsを使用して、毎日朝6時（日本時間）に自動でニュースを収集し、戦術データを更新します。

### 必要な設定

1. GitHubリポジトリのSecretsに以下を追加：
   - `GEMINI_API_KEY`（必須・無料枠あり）
   - `OPENAI_API_KEY`（オプション、戦術分析のみ、Geminiがない場合）

2. GitHub Actionsが有効になっていることを確認

3. `main`ブランチへの自動コミットが許可されていることを確認

**注意**: 
- Gemini APIは無料枠が充実（1日15Mトークン）しており、ニュース収集と戦術分析の両方で使用できます
- Google Search Grounding機能により、リアルタイムのWeb検索結果を活用した最新ニュース収集が可能です

## ディレクトリ構成

```
ai-code/
├── app.py                  # メインアプリ（画面表示）
├── styles.py               # デザイン設定
├── data/
│   └── situations.json     # ナレッジデータ（自動更新される）
├── scripts/                # 自動化スクリプト
│   ├── collector.py        # ニュース収集スクリプト
│   ├── analyst.py          # 戦術分析スクリプト
│   └── merge_tactics.py    # データマージスクリプト
├── .github/
│   └── workflows/
│       └── daily_intel.yml # 毎日自動実行の設定
└── requirements.txt        # 必要なライブラリ一覧
```

## ライセンス

MIT License
