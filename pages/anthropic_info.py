import streamlit as st
import sys
import os

# プロジェクトルートをパスに追加
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from styles import get_custom_css, render_sidebar

# ページ設定（サイドバーを常に展開）
st.set_page_config(
    page_title="Anthropic企業情報 | AI Daily News",
    layout="wide",
    initial_sidebar_state="expanded"
)

# カスタムCSS適用
st.markdown(get_custom_css(), unsafe_allow_html=True)

# サイドバーナビゲーション
render_sidebar()

st.markdown("# 市場調査レポート：ANTHROPIC")

st.markdown("---")

# エグゼクティブ・サマリー
st.markdown("## 1. エグゼクティブ・サマリー")
st.markdown("""
Anthropicは、2021年にOpenAIの元メンバーによって設立されたAI安全性と研究企業である。大規模言語モデル「Claude」を開発し、OpenAIのChatGPT等と競合する高性能モデルとして市場での存在感を高めている。AmazonとGoogleからの大規模な資金調達により急成長を遂げ、倫理的AI開発と信頼性のあるAIシステム構築を重視している。
""")

st.markdown("---")

# 主要トレンドと市場背景
st.markdown("## 2. 主要トレンドと市場背景")

with st.expander("**倫理的AI開発の加速**", expanded=True):
    st.markdown("""
    Anthropicは、OpenAIの元幹部が倫理的AI開発を重視するビジョンに基づき設立された。責任あるAIの使用を企業理念とし、独自の「Claude's Constitution（憲法的AI）」を提唱するなど、AIの潜在能力と社会的責任のバランスを重視するトレンドを牽引している。同社の企業名の和訳が「人類または人類の存在期間に関連するさま」であることからも、人類の長期的な未来を見据えたAI開発を主軸としていることが示唆される。
    """)

with st.expander("**高性能大規模言語モデル（LLM）の競争激化**"):
    st.markdown("""
    Anthropicが開発した「Claude」は、OpenAIのGPT、GoogleのGemini、xAIのGrokと並ぶ高性能AIモデルとして市場シェアを拡大している。2023年6月時点で、AIモデルへの関心度においてOpenAIのGPTが91%を占める中、Anthropicへの関心は前四半期と比較して15%にまで上昇しており、この分野における競争が激化していることを示唆する。
    """)

with st.expander("**AIスタートアップへの大規模投資**"):
    st.markdown("""
    Anthropicは、GoogleやSalesforceなどから4.5億ドルを調達したのを皮切りに、わずか1年足らずで総額73億ドル（約1兆円）もの投資を獲得した。特にAmazonから累計80億ドル、Googleから最大20億ドル（5億ドル出資、追加15億ドル約束）の出資を受けるなど、AI技術開発への大規模な投資が市場を牽引している。
    """)

with st.expander("**クラウドプロバイダーとの戦略的提携**"):
    st.markdown("""
    AmazonはAnthropicへの巨額投資の一環として、AnthropicがAmazon Web Services (AWS) を主要なクラウドプロバイダーとして使用し、AWSの顧客がそのAIモデルを利用できるようにする戦略的提携を結んだ。これにより、AIモデルの普及と利用拡大に向けたエコシステム構築が加速している。
    """)

st.markdown("---")

# 主要プレイヤーと動向
st.markdown("## 3. 主要プレイヤーと動向")

players_data = {
    "企業名": ["Anthropic", "OpenAI", "Google AI / DeepMind", "Amazon", "xAI"],
    "最新の取り組み": [
        "OpenAIの元幹部によって2021年に設立。Claude 1（2023年3月）、Claude 2（2023年7月）、Claude 3.5 Sonnetなどをリリース。Amazonから累計80億ドル、Googleから最大20億ドルの出資を受ける。ルワンダ政府と提携し、Claudeベースの学習コンパニオン「Chidi」を提供。",
        "GPTシリーズを開発し、AIモデルへの関心度で市場をリード（2023年6月時点で91%）。Anthropicの主要な競合企業の一つ。",
        "Anthropicに最大20億ドルの出資。自社でも大規模言語モデル「Gemini」を開発し、Claudeと競合。",
        "Anthropicに累計80億ドルを出資し、主要な株主に。AnthropicをAWSエコシステムに統合し、AWS顧客にAIモデルを提供。",
        "Grokを開発し、ClaudeやGPTと競合する新たなAIプレイヤー。"
    ]
}

import pandas as pd
df_players = pd.DataFrame(players_data)
st.dataframe(df_players, use_container_width=True, hide_index=True)

st.markdown("---")

# 戦略的インサイト
st.markdown("## 4. 戦略的インサイト")

st.markdown("""
Anthropicは、倫理的AI開発という明確なビジョンと、OpenAIの元メンバーによる技術的専門性を基盤に、LLM市場で急速な存在感を確立した。特に、AmazonとGoogleという巨大テック企業からの大規模な資金調達と戦略的提携は、同社の技術開発、市場投入、そしてエコシステムへの組み込みを強力に推進する原動力となっている。

今後の戦略としては、以下の点が重要である。
""")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    ### 1️⃣ 「信頼と倫理」のブランド確立
    
    競合他社が性能競争に注力する中、Anthropicは「信頼性、解釈可能性、操縦可能性のあるAIシステム」という独自の強みをさらに強化すべきである。独自の「Claude's Constitution」を具体的な製品機能や利用ガイドラインに落とし込み、企業や公共機関が安心して導入できるAIとしてのブランドイメージを確立することが、差別化の鍵となる。
    """)

with col2:
    st.markdown("""
    ### 2️⃣ 垂直統合型パートナーシップの深化
    
    Amazon AWSとの提携をさらに深め、特定の産業やユースケースに特化したソリューションを共同開発することで、市場への浸透を加速させるべきである。金融、医療、教育といった分野で、規制準拠や倫理的配慮が特に求められるAIアプリケーションにおいて、Anthropicの強みを最大限に活かすことが可能である。
    """)

with col3:
    st.markdown("""
    ### 3️⃣ グローバル展開の加速
    
    アフリカ大陸での教育イニシアティブは、新興市場における大きな可能性を示している。先進国市場での競争が激化する中で、AI技術への需要が高まる新興市場でのプレゼンスを早期に確立することで、長期的な成長基盤を構築できる。現地の文化やニーズに合わせたローカライズ戦略が成功の鍵となる。
    """)

st.markdown("---")

st.info("""
💡 **結論**: Anthropicは、単なる高性能AIモデルの提供者にとどまらず、「責任あるAI」の標準を確立し、その普及を牽引するリーダーとしての地位を築くことで、持続的な競争優位性を確立できるだろう。
""")

st.markdown("---")

# フッター
st.markdown("""
<div style="text-align: center; color: #999; padding: 2rem 0;">
    <p>AI Daily News © 2025 | 最終更新: 2025年12月</p>
</div>
""", unsafe_allow_html=True)

# 戻るボタン（下部）
if st.button("⬅️ AI早わかりガイドに戻る", key="back_bottom", use_container_width=False):
    st.switch_page("pages/ai_guide.py")
