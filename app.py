import streamlit as st
import json
import os
import base64
from datetime import datetime, timedelta, timezone

from styles import get_custom_css, render_sidebar

# ページ設定（サイドバーを常に展開）
st.set_page_config(
    page_title="AI Daily News",
    layout="wide",
    initial_sidebar_state="expanded"
)

# カスタムCSS適用
st.markdown(get_custom_css(), unsafe_allow_html=True)

# サイドバーナビゲーション
render_sidebar()


@st.cache_data(ttl=300)
def load_knowledge_base():
    """AI戦術データをJSONファイルから読み込む"""
    base_dir = os.path.dirname(__file__)
    ai_tactics_path = os.path.join(base_dir, "data", "ai_tactics.json")
    
    try:
        if os.path.exists(ai_tactics_path):
            with open(ai_tactics_path, "r", encoding="utf-8") as f:
                ai_tactics = json.load(f)
                ai_tactics.sort(key=lambda x: x.get("date", ""), reverse=True)
                return ai_tactics
        return []
    except Exception as e:
        st.error(f"❌ データ読み込みエラー: {e}")
        return []


def get_svg_as_base64(svg_path):
    """SVGファイルをBase64エンコード"""
    try:
        with open(svg_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except:
        return None


def is_today(date_str):
    """日付が今日かどうかを判定"""
    if not date_str:
        return False
    JST = timezone(timedelta(hours=9))
    today = datetime.now(JST).strftime("%Y-%m-%d")
    return date_str == today


# ロゴ表示
logo_path = os.path.join(os.path.dirname(__file__), "assets", "logo_b.svg")
logo_b64 = get_svg_as_base64(logo_path)

if logo_b64:
    st.markdown(
        f"""
        <div style="text-align: center; padding: 2rem 0 1rem 0;">
            <img src="data:image/svg+xml;base64,{logo_b64}" width="300" alt="Logo">
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown(
    """
    <h1 style="text-align: center; font-size: 2.5rem; color: #1B5D93; margin-bottom: 0.5rem;">
        📰 AI Daily News
    </h1>
    <p style="text-align: center; color: #666; font-size: 1.1rem; margin-bottom: 2rem;">
        毎朝6時に最新AIニュースをお届け
    </p>
    """,
    unsafe_allow_html=True
)

# データ読み込み
knowledge_base = load_knowledge_base()

# 全記事を日付降順で表示
all_news = sorted(knowledge_base, key=lambda x: x.get("date", ""), reverse=True)

if not all_news:
    st.info("📭 記事がまだありません。毎朝6時に更新されます。")
    st.stop()

# カードグリッド表示
st.markdown("---")

cols = st.columns(3)

for idx, item in enumerate(all_news):
    with cols[idx % 3]:
        # 画像パスがあればそれを使用、なければグラデーション
        image_path = item.get("image_path")
        
        if image_path and os.path.exists(image_path):
            # 実際の画像を表示
            try:
                with open(image_path, "rb") as f:
                    img_data = f.read()
                img_b64 = base64.b64encode(img_data).decode()
                image_html = f'<img src="data:image/png;base64,{img_b64}" style="width: 100%; height: 200px; object-fit: cover; border-radius: 12px 12px 0 0;">'
            except:
                # 画像読み込み失敗時はグラデーション
                image_html = '<div style="height: 200px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); display: flex; align-items: center; justify-content: center; color: white; font-size: 3rem; font-weight: bold; border-radius: 12px 12px 0 0;"></div>'
        else:
            # デフォルトのグラデーション
            image_html = '<div style="height: 200px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); display: flex; align-items: center; justify-content: center; color: white; font-size: 3rem; font-weight: bold; border-radius: 12px 12px 0 0;"></div>'
        
        title = item.get("title", "")[:60]
        title_ellipsis = "..." if len(item.get("title", "")) > 60 else ""
        highlight = item.get("news_highlight", "")[:80]
        highlight_ellipsis = "..." if len(item.get("news_highlight", "")) > 80 else ""
        
        card_html = f'''<div style="border: 1px solid #e0e0e0; border-radius: 12px; margin-bottom: 0.5rem; box-shadow: 0 2px 8px rgba(0,0,0,0.1); overflow: hidden; height: 380px; display: flex; flex-direction: column;">
{image_html}
<div style="padding: 1rem 1.5rem; flex: 1; display: flex; flex-direction: column;">
<div style="font-size: 0.8rem; color: #999;">{item.get("date", "")}</div>
<h3 style="font-size: 1.5rem; color: #333; margin: 0.3rem 0; line-height: 1.3; overflow: hidden; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical;">{title}{title_ellipsis}</h3>
<p style="font-size: 0.85rem; color: #666; margin: 0.2rem 0; flex: 1; overflow: hidden; display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical;">{highlight}{highlight_ellipsis}</p>
</div>
</div>'''
        
        st.markdown(card_html, unsafe_allow_html=True)
        
        # 記事へのリンクボタン
        if st.button("📖 記事を読む", key=f"read_{item.get('id', idx)}", use_container_width=True):
            st.session_state.selected_article_id = item.get("id")
            st.switch_page("pages/article.py")

# フッター
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: #999; padding: 2rem 0;">
        <p>毎朝6時に自動更新 | Powered by Gemini AI</p>
    </div>
    """,
    unsafe_allow_html=True
)
