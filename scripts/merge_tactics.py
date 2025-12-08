"""
新しい戦術データをai_tactics.jsonにマージする
（situations.jsonはユーザーの経験則専用、ai_tactics.jsonはAI生成専用）
"""
import json
import os
import sys
from datetime import datetime

# プロジェクトルートをパスに追加
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def load_json_file(file_path):
    """JSONファイルを読み込む"""
    if not os.path.exists(file_path):
        return []
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"エラー: {file_path} の読み込みに失敗しました: {e}")
        return []


def merge_tactics():
    """新しい戦術をAI戦術データにマージ"""
    base_dir = os.path.dirname(os.path.dirname(__file__))
    
    # AI生成戦術データを読み込む（situations.jsonではなくai_tactics.json）
    existing_path = os.path.join(base_dir, "data", "ai_tactics.json")
    existing_tactics = load_json_file(existing_path)
    
    # 新しい戦術を読み込む
    new_tactics_path = os.path.join(base_dir, "new_tactics.json")
    new_tactics = load_json_file(new_tactics_path)
    
    if not new_tactics:
        print("警告: 新しい戦術データがありません")
        return existing_tactics
    
    # 既存のIDを取得（重複チェック用）
    existing_ids = {tactic.get("id") for tactic in existing_tactics if tactic.get("id")}
    
    # 新しい戦術を追加（重複を避ける）
    added_count = 0
    for tactic in new_tactics:
        if tactic.get("id") and tactic["id"] not in existing_ids:
            existing_tactics.append(tactic)
            existing_ids.add(tactic["id"])
            added_count += 1
        else:
            print(f"⚠️ 重複をスキップ: {tactic.get('id', 'N/A')}")
    
    # 日付でソート（新しい順）
    existing_tactics.sort(key=lambda x: x.get("date", ""), reverse=True)
    
    # 最大500件に制限（AI生成は多くなりすぎる可能性があるため）
    if len(existing_tactics) > 500:
        existing_tactics = existing_tactics[:500]
        print(f"⚠️ データが500件を超えたため、最新500件のみ保持します")
    
    # 保存
    with open(existing_path, "w", encoding="utf-8") as f:
        json.dump(existing_tactics, f, ensure_ascii=False, indent=2)
    
    print(f"✅ マージ完了: {added_count}件の新しいAI戦術を追加しました")
    print(f"   AI戦術総件数: {len(existing_tactics)}件")
    
    return existing_tactics


if __name__ == "__main__":
    print("=" * 50)
    print("戦術データのマージを開始します...")
    print("=" * 50)
    
    result = merge_tactics()
    
    if result:
        print("=" * 50)
        print("✅ マージが正常に完了しました")
        print("=" * 50)
    else:
        print("=" * 50)
        print("❌ マージに失敗しました")
        print("=" * 50)
        sys.exit(1)
