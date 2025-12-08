"""
Gemini APIの検索機能を使って最新のAI/MLニュースを集める
"""
import json
import os
import sys
import re
from datetime import datetime
import time
import requests

# プロジェクトルートをパスに追加
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from google import genai
    from google.genai import types
except ImportError:
    print("エラー: google-genaiライブラリがインストールされていません")
    print("pip install google-genai を実行してください")
    sys.exit(1)

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("警告: python-dotenvがインストールされていません（環境変数の自動読み込みが無効）")


def resolve_redirect_url(url, timeout=15, max_retries=2):
    """リダイレクトURLを実際のソースURLに解決する"""
    if not url or not url.startswith('http'):
        return url
    
    # Google Vertex AIのリダイレクトURLの場合のみ解決
    if 'vertexaisearch.cloud.google.com/grounding-api-redirect' not in url:
        return url
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    for attempt in range(max_retries):
        try:
            # GETリクエストでリダイレクト先を取得
            response = requests.get(
                url, 
                allow_redirects=True, 
                timeout=timeout, 
                headers=headers,
                stream=True
            )
            resolved_url = response.url
            
            # リダイレクトが成功した場合
            if resolved_url and 'vertexaisearch.cloud.google.com' not in resolved_url:
                return resolved_url
                
        except requests.exceptions.RequestException as e:
            if attempt < max_retries - 1:
                time.sleep(1)  # リトライ前に待機
                continue
            # 最終試行で失敗
            pass
    
    return url  # 失敗時は元のURLを返す


def parse_markdown_to_news_items(markdown_text):
    """Markdown形式のレスポンスを解析してニュースデータに変換"""
    news_items = []
    
    try:
        # Markdownのリスト形式をパース: - [タイトル](URL): 要約
        pattern = r'- \[([^\]]+)\]\(([^)]+)\):\s*(.+?)(?=\n- |\n\n|$)'
        matches = re.findall(pattern, markdown_text, re.MULTILINE | re.DOTALL)
        
        for title, url, summary in matches:
            news_items.append({
                "title": title.strip(),
                "summary": summary.strip()[:500],  # 最大500文字
                "url": url.strip(),
                "collected_at": datetime.now().isoformat()
            })
        
        # パターンマッチが失敗した場合、簡易的なパースを試みる
        if not news_items:
            # 行ごとに分割して、URLを含む行を探す
            lines = markdown_text.split('\n')
            current_item = {}
            for line in lines:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                
                # URLを含む行を検出
                url_match = re.search(r'https?://[^\s\)]+', line)
                if url_match:
                    url = url_match.group(0)
                    # タイトルを抽出（[タイトル]または行の最初の部分）
                    title_match = re.search(r'\[([^\]]+)\]', line)
                    title = title_match.group(1) if title_match else line.split(':')[0].strip()
                    
                    # 要約を抽出
                    summary = line.split(':', 1)[1].strip() if ':' in line else line
                    
                    news_items.append({
                        "title": title[:200],
                        "summary": summary[:500],
                        "url": url,
                        "collected_at": datetime.now().isoformat()
                    })
        
        # それでも見つからない場合、全体を1つのニュースとして扱う
        if not news_items:
            news_items.append({
                "title": "AI/ML News Collection",
                "summary": markdown_text[:500],
                "url": "",
                "collected_at": datetime.now().isoformat()
            })
            
    except Exception as e:
        print(f"⚠️ Markdown解析エラー: {e}")
        # フォールバック: 全体を1つのニュースとして扱う
        news_items.append({
            "title": "AI/ML News Collection",
            "summary": markdown_text[:500],
            "url": "",
            "collected_at": datetime.now().isoformat()
        })
    
    return news_items


