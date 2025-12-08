import streamlit as st

st.set_page_config(page_title="AI早わかりガイド", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
.ai-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    color: white;
}
.ai-card h3 { margin: 0 0 0.5rem 0; }
.ai-card p { margin: 0; opacity: 0.9; }
.comparison-table { font-size: 0.9rem; }
.tag-best { background: #10b981; color: white; padding: 2px 8px; border-radius: 4px; font-size: 0.75rem; }
.tag-good { background: #3b82f6; color: white; padding: 2px 8px; border-radius: 4px; font-size: 0.75rem; }
</style>
""", unsafe_allow_html=True)

st.markdown("# 🤖 AI早わかりガイド")
st.markdown("**どのAIを使えばいい？** 目的別に最適なAIを解説します")

st.markdown("---")

# ============================================
# クイック選択
# ============================================
st.markdown("## ⚡ 30秒で選ぶ")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    ### 🎯 コードを書く
    **Claude** か **Cursor**
    
    理由: コード理解力が最も高く、長いコードも正確に扱える
    """)
    st.link_button("Claude を開く", "https://claude.ai/new", type="primary")

with col2:
    st.markdown("""
    ### 🔍 調べ物・検索
    **Perplexity** か **Gemini**
    
    理由: Web検索と統合されており、ソース付きで回答
    """)
    st.link_button("Perplexity を開く", "https://www.perplexity.ai/", type="primary")

with col3:
    st.markdown("""
    ### 💬 なんでも相談
    **ChatGPT**
    
    理由: 最もバランスが良く、幅広い用途に対応
    """)
    st.link_button("ChatGPT を開く", "https://chat.openai.com/", type="primary")

st.markdown("---")

# ============================================
# AI比較表
# ============================================
st.markdown("## 📊 主要AI比較")

comparison_data = {
    "AI": ["Claude", "ChatGPT", "Gemini", "Perplexity", "DeepSeek", "Mistral"],
    "得意分野": [
        "コード生成・長文理解",
        "汎用・バランス型",
        "Google連携・マルチモーダル",
        "Web検索・リサーチ",
        "数学・コード（低コスト）",
        "オープンソース・自社運用"
    ],
    "コード力": ["⭐⭐⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐", "⭐⭐⭐⭐⭐", "⭐⭐⭐⭐"],
    "推論力": ["⭐⭐⭐⭐⭐", "⭐⭐⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐⭐"],
    "速度": ["⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐⭐⭐", "⭐⭐⭐⭐⭐"],
    "無料枠": ["あり", "あり", "あり", "あり", "あり", "あり"],
    "URL": [
        "https://claude.ai/new",
        "https://chat.openai.com/",
        "https://gemini.google.com/app",
        "https://www.perplexity.ai/",
        "https://chat.deepseek.com/",
        "https://chat.mistral.ai/"
    ]
}

import pandas as pd
df = pd.DataFrame(comparison_data)
st.dataframe(df.drop(columns=["URL"]), use_container_width=True, hide_index=True)

st.markdown("---")

# ============================================
# 各AI詳細
# ============================================
st.markdown("## 📖 各AIの特徴")

# Claude
with st.expander("🟣 **Claude** (Anthropic) - コーディング最強", expanded=True):
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
        **こんな人におすすめ:**
        - コードを書いてほしい
        - 長いドキュメントを読んで要約してほしい
        - 論理的で正確な回答がほしい
        
        **モデルの違い:**
        | モデル | 特徴 |
        |--------|------|
        | **Opus 4.5** | 最高性能。複雑な推論・長いコード |
        | **Sonnet 4** | バランス型。日常使いに最適 |
        | **Haiku** | 高速・低コスト。簡単なタスク向け |
        
        **弱点:** Web検索できない、画像生成できない
        """)
    with col2:
        st.link_button("🚀 Claude を開く", "https://claude.ai/new", type="primary", use_container_width=True)
        st.caption("無料: Sonnet 4が使える")

# ChatGPT
with st.expander("🟢 **ChatGPT** (OpenAI) - 万能型"):
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
        **こんな人におすすめ:**
        - 何でも聞きたい（汎用性重視）
        - 画像生成もしたい（DALL-E連携）
        - プラグインで機能拡張したい
        
        **モデルの違い:**
        | モデル | 特徴 |
        |--------|------|
        | **GPT-4o** | 最新。マルチモーダル対応 |
        | **GPT-4** | 高性能。複雑なタスク向け |
        | **GPT-3.5** | 無料版。簡単なタスク向け |
        
        **弱点:** 長いコードで精度が落ちることがある
        """)
    with col2:
        st.link_button("🚀 ChatGPT を開く", "https://chat.openai.com/", type="primary", use_container_width=True)
        st.caption("無料: GPT-4oが制限付きで使える")

