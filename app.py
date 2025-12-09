import streamlit as st
import json
import os
import urllib.parse
from datetime import datetime, timedelta

from styles import get_custom_css

# ページ設定
st.set_page_config(page_title="毎朝6時AIニュース", layout="wide", initial_sidebar_state="collapsed")

# カスタムCSS適用
st.markdown(get_custom_css(), unsafe_allow_html=True)

# 済ボタン用のセッション状態を初期化
if "completed_tactics" not in st.session_state:
    st.session_state.completed_tactics = set()


def is_today(date_str):
    """日付が今日かどうかを判定"""
    if not date_str:
        return False
    today = datetime.now().strftime("%Y-%m-%d")
    return date_str == today


def get_ai_url(model_name):
    """AIモデル名からチャットURLを取得"""
    model_lower = model_name.lower()
    
    # Claude系
    if "claude" in model_lower or "opus" in model_lower or "sonnet" in model_lower:
        return "https://claude.ai/new"
    
    # ChatGPT/GPT系
    if "gpt" in model_lower or "chatgpt" in model_lower or "openai" in model_lower:
        return "https://chat.openai.com/"
    
    # Gemini系
    if "gemini" in model_lower:
        return "https://gemini.google.com/app"
    
    # DeepSeek系
    if "deepseek" in model_lower:
        return "https://chat.deepseek.com/"
    
    # Mistral系
    if "mistral" in model_lower:
        return "https://chat.mistral.ai/"
    
    # Perplexity
    if "perplexity" in model_lower:
        return "https://www.perplexity.ai/"
    
    # Copilot
    if "copilot" in model_lower:
        return "https://copilot.microsoft.com/"
    
    return None


@st.cache_data(ttl=300)  # 5分ごとにキャッシュを更新（GitHubからの変更を反映）
def load_knowledge_base():
    """AI戦術データをJSONファイルから読み込む"""
    base_dir = os.path.dirname(__file__)
    ai_tactics_path = os.path.join(base_dir, "data", "ai_tactics.json")
    
    try:
        if os.path.exists(ai_tactics_path):
            with open(ai_tactics_path, "r", encoding="utf-8") as f:
                ai_tactics = json.load(f)
                # 日付で新しい順にソート
                ai_tactics.sort(key=lambda x: x.get("date", ""), reverse=True)
                return ai_tactics
        
        st.warning("⚠️ データファイルが見つかりません。")
        return []
        
    except Exception as e:
        st.error(f"❌ データ読み込みエラー: {e}")
        return []


def render_tactic_card(item, is_new=False):
    """戦術カードを描画"""
    item_id = item.get("id", "")
    item_date = item.get("date", "")
    
    fire_badge = "🔥 " if is_new else ""
    date_display = f"{item_date}" if item_date else ""
    
    # 済チェック
    is_completed = item_id in st.session_state.completed_tactics
    completed_badge = "✅ " if is_completed else ""
    
    # タイトル（なければsituationを使用）
    title = item.get("title", item.get("situation", "タイトルなし"))
    
    # エクスパンダーのタイトル（今日の新着は🔥、日付とタイトル）
    expander_title = f"{fire_badge}{completed_badge}{date_display} {title[:50]}{'...' if len(title) > 50 else ''}"
    
    with st.expander(f"**{expander_title}**"):
        # 推奨AIとリンク（最重要 - 一番上に配置）
        recommended_ai = item.get("recommended_ai")
        if recommended_ai:
            model_name = recommended_ai.get("model", "")
            reason = recommended_ai.get("reason", "")
            ai_url = get_ai_url(model_name)
            
            if ai_url:
                st.markdown(f"### [🚀 {model_name} を開く →]({ai_url})")
            else:
                st.markdown(f"### 🚀 {model_name}")
            if reason:
                st.caption(f"💡 {reason}")
        
        # タグと済チェック（小さく横並び）
        tags = item.get("tags", [])
        
        tag_html = " ".join([
            f'<span style="background:#e8ecf0; padding:2px 6px; border-radius:4px; font-size:0.7rem; color:#666;">{tag}</span>'
            for tag in tags
        ])
        st.markdown(tag_html, unsafe_allow_html=True)
        
        # 済チェックボックス（タグサイズ）
        st.checkbox(
            "試した",
            value=is_completed,
            key=f"done_{item_id}",
            on_change=lambda iid=item_id: (
                st.session_state.completed_tactics.discard(iid) 
                if iid in st.session_state.completed_tactics 
                else st.session_state.completed_tactics.add(iid)
            )
        )
        
        st.markdown("---")
        
        # 🎯 使える場面
        use_cases = item.get("use_cases", [])
        if use_cases:
            st.markdown("**🎯 こんな時に使える:**")
            for uc in use_cases:
                st.markdown(f"- {uc}")
        
        # 📝 ステップ（簡潔に）
        steps = item.get("steps", [])
        if steps:
            st.markdown("**📝 手順:**")
            steps_text = " → ".join([f"**{i}.** {s}" for i, s in enumerate(steps, 1)])
            st.markdown(steps_text)
        
        st.markdown("---")
        
        # プロンプト（コピーしやすく）
        prompt = item.get("prompt", "")
        if prompt:
            st.markdown("**💡 このプロンプトをコピーしてAIに貼り付け:**")
            st.code(prompt, language="markdown")
        
        # ソースニュース表示（Google検索リダイレクトで確実に表示）
        source_news = item.get("source_news")
        if source_news:
            news_title = source_news.get("title", "")
            if news_title:
                search_query_encoded = urllib.parse.quote(news_title)
                google_search_url = f"https://www.google.com/search?q={search_query_encoded}"
                display_title = news_title[:25] + "..." if len(news_title) > 25 else news_title
                st.caption(f"[🔍 「{display_title}」を検索 ↗]({google_search_url})")


