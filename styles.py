"""
CSSスタイル定義
Streamlitアプリのスタイリングを管理
"""

def get_custom_css():
    """カスタムCSSを返す - モダンSaaS × 近未来SF/RPG UI"""
    return """
<style>
    /* ============================================
       カラーパレット定義
       ============================================ */
    :root {
        --tech-white: #f8f9fa;
        --blue-gray: #e8ecf0;
        --deep-navy: #1a253a;
        --navy-dark: #0f1626;
        --cyan-bright: #00f2ff;
        --cyan-glow: rgba(0, 242, 255, 0.3);
        --gold-subtle: #cfb53b;
        --gold-glow: rgba(207, 181, 59, 0.2);
        --text-primary: #1a253a;
        --text-secondary: #6b7280;
        --border-subtle: rgba(26, 37, 58, 0.1);
    }
    
    /* ============================================
       全体背景 - テックホワイト/淡いブルーグレー
       ============================================ */
    .stApp {
        background: linear-gradient(135deg, #f8f9fa 0%, #e8ecf0 100%);
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Helvetica Neue', Arial, sans-serif;
    }
    
    /* ============================================
       ロゴエリア - シャープで洗練されたデザイン
       ============================================ */
    .logo-area {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 1.5rem;
    }
    .logo-area img {
        height: 40px;
    }
    .logo-text {
        font-size: 1.5rem;
        font-weight: 700;
        color: var(--deep-navy);
        letter-spacing: -0.02em;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
    }
    
    /* ============================================
       メインヘッダー - コックピット風デザイン
       ============================================ */
    .main-header {
        background: linear-gradient(135deg, var(--deep-navy) 0%, var(--navy-dark) 100%);
        padding: 3rem 2.5rem;
        border-radius: 16px;
        color: #ffffff;
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
        box-shadow: 0 20px 60px rgba(26, 37, 58, 0.4),
                    0 0 0 1px rgba(255, 255, 255, 0.05) inset;
        border: 1px solid rgba(0, 242, 255, 0.1);
    }
    .main-header::before {
        content: "";
        position: absolute;
        top: 0;
        right: 0;
        width: 300px;
        height: 300px;
        background: radial-gradient(circle, var(--cyan-glow) 0%, transparent 70%);
        opacity: 0.3;
        pointer-events: none;
    }
    .main-header::after {
        content: "";
        position: absolute;
        bottom: -50px;
        left: -50px;
        width: 200px;
        height: 200px;
        background: radial-gradient(circle, var(--gold-glow) 0%, transparent 70%);
        opacity: 0.2;
        pointer-events: none;
    }
    .main-header h1 {
        margin: 0;
        font-size: 2.2rem;
        font-weight: 700;
        color: #ffffff;
        letter-spacing: -0.02em;
        text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
        position: relative;
        z-index: 1;
    }
    .main-header p {
        margin: 0.75rem 0 0 0;
        opacity: 0.9;
        font-size: 1rem;
        font-weight: 400;
        color: rgba(255, 255, 255, 0.85);
        position: relative;
        z-index: 1;
    }
    
    /* ============================================
       チャプターカード - グラスモーフィズム風
       ============================================ */
    .chapter-card {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        padding: 2rem;
        border-radius: 16px;
        margin: 1.5rem 0;
        color: var(--text-primary);
        box-shadow: 0 8px 32px rgba(26, 37, 58, 0.08),
                    0 0 0 1px rgba(255, 255, 255, 0.5) inset;
        border: 1px solid rgba(255, 255, 255, 0.3);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .chapter-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 48px rgba(26, 37, 58, 0.12),
                    0 0 0 1px rgba(255, 255, 255, 0.6) inset;
        border-color: rgba(0, 242, 255, 0.3);
    }
    .chapter-card h3 {
        color: var(--deep-navy);
        margin-top: 0;
        font-weight: 700;
        font-size: 1.3rem;
    }
    
    /* ============================================
       Bad Result - 洗練された警告スタイル
       ============================================ */
    .bad-result {
        background: rgba(255, 245, 245, 0.8);
        backdrop-filter: blur(10px);
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid rgba(220, 38, 38, 0.2);
        color: var(--text-primary);
        box-shadow: 0 4px 16px rgba(220, 38, 38, 0.1);
        position: relative;
    }
    .bad-result::before {
        content: "⚠";
        position: absolute;
        right: 20px;
        top: 20px;
        font-size: 1.5rem;
        opacity: 0.6;
    }
    .bad-result h4 {
        color: #dc2626;
        margin-top: 0;
        font-weight: 600;
    }
    .bad-result ul {
        color: var(--text-secondary);
    }
    
    /* ============================================
       Good Result - 成功スタイル
       ============================================ */
    .good-result {
        background: rgba(240, 255, 244, 0.8);
        backdrop-filter: blur(10px);
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid rgba(0, 242, 255, 0.2);
        color: var(--text-primary);
        box-shadow: 0 4px 16px rgba(0, 242, 255, 0.1);
        position: relative;
    }
    .good-result::before {
        content: "✓";
        position: absolute;
        right: 20px;
        top: 20px;
        font-size: 1.5rem;
        color: var(--cyan-bright);
        opacity: 0.8;
    }
    .good-result h4 {
        color: var(--cyan-bright);
        margin-top: 0;
        font-weight: 600;
    }
    .good-result ul {
        color: var(--text-secondary);
    }
    
    /* ============================================
       ボタン - 光沢感とホバーエフェクト
       ============================================ */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, var(--deep-navy) 0%, var(--navy-dark) 100%);
        color: #ffffff;
        font-weight: 600;
        border: none;
        border-radius: 12px;
        padding: 0.875rem 1.75rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 16px rgba(26, 37, 58, 0.3),
                    0 0 0 1px rgba(255, 255, 255, 0.1) inset;
        font-size: 1rem;
        position: relative;
        overflow: hidden;
    }
    .stButton>button::before {
        content: "";
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
        transition: left 0.5s;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(26, 37, 58, 0.4),
                    0 0 0 1px rgba(0, 242, 255, 0.3) inset,
                    0 0 20px var(--cyan-glow);
    }
    .stButton>button:hover::before {
        left: 100%;
    }
    .stButton>button:active {
        transform: translateY(0);
        box-shadow: 0 2px 8px rgba(26, 37, 58, 0.3);
    }
    
    /* ============================================
       サイドバー - 非表示
       ============================================ */
    [data-testid="stSidebar"] {
        display: none !important;
    }
    
    /* メインコンテンツエリアを全幅に */
    .main .block-container {
        max-width: 100% !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
    }
    
    
    /* ============================================
       レベルバッジ - シャープでメタリック
       ============================================ */
    .level-badge {
        display: inline-block;
        background: linear-gradient(135deg, var(--deep-navy) 0%, var(--navy-dark) 100%);
        color: #ffffff;
        padding: 6px 16px;
        border-radius: 8px;
        font-size: 0.75rem;
        font-weight: 700;
        margin-bottom: 1rem;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        box-shadow: 0 2px 8px rgba(26, 37, 58, 0.3),
                    0 0 0 1px rgba(0, 242, 255, 0.2) inset;
        border: 1px solid rgba(0, 242, 255, 0.1);
        position: relative;
    }
    .level-badge::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.1) 0%, transparent 50%);
        border-radius: 8px;
        pointer-events: none;
    }
    
    /* ============================================
       タイポグラフィ強化
       ============================================ */
    h1, h2, h3 {
        font-weight: 700;
        letter-spacing: -0.02em;
        color: var(--deep-navy);
    }
    
    /* 記事本文のフォントサイズを大きく（本文テキストのみ） */
    .main p, .main li, .main td, .main th, .main span, .main div {
        font-size: 1.35rem !important;
        line-height: 1.9 !important;
    }
    
    .main ul, .main ol {
        margin-left: 1.5rem !important;
    }
    
    .main table {
        font-size: 1.3rem !important;
    }
    
    /* ============================================
       スクロールバーカスタマイズ（オプション）
       ============================================ */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    ::-webkit-scrollbar-track {
        background: var(--tech-white);
    }
    ::-webkit-scrollbar-thumb {
        background: var(--deep-navy);
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: var(--cyan-bright);
    }
</style>
"""


def render_sidebar():
    """共通サイドバーナビゲーションを描画"""
    import streamlit as st
    
    with st.sidebar:
        st.markdown("## 📚 メニュー")
        st.markdown("---")
        
        if st.button("🏠 ホーム", use_container_width=True, key="nav_home"):
            st.switch_page("app.py")
        
        if st.button("🤖 AI早わかりガイド", use_container_width=True, key="nav_ai_guide"):
            st.switch_page("pages/ai_guide.py")
        
        st.markdown("### 📊 市場調査レポート")
        
        if st.button("🏢 Anthropic企業情報", use_container_width=True, key="nav_anthropic"):
            st.switch_page("pages/anthropic_info.py")
        
        if st.button("🔧 AI保守基盤", use_container_width=True, key="nav_maintenance"):
            st.switch_page("pages/maintenance_ai_info.py")
        
        st.markdown("---")
        st.markdown(
            """
            <div style="color: #888; font-size: 0.8rem; text-align: center;">
                毎朝6時に自動更新<br>
                Powered by Gemini AI
            </div>
            """,
            unsafe_allow_html=True
        )