import streamlit as st
import json
import os
from datetime import datetime, timedelta

from styles import get_custom_css

# ページ設定
st.set_page_config(page_title="AI司令塔ナレッジ", layout="wide", initial_sidebar_state="collapsed")

# カスタムCSS適用
st.markdown(get_custom_css(), unsafe_allow_html=True)

# 済ボタン用のセッション状態を初期化
if "completed_tactics" not in st.session_state:
    st.session_state.completed_tactics = set()


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


def is_new(date_str):
    """作成日が3日以内かどうかを判定"""
    try:
        item_date = datetime.strptime(date_str, "%Y-%m-%d")
        days_diff = (datetime.now() - item_date).days
        return days_diff <= 3
    except:
        return False


# ナレッジデータを読み込む
knowledge_base = load_knowledge_base()

# 全タグを抽出
all_tags = sorted(set(tag for item in knowledge_base for tag in item.get("tags", [])))

# --- UI ---

# ヘッダー
col_title, col_guide = st.columns([4, 1])
with col_title:
    st.markdown("""
    <div style="margin-bottom: 1rem;">
        <h1 style="font-size: 1.8rem; margin: 0; color: #1a253a;">🎯 AI司令塔ナレッジ</h1>
        <p style="color: #666; margin-top: 0.5rem;">最新AIニュースを自動収集 → 使える場面・手順・プロンプトに変換</p>
    </div>
    """, unsafe_allow_html=True)
with col_guide:
    st.page_link("pages/ai_guide.py", label="🤖 AI早わかりガイド", icon="📖")

# 検索・フィルターエリア
col_search, col_tags = st.columns([2, 1])

with col_search:
    search_query = st.text_input("🔍 キーワード検索", placeholder="例: Claude, コード生成, API...")

with col_tags:
    selected_tags = st.multiselect("🏷️ タグで絞り込み", all_tags)

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

if selected_tags:
    filtered = [
        item for item in filtered
        if any(tag in item.get("tags", []) for tag in selected_tags)
    ]

# NEW件数と済件数をカウント
new_count = sum(1 for item in filtered if is_new(item.get("date", "")))
completed_count = sum(1 for item in filtered if item.get("id", "") in st.session_state.completed_tactics)

# 結果表示
if not filtered:
    st.info("📭 戦術がまだありません。毎朝6時に自動更新されます。")
else:
    status_parts = [f"📚 {len(filtered)} 件の戦術"]
    if new_count > 0:
        status_parts.append(f"🔥 NEW: {new_count}件")
    if completed_count > 0:
        status_parts.append(f"✅ 済: {completed_count}件")
    st.caption(" | ".join(status_parts))
    
    for item in filtered:
        item_id = item.get("id", "")
        
        # NEWマークと日付
        item_date = item.get("date", "")
        is_new_item = is_new(item_date)
        new_badge = "🔥 NEW " if is_new_item else ""
        date_display = f"[{item_date}]" if item_date else ""
        
        # 済チェック
        is_completed = item_id in st.session_state.completed_tactics
        completed_badge = "✅ " if is_completed else ""
        
        # タイトル（なければsituationを使用）
        title = item.get("title", item.get("situation", "タイトルなし"))
        
        # エクスパンダーのタイトル
        expander_title = f"{completed_badge}{new_badge}{date_display} {title[:50]}{'...' if len(title) > 50 else ''}"
        
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
            done_label = "✅済" if is_completed else "☐"
            done_style = "background:#d4edda; color:#155724;" if is_completed else "background:#f8f9fa; color:#666; cursor:pointer;"
            
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
            
            # ソースニュース表示（小さく下部に）
            source_news = item.get("source_news")
            if source_news and source_news.get("url"):
                source_url = source_news.get("url", "")
                st.caption(f"[📰 ソース ↗]({source_url})")

# フッター
st.markdown("""
<div style="margin-top: 4rem; padding-top: 1rem; border-top: 1px solid #e0e0e0; text-align: center; color: #999; font-size: 0.75rem;">
    AI司令塔ナレッジ - 毎日自動で進化するナレッジベース
</div>
""", unsafe_allow_html=True)
