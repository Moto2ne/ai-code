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
                model='gemini-2.5-flash',
                contents=[prompt_text],
                config=types.GenerateContentConfig(
                    temperature=0.3  # さらに低くして確実性を上げる
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
            
            # 改行を除去
            response_text = response_text.replace('\n', ' ').replace('\r', '').replace('\t', ' ')
            
            # 途中で切れた文字列を修復
            def fix_truncated_json(text):
                """途中で切れたJSONを修復"""
                # 開いている引用符を閉じる
                in_string = False
                escaped = False
                fixed = []
                for i, char in enumerate(text):
                    if escaped:
                        escaped = False
                        fixed.append(char)
                        continue
                    if char == '\\':
                        escaped = True
                        fixed.append(char)
                        continue
                    if char == '"':
                        in_string = not in_string
                    fixed.append(char)
                
                result = ''.join(fixed)
                if in_string:
                    result += '"'  # 閉じ引用符を追加
                
                # 括弧を補完
                open_braces = result.count('{') - result.count('}')
                open_brackets = result.count('[') - result.count(']')
                result += ']' * open_brackets + '}' * open_braces
                
                return result
            
            # まず直接パースを試みる
            try:
                tactic_data = json.loads(response_text)
            except json.JSONDecodeError:
                # 修復を試みる
                fixed_text = fix_truncated_json(response_text)
                try:
                    tactic_data = json.loads(fixed_text)
                except json.JSONDecodeError:
                    # 最後の手段：必須フィールドだけの最小JSONを構築
                    # titleとpromptを抽出
                    title_match = response_text.split('"title"')[1].split('"')[1] if '"title"' in response_text else "AI戦術"
                    tactic_data = {
                        "title": title_match[:50],
                        "problem_context": "AI技術の活用",
                        "recommended_ai": {"model": "Gemini", "reason": "高性能", "badge_color": "orange"},
                        "prompt": "最新のAI技術を活用して効率化を図ってください。",
                        "tags": ["AI", "自動生成"]
                    }
            
            return tactic_data
            
        except Exception as e:
            wait_time = 5 + (5 * attempt)
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
    
    # ダミーニュースをフィルタリング（collector.pyがパース失敗した場合のフォールバック）
    valid_news = [
        news for news in news_items 
        if news.get("title") != "AI/ML News Collection" 
        and news.get("url", "").startswith("http")
    ]
    
    if not valid_news:
        print("⚠️ 有効なニュースがありません（URLが含まれるニュースのみ処理）")
        return []
    
    print(f"📰 {len(valid_news)}件のニュースを戦術に変換します...\n")
    
    tactics = []
    date_str = datetime.now().strftime("%Y%m%d")
    
    for idx, news in enumerate(valid_news, 1):
        print(f"🔄 [{idx}/{len(valid_news)}] {news.get('title', 'N/A')[:40]}...")
        
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
        if idx < len(valid_news):
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
    
    if result is not None:  # 0件でも成功（有効なニュースがなかった場合）
        print("\n" + "=" * 50)
        print(f"✅ 完了！{len(result)}件の戦術を生成しました")
        print("=" * 50)
    else:
        print("\n" + "=" * 50)
        print("❌ 戦術分析に失敗しました")
        print("=" * 50)
        sys.exit(1)
