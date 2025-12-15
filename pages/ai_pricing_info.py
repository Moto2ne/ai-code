import streamlit as st
import sys
import os
import pandas as pd

# プロジェクトルートをパスに追加
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from styles import get_custom_css, render_sidebar

# ページ設定（サイドバーを常に展開）
st.set_page_config(
    page_title="AIモデル性能と価格 | AI Daily News",
    layout="wide",
    initial_sidebar_state="expanded"
)

# カスタムCSS適用
st.markdown(get_custom_css(), unsafe_allow_html=True)

# サイドバーナビゲーション
render_sidebar()

st.markdown("# 市場調査レポート：AIモデルの性能とトークン単価")

st.markdown("---")

# エグゼクティブ・サマリー
st.markdown("## 1. エグゼクティブ・サマリー")
st.markdown("""
AIモデルの利用コストは、**トークン単価**と**モデル性能**に直結する。特に従量課金制の下では、トークン管理がROIを左右する中核指標となる。高性能モデルは高単価だが、タスクによっては総合的なコスト効率に優れるため、**ユースケースに応じた最適なモデル選定とトークン最適化**が不可欠である。
""")

st.markdown("---")

# 主要トレンドと市場背景
st.markdown("## 2. 主要トレンドと市場背景")

with st.expander("💰 API従量課金モデルの主流化", expanded=True):
    st.markdown("""
    多くの生成AIプラットフォームは、**入力・出力トークン数に応じた従量課金制**を採用している。
    
    プロンプトの冗長性や出力の長さが直接的な請求額に反映されるため、**「トークン＝実質通貨」**として認識されている。
    """)

with st.expander("📊 トークン管理の重要性", expanded=True):
    st.markdown("""
    トークンは生成AIにおける最小単位であり、以下の3つの側面からその重要性が高まっている：
    
    1. **コスト管理**: 月額予算の正確な見積もり
    2. **処理品質**: モデルの性能を最大限に活用
    3. **リスク管理**: コンテキストウィンドウ上限の回避
    
    トークン数の把握は、これら全ての基礎となる。
    """)

with st.expander("🔄 コンテキストウィンドウ上限と処理品質", expanded=True):
    st.markdown("""
    AIモデルには一度に処理できるトークン量の上限（**コンテキストウィンドウ**）が存在する。
    
    **上限を超過した場合の影響:**
    - 入力の一部が無視される
    - 回答が途中で途切れる
    - 処理品質が著しく低下する
    
    長文処理や複雑な会話には、広いコンテキストウィンドウを持つモデルの選択が重要である。
    """)

with st.expander("⚖️ 性能あたりのコストパフォーマンス重視", expanded=True):
    st.markdown("""
    単純なトークン単価だけでなく、**モデルの性能とタスクの要求水準**を考慮したコストパフォーマンスが重視されている。
    
    **重要な考慮点:**
    - 安価なモデルでも高度な推論には再試行や追加計算が必要になる場合がある
    - 結果として、高精度モデルの方が総合的な利用コストを抑えられる可能性がある
    - タスクの複雑度に応じた適切なモデル選択が、最終的なROIを向上させる
    """)

st.markdown("---")

# 主要プレイヤーと動向
st.markdown("## 3. 主要プレイヤーと動向")

st.markdown("### 💵 トークン単価比較（2025年8月時点）")

pricing_data = {
    "企業": [
        "OpenAI",
        "OpenAI",
        "Anthropic",
        "Anthropic",
        "Anthropic",
        "Google",
        "Google",
        "RINNA",
        "Cohere"
    ],
    "モデル": [
        "GPT-4o",
        "GPT-4o mini",
        "Claude 3 Opus",
        "Claude 3 Sonnet",
        "Claude 3 Haiku",
        "Gemini 1.5 Pro",
        "Gemini 1.5 Flash",
        "日本語特化モデル",
        "Enterprise Model"
    ],
    "入力単価": [
        "$5.00/1M",
        "$0.15/1M",
        "$15.00/1M",
        "$3.00/1M",
        "$0.25/1M",
        "$3.50/1M",
        "$0.35/1M",
        "$0.0003～0.002/1K",
        "$1.00/1M"
    ],
    "出力単価": [
        "$15.00/1M",
        "$0.60/1M",
        "$75.00/1M",
        "$15.00/1M",
        "$1.25/1M",
        "$10.50/1M",
        "$1.05/1M",
        "-",
        "$2.00/1M"
    ],
    "特徴": [
        "高精度、幅広い用途対応",
        "軽量・低コスト、PoCに最適",
        "最高精度、長文・複雑推論",
        "精度と料金のバランス",
        "低コスト、日常業務向け",
        "高性能、Workspace連携",
        "高速・低価格",
        "日本語理解に優れる",
        "カスタマイズ性高い"
    ]
}

df_pricing = pd.DataFrame(pricing_data)

