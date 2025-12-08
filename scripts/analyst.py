"""
集めたニュースを戦術データに変換する
Google Gemini API を使用
"""
import json
import os
import sys
from datetime import datetime
import time

# プロジェクトルートをパスに追加
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Gemini APIライブラリのインポート
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
    pass


def analyze_news_to_tactic(client, news_item, max_retries=3):
    """ニュースを実務で使える戦術に変換"""
    
    prompt_text = f"""あなたは戦術的AIコンサルタントです。
最新のAI技術ニュースを、エンジニアが明日から使える実践的なプロンプトに変換してください。

【ニュース情報】
タイトル: {news_item.get('title', 'N/A')}
要約: {news_item.get('summary', 'N/A')}
URL: {news_item.get('url', 'N/A')}

【あなたのタスク】
このニュースを読んで、エンジニアが実務で「こういう場面で使える！」と思える具体的なユースケースと、すぐにコピペで使えるプロンプトを作成してください。

以下のJSON形式で回答してください：
{{
  "title": "戦術のタイトル（例: 'Mistral 3でコードレビューを自動化'）",
  "problem_context": "どんな実務課題を解決するか（例: 'PRのコードレビューに時間がかかる'）",
  "recommended_ai": {{
    "model": "推奨AIモデル名（例: Mistral 3, Claude 3.5 Sonnet, GPT-4o）",
    "reason": "なぜこのモデルが最適か（例: 'オープンソースで無料、コード理解に優れる'）",
    "badge_color": "orange"
  }},
  "prompt": "すぐに使えるプロンプト（変数は{{変数名}}の形式で）",
  "tags": ["タグ1", "タグ2", "タグ3"]
}}

【重要】
- promptは具体的で、コピペしてすぐ使えるものにしてください
- 変数（例: {{コード}}, {{言語}}）を含めて汎用的にしてください
- tagsは3つ程度、日本語で

JSON形式のみで回答してください。"""

    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model='gemini-2.5-flash',  # JSON生成が複雑なので新しいモデルを使用
                contents=[prompt_text],
                config=types.GenerateContentConfig(
                    temperature=0.7
                )
            )
            
            response_text = response.text.strip()
            
            # デバッグ出力（エラー時のみ）
            # print(f"DEBUG: {response_text[:200]}")
            
            # JSONマークダウンコードブロックを除去
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                parts = response_text.split("```")
                if len(parts) >= 2:
                    response_text = parts[1].strip()
            
            # JSONの開始位置を見つける
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            if json_start != -1 and json_end > json_start:
                response_text = response_text[json_start:json_end]
            
            tactic_data = json.loads(response_text)
            return tactic_data
            
        except Exception as e:
            wait_time = 2 ** attempt
            print(f"  ⚠️ APIエラー (試行 {attempt + 1}/{max_retries}): {str(e)[:80]}")
            if attempt < max_retries - 1:
                print(f"     {wait_time}秒後にリトライします...")
                time.sleep(wait_time)
    
    return None
    
def analyze_and_generate_tactics():
    """ニュースを戦術に変換するメイン処理"""
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        print("エラー: GEMINI_API_KEYが設定されていません")
        return None
    
    # Gemini APIクライアントを初期化
    client = genai.Client(api_key=api_key)
    print("📊 Gemini API (gemini-2.5-flash) を使用します")
    
    # ニュースデータを読み込む
    news_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "news_raw.json")
    
    if not os.path.exists(news_path):
        print(f"エラー: {news_path} が見つかりません")
        print("先に collector.py を実行してください")
        return None
    
    with open(news_path, "r", encoding="utf-8") as f:
        news_items = json.load(f)
    
    if not news_items:
        print("警告: ニュースデータが空です")
        return []
    
    print(f"📰 {len(news_items)}件のニュースを戦術に変換します...\n")
    
    tactics = []
    date_str = datetime.now().strftime("%Y%m%d")
    
    for idx, news in enumerate(news_items, 1):
        print(f"🔄 [{idx}/{len(news_items)}] {news.get('title', 'N/A')[:40]}...")
        
        tactic_data = analyze_news_to_tactic(client, news)
        
        if tactic_data:
            # IDと日付を追加
            tactic_data["id"] = f"{date_str}_{idx:02d}"
            tactic_data["date"] = datetime.now().strftime("%Y-%m-%d")
            
            # ソース情報を追加
            tactic_data["source_news"] = {
                "title": news.get("title", ""),
                "url": news.get("url", "")
            }
            
            tactics.append(tactic_data)
            print(f"   ✅ → {tactic_data.get('title', 'N/A')[:50]}")
        else:
            print(f"   ❌ スキップ")
        
        # レート制限対策
        if idx < len(news_items):
            time.sleep(2)
    
    # 結果をファイルに保存
    output_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "new_tactics.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(tactics, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 戦術分析完了: {len(tactics)}件の戦術を生成しました")
    print(f"📁 保存先: {output_path}")
    return tactics


if __name__ == "__main__":
    print("=" * 50)
    print("🎯 戦術分析エージェント起動")
    print("ニュースを実務で使えるプロンプトに変換します...")
    print("=" * 50)
    
    result = analyze_and_generate_tactics()
    
    if result:
        print("\n" + "=" * 50)
        print(f"✅ 完了！{len(result)}件の戦術を生成しました")
        print("=" * 50)
    else:
        print("\n" + "=" * 50)
        print("❌ 戦術分析に失敗しました")
        print("=" * 50)
        sys.exit(1)
