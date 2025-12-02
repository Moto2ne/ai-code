# GitHub Copilot Instructions

このプロジェクトは **AICode** - Progate風のプログラミング学習プラットフォームです。

## 技術スタック

- **フレームワーク**: Next.js 14 (App Router)
- **言語**: TypeScript (strict mode)
- **スタイリング**: Tailwind CSS
- **エディタ**: Monaco Editor (@monaco-editor/react)
- **アイコン**: Lucide React
- **テーマ**: next-themes

## プロジェクト構造

```
app/           # App Router ページ（ホーム、コース、レッスン、ダッシュボード等）
components/    # 再利用可能なUIコンポーネント
lib/           # ユーティリティ、データモデル、コンテキスト
public/        # 静的ファイル（スライド画像等）
```

## コーディング規約

### TypeScript

- `strict: true` を使用
- 型定義は明示的に記述する
- `any` 型の使用は避ける
- インターフェースより型エイリアス（`type`）を優先

### React / Next.js

- クライアントコンポーネントには `"use client"` ディレクティブを使用
- Server Components をデフォルトとして活用
- `@/` エイリアスを使用したインポート（例: `@/lib/content`）
- カスタムフックは `use` プレフィックスを使用

### コンポーネント

- 関数コンポーネントを使用（`function` キーワード）
- Props は分割代入でインラインに定義
- コンポーネントファイルは kebab-case（例: `lesson-shell.tsx`）
- コンポーネント名は PascalCase（例: `LessonShell`）

### スタイリング

- Tailwind CSS のユーティリティクラスを使用
- カスタムカラーは `brand-*` パレットを使用（`tailwind.config.ts` 参照）
- `clsx` を使用した条件付きクラス名

### 状態管理

- React Context（`lib/progress-store.tsx`）を使用
- `useState`, `useMemo`, `useCallback` を適切に使用
- パフォーマンス最適化には `useDeferredValue` を活用

## 主要コンポーネント

| コンポーネント | 役割 |
|---------------|------|
| `LessonShell` | レッスン画面のメインレイアウト（スライド/エディタ/プレビュー/テスト） |
| `CodeEditor` | Monaco エディタのラッパー |
| `LivePreview` | リアルタイムプレビュー用 iframe |
| `TestRunner` | DOM ベースの自動テスト実行 |
| `AIChatPanel` | AI ヒント・質問テンプレート表示 |
| `SlidePane` | スライドベースの説明表示 |

## ファイル命名規則

- コンポーネント: `kebab-case.tsx`
- ページ: `page.tsx`（App Router 規約）
- レイアウト: `layout.tsx`
- ユーティリティ: `kebab-case.ts`

## コミットメッセージ

日本語または英語で、変更内容を簡潔に記述してください。

## 注意事項

- このプロジェクトは教育目的のプロトタイプです
- モックデータは `lib/content.ts` に定義されています
- 将来的に Firestore との連携を予定しています