# Gemini
with st.expander("🔵 **Gemini** (Google) - Google連携最強"):
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
        **こんな人におすすめ:**
        - Googleサービスと連携したい
        - 最新情報を検索しながら聞きたい
        - YouTubeの要約がしたい
        
        **モデルの違い:**
        | モデル | 特徴 |
        |--------|------|
        | **Gemini 2.5 Pro** | 最高性能。100万トークン |
        | **Gemini 2.5 Flash** | 高速。API向け |
        | **Deep Think** | 複雑な推論特化 |
        
        **弱点:** コード生成はClaudeに劣る
        """)
    with col2:
        st.link_button("🚀 Gemini を開く", "https://gemini.google.com/app", type="primary", use_container_width=True)
        st.caption("無料: Gemini 2.5 Proが使える")

# Perplexity
with st.expander("🟠 **Perplexity** - AI検索エンジン"):
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
        **こんな人におすすめ:**
        - 最新情報を調べたい
        - ソース（出典）付きで回答がほしい
        - Google検索の代わりに使いたい
        
        **特徴:**
        - リアルタイムWeb検索
        - 回答に必ずソースURLが付く
        - 複数のAIモデルを切り替え可能
        
        **弱点:** コード生成は専門外
        """)
    with col2:
        st.link_button("🚀 Perplexity を開く", "https://www.perplexity.ai/", type="primary", use_container_width=True)
        st.caption("無料: 1日の検索数に制限あり")

# DeepSeek
with st.expander("⚫ **DeepSeek** - 高性能オープンソース"):
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
        **こんな人におすすめ:**
        - 無料で高性能AIを使いたい
        - 数学・コーディングに使いたい
        - 中国発でも気にしない
        
        **特徴:**
        - MITライセンスでオープンソース
        - GPT-4レベルの性能を無料で
        - 数学・コード特化
        
        **弱点:** 日本語は若干弱い、中国サーバー
        """)
    with col2:
        st.link_button("🚀 DeepSeek を開く", "https://chat.deepseek.com/", type="primary", use_container_width=True)
        st.caption("無料: 制限ほぼなし")

# Mistral
with st.expander("🔴 **Mistral** - 欧州発オープンソース"):
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
        **こんな人におすすめ:**
        - 自社サーバーで動かしたい
        - EUのデータ規制を遵守したい
        - オープンソースを重視
        
        **特徴:**
        - Apache 2.0ライセンス
        - 自社環境にデプロイ可能
        - 機密コードも安心
        
        **弱点:** 日本語対応は発展途上
        """)
    with col2:
        st.link_button("🚀 Mistral を開く", "https://chat.mistral.ai/", type="primary", use_container_width=True)
        st.caption("無料: 基本機能は無料")

st.markdown("---")

# ============================================
# 使い分けチャート
# ============================================
st.markdown("## 🎯 目的別おすすめ")

use_cases = {
    "目的": [
        "🖥️ コードを書いてほしい",
        "🐛 バグを直してほしい", 
        "📄 長い文章を要約",
        "🔍 最新情報を調べる",
        "📊 データ分析",
        "✍️ 文章を書く",
        "🎨 画像を生成",
        "🏢 社内で安全に使う",
    ],
    "1st": [
        "Claude",
        "Claude / Cursor",
        "Claude",
        "Perplexity",
        "ChatGPT",
        "ChatGPT",
        "ChatGPT (DALL-E)",
        "Mistral / DeepSeek",
    ],
    "2nd": [
        "DeepSeek",
        "ChatGPT",
        "Gemini",
        "Gemini",
        "Claude",
        "Claude",
        "Gemini (Imagen)",
        "Claude API",
    ],
    "理由": [
        "コード理解力が最も高い",
        "エラー分析と修正提案が優秀",
        "20万トークンの長文対応",
        "リアルタイムWeb検索",
        "Code Interpreterでコード実行",
        "自然な日本語",
        "DALL-E 3の品質が高い",
        "オープンソースで自社運用可",
    ]
}

df_usecase = pd.DataFrame(use_cases)
st.dataframe(df_usecase, use_container_width=True, hide_index=True)

st.markdown("---")

# フッター
st.caption("💡 このガイドは定期的に更新されます。最終更新: 2025年12月")

# ホームに戻るリンク
st.page_link("app.py", label="← AI司令塔ナレッジに戻る", icon="🏠")