def collect_news(max_retries=3):
    """Gemini APIの検索機能を使って、最新のAIトレンドを収集する"""
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        print("エラー: GEMINI_API_KEYが設定されていません")
        return None
    
    try:
        client = genai.Client(api_key=api_key)
    except Exception as e:
        print(f"エラー: Gemini APIクライアントの初期化に失敗しました: {e}")
        return None
    
    # Gemini 2.5 Flash Lite を使用（ニュース収集用）
    # 軽量版でクォータに余裕がある
    model_name = 'gemini-2.5-flash-lite'
    
    # 今日の日付を取得
    today = datetime.now().strftime("%Y年%m月%d日")
    
    # ニュース収集指示プロンプト（エンジニア向け、信頼性の高いソース指定）
    prompt = f"""あなたはソフトウェアエンジニア向けAI技術ニュースのキュレーターです。
今日は{today}です。

【対象読者】
ソフトウェアエンジニア、開発者、MLエンジニア

【収集するニュースの種類】（優先度順）
1. 新しいAIモデルのリリース（GPT、Claude、Gemini、Llama、Mistralなど）
2. AI開発ツール・ライブラリのアップデート（LangChain、Hugging Face、vLLMなど）
3. APIの新機能・変更（OpenAI API、Anthropic API、Google AI APIなど）
4. AI関連のOSSの重要リリース（GitHub）
5. 開発者向けAIサービスの発表

【必須ソース】以下のドメインからのみ選定：
- openai.com, anthropic.com, blog.google, ai.meta.com
- techcrunch.com, theverge.com, venturebeat.com, arstechnica.com
- huggingface.co, github.blog, github.com/releases
- itmedia.co.jp, watch.impress.co.jp, gigazine.net

【除外】
- 電力、医療、金融などの業界特化ニュース（エンジニア向けでないもの）
- 規制・政策ニュース（技術的でないもの）
- 個人ブログ、note、Qiita、まとめサイト
- AI企業の資金調達・買収ニュース（技術発表を除く）

【出力形式】
- [タイトル](URL): 要約テキスト（50字以内、技術的なポイントを含める）

【必須条件】
- 各ニュースは2025年12月のものであること
- 公式発表または信頼できるテックメディアのURLであること
- 5件選定すること"""
    
    for attempt in range(max_retries):
        try:
            # Google Search Groundingを有効化して実際のWeb検索結果を取得
            grounding_tool = types.Tool(
                google_search=types.GoogleSearch()
            )
            config = types.GenerateContentConfig(
                tools=[grounding_tool],
                temperature=0.3  # 低めにして事実重視
            )
            
            response = client.models.generate_content(
                model=model_name,
                contents=[prompt],
                config=config
            )
            
            # レスポンスはMarkdown形式のテキストとして取得
            markdown_text = response.text
            
            # MarkdownをJSON形式に変換
            news_items = parse_markdown_to_news_items(markdown_text)
            
            # リダイレクトURLを実際のソースURLに解決
            print("🔗 URLを解決中...")
            for i, item in enumerate(news_items):
                original_url = item.get("url", "")
                if 'vertexaisearch.cloud.google.com' in original_url:
                    resolved_url = resolve_redirect_url(original_url)
                    if resolved_url != original_url:
                        print(f"  ✅ [{i+1}] {resolved_url[:60]}...")
                        item["url"] = resolved_url
                    else:
                        print(f"  ⚠️ [{i+1}] URL解決できず（元のURLを使用）")
            
            # 結果をファイルに保存（analyst.pyが読み込む形式）
            output_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "news_raw.json")
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(news_items, f, ensure_ascii=False, indent=2)
            
            print(f"✅ ニュース収集完了: {len(news_items)}件")
            return news_items
            
        except Exception as e:
            wait_time = 2 ** attempt  # 指数バックオフ
            print(f"⚠️ APIエラー (試行 {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                print(f"   {wait_time}秒後にリトライします...")
                time.sleep(wait_time)
            else:
                print("❌ 最大リトライ回数に達しました")
                return None
    
    return None


if __name__ == "__main__":
    print("=" * 50)
    print("--- ニュース収集エージェント起動 ---")
    print("Gemini APIを使用して最新のAIトレンドを収集します...")
    print("=" * 50)
    
    result = collect_news()
    
    if result:
        print("=" * 50)
        print(f"✅ ニュース収集が正常に完了しました（{len(result)}件）")
        print("=" * 50)
    else:
        print("=" * 50)
        print("❌ ニュース収集に失敗しました")
        print("GEMINI_API_KEYを確認してください。")
        print("=" * 50)
        sys.exit(1)
