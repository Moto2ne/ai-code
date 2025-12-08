# APIキー設定ガイド

## 📋 概要

このシステムは以下のAPIを使用します：
- **Google Gemini API**: ニュース収集用・戦術分析用（無料枠あり・推奨）
- **OpenAI API**: 戦術分析用（オプション、Geminiがない場合）

## 💰 料金について

### Google Gemini API（推奨・無料枠あり）
- **無料枠**: ✅ あり（1日15Mトークン）
- **料金体系**: 無料枠を超えた分は従量課金
- **使用モデル**: 
  - ニュース収集: `gemini-1.5-flash`（無料枠対応）
  - 戦術分析: `gemini-1.5-flash`
- **Google Search Grounding**: 有料プランまたは制限緩和時に利用可能（環境変数`USE_GOOGLE_SEARCH_GROUNDING=true`で有効化）
- **詳細**: [Google AI Studio](https://aistudio.google.com/app/apikey)

### OpenAI API（オプション）
- **無料トライアル**: ❌ なし（2024年後半に廃止）
- **料金体系**: 従量課金（使用した分だけ支払い）
- **GPT-4o**: 約$2.50/1M入力トークン、$10/1M出力トークン
- **詳細**: [OpenAI Pricing](https://openai.com/api/pricing/)

## 🔑 APIキーの取得方法

### 1. Google Gemini APIキーの取得（必須・無料）

1. [Google AI Studio](https://aistudio.google.com/app/apikey) にアクセス
2. Googleアカウントでログイン
3. 「Create API Key」をクリック
4. プロジェクトを選択（または新規作成）
5. APIキーをコピー（**一度しか表示されないので注意**）

**メリット**:
- ✅ 無料枠が充実（1日15Mトークン）
- ✅ 支払い方法の登録不要（無料枠内なら）
- ✅ 簡単に取得可能

**注意**: 
- 無料枠を超えると従量課金が発生します
- APIキーは安全に管理してください

### 2. OpenAI APIキーの取得（オプション）

1. [OpenAI Platform](https://platform.openai.com/) にアクセス
2. アカウントを作成（無料）
3. [API Keys](https://platform.openai.com/api-keys) ページにアクセス
4. 「Create new secret key」をクリック
5. APIキーをコピー（**一度しか表示されないので注意**）
6. 支払い方法を登録（API使用には必須）

**注意**: 
- API使用には有効な支払い方法の登録が必要です
- 使用量に応じて自動課金されます
- 使用量上限を設定することを推奨します

## ⚙️ 設定手順

### ステップ1: `.env`ファイルの作成

プロジェクトルートに`.env`ファイルを作成します：

```bash
# Windowsの場合
copy .env.example .env

# Mac/Linuxの場合
cp .env.example .env
```

### ステップ2: APIキーを設定

`.env`ファイルを開き、取得したAPIキーを設定します：

```env
# .env ファイル

# Gemini API（必須・無料枠あり）
# ニュース収集と戦術分析の両方で使用
GEMINI_API_KEY=AIzaSyxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# OpenAI API（オプション、戦術分析のみ、Geminiがない場合）
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

**優先順位**: 
- ニュース収集: `GEMINI_API_KEY`が必須（Google Search Grounding機能を使用）
- 戦術分析: `GEMINI_API_KEY`が設定されている場合、Gemini APIを使用（無料枠優先）
- 戦術分析: `GEMINI_API_KEY`がない場合、`OPENAI_API_KEY`を使用

**重要**: 
- `.env`ファイルはGitにコミットしないでください（`.gitignore`に含まれています）
- APIキーは他人に共有しないでください

### ステップ3: 動作確認

```bash
# アプリを起動
streamlit run app.py
```

## 💡 無料で試す方法

### オプション1: 自動更新機能を無効化

自動更新機能（GitHub Actions）を使わず、手動でナレッジを追加する方法：

1. `data/situations.json`を直接編集
2. 既存のナレッジデータを使用
3. 自動更新スクリプトは実行しない

### オプション2: 代替APIの使用

無料または低コストの代替案：

#### Google Gemini API（無料枠あり）✅ 実装済み
- **無料枠**: 1日15Mトークン
- **設定**: `GEMINI_API_KEY`を`.env`に設定するだけ
- **自動切り替え**: `GEMINI_API_KEY`が設定されていれば自動でGemini APIを使用

#### DeepSeek API（低コスト）
- **料金**: GPT-4oより大幅に安価
- **詳細**: [DeepSeek Pricing](https://www.deepseek.com/)

### オプション3: ローカル開発のみ

- 自動更新機能を使わない
- 既存の`data/situations.json`のみを使用
- APIキーは設定不要

## 🛡️ セキュリティ注意事項

1. **APIキーの保護**
   - `.env`ファイルをGitにコミットしない
   - 公開リポジトリにAPIキーをアップロードしない
   - 環境変数として管理する

2. **使用量の監視**
   - OpenAI: [Usage Dashboard](https://platform.openai.com/usage)
   - Perplexity: API設定ページで確認
   - 使用量上限を設定することを推奨

3. **GitHub Actions使用時**
   - GitHub SecretsにAPIキーを設定
   - リポジトリのSettings > Secrets and variables > Actions
   - 設定するSecrets:
     - `GEMINI_API_KEY`（必須・無料枠あり）
     - `OPENAI_API_KEY`（オプション、戦術分析のみ、Geminiがない場合）

## 📊 コスト見積もり（参考）

### 1日あたりの想定コスト

**Google Gemini API**（推奨）:
- ニュース収集: **無料**（無料枠内なら、Google Search Grounding機能付き）
- 戦術分析: **無料**（無料枠内なら）
- 無料枠超過時: 約$0.01-0.10/日

**OpenAI API**（オプション）:
- 戦術分析のみ: 約$0.10-0.30/日（5件のニュースを分析）

**合計（Gemini使用時・推奨）**: **無料**（無料枠内なら）または 約$0.01-0.10/日（月額約$0.30-3）
**合計（OpenAI使用時）**: 約$0.10-0.30/日（月額約$3-9）

**注意**: 実際のコストは使用量によって異なります。

## 🔧 トラブルシューティング

### APIキーが認識されない

1. `.env`ファイルがプロジェクトルートにあるか確認
2. ファイル名が`.env`（先頭にドット）であることを確認
3. APIキーに余分なスペースや改行がないか確認
4. アプリを再起動

### 認証エラー

1. APIキーが正しいか確認
2. APIキーに有効期限がないか確認
3. アカウントに十分なクレジット/残高があるか確認

### レート制限エラー

1. リトライ機能が自動で動作します
2. しばらく待ってから再実行
3. APIプランの上限を確認

## 📚 参考リンク

- [Perplexity API Documentation](https://docs.perplexity.ai/)
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Google Gemini API](https://ai.google.dev/docs)
- [DeepSeek API](https://platform.deepseek.com/docs)
