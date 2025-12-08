import streamlit as st
import json
import os
from datetime import datetime, timedelta

from styles import get_custom_css

# ページ設定
st.set_page_config(page_title="AI司令塔ナレッジ", layout="wide", initial_sidebar_state="collapsed")

# カスタムCSS適用
st.markdown(get_custom_css(), unsafe_allow_html=True)


@st.cache_data
def load_knowledge_base():
    """ナレッジデータをJSONファイルから読み込む（経験則 + AI戦術）"""
    base_dir = os.path.dirname(__file__)
    
    # 経験則（ユーザーの知見）
    situations_path = os.path.join(base_dir, "data", "situations.json")
    # AI生成戦術
    ai_tactics_path = os.path.join(base_dir, "data", "ai_tactics.json")
    
    all_items = []
    
    try:
        # 経験則を読み込み（sourceを追加）
        if os.path.exists(situations_path):
            with open(situations_path, "r", encoding="utf-8") as f:
                situations = json.load(f)
                for item in situations:
                    item["_source"] = "experience"  # 経験則マーク
                all_items.extend(situations)
        
        # AI戦術を読み込み（sourceを追加）
        if os.path.exists(ai_tactics_path):
            with open(ai_tactics_path, "r", encoding="utf-8") as f:
                ai_tactics = json.load(f)
                for item in ai_tactics:
                    item["_source"] = "ai"  # AI生成マーク
                all_items.extend(ai_tactics)
        
        if not all_items:
            st.warning("⚠️ データファイルが見つかりません。")
            return []
        
        # 日付で新しい順にソート
        all_items.sort(key=lambda x: x.get("date", ""), reverse=True)
        return all_items
        
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
st.markdown("""
<div style="margin-bottom: 2rem;">
    <h1 style="font-size: 1.8rem; margin: 0; color: #1a253a;">🎯 AI司令塔ナレッジ</h1>
    <p style="color: #666; margin-top: 0.5rem;">世界中のAIトレンドを自動収集 → 実務に使える戦術に変換</p>
</div>
""", unsafe_allow_html=True)

# 検索・フィルターエリア
col_search, col_tags, col_source = st.columns([2, 1, 1])

with col_search:
    search_query = st.text_input("🔍 キーワード検索", placeholder="例: テスト, 要件, バグ...")

with col_tags:
    selected_tags = st.multiselect("🏷️ タグで絞り込み", all_tags)

with col_source:
    source_filter = st.selectbox(
        "📂 ソース",
        ["すべて", "✍️ 経験則のみ", "🤖 AI提案のみ"]
    )

# 変数設定（折りたたみ）
with st.expander("⚙️ プロンプト変数を設定"):
    col1, col2 = st.columns(2)
    with col1:
        tech_stack = st.text_input("使用技術", value="Python", placeholder="例: Python, React")
    with col2:
        role = st.text_input("ターゲット読者", value="上司", placeholder="例: クライアント")

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

# ソースフィルター
if source_filter == "✍️ 経験則のみ":
    filtered = [item for item in filtered if item.get("_source") == "experience"]
elif source_filter == "🤖 AI提案のみ":
    filtered = [item for item in filtered if item.get("_source") == "ai"]

# NEW件数をカウント
new_count = sum(1 for item in filtered if is_new(item.get("date", "")))

# 結果表示
if not filtered:
    st.warning("該当するナレッジがありません")
else:
    # 件数カウント
    exp_count = sum(1 for item in filtered if item.get("_source") == "experience")
    ai_count = sum(1 for item in filtered if item.get("_source") == "ai")
    
    st.caption(
        f"📚 {len(filtered)} 件のナレッジ "
        f"（✍️ 経験則: {exp_count}件 / 🤖 AI提案: {ai_count}件）"
        + (f" 🔥 NEW: {new_count}件" if new_count > 0 else "")
    )
    
    for item in filtered:
        # NEWマークと日付
        item_date = item.get("date", "")
        is_new_item = is_new(item_date)
        new_badge = "🔥 NEW " if is_new_item else ""
        date_display = f"[{item_date}]" if item_date else ""
        
        # ソースバッジ（経験則 or AI）
        source_badge = "✍️ " if item.get("_source") == "experience" else "🤖 "
        
        # タイトル（なければsituationを使用）
        title = item.get("title", item.get("situation", "タイトルなし"))
        
        # エクスパンダーのタイトル
        expander_title = f"{source_badge}{new_badge}{date_display} {title[:55]}{'...' if len(title) > 55 else ''}"
        
        with st.expander(f"**{expander_title}**"):
            # タグ表示
            tags = item.get("tags", [])
            if tags:
                tag_html = " ".join([
                    f'<span style="background:#e8ecf0; padding:2px 8px; border-radius:4px; font-size:0.75rem; margin-right:4px;">{tag}</span>'
                    for tag in tags
                ])
                st.markdown(tag_html, unsafe_allow_html=True)
            
            # 推奨AI表示
            recommended_ai = item.get("recommended_ai")
            if recommended_ai:
                model_name = recommended_ai.get("model", "")
                reason = recommended_ai.get("reason", "")
                badge_color = recommended_ai.get("badge_color", "blue")
                
                col_ai, col_reason = st.columns([1, 2])
                with col_ai:
                    st.markdown(f"**🚀 推奨: {model_name}**")
                with col_reason:
                    if reason:
                        st.markdown(f"💡 **なぜ{model_name.split()[0]}を推奨するのか？**")
                        st.markdown(reason)
            
            st.markdown("---")
            
            # シチュエーション（problem_context）
            problem_context = item.get("problem_context", item.get("situation", ""))
            if problem_context:
                st.markdown(f"**シチュエーション:**")
                st.markdown(problem_context)
            
            # プロンプト
            prompt = item.get("prompt", "")
            if prompt:
                st.markdown("**💡 司令塔のアクション:**")
                st.info(prompt, icon="💡")
            
            # ソースニュース表示
            source_news = item.get("source_news")
            if source_news and source_news.get("url"):
                source_title = source_news.get("title", "ソース")
                source_url = source_news.get("url", "")
                st.markdown(f"[📰 ソース: {source_title} ↗]({source_url})")
            
            st.markdown("---")
            
            # プロンプト発行
            mode_key = f"mode_{item['id']}"
            if mode_key not in st.session_state:
                st.session_state[mode_key] = False
            
            if st.button("✨ プロンプト発行", key=f"btn_{item['id']}"):
                st.session_state[mode_key] = not st.session_state[mode_key]
            
            if st.session_state[mode_key]:
                final_prompt = f"""# あなたの役割
あなたは{tech_stack}の熟練エキスパートです。

# 依頼内容
【課題・状況】
{problem_context}

【指示】
{prompt}

【制約条件】
- 技術スタック: {tech_stack}
- ターゲット読者: {role}
- 出力形式: 具体的で実行可能なコード、またはマークダウン形式のドキュメント

プロフェッショナルとして、私の指示待ちではなく、最善の解を提案してください。"""
                st.markdown("**📋 コピーしてAIに貼り付けてください:**")
                st.code(final_prompt, language="markdown")

# フッター
st.markdown("""
<div style="margin-top: 4rem; padding-top: 1rem; border-top: 1px solid #e0e0e0; text-align: center; color: #999; font-size: 0.75rem;">
    AI司令塔ナレッジ - 毎日自動で進化するナレッジベース
</div>
""", unsafe_allow_html=True)