# スタイル付きデータフレーム
st.dataframe(
    df_pricing,
    use_container_width=True,
    hide_index=True,
    column_config={
        "企業": st.column_config.TextColumn("企業", width="medium"),
        "モデル": st.column_config.TextColumn("モデル", width="medium"),
        "入力単価": st.column_config.TextColumn("入力単価", width="medium"),
        "出力単価": st.column_config.TextColumn("出力単価", width="medium"),
        "特徴": st.column_config.TextColumn("特徴", width="large")
    }
)

st.info("💡 **注意**: 単価は1Mトークンあたりの料金（一部を除く）。為替変動は考慮していない。最新の料金は各プロバイダーの公式サイトを参照してください。")

st.markdown("---")

# 各社の詳細情報
st.markdown("### 📋 各社の最新動向")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("#### 🟢 OpenAI")
    st.markdown("""
    - **GPT-4o**: 高精度で幅広い用途に対応
    - **GPT-4o mini**: 軽量・低コストでPoCや社内ボットに最適
    - 広く利用され、多くの開発ツールやライブラリが対応
    - 豊富なドキュメントとコミュニティサポート
    """)

with col2:
    st.markdown("#### 🟠 Anthropic")
    st.markdown("""
    - **Claude 3 Opus**: 高精度で長文処理・複雑推論に優れる
    - **Claude 3 Sonnet**: 精度と料金のバランスが良い中間モデル
    - **Claude 3 Haiku**: 低コストで日常業務向け
    - 最大200Kトークンの広い文脈窓
    """)

with col3:
    st.markdown("#### 🔵 Google")
    st.markdown("""
    - **Gemini 1.5 Pro**: 高性能でWorkspace連携が可能
    - **Gemini 1.5 Flash**: 高速・低価格が特徴
    - Google Cloud Platform統合
    - マルチモーダル対応（テキスト・画像・音声）
    """)

st.markdown("---")

# 戦略的インサイト
st.markdown("## 4. 戦略的インサイト")

st.info("💡 生成AIの導入効果を最大化するためには、単にトークン単価の低さでモデルを選択するのではなく、以下の戦略的視点を持つべきである。")

st.markdown("### 1️⃣ ユースケースに応じた多角的なモデル選定")
st.markdown("""
プロジェクトの目的、求められる精度、処理速度、コンテキスト長、予算を総合的に評価し、最適なAIモデルを選定すべきである。

**推奨される使い分け:**
- **PoCや社内ボット**: GPT-4o mini、Claude 3 Haiku
- **複雑な法務文書の分析**: Claude 3 Opus、GPT-4o
- **高度な推論タスク**: Claude 3 Opus、GPT-4o
- **大量の軽量タスク**: Gemini 1.5 Flash、GPT-4o mini
- **日本語特化**: RINNA（文脈理解重視の場合）

目的に応じたモデルの使い分けが、コスト効率と品質の最大化に繋がる。
""")

st.markdown("### 2️⃣ 徹底したトークン管理と最適化")
st.markdown("""
トークン削減・最適化テクニックを積極的に導入すべきである。

**具体的な最適化手法:**
- ✂️ **プロンプトの簡潔化**: 不要な説明や冗長な表現を削除
- 🧹 **入力テキストの前処理**: 余分な空白、改行、特殊文字の削除
- 📦 **チャンク分割**: 長文を適切なサイズに分割して処理
- 🔄 **コンテキスト再利用**: 繰り返し使用する情報をキャッシュ
- 📏 **出力長の制限**: 必要最小限の出力長を指定

これにより、従量課金制におけるコストを抑制し、ROIを向上させることが可能となる。
""")

st.markdown("### 3️⃣ 継続的な市場と利用状況のモニタリング")
st.markdown("""
AIモデルの性能向上や料金体系は急速に変化している。

**必要なアクション:**
- 📅 定期的に市場の最新動向を調査
- 📊 自社のAI利用状況を継続的にモニタリング
  - トークン消費量
  - モデル性能
  - 実際のコスト
- 🔄 常に最適なモデルと利用戦略を維持・更新

特に、**国産AIサービス**は日本語処理に優れるが、国際サービスと比較して単価が高い傾向があるため、利用シーンに応じた費用対効果の検証が重要である。
""")

st.markdown("---")

# まとめ
st.success("""
**🎯 まとめ**

AIモデルの選定においては、単価だけでなく、性能・用途・総合的なコスト効率を考慮した戦略的判断が不可欠である。
適切なトークン管理と継続的な最適化により、AI投資のROIを最大化できる。
""")

st.markdown("---")

# フッター
st.markdown(
    """
    <div style="text-align: center; color: #999; padding: 1rem 0;">
        <p>AI Daily News | 市場調査レポートシリーズ</p>
    </div>
    """,
    unsafe_allow_html=True
)
