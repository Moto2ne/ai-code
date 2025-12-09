"""
公式RSSフィードから最新のAI/MLニュースを収集
英語ソースから直接取得 → LLMで日本語に超要約
"""
import json
import os
import sys
import re
from datetime import datetime, timedelta
import time

# プロジェクトルートをパスに追加
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    import feedparser
except ImportError:
    print("エラー: feedparserライブラリがインストールされていません")
    print("pip install feedparser を実行してください")
    sys.exit(1)

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


# 信頼性の高い公式RSSフィード
RSS_FEEDS = [
    {
        "name": "OpenAI Blog",
        "url": "https://openai.com/blog/rss.xml",
        "priority": 1,  # 最優先
    },
    {
        "name": "Google AI Blog", 
        "url": "https://blog.google/technology/ai/rss/",
        "priority": 1,
    },
    {
        "name": "Anthropic",
        "url": "https://www.anthropic.com/index.xml",
        "priority": 1,
    },
    {
        "name": "Microsoft Research",
        "url": "https://www.microsoft.com/en-us/research/feed/",
        "priority": 2,
    },
    {
        "name": "AWS Machine Learning",
        "url": "https://aws.amazon.com/blogs/machine-learning/feed/",
        "priority": 2,
    },
    {
        "name": "Hugging Face Blog",
        "url": "https://huggingface.co/blog/feed.xml",
        "priority": 2,
    },
]


def fetch_rss_entries(max_age_days=7):
    """RSSフィードから最新エントリを取得"""
    all_entries = []
    cutoff_date = datetime.now() - timedelta(days=max_age_days)
    
    for feed_info in RSS_FEEDS:
        try:
            print(f"📡 {feed_info['name']} を取得中...")
            feed = feedparser.parse(feed_info["url"])
            
            if feed.bozo and not feed.entries:
                print(f"  ⚠️ フィード取得失敗: {feed_info['name']}")
                continue
            
            for entry in feed.entries[:5]:  # 各フィードから最新5件まで
                # 日付を取得
                published = None
                if hasattr(entry, 'published_parsed') and entry.published_parsed:
                    published = datetime(*entry.published_parsed[:6])
                elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
                    published = datetime(*entry.updated_parsed[:6])
                
                # 古すぎる記事はスキップ
                if published and published < cutoff_date:
                    continue
                
                # タイトルにAI関連キーワードが含まれるかチェック
                title = entry.get('title', '')
                summary = entry.get('summary', entry.get('description', ''))[:500]
                
                all_entries.append({
                    "title": title,
                    "summary": summary,
                    "url": entry.get('link', ''),
                    "source": feed_info['name'],
                    "priority": feed_info['priority'],
                    "published": published.isoformat() if published else None,
                    "collected_at": datetime.now().isoformat()
                })
            
            print(f"  ✅ {len(feed.entries[:5])}件取得")
            
        except Exception as e:
            print(f"  ❌ エラー: {feed_info['name']} - {str(e)[:50]}")
            continue
    
    # 優先度と日付でソート
    all_entries.sort(key=lambda x: (x['priority'], x['published'] or ''), reverse=False)
    
    return all_entries


def filter_ai_news_with_llm(client, entries, max_news=3):
    """LLMを使ってAI関連の重要ニュースを選定・要約"""
    
    if not entries:
        return []
    
    # エントリをテキストにまとめる
    entries_text = "\n".join([
        f"[{i+1}] {e['source']}: {e['title']}\n    {e['summary'][:200]}...\n    URL: {e['url']}"
        for i, e in enumerate(entries[:20])  # 最大20件から選定
    ])
    
    prompt = f"""以下のニュース一覧から、エンジニアにとって最も重要なAI/ML関連ニュースを{max_news}件選んでください。

【選定基準】
- 新しいAIモデルのリリース（GPT, Claude, Gemini, Llama等）
- 開発者向けAPI・ツールのアップデート
- 実務に直結する技術発表
- 具体的な性能数値やベンチマーク結果があるもの

【除外基準】
- 一般的なAI解説・入門記事
- 企業の採用・資金調達ニュース
- 規制・政策関連（技術発表を除く）

【ニュース一覧】
{entries_text}

【出力形式】
選んだニュースの番号と、日本語での超要約（1行50文字以内）をJSON配列で出力:
[{{"index": 1, "summary_ja": "GPT-5が発表、コード生成速度が3倍に向上"}}, ...]

JSONのみ出力してください。"""

    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[prompt],
            config=types.GenerateContentConfig(temperature=0.2)
        )
        
        response_text = response.text.strip()
        
        # JSONを抽出
        if "```json" in response_text:
            response_text = response_text.split("```json")[1].split("```")[0].strip()
        elif "```" in response_text:
            response_text = response_text.split("```")[1].split("```")[0].strip()
        
        json_start = response_text.find('[')
        json_end = response_text.rfind(']') + 1
        if json_start != -1 and json_end > json_start:
            response_text = response_text[json_start:json_end]
        
        selected = json.loads(response_text)
        
        # 選定されたニュースを返す
        result = []
        for item in selected[:max_news]:
            idx = item.get('index', 1) - 1
            if 0 <= idx < len(entries):
                entry = entries[idx]
                entry['summary_ja'] = item.get('summary_ja', entry['title'])
                result.append(entry)
        
        return result
        
    except Exception as e:
        print(f"⚠️ LLM選定エラー: {e}")
        # フォールバック: 優先度順に上位を返す
        return entries[:max_news]


def collect_news():
    """ニュース収集のメイン処理"""
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        print("エラー: GEMINI_API_KEYが設定されていません")
        return None
    
    client = genai.Client(api_key=api_key)
    print("📊 Gemini API を使用してニュースを選定・要約します")
    
    # RSSフィードから取得
    print("\n" + "=" * 50)
    print("📡 公式RSSフィードからニュースを収集中...")
    print("=" * 50)
    
    entries = fetch_rss_entries(max_age_days=7)
    print(f"\n📰 合計 {len(entries)}件のエントリを取得")
    
    if not entries:
        print("⚠️ ニュースが取得できませんでした")
        return []
    
    # LLMで選定・要約
    print("\n🤖 LLMで重要ニュースを選定中...")
    selected_news = filter_ai_news_with_llm(client, entries, max_news=3)
    
    print(f"✅ {len(selected_news)}件のニュースを選定しました")
    
    # 保存形式に変換
    news_items = []
    for news in selected_news:
        news_items.append({
            "title": news.get('summary_ja', news['title']),
            "summary": news['summary'][:300],
            "url": news['url'],
            "source": news['source'],
            "collected_at": news['collected_at']
        })
    
    # 保存
    output_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "news_raw.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(news_items, f, ensure_ascii=False, indent=2)
    
    print(f"📁 保存先: {output_path}")
    
    return news_items


if __name__ == "__main__":
    print("=" * 50)
    print("--- ニュース収集エージェント起動 ---")
    print("公式RSSフィードから最新AIニュースを収集します...")
    print("=" * 50)
    
    result = collect_news()
    
    if result:
        print("\n" + "=" * 50)
        print(f"✅ 完了！{len(result)}件のニュースを収集しました")
        for i, news in enumerate(result, 1):
            print(f"  {i}. [{news['source']}] {news['title'][:40]}...")
        print("=" * 50)
    else:
        print("\n" + "=" * 50)
        print("❌ ニュース収集に失敗しました")
        print("GEMINI_API_KEYを確認してください。")
        print("=" * 50)
        sys.exit(1)
