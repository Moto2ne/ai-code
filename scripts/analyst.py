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
    
    news_title = news_item.get('title', 'N/A')[:100]
    news_summary = news_item.get('summary', 'N/A')[:200]
    news_url = news_item.get('url', '')
    
    prompt_text = f"""あなたはAI技術コンサルタントです。以下のニュースを、エンジニアが実務で使える戦術に変換してください。

ニュース: {news_title}
要約: {news_summary}

以下のJSON形式で出力してください。文字列内に改行を入れないでください：

{{"title": "戦術タイトル（30文字以内）", "problem_context": "解決する課題（50文字以内）", "recommended_ai": {{"model": "推奨AIモデル名", "reason": "推奨理由（30文字以内）", "badge_color": "orange"}}, "prompt": "使えるプロンプト（改行なし、100文字以内）", "tags": ["タグ1", "タグ2"]}}

JSONのみ出力してください。"""

    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model='gemini-2.5-flash',  # 動作確認済みのモデル
                contents=[prompt_text],
                config=types.GenerateContentConfig(
                    temperature=0.5  # より確実なJSON生成のため温度を下げる
                )
            )
            
            response_text = response.text.strip()
            
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
            
            # 不完全なJSONを修正する試み
            response_text = response_text.replace('\n', ' ').replace('\r', '')
            
            # 閉じていない文字列を修正
            try:
                tactic_data = json.loads(response_text)
            except json.JSONDecodeError:
                # 閉じ括弧が足りない場合の補完
                if response_text.count('{') > response_text.count('}'):
                    response_text += '}' * (response_text.count('{') - response_text.count('}'))
                if response_text.count('[') > response_text.count(']'):
                    response_text += ']' * (response_text.count('[') - response_text.count(']'))
                # 末尾の不完全な部分を削除して再試行
                for end_pattern in ['"}', '"]', '"}]', '"}]}']:
                    try:
                        # 最後の完全なフィールドまで切り詰める
                        last_complete = response_text.rfind('",')
                        if last_complete > 0:
                            truncated = response_text[:last_complete+1] + '}'
                            # tagsがない場合は追加
                            if '"tags"' not in truncated:
                                truncated = truncated[:-1] + ', "tags": ["AI", "自動生成"]}'
                            tactic_data = json.loads(truncated)
                            break
                    except:
                        continue
                else:
                    raise
            
            return tactic_data
            
        except Exception as e:
            wait_time = 5 + (5 * attempt)  # 5秒, 10秒, 15秒と待機
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
        
        # レート制限対策（十分に待機）
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
