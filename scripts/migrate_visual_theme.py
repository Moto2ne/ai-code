"""
既存データにvisual_themeを追加し、image_pathを削除するマイグレーションスクリプト
"""
import json
import os

# データファイルのパス
data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "ai_tactics.json")

# テーマ設定
GRADIENT_THEMES = [
    {"gradient": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)", "icon": "🤖"},
    {"gradient": "linear-gradient(135deg, #f093fb 0%, #f5576c 100%)", "icon": "🧠"},
    {"gradient": "linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)", "icon": "💡"},
    {"gradient": "linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)", "icon": "⚡"},
    {"gradient": "linear-gradient(135deg, #fa709a 0%, #fee140 100%)", "icon": "🔥"},
    {"gradient": "linear-gradient(135deg, #a8edea 0%, #fed6e3 100%)", "icon": "✨"},
    {"gradient": "linear-gradient(135deg, #5ee7df 0%, #b490ca 100%)", "icon": "🚀"},
    {"gradient": "linear-gradient(135deg, #d299c2 0%, #fef9d7 100%)", "icon": "💎"},
    {"gradient": "linear-gradient(135deg, #89f7fe 0%, #66a6ff 100%)", "icon": "🌐"},
    {"gradient": "linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%)", "icon": "🎯"},
]

def get_visual_theme(item, index):
    """タイトルに基づいてビジュアルテーマを決定"""
    title = item.get("title", "").lower()
    
    if any(kw in title for kw in ["gpt", "openai", "chatgpt"]):
        return {"gradient": "linear-gradient(135deg, #10a37f 0%, #1a7f5a 100%)", "icon": "🤖"}
    elif any(kw in title for kw in ["gemini", "google", "bard"]):
        return {"gradient": "linear-gradient(135deg, #4285f4 0%, #34a853 100%)", "icon": "✨"}
    elif any(kw in title for kw in ["claude", "anthropic"]):
        return {"gradient": "linear-gradient(135deg, #d4a27f 0%, #cc785c 100%)", "icon": "🧠"}
    elif any(kw in title for kw in ["llama", "meta"]):
        return {"gradient": "linear-gradient(135deg, #0668E1 0%, #1877f2 100%)", "icon": "🦙"}
    elif any(kw in title for kw in ["code", "codex", "coding", "developer"]):
        return {"gradient": "linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%)", "icon": "💻"}
    elif any(kw in title for kw in ["image", "vision"]):
        return {"gradient": "linear-gradient(135deg, #ec4899 0%, #f43f5e 100%)", "icon": "🎨"}
    elif any(kw in title for kw in ["agent", "lightning", "workflow"]):
        return {"gradient": "linear-gradient(135deg, #f59e0b 0%, #ef4444 100%)", "icon": "🚀"}
    elif any(kw in title for kw in ["promptions", "prompt", "ui"]):
        return {"gradient": "linear-gradient(135deg, #0ea5e9 0%, #8b5cf6 100%)", "icon": "🎛️"}
    elif any(kw in title for kw in ["nemotron", "nvidia"]):
        return {"gradient": "linear-gradient(135deg, #76b900 0%, #1a1a1a 100%)", "icon": "⚡"}
    elif any(kw in title for kw in ["apriel", "hugging"]):
        return {"gradient": "linear-gradient(135deg, #FFD21E 0%, #FF9D00 100%)", "icon": "🤗"}
    else:
        return GRADIENT_THEMES[index % len(GRADIENT_THEMES)]


if __name__ == "__main__":
    # データ読み込み
    with open(data_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # visual_theme追加、image_path削除
    for idx, item in enumerate(data):
        item["visual_theme"] = get_visual_theme(item, idx)
        if "image_path" in item:
            del item["image_path"]

    # 保存
    with open(data_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"✅ {len(data)}件のデータにvisual_themeを追加しました")