# ナレッジデータを読み込む
knowledge_base = load_knowledge_base()

# --- UI ---

# ヘッダー
col_title, col_guide = st.columns([4, 1])
with col_title:
    st.markdown("""
    <div style="margin-bottom: 1rem;">
        <h1 style="font-size: 1.8rem; margin: 0; color: #1a253a;">📰毎朝6時のAIニュース</h1>
        <p style="color: #666; margin-top: 0.5rem;">最新情報を自動収集 → 使える場面・プロンプトに変換</p>
    </div>
    """, unsafe_allow_html=True)
with col_guide:
    st.page_link("pages/ai_guide.py", label="AI早わかりガイド", icon="📖")

# 検索エリア
search_query = st.text_input("🔍 キーワード検索", placeholder="例: Claude, コード生成, API...")

st.markdown("---")

# フィルタリング
filtered = knowledge_base

if search_query:
    filtered = [
        item for item in filtered
        if search_query.lower() in item.get("title", "").lower()
        or search_query.lower() in item.get("problem_context", "").lower()
        or search_query.lower() in item.get("prompt", "").lower()
        or any(search_query.lower() in tag.lower() for tag in item.get("tags", []))
    ]

# 済件数をカウント
completed_count = sum(1 for item in filtered if item.get("id", "") in st.session_state.completed_tactics)

# 結果表示
if not filtered:
    st.info("📭 戦術がまだありません。毎朝6時に自動更新されます。")
else:
    status_parts = [f"📚 全{len(filtered)}件"]
    if completed_count > 0:
        status_parts.append(f"✅ 試した: {completed_count}件")
    st.caption(" | ".join(status_parts))
    
    # 今日の戦術と過去の戦術を分離
    today_tactics = [item for item in filtered if is_today(item.get("date", ""))]
    past_tactics = [item for item in filtered if not is_today(item.get("date", ""))]
    
    # 🔥 今日仕入れたニュース
    if today_tactics:
        st.markdown("### 🔥 今日仕入れたニュース")
        st.caption(f"本日 {len(today_tactics)}件 のAI戦術を自動生成しました")
        for item in today_tactics:
            render_tactic_card(item, is_new=True)
        
        if past_tactics:
            st.markdown("---")
    
    # 📚 過去の戦術
    if past_tactics:
        st.markdown("### 📚 これまでの戦術")
        for item in past_tactics:
            render_tactic_card(item, is_new=False)

# フッター
st.markdown("""
<div style="margin-top: 4rem; padding-top: 1rem; border-top: 1px solid #e0e0e0; text-align: center; color: #999; font-size: 0.75rem;">
    毎日AIニュース & 戦術生成アプリ © 2025 WBS株式会社
</div>
""", unsafe_allow_html=True)
