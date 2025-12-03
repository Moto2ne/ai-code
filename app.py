import streamlit as st
import time

# ページ設定（見た目をリッチに）
st.set_page_config(page_title="AI開発トレーニング | 魔王流", layout="wide", initial_sidebar_state="expanded")

# カスタムCSS（見た目をさらにリッチに）
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 2rem;
    }
    .chapter-card {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 8px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
    .bad-result {
        background: #fee;
        padding: 1rem;
        border-radius: 5px;
        border-left: 4px solid #f00;
    }
    .good-result {
        background: #efe;
        padding: 1rem;
        border-radius: 5px;
        border-left: 4px solid #0a0;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: bold;
        border: none;
        border-radius: 5px;
        padding: 0.5rem 1rem;
    }
</style>
""", unsafe_allow_html=True)

# サイドバー（コース風の見た目を作る）
st.sidebar.title("📚 コース一覧")
st.sidebar.markdown("---")

course = st.sidebar.radio(
    "学習するチャプターを選択",
    [
        "Chapter 1: 要件定義の破壊",
        "Chapter 2: エラー修正の極意",
        "Chapter 3: テスト自動化",
        "Chapter 4: リファクタリングの神髄",
        "Chapter 5: デバッグの哲学"
    ]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🎯 学習のポイント")
st.sidebar.info("""
**魔王流の核心:**
- AIは完璧ではない
- 構造化が全て
- 小さく始めて大きく育てる
- エラーは最高の教師
""")

# メインコンテンツ
st.markdown('<div class="main-header"><h1>🔥 AI Driven Dev - Simulation Mode</h1><p>従来のAI開発の常識を破壊する「魔王流」を学べ</p></div>', unsafe_allow_html=True)

# Chapter 1: 要件定義の破壊
if course == "Chapter 1: 要件定義の破壊":
    st.subheader("📖 Chapter 1: 要件定義の破壊")
    st.markdown("---")
    
    st.markdown("""
    <div class="chapter-card">
    <h3>🎯 学習目標</h3>
    <p>AIに丸投げするのではなく、<strong>構造化された指示</strong>を与えることで、実用的なコードを生成させる技術を習得する。</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("### 💭 シナリオ")
    st.info("💡 あなたは新しいツール開発をAIに依頼しようとしています。どのプロンプトを使いますか？")
    
    st.write("**Q. Excelデータを読み込んでグラフ化するアプリを作りたい場合、どの指示を選びますか？**")
    
    option = st.radio(
        "指示を選択してください:",
        (
            "A: 「Excelデータを読み込んでグラフ化するアプリを作って」と頼む",
            "B: 「まずは要件定義を行い、必要なファイル構成と設計概要を出力して」と頼む"
        ),
        label_visibility="collapsed"
    )
    
    if st.button("AIに指示を送る 🚀"):
        with st.spinner('AIが思考中...（GPT-4 Turbo）'):
            time.sleep(1.5)
        
        if "A:" in option:
            st.error("❌ **Bad Result - 従来のAI開発の常識**")
            st.markdown("""
            <div class="bad-result">
            <h4>何が起きたか:</h4>
            <ul>
                <li>AIは文脈を理解できず、動かないPythonコードを1つだけ出力</li>
                <li>ファイルパスがハードコードされ、エラーが発生</li>
                <li>依存関係が不明確で、環境構築ができない</li>
                <li>グラフの種類やスタイルが指定されていない</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
            
            st.code("""
import pandas as pd
import matplotlib.pyplot as plt

# エラー：ファイルパスが指定されていません...
df = pd.read_excel('data.xlsx')  # ← このファイルは存在しない
df.plot()  # ← どの列をグラフ化するの？
plt.show()  # ← Streamlitで動かない...
            """, language="python")
            
            st.warning("""
            **解説：** 丸投げすると、AIは『想像』でコードを書くため、実務では使えません。
            何度もやり直しが発生し、時間の無駄になります。
            """)
            
        else:
            st.success("⭕ **Perfect Result - 魔王流のアプローチ**")
            st.markdown("""
            <div class="good-result">
            <h4>何が起きたか:</h4>
            <ul>
                <li>AIは実装の前に、完璧な設計図を出力</li>
                <li>ファイル構成、依存関係、処理フローが明確化</li>
                <li>実装前に問題点を洗い出し、手戻りを防止</li>
                <li>段階的な実装計画が提示された</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            **設計図の出力例:**
            ```markdown
            # プロジェクト構成案
            
            /excel-graph-app
              ├── main.py (エントリーポイント)
              ├── utils/
              │   ├── data_loader.py (Excel読み込みロジック)
              │   └── graph_generator.py (グラフ生成ロジック)
              ├── config/
              │   └── settings.py (設定管理)
              ├── requirements.txt (依存関係)
              └── README.md (使用方法)
            
            # 処理フロー
            1. ファイルアップロード受付
            2. Excel形式検証
            3. データ読み込み（エラーハンドリング付き）
            4. グラフタイプ選択UI
            5. グラフ生成と表示
            ```
            """)
            
            st.success("""
            **解説：** このように構造化させることで、手戻りを防げます。
            AIは設計図を見ながら、段階的に実装できるようになります。
            これが『魔王流』の第一歩です。
            """)
    
    st.markdown("---")
    st.markdown("### 📝 魔王流のポイント")
    st.markdown("""
    1. **AIに設計をさせる**: コードを書かせる前に、設計図を描かせる
    2. **段階的に進める**: 一度に全部作らせず、小さな単位で進める
    3. **文脈を明確にする**: 曖昧な指示は、曖昧な結果を生む
    """)

# Chapter 2: エラー修正の極意
elif course == "Chapter 2: エラー修正の極意":
    st.subheader("📖 Chapter 2: エラー修正の極意")
    st.markdown("---")
    
    st.markdown("""
    <div class="chapter-card">
    <h3>🎯 学習目標</h3>
    <p>エラーメッセージを<strong>そのままAIに投げる</strong>のではなく、<strong>文脈と一緒に</strong>提示することで、的確な修正を引き出す技術を習得する。</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("### 💭 シナリオ")
    st.info("💡 あなたのコードでエラーが発生しました。AIに修正を依頼する際、どの方法を選びますか？")
    
    st.write("**Q. 以下のエラーが発生しました。どのようにAIに依頼しますか？**")
    
    st.code("""
FileNotFoundError: [Errno 2] No such file or directory: 'data.xlsx'
    at line 15 in data_loader.py
    """, language="python")
    
    option = st.radio(
        "依頼方法を選択してください:",
        (
            "A: 「FileNotFoundErrorが出た。直して」とエラーメッセージだけ送る",
            "B: 「以下のエラーが発生。コード全体と実行環境の情報も一緒に送る」"
        ),
        label_visibility="collapsed"
    )
    
    if st.button("AIに修正を依頼する 🔧"):
        with st.spinner('AIが思考中...（GPT-4 Turbo）'):
            time.sleep(2.0)
        
        if "A:" in option:
            st.error("❌ **Bad Result - 従来のAI開発の常識**")
            st.markdown("""
            <div class="bad-result">
            <h4>何が起きたか:</h4>
            <ul>
                <li>AIは表面的な修正のみ（ファイルパスをハードコード）</li>
                <li>根本原因を理解せず、別のエラーを誘発</li>
                <li>エラーハンドリングが追加されない</li>
                <li>再発防止策が提示されない</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
            
            st.code("""
# AIの回答（悪い例）
df = pd.read_excel('C:/Users/YourName/data.xlsx')  # ← ハードコード！
# これでは他の環境で動かない...
            """, language="python")
            
            st.warning("""
            **解説：** エラーメッセージだけでは、AIは文脈を理解できません。
            結果として、その場しのぎの修正しかできません。
            """)
            
        else:
            st.success("⭕ **Perfect Result - 魔王流のアプローチ**")
            st.markdown("""
            <div class="good-result">
            <h4>何が起きたか:</h4>
            <ul>
                <li>AIはコード全体を分析し、根本原因を特定</li>
                <li>エラーハンドリングとバリデーションを追加</li>
                <li>複数の解決策を提示（ファイル選択UI、デフォルトパス設定など）</li>
                <li>再発防止のためのベストプラクティスを提案</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            **AIの回答（良い例）:**
            ```python
            import os
            from pathlib import Path
            
            def load_excel_data(file_path=None):
                # 1. ファイルパスの検証
                if file_path is None:
                    # Streamlitのファイルアップローダーを使用
                    uploaded_file = st.file_uploader("Excelファイルを選択", type=['xlsx'])
                    if uploaded_file is None:
                        st.warning("ファイルが選択されていません")
                        return None
                    file_path = uploaded_file
                
                # 2. ファイル存在確認
                if isinstance(file_path, str) and not os.path.exists(file_path):
                    st.error(f"ファイルが見つかりません: {file_path}")
                    return None
                
                # 3. エラーハンドリング付きで読み込み
                try:
                    df = pd.read_excel(file_path)
                    st.success(f"データを読み込みました: {len(df)}行")
                    return df
                except Exception as e:
                    st.error(f"読み込みエラー: {str(e)}")
                    return None
            ```
            """)
            
            st.success("""
            **解説：** 文脈を一緒に送ることで、AIは根本的な解決策を提案できます。
            エラーは単なる問題ではなく、コードを改善する機会なのです。
            """)
    
    st.markdown("---")
    st.markdown("### 📝 魔王流のポイント")
    st.markdown("""
    1. **エラーだけ送らない**: コード全体、実行環境、期待する動作も一緒に送る
    2. **根本原因を探る**: 表面的な修正ではなく、なぜエラーが起きたかを理解させる
    3. **再発防止を考える**: エラーハンドリングとバリデーションを追加させる
    """)

# Chapter 3: テスト自動化
elif course == "Chapter 3: テスト自動化":
    st.subheader("📖 Chapter 3: テスト自動化")
    st.markdown("---")
    
    st.markdown("""
    <div class="chapter-card">
    <h3>🎯 学習目標</h3>
    <p>AIにコードを書かせた<strong>後</strong>にテストを書かせるのではなく、<strong>テストファースト</strong>で開発させることで、品質の高いコードを生成する技術を習得する。</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("### 💭 シナリオ")
    st.info("💡 あなたは新しい機能を実装しようとしています。AIにどの順序で依頼しますか？")
    
    st.write("**Q. ユーザー認証機能を実装する場合、どの順序でAIに依頼しますか？**")
    
    option = st.radio(
        "開発順序を選択してください:",
        (
            "A: まず実装コードを書かせ、後でテストを書かせる",
            "B: まずテストケースを書かせ、その後に実装コードを書かせる（TDD）"
        ),
        label_visibility="collapsed"
    )
    
    if st.button("AIに開発を依頼する 🧪"):
        with st.spinner('AIが思考中...（GPT-4 Turbo）'):
            time.sleep(2.0)
        
        if "A:" in option:
            st.error("❌ **Bad Result - 従来のAI開発の常識**")
            st.markdown("""
            <div class="bad-result">
            <h4>何が起きたか:</h4>
            <ul>
                <li>実装コードは書けたが、エッジケースが考慮されていない</li>
                <li>後からテストを書こうとすると、テストしにくい構造になっている</li>
                <li>テストカバレッジが低く、バグが残る可能性が高い</li>
                <li>リファクタリングが困難なコードになっている</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
            
            st.code("""
# 実装コード（悪い例）
def authenticate(username, password):
    if username == "admin" and password == "1234":
        return True
    return False
# 問題点：
# - パスワードが平文
# - エラーハンドリングなし
# - テストしにくい（外部依存あり）
            """, language="python")
            
            st.warning("""
            **解説：** 実装後にテストを書くと、テストしにくいコードになりがちです。
            また、エッジケースを見落としやすくなります。
            """)
            
        else:
            st.success("⭕ **Perfect Result - 魔王流のアプローチ**")
            st.markdown("""
            <div class="good-result">
            <h4>何が起きたか:</h4>
            <ul>
                <li>AIはまず要件を明確にするためのテストケースを作成</li>
                <li>テスト可能な設計で実装コードを生成</li>
                <li>エッジケースが網羅的にカバーされている</li>
                <li>リファクタリングしやすい構造になっている</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            **テストファーストの流れ:**
            
            **Step 1: テストケースの作成**
            ```python
            # test_auth.py
            import pytest
            from auth import authenticate, hash_password
            
            def test_authenticate_success():
                hashed = hash_password("correct_password")
                assert authenticate("user1", "correct_password", hashed) == True
            
            def test_authenticate_wrong_password():
                hashed = hash_password("correct_password")
                assert authenticate("user1", "wrong", hashed) == False
            
            def test_authenticate_empty_input():
                assert authenticate("", "") == False
            
            def test_authenticate_sql_injection_attempt():
                # セキュリティテスト
                assert authenticate("admin'; --", "password") == False
            ```
            
            **Step 2: テストを満たす実装コード**
            ```python
            # auth.py
            import hashlib
            import re
            
            def hash_password(password):
                return hashlib.sha256(password.encode()).hexdigest()
            
            def authenticate(username, password, stored_hash):
                # バリデーション
                if not username or not password:
                    return False
                
                # SQLインジェクション対策
                if re.search(r"[;'--]", username):
                    return False
                
                # 認証
                input_hash = hash_password(password)
                return input_hash == stored_hash
            ```
            """)
            
            st.success("""
            **解説：** テストファーストで開発することで、AIは要件を明確に理解し、
            テスト可能で保守しやすいコードを生成します。
            これが『魔王流』の品質保証の極意です。
            """)
    
    st.markdown("---")
    st.markdown("### 📝 魔王流のポイント")
    st.markdown("""
    1. **テストファースト**: 実装の前にテストを書かせる
    2. **要件の明確化**: テストケースが要件定義書の役割も果たす
    3. **品質の担保**: テスト可能な設計が、保守しやすいコードを生む
    """)

# Chapter 4: リファクタリングの神髄
elif course == "Chapter 4: リファクタリングの神髄":
    st.subheader("📖 Chapter 4: リファクタリングの神髄")
    st.markdown("---")
    
    st.markdown("""
    <div class="chapter-card">
    <h3>🎯 学習目標</h3>
    <p>AIに「リファクタリングして」と丸投げするのではなく、<strong>具体的な改善点</strong>を指示することで、効果的なリファクタリングを実現する技術を習得する。</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("### 💭 シナリオ")
    st.info("💡 あなたは既存のコードをリファクタリングしたいと考えています。AIにどのように依頼しますか？")
    
    st.write("**Q. 以下のコードをリファクタリングする場合、どの指示を選びますか？**")
    
    st.code("""
def process_data(data):
    result = []
    for item in data:
        if item['status'] == 'active':
            if item['type'] == 'premium':
                result.append(item['name'].upper() + ' - PREMIUM')
            else:
                result.append(item['name'].upper())
    return result
    """, language="python")
    
    option = st.radio(
        "指示を選択してください:",
        (
            "A: 「このコードをリファクタリングして」とだけ頼む",
            "B: 「可読性を向上させ、DRY原則に従い、型ヒントを追加してリファクタリングして」と具体的に指示する"
        ),
        label_visibility="collapsed"
    )
    
    if st.button("AIにリファクタリングを依頼する 🔄"):
        with st.spinner('AIが思考中...（GPT-4 Turbo）'):
            time.sleep(2.0)
        
        if "A:" in option:
            st.error("❌ **Bad Result - 従来のAI開発の常識**")
            st.markdown("""
            <div class="bad-result">
            <h4>何が起きたか:</h4>
            <ul>
                <li>AIは表面的な変更のみ（変数名の変更など）</li>
                <li>根本的な問題（ネストの深さ、重複コード）が残る</li>
                <li>意図が不明確で、かえって読みにくくなる可能性</li>
                <li>テストが壊れるリスクがある</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
            
            st.code("""
# AIの回答（悪い例）
def process_data(data):
    output = []
    for element in data:
        if element['status'] == 'active':
            if element['type'] == 'premium':
                output.append(element['name'].upper() + ' - PREMIUM')
            else:
                output.append(element['name'].upper())
    return output
# 問題点：
# - ネストが深いまま
# - 重複コード（.upper()）が残る
# - 型情報がない
            """, language="python")
            
            st.warning("""
            **解説：** 曖昧な指示では、AIは何を改善すべきか理解できません。
            結果として、表面的な変更に留まってしまいます。
            """)
            
        else:
            st.success("⭕ **Perfect Result - 魔王流のアプローチ**")
            st.markdown("""
            <div class="good-result">
            <h4>何が起きたか:</h4>
            <ul>
                <li>AIは具体的な改善点を理解し、構造的なリファクタリングを実施</li>
                <li>DRY原則に従い、重複コードを関数化</li>
                <li>型ヒントを追加し、可読性と保守性が向上</li>
                <li>早期リターンでネストを浅くし、理解しやすくなった</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            **リファクタリング結果:**
            ```python
            from typing import List, Dict, Any

            def format_name(name: str, is_premium: bool = False) -> str:
                \"\"\"名前をフォーマットする\"\"\"
                formatted = name.upper()
                if is_premium:
                    formatted += ' - PREMIUM'
                return formatted

            def is_active_item(item: Dict[str, Any]) -> bool:
                \"\"\"アイテムがアクティブかどうかを判定\"\"\"
                return item.get('status') == 'active'

            def process_data(data: List[Dict[str, Any]]) -> List[str]:
                \"\"\"アクティブなアイテムの名前を処理する\"\"\"
                result = []
                for item in data:
                    if not is_active_item(item):
                        continue
                    
                    is_premium = item.get('type') == 'premium'
                    formatted_name = format_name(item['name'], is_premium)
                    result.append(formatted_name)
                
                return result
            ```
            
            **改善点:**
            - ✅ 型ヒントで意図が明確
            - ✅ 関数分割で単一責任原則を遵守
            - ✅ 早期リターンでネストを削減
            - ✅ DRY原則で重複を排除
            - ✅ ドキュメンテーション追加
            """)
            
            st.success("""
            **解説：** 具体的な指示を与えることで、AIは構造的な改善を実施できます。
            リファクタリングは単なる書き直しではなく、コードの品質向上なのです。
            """)
    
    st.markdown("---")
    st.markdown("### 📝 魔王流のポイント")
    st.markdown("""
    1. **具体的な指示**: 「リファクタリングして」ではなく、「何を改善するか」を明確に
    2. **原則の提示**: DRY、SOLID原則など、具体的な原則を指示に含める
    3. **段階的な改善**: 一度に全部変えず、小さな改善を積み重ねる
    """)

# Chapter 5: デバッグの哲学
elif course == "Chapter 5: デバッグの哲学":
    st.subheader("📖 Chapter 5: デバッグの哲学")
    st.markdown("---")
    
    st.markdown("""
    <div class="chapter-card">
    <h3>🎯 学習目標</h3>
    <p>バグが発生した際に、AIに「直して」と頼むのではなく、<strong>原因分析を一緒に行う</strong>ことで、根本的な解決と学習を実現する技術を習得する。</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("### 💭 シナリオ")
    st.info("💡 あなたのアプリケーションで予期しない動作が発生しています。AIにどのように依頼しますか？")
    
    st.write("**Q. ユーザー登録機能で、同じメールアドレスで複数回登録できてしまうバグを発見しました。どのようにAIに依頼しますか？**")
    
    option = st.radio(
        "依頼方法を選択してください:",
        (
            "A: 「同じメールで複数回登録できるバグがある。直して」とだけ頼む",
            "B: 「同じメールで複数回登録できる問題を発見。原因分析と修正案を提示して。テストケースも追加して」と詳しく頼む"
        ),
        label_visibility="collapsed"
    )
    
    if st.button("AIにデバッグを依頼する 🐛"):
        with st.spinner('AIが思考中...（GPT-4 Turbo）'):
            time.sleep(2.5)
        
        if "A:" in option:
            st.error("❌ **Bad Result - 従来のAI開発の常識**")
            st.markdown("""
            <div class="bad-result">
            <h4>何が起きたか:</h4>
            <ul>
                <li>AIは表面的な修正のみ（チェックを追加）</li>
                <li>根本原因（データベース設計の問題）が残る</li>
                <li>他の類似バグが発見されない</li>
                <li>テストケースが追加されず、再発のリスクがある</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
            
            st.code("""
# AIの回答（悪い例）
def register_user(email, password):
    # チェックを追加（表面的な修正）
    if email in existing_users:
        return "既に登録されています"
    # 問題点：
    # - データベースのユニーク制約がない
    # - レースコンディションの可能性
    # - 他の類似問題が残る
            """, language="python")
            
            st.warning("""
            **解説：** 表面的な修正では、根本原因が残り、別のバグを誘発する可能性があります。
            また、同じような問題が他の箇所にも潜んでいる可能性があります。
            """)
            
        else:
            st.success("⭕ **Perfect Result - 魔王流のアプローチ**")
            st.markdown("""
            <div class="good-result">
            <h4>何が起きたか:</h4>
            <ul>
                <li>AIは根本原因を分析し、データベース設計の問題を指摘</li>
                <li>複数の解決策を提示（アプリケーション層とDB層の両方）</li>
                <li>レースコンディションなどの潜在的な問題も発見</li>
                <li>包括的なテストケースを追加し、再発を防止</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            **AIの分析と修正:**
            
            **Step 1: 原因分析**
            ```python
            # 問題点の分析
            1. データベースにユニーク制約がない
            2. アプリケーション層でのチェックのみでは不十分（レースコンディション）
            3. エラーハンドリングが不適切
            ```
            
            **Step 2: 根本的な修正**
            ```python
            # データベースマイグレーション
            ALTER TABLE users ADD UNIQUE INDEX idx_email (email);
            
            # アプリケーションコード
            from sqlalchemy.exc import IntegrityError
            
            def register_user(email: str, password: str) -> dict:
                \"\"\"ユーザー登録(重複チェック付き)\"\"\"
                # 1. 事前バリデーション
                if not is_valid_email(email):
                    return {\"success\": False, \"error\": \"無効なメールアドレス\"}
                
                # 2. 重複チェック(アプリケーション層)
                if user_exists(email):
                    return {\"success\": False, \"error\": \"既に登録されています\"}
                
                # 3. 登録処理(DB層の制約も活用)
                try:
                    new_user = User(email=email, password=hash_password(password))
                    db.session.add(new_user)
                    db.session.commit()
                    return {\"success\": True, \"user_id\": new_user.id}
                except IntegrityError:
                    # DB層での重複検出(レースコンディション対策)
                    db.session.rollback()
                    return {\"success\": False, \"error\": \"既に登録されています\"}
            ```
            
            **Step 3: テストケースの追加**
            ```python
            def test_duplicate_email_registration():
                \"\"\"同じメールでの重複登録を防ぐテスト\"\"\"
                register_user(\"test@example.com\", \"password1\")
                result = register_user(\"test@example.com\", \"password2\")
                assert result[\"success\"] == False
                assert \"既に登録されています\" in result[\"error\"]
            
            def test_concurrent_registration():
                \"\"\"並行登録のテスト(レースコンディション)\"\"\"
                # マルチスレッドで同時登録を試みる
                # DB層の制約で防げることを確認
            ```
            """)
            
            st.success("""
            **解説：** 原因分析を一緒に行うことで、AIは根本的な解決策を提案できます。
            デバッグは単なる修正ではなく、システムを改善する機会なのです。
            これが『魔王流』のデバッグ哲学です。
            """)
    
    st.markdown("---")
    st.markdown("### 📝 魔王流のポイント")
    st.markdown("""
    1. **原因分析を一緒に**: 「直して」ではなく、「なぜ起きたか」を分析させる
    2. **根本的な解決**: 表面的な修正ではなく、設計レベルでの改善を求める
    3. **再発防止**: テストケースを追加し、同じ問題が起きないようにする
    4. **学習の機会**: バグから学び、システム全体を改善する
    """)

# フッター
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem;">
    <p>🔥 <strong>魔王流 AI開発トレーニング</strong> 🔥</p>
    <p>従来のAI開発の常識を破壊し、実用的なスキルを習得せよ</p>
</div>
""", unsafe_allow_html=True)

