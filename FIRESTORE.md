# Firestore データベース設計

## コレクション構造

### users
ユーザープロフィールと進捗情報を管理

```typescript
{
  id: string;                    // ユーザーID (UID)
  name: string;                  // 表示名
  email: string;                 // メールアドレス
  plan: "free" | "pro" | "enterprise"; // プラン
  xp: number;                    // 経験値
  badges: string[];              // 獲得バッジ
  streakDays: number;            // 連続学習日数
  completedLessons: string[];    // 完了レッスンID
  currentCourseId: string;       // 現在のコース
  currentLessonId: string;       // 現在のレッスン
  createdAt: Timestamp;          // 作成日時
  lastLoginAt: Timestamp;        // 最終ログイン日時
}
```

### courses
コース情報

```typescript
{
  id: string;                    // コースID
  title: string;                 // タイトル
  description: string;           // 説明
  audience: string;              // 対象者
  durationMinutes: number;       // 推定時間
  prerequisites: string[];       // 前提知識
  chapters: ChapterDefinition[]; // チャプター
  outcomes: string[];            // 学習成果
  published: boolean;            // 公開状態
  createdAt: Timestamp;
  updatedAt: Timestamp;
}
```

### lessons
レッスン詳細

```typescript
{
  id: string;                    // レッスンID
  chapterId: string;             // チャプターID
  courseId: string;              // コースID
  title: string;                 // タイトル
  durationMinutes: number;       // 推定時間
  slides: SlideBlock[];          // スライド
  starterFiles: Record<string, string>; // 初期ファイル
  task: LessonTask;              // 課題
  qa: string[];                  // FAQ
  summary: {                     // まとめ
    recap: string[];
    nextLessonId?: string;
  };
  order: number;                 // 順序
  published: boolean;
  createdAt: Timestamp;
  updatedAt: Timestamp;
}
```

### progress
ユーザーの詳細進捗（オプション）

```typescript
{
  id: string;                    // userId_lessonId
  userId: string;
  lessonId: string;
  courseId: string;
  status: "not_started" | "in_progress" | "completed";
  completedAt?: Timestamp;
  timeSpentMinutes: number;
  attempts: number;
  codeSubmissions: {
    timestamp: Timestamp;
    code: string;
    passed: boolean;
  }[];
}
```

### achievements
バッジ・実績定義

```typescript
{
  id: string;                    // バッジID
  name: string;                  // バッジ名
  description: string;           // 説明
  icon: string;                  // アイコンURL
  requirement: {                 // 取得条件
    type: "lessons_completed" | "streak_days" | "xp_earned" | "course_completed";
    value: number;
    courseId?: string;
  };
  rarity: "common" | "rare" | "epic" | "legendary";
}
```

## インデックス

### users
- email (単一フィールドインデックス)
- xp (単一フィールドインデックス - ランキング用)

### lessons
- courseId (単一フィールドインデックス)
- chapterId (単一フィールドインデックス)
- (courseId, order) (複合インデックス)

### progress
- userId (単一フィールドインデックス)
- (userId, courseId) (複合インデックス)
- (userId, status) (複合インデックス)

## セキュリティルール例

```
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    
    // ユーザーは自分のドキュメントのみ読み書き可能
    match /users/{userId} {
      allow read, write: if request.auth != null && request.auth.uid == userId;
    }
    
    // コースとレッスンは認証済みユーザー全員が読み取り可能
    match /courses/{courseId} {
      allow read: if request.auth != null;
      allow write: if false; // 管理画面でのみ更新
    }
    
    match /lessons/{lessonId} {
      allow read: if request.auth != null;
      allow write: if false;
    }
    
    // 進捗は自分のもののみ読み書き可能
    match /progress/{progressId} {
      allow read, write: if request.auth != null && 
        resource.data.userId == request.auth.uid;
    }
    
    // 実績は全員読み取り可能
    match /achievements/{achievementId} {
      allow read: if request.auth != null;
      allow write: if false;
    }
  }
}
```

## 初期データ投入

lib/content.ts のモックデータを Firestore に移行する際は、以下のスクリプトを使用：

```bash
# scripts/seed-firestore.ts を作成して実行
npm run seed
```
