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
    
    if not markdown_text:
        print("⚠️ 空のレスポンスを受信")
        return news_items
    
    try:
        # パターン1: - [タイトル](URL): 要約
        pattern1 = r'- \[([^\]]+)\]\(([^)]+)\):\s*(.+?)(?=\n- |\n\n|$)'
        matches = re.findall(pattern1, markdown_text, re.MULTILINE | re.DOTALL)
        
        for title, url, summary in matches:
            if url.strip().startswith('http'):
                news_items.append({
                    "title": title.strip(),
                    "summary": summary.strip()[:500],
                    "url": url.strip(),
                    "collected_at": datetime.now().isoformat()
                })
        
        # パターン2: **番号. タイトル**\n[URL](URL): 要約 形式（Geminiの主要出力形式）
        if not news_items:
            pattern2 = r'\*\*\d+\.\s*([^*]+)\*\*\s*\n?\[?(https?://[^\s\)\]\n]+)\]?(?:\([^)]*\))?[:\s]*([^\n*]+)'
            matches = re.findall(pattern2, markdown_text, re.MULTILINE)
            for title, url, summary in matches:
                news_items.append({
                    "title": title.strip(),
                    "summary": summary.strip()[:500],
                    "url": url.strip(),
                    "collected_at": datetime.now().isoformat()
                })
        
        # パターン3: 番号付きリスト 1. [タイトル](URL): 要約
        if not news_items:
            pattern3 = r'\d+\.\s*\[([^\]]+)\]\(([^)]+)\)[:\s]+(.+?)(?=\n\d+\.|\n\n|$)'
            matches = re.findall(pattern3, markdown_text, re.MULTILINE | re.DOTALL)
            for title, url, summary in matches:
                if url.strip().startswith('http'):
                    news_items.append({
                        "title": title.strip(),
                        "summary": summary.strip()[:500],
                        "url": url.strip(),
                        "collected_at": datetime.now().isoformat()
                    })
        
        # パターン4: 行ごとにURLを探す（フォールバック）
        if not news_items:
            print("📝 標準パターンで解析失敗、行ごとの解析を試行...")
            lines = markdown_text.split('\n')
            current_title = None
            
            for i, line in enumerate(lines):
                line = line.strip()
                if not line:
                    continue
                
                # **タイトル** を検出して保持
                bold_match = re.search(r'\*\*\d*\.?\s*([^*]+)\*\*', line)
                if bold_match and 'http' not in line:
                    current_title = bold_match.group(1).strip()
                    continue
                
                # URLを含む行を検出
                url_match = re.search(r'https?://[^\s\)\]>\n]+', line)
                if url_match:
                    url = url_match.group(0).rstrip('.,;:')
                    
                    # タイトルを決定
                    title = None
                    # [タイトル] 形式を探す
                    title_match = re.search(r'\[([^\]]+)\]', line)
                    if title_match:
                        title = title_match.group(1)
                    elif current_title:
                        title = current_title
                    else:
                        # 行の最初の部分をタイトルとして使用
                        title = re.sub(r'https?://[^\s]+', '', line).strip()[:100]
                    
                    # 要約を抽出
                    summary_match = re.search(r'[:\-]\s*(.+)$', line)
                    summary = summary_match.group(1) if summary_match else ""
                    
                    if title and url and url.startswith('http'):
                        news_items.append({
                            "title": title[:200],
                            "summary": summary[:500],
                            "url": url,
                            "collected_at": datetime.now().isoformat()
                        })
                    
                    current_title = None  # リセット
        
        print(f"📊 解析結果: {len(news_items)}件のニュースを検出")
        
        # 重複URLを除去
        seen_urls = set()
        unique_items = []
        for item in news_items:
            if item["url"] not in seen_urls:
                seen_urls.add(item["url"])
                unique_items.append(item)
        news_items = unique_items
        
        # それでも見つからない場合、全体を1つのニュースとして扱う
        if not news_items:
            print("⚠️ ニュースを解析できませんでした（フォールバック）")
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

【出力形式】厳密に以下の形式で出力してください:
- [ニュースのタイトル](実際のURL): 要約（50字以内）

例:
- [Claude 3.5 Sonnetがリリース](https://anthropic.com/news/claude-3-5): 推論能力が大幅に向上し、コーディングタスクで最高性能を達成

【必須条件】
- 各ニュースは2025年12月のものであること
- URLは必ず https:// で始まる実際のURLであること
- 5件選定すること
- 余計な説明は不要、上記形式のリストのみ出力"""
    
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
            
            # デバッグ: レスポンス内容を出力（GitHub Actions用）
            print("=" * 50)
            print("📝 Gemini APIレスポンス (先頭1000文字):")
            print(markdown_text[:1000] if markdown_text else "(空)")
            print("=" * 50)
            
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
