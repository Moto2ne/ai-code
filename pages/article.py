import streamlit as st
import json
import os
import base64
from datetime import datetime, timedelta, timezone

from styles import get_custom_css, render_sidebar

# ページ設定
st.set_page_config(
    page_title="記事詳細 | AI Daily News",
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
    base_dir = os.path.dirname(os.path.dirname(__file__))
    ai_tactics_path = os.path.join(base_dir, "data", "ai_tactics.json")
    
    try:
        if os.path.exists(ai_tactics_path):
            with open(ai_tactics_path, "r", encoding="utf-8") as f:
                ai_tactics = json.load(f)
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


# 戻るボタン
col_back, col_logo = st.columns([1, 5])
with col_back:
    if st.button("⬅️ トップに戻る", use_container_width=True):
        st.switch_page("app.py")

# ロゴとヘッダー画像
logo_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "logo_b.svg")
logo_b64 = get_svg_as_base64(logo_path)

if logo_b64:
    st.markdown(
        f"""
        <div style="text-align: center; padding: 1rem 0;">
            <img src="data:image/svg+xml;base64,{logo_b64}" width="200" alt="Logo">
        </div>
        """,
        unsafe_allow_html=True
    )

# 記事データ取得
knowledge_base = load_knowledge_base()
selected_article_id = st.session_state.get("selected_article_id")

if not selected_article_id:
    st.warning("記事が選択されていません。")
    st.stop()

# 記事を検索
article = None
for item in knowledge_base:
    if item.get("id") == selected_article_id:
        article = item
        break

if not article:
    st.error("記事が見つかりません。")
    st.stop()

# ヘッダー画像（実際の画像 or グラデーション）
image_path = article.get("image_path")

if image_path and os.path.exists(os.path.join(os.path.dirname(os.path.dirname(__file__)), image_path)):
    # 実際の画像を表示
    full_image_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), image_path)
    try:
        with open(full_image_path, "rb") as f:
            img_data = f.read()
        img_b64 = base64.b64encode(img_data).decode()
        st.markdown(
            f"""
            <div style="
                border-radius: 12px;
                overflow: hidden;
                margin-bottom: 2rem;
            ">
                <img src="data:image/png;base64,{img_b64}" style="width: 100%; height: 400px; object-fit: cover;">
            </div>
            """,
            unsafe_allow_html=True
        )
    except:
        # 画像読み込み失敗時はグラデーション
        st.markdown(
            f"""
            <div style="
                height: 250px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                display: flex;
                align-items: center;
                justify-content: center;
                color: white;
                font-size: 4rem;
                font-weight: bold;
                border-radius: 12px;
                margin-bottom: 2rem;
            ">
                🤖
            </div>
            """,
            unsafe_allow_html=True
        )
else:
    # デフォルトのグラデーション
    st.markdown(
        f"""
        <div style="
            height: 250px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 4rem;
            font-weight: bold;
            border-radius: 12px;
            margin-bottom: 2rem;
        ">
            🤖
        </div>
        """,
        unsafe_allow_html=True
    )

# 記事メタ情報
st.caption(f"📅 {article.get('date', '')} | 📰 AI Daily News")

# タイトル
st.markdown(f"# {article.get('title', '')}")

# ニュースハイライト
news_highlight = article.get("news_highlight", "")
if news_highlight:
    st.info(f"**📰 {news_highlight}**")

st.markdown("---")

# 記事本文
article_content = article.get("article")
if article_content:
    # 目次を生成
    lines = article_content.split('\n')
    toc_items = []
    heading_count = 0 
    
    for line in lines:
        # ## 見出しを検出（##で始まる行）
        if line.startswith('## '):
            heading = line.replace('## ', '').strip()
            # アンカー用のIDを生成
            anchor = f"heading-{heading_count}"
            toc_items.append((heading, anchor))
            heading_count += 1

    
    # 目次を表示
    if toc_items:
        st.markdown("### 📑 目次")
        toc_md = ""
        for heading, anchor in toc_items:
            toc_md += f"- [{heading}](#{anchor})\n"
        st.markdown(toc_md)
        st.markdown("---")
    
    # 本文を表示（見出しにアンカーIDを追加）
    modified_lines = []
    idx = 0
    for line in lines:
        if line.startswith('## '):
            heading = line.replace('## ', '').strip()
            anchor = f"heading-{idx}"
            # Markdownの見出しにHTMLアンカーを追加（ヘッダー被り対策のオフセット付き）
            modified_lines.append(f'<div id="{anchor}" style="position: relative; top: -100px; visibility: hidden;"></div>')
            modified_lines.append("") # Markdownとして認識させるための空行
            modified_lines.append(line)
            idx += 1
        else:
            modified_lines.append(line)
    
    modified_content = '\n'.join(modified_lines)
    st.markdown(modified_content, unsafe_allow_html=True)
else:
    st.warning("記事コンテンツがありません。")

# ソースニュース
st.markdown("---")
source_news = article.get("source_news")
if source_news:
    news_title = source_news.get("title", "")
    source_url = source_news.get("url", "")
    if source_url and source_url.startswith("http"):
        st.markdown(f"**📰 元記事:** [{news_title}]({source_url})")

# 戻るボタン（下部）
st.markdown("---")
if st.button("⬅️ トップに戻る", key="back_bottom", use_container_width=True):
    st.switch_page("app.py")

# フッター
st.markdown(
    """
    <div style="text-align: center; color: #999; padding: 2rem 0;">
        <p>AI Daily News © 2025 | Powered by Gemini AI</p>
    </div>
    """,
    unsafe_allow_html=True
)
