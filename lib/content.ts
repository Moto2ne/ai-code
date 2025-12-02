export type SlideBlock =
  | { type: "text"; content: string }
  | { type: "image"; src: string; alt?: string }
  | { type: "note"; content: string }
  | { type: "code"; language: string; content: string };

export type TestCase =
  | { type: "dom"; selector: string; exists: boolean; text?: string }
  | { type: "function"; exportName: string; expected: unknown }
  | { type: "unit"; file: string };

export interface LessonTask {
  goal: string;
  hints: string[];
  tests: TestCase[];
}

export interface LessonDefinition {
  id: string;
  chapterId: string;
  title: string;
  durationMinutes: number;
  slides: SlideBlock[];
  starterFiles: Record<string, string>;
  task: LessonTask;
  qa: string[];
  summary: {
    recap: string[];
    nextLessonId?: string;
  };
}

export interface ChapterDefinition {
  id: string;
  title: string;
  description: string;
  order: string[];
}

export interface CourseDefinition {
  id: string;
  title: string;
  description: string;
  audience: string;
  durationMinutes: number;
  prerequisites: string[];
  chapters: ChapterDefinition[];
  outcomes: string[];
}

export interface CourseCatalogEntry {
  id: string;
  title: string;
  description: string;
  modules: Array<{
    id: string;
    title: string;
    description?: string;
    lessonId?: string;
    status?: "available" | "comingSoon";
  }>;
}

export interface UserProfile {
  id: string;
  name: string;
  plan: "free" | "pro" | "enterprise";
  xp: number;
  badges: string[];
  streakDays: number;
  completedLessons: string[];
  currentCourseId: string;
  currentLessonId: string;
}

export const userProfile: UserProfile = {
  id: "user_12345",
  name: "山田花子",
  plan: "free",
  xp: 300,
  badges: ["初めてのレッスン"],
  streakDays: 3,
  completedLessons: ["homepage01"],
  currentCourseId: "nextjs-basic",
  currentLessonId: "state01"
};

export const courseCatalog: CourseCatalogEntry[] = [
  {
    id: "ai-coding",
    title: "AIコーディング入門",
    description: "AIチャットとライブプレビューでWeb制作を体験する入門コースです。初級から実践編まで一本道のステップで進められます。",
    modules: [
      {
        id: "ai-coding-basic",
        title: "AIコーディング初級編",
        description: "AIチャットへの質問と基本的なUI作成を体験します。",
        lessonId: "ai01",
        status: "available"
      },
      {
        id: "ai-coding-intermediate",
        title: "AIコーディング中級編",
        description: "HTML/CSS生成のコツを学び、カードやフォームを仕上げます。",
        lessonId: "ai02",
        status: "available"
      },
      {
        id: "ai-coding-advanced",
        title: "AIコーディング上級編",
        description: "ランディングページの各セクションをAIと共同で作り込みます。",
        lessonId: "ai05",
        status: "available"
      },
      {
        id: "ai-coding-practical",
        title: "AIコーディング実践編",
        description: "学んだ内容をベースに実サービスを想定したページを構築します。",
        status: "comingSoon"
      }
    ]
  },
  {
    id: "ai-web-app",
    title: "AIで作る！Webアプリ開発編",
    description: "AIと協働しながらWebアプリの設計から公開までを駆け抜けます。",
    modules: [
      { id: "ai-web-app-basics", title: "AIコーディング入門", status: "comingSoon" },
      { id: "ai-web-app-backend", title: "バックエンド連携入門", status: "comingSoon" },
      { id: "ai-web-app-testing", title: "テスト自動化を学ぼう", status: "comingSoon" },
      { id: "ai-web-app-deploy", title: "デプロイ準備編", status: "comingSoon" }
    ]
  },
  {
    id: "ai-todo",
    title: "AIで作る！Todoアプリ開発編",
    description: "シンプルなTodoアプリをAIの提案を活かしながら完成させます。",
    modules: [
      { id: "ai-todo-plan", title: "要件整理とプロンプト設計", status: "comingSoon" },
      { id: "ai-todo-ui", title: "UIコンポーネント構築", status: "comingSoon" },
      { id: "ai-todo-state", title: "状態管理をAIと一緒に", status: "comingSoon" },
      { id: "ai-todo-polish", title: "仕上げと改善提案", status: "comingSoon" }
    ]
  },
  {
    id: "ai-portfolio",
    title: "AIで作る！マイポートフォリオ編",
    description: "AIと共に自己紹介サイトを構築し、魅力的にアピールしましょう。",
    modules: [
      { id: "ai-portfolio-story", title: "ストーリー設計", status: "comingSoon" },
      { id: "ai-portfolio-layout", title: "レイアウトデザイン", status: "comingSoon" },
      { id: "ai-portfolio-brand", title: "ブランド表現", status: "comingSoon" },
      { id: "ai-portfolio-launch", title: "公開とフィードバック", status: "comingSoon" }
    ]
  }
];

export const course: CourseDefinition = {
  id: "nextjs-basic",
  title: "Next.js入門",
  description: "ゼロからNext.jsでWebページを構築し、公開まで体験するコース",
  audience: "HTML/CSSに触れたことがある初学者",
  durationMinutes: 180,
  prerequisites: ["PCとインターネット環境", "VS Codeがインストール済みであること"],
  outcomes: [
    "Next.jsの基本的なフォルダ構造が分かる",
    "ReactコンポーネントでUIを作成できる",
    "API連携と公開フローを理解する"
  ],
  chapters: [
    {
      id: "chapter-setup",
      title: "環境構築",
      description: "学習を快適に進めるための環境準備を行います",
      order: ["setup01", "setup02", "setup03"]
    },
    {
      id: "chapter-next-intro",
      title: "Next.js超入門",
      description: "ページとコンポーネントの基本を押さえます",
      order: ["homepage01", "state01", "event01"]
    },
    {
      id: "chapter-api",
      title: "APIと非同期",
      description: "fetchを用いたデータ取得を体験します",
      order: ["fetch01", "error01"]
    },
    {
      id: "chapter-ai",
      title: "AIに触れてみよう！",
      description: "AIチャットを使ってアイデアをまとめ、コードに反映する体験をします",
      order: ["ai01", "ai02", "ai03", "ai04", "ai05", "ai06", "ai07"]
    },
    {
      id: "chapter-publish",
      title: "公開",
      description: "Vercelでデプロイし、アクセス共有までを行います",
      order: ["publish01"]
    }
  ]
};

export const lessons: Record<string, LessonDefinition> = {
  setup01: {
    id: "setup01",
    chapterId: "chapter-setup",
    title: "VS Codeをインストールしよう",
    durationMinutes: 8,
    slides: [
      { type: "text", content: "VS CodeはMicrosoftが提供する開発者向けエディタです。" },
      {
        type: "note",
        content: "公式サイトからダウンロードし、推奨拡張機能(ESLint, Prettier)も追加しましょう。"
      },
      {
        type: "image",
  src: "/slides/vscode-download.svg",
        alt: "VS Codeダウンロード画面"
      }
    ],
    starterFiles: {},
    task: {
      goal: "VS Codeをインストールして必要な拡張を追加する",
      hints: ["検索バーでExtensionsと入力", "ESLintとPrettierを追加"],
      tests: []
    },
    qa: ["Q. 公式サイトにアクセスできません A. ネットワーク設定を確認してください"],
    summary: {
      recap: ["VS Codeのインストール方法", "必要な拡張機能"],
      nextLessonId: "setup02"
    }
  },
  setup02: {
    id: "setup02",
    chapterId: "chapter-setup",
    title: "Node.jsをセットアップしよう",
    durationMinutes: 7,
    slides: [
      { type: "text", content: "LTS版のNode.jsをインストールします" },
      {
        type: "code",
        language: "bash",
        content: "node -v\nnpm -v"
      }
    ],
    starterFiles: {},
    task: {
      goal: "Node.js LTSをインストールし、バージョンを確認する",
      hints: ["公式サイトからインストーラを取得", "PowerShellでnode -vを実行"],
      tests: []
    },
    qa: ["Q. nodeコマンドが見つかりません A. PATHにNode.jsが登録されているか確認"],
    summary: {
      recap: ["Node.js LTSのインストール", "バージョン確認方法"],
      nextLessonId: "setup03"
    }
  },
  setup03: {
    id: "setup03",
    chapterId: "chapter-setup",
    title: "Gitをセットアップしよう",
    durationMinutes: 6,
    slides: [
      { type: "text", content: "Gitでバージョン管理を行います" },
      {
        type: "note",
        content: "git config --global user.name と user.email を設定しましょう"
      }
    ],
    starterFiles: {},
    task: {
      goal: "Gitをインストールしてユーザー設定を完了する",
      hints: ["公式サイトからインストーラを取得", "PowerShellでgit --versionを実行"],
      tests: []
    },
    qa: ["Q. git --versionでエラー A. shellを再起動"],
    summary: {
      recap: ["Gitの初期設定"],
      nextLessonId: "homepage01"
    }
  },
  homepage01: {
    id: "homepage01",
    chapterId: "chapter-next-intro",
    title: "Webページを作成する",
    durationMinutes: 10,
    slides: [
      { type: "text", content: "Next.jsでシンプルなホームページを作成しましょう。" },
      {
        type: "image",
  src: "/slides/homepage_layout.svg",
        alt: "ホームページレイアウト"
      },
      {
        type: "note",
        content: "header, main, footerタグを使うとセマンティックな構造になります。"
      },
      {
        type: "code",
        language: "tsx",
        content: "export default function Home() {\n  return (\n    <div className=\"min-h-screen bg-white\">\n      {/* ここにコードを書いてください */}\n    </div>\n  );\n}"
      }
    ],
    starterFiles: {
      "pages/index.js": "export default function Home() {\n  return (\n    <div>\n      {/* ここにコードを書いてください */}\n    </div>\n  );\n}\n",
      "package.json": "{\n  \"name\": \"my-homepage\",\n  \"dependencies\": {\n    \"next\": \"latest\",\n    \"react\": \"latest\",\n    \"react-dom\": \"latest\"\n  }\n}"
    },
    task: {
      goal: "ヘッダー、メインコンテンツ、フッターを含むホームページを作る",
      hints: ["header, main, footerタグを使用", "タイトルとナビゲーションを追加"],
      tests: [
        { type: "dom", selector: "header", exists: true },
        { type: "dom", selector: "main", exists: true },
        { type: "dom", selector: "footer", exists: true },
        { type: "dom", selector: "h1", exists: true, text: "Welcome" }
      ]
    },
    qa: [
      "Q. 画面が真っ白です A. 開発サーバーのログにエラーがないか確認",
      "Q. テストが通りません A. セレクタが正しいか確認"
    ],
    summary: {
      recap: ["セマンティックなHTML構造", "基本レイアウトの作成"],
      nextLessonId: "state01"
    }
  },
  state01: {
    id: "state01",
    chapterId: "chapter-next-intro",
    title: "状態を扱う",
    durationMinutes: 9,
    slides: [
      { type: "text", content: "useStateで入力フォームとカウンターを作ります。" },
      {
        type: "code",
        language: "tsx",
        content: "const [value, setValue] = useState('');"
      }
    ],
    starterFiles: {},
    task: {
      goal: "useStateでカウンター機能を作る",
      hints: ["初期値を0に設定", "+/-ボタンで更新"],
      tests: []
    },
    qa: ["Q. 状態が更新されません A. setStateの呼出を確認"],
    summary: {
      recap: ["useStateの基礎"],
      nextLessonId: "event01"
    }
  },
  event01: {
    id: "event01",
    chapterId: "chapter-next-intro",
    title: "イベントを扱う",
    durationMinutes: 8,
    slides: [
      { type: "text", content: "onClickでイベントハンドラを登録します。" }
    ],
    starterFiles: {},
    task: {
      goal: "クリックイベントを扱う",
      hints: ["関数をpropsに渡す"],
      tests: []
    },
    qa: ["Q. イベントが発火しません A. ボタンの型を確認"],
    summary: {
      recap: ["イベントハンドラの登録方法"],
      nextLessonId: "fetch01"
    }
  },
  fetch01: {
    id: "fetch01",
    chapterId: "chapter-api",
    title: "APIからデータを取得する",
    durationMinutes: 10,
    slides: [
      { type: "text", content: "Next.jsのRoute HandlerでAPIを作ります。" }
    ],
    starterFiles: {},
    task: {
      goal: "fetchでJSONを取得する",
      hints: ["useEffectで初回取得", "ローディング表示"],
      tests: []
    },
    qa: ["Q. CORSエラーが出ます A. 同一オリジンを確認"],
    summary: {
      recap: ["fetchの基本"],
      nextLessonId: "error01"
    }
  },
  error01: {
    id: "error01",
    chapterId: "chapter-api",
    title: "エラーハンドリング",
    durationMinutes: 7,
    slides: [
      { type: "text", content: "try/catchでエラーを捕捉します。" }
    ],
    starterFiles: {},
    task: {
      goal: "エラー表示を実装",
      hints: ["catch句でstateを更新"],
      tests: []
    },
    qa: ["Q. エラーが表示されません A. stateの依存関係を確認"],
    summary: {
      recap: ["エラー表示のベストプラクティス"],
      nextLessonId: "ai01"
    }
  },
  ai01: {
    id: "ai01",
    chapterId: "chapter-ai",
    title: "AIに触れてみよう！",
    durationMinutes: 10,
    slides: [
      { type: "text", content: "AIに触れてみましょう。" },
      {
        type: "note",
        content: "🤖AIチャットに、「AIコーディングについて教えてください。」と入力してください。"
      },
      {
        type: "note",
        content: "AIからの回答をコピーして、中央のコードエリアに貼り付けましょう。"
      },
      {
        type: "note",
        content: "プレビューで内容を確認したら、右下のチェックボタンを押して結果を見てみましょう。"
      }
    ],
    starterFiles: {
      "result.tsx": `export default function Result() {\n  return (\n    <main className="p-6 space-y-4">\n      <p data-placeholder="ai-response">AIチャットの回答をここに貼り付けましょう。</p>\n    </main>\n  );\n}\n`
    },
    task: {
      goal: "AIチャットの回答をまとめてページに表示する",
      hints: [
        "まずはAIチャットで質問を送って回答を確認しましょう",
        "回答をコピーしてプレースホルダーの段落を置き換えます",
        "見出しや箇条書きを追加すると読みやすくなります"
      ],
      tests: [
        { type: "dom", selector: "h1", exists: true },
        { type: "dom", selector: "p", exists: true }
      ]
    },
    qa: [
      "Q. AIの回答が貼り付けられません A. コードエリアのプレースホルダーを選択してから貼り付けてください",
      "Q. プレビューに表示されません A. コードの保存状態を確認するか、エディタで内容をもう一度コピーしてください"
    ],
    summary: {
      recap: ["AIチャットへの質問", "回答のコピペと整形"],
      nextLessonId: "publish01"
    }
  },
  publish01: {
    id: "publish01",
    chapterId: "chapter-publish",
    title: "Vercelに公開する",
    durationMinutes: 10,
    slides: [
      { type: "text", content: "Vercelへのデプロイ手順を確認します。" },
      {
        type: "image",
  src: "/slides/vercel-deploy.svg",
        alt: "Vercelデプロイ画面"
      }
    ],
    starterFiles: {},
    task: {
      goal: "Vercelでアプリを公開する",
      hints: ["GitHub連携", "環境変数の設定"],
      tests: []
    },
    qa: ["Q. Buildに失敗します A. Environment Variablesを確認"],
    summary: {
      recap: ["Vercelデプロイの流れ"],
      nextLessonId: undefined
    }
  },
  ai02: {
    id: "ai02",
    chapterId: "chapter-ai",
    title: "カードコンポーネントを作成しよう",
    durationMinutes: 15,
    slides: [
      { type: "text", content: "AIを使ってカードコンポーネントを作成します。" },
      {
        type: "note",
        content: "🤖AIチャットに、「画像、タイトル、説明文を含むカードコンポーネントをReactで作成してください。」と質問してみましょう。"
      },
      {
        type: "code",
        language: "tsx",
        content: "// カードの例\n<div className=\"rounded-lg border p-4 shadow\">\n  <img src=\"...\" alt=\"...\" />\n  <h3>タイトル</h3>\n  <p>説明文</p>\n</div>"
      }
    ],
    starterFiles: {
      "card.tsx": `export default function Card() {\n  return (\n    <div className="max-w-sm mx-auto p-6">\n      {/* ここにカードコンポーネントを作成 */}\n    </div>\n  );\n}\n`
    },
    task: {
      goal: "画像、タイトル、説明文を含むカードコンポーネントを作成する",
      hints: [
        "AIに「カードコンポーネントの作成方法」を質問してみましょう",
        "画像はimg タグまたは Next.js の Image コンポーネントを使用",
        "shadow や rounded などの Tailwind クラスで見た目を整えます"
      ],
      tests: [
        { type: "dom", selector: "img", exists: true },
        { type: "dom", selector: "h3", exists: true },
        { type: "dom", selector: "p", exists: true }
      ]
    },
    qa: [
      "Q. 画像が表示されません A. srcパスが正しいか確認してください",
      "Q. スタイルが適用されません A. Tailwind のクラス名が正しいか確認"
    ],
    summary: {
      recap: ["カードコンポーネントの基本構造", "AIを使ったコード生成"],
      nextLessonId: "ai03"
    }
  },
  ai03: {
    id: "ai03",
    chapterId: "chapter-ai",
    title: "フォームコンポーネントを作成しよう",
    durationMinutes: 20,
    slides: [
      { type: "text", content: "AIを使ってお問い合わせフォームを作成します。" },
      {
        type: "note",
        content: "🤖AIチャットに、「名前、メール、メッセージを入力できるお問い合わせフォームを作成してください。」と質問してみましょう。"
      },
      {
        type: "code",
        language: "tsx",
        content: "const [formData, setFormData] = useState({\n  name: '',\n  email: '',\n  message: ''\n});"
      }
    ],
    starterFiles: {
      "contact-form.tsx": `'use client';\nimport { useState } from 'react';\n\nexport default function ContactForm() {\n  return (\n    <div className="max-w-md mx-auto p-6">\n      <h2 className="text-2xl font-bold mb-4">お問い合わせ</h2>\n      {/* ここにフォームを作成 */}\n    </div>\n  );\n}\n`
    },
    task: {
      goal: "名前、メール、メッセージの入力フィールドを持つフォームを作成する",
      hints: [
        "useStateでフォームデータを管理します",
        "各input要素にname属性とvalue属性を設定",
        "onChangeでsetStateを呼び出して状態を更新"
      ],
      tests: [
        { type: "dom", selector: "form", exists: true },
        { type: "dom", selector: "input[name='name']", exists: true },
        { type: "dom", selector: "input[name='email']", exists: true },
        { type: "dom", selector: "textarea", exists: true },
        { type: "dom", selector: "button[type='submit']", exists: true }
      ]
    },
    qa: [
      "Q. 入力しても変わりません A. onChangeとvalueが正しく設定されているか確認",
      "Q. submitで画面がリロードされます A. e.preventDefault()を追加"
    ],
    summary: {
      recap: ["フォームの状態管理", "制御されたコンポーネント", "イベントハンドリング"],
      nextLessonId: "ai04"
    }
  },
  ai04: {
    id: "ai04",
    chapterId: "chapter-ai",
    title: "レスポンシブデザインを実装しよう",
    durationMinutes: 18,
    slides: [
      { type: "text", content: "Tailwind CSSでレスポンシブなグリッドレイアウトを作成します。" },
      {
        type: "note",
        content: "🤖AIチャットに、「スマホでは1列、タブレットでは2列、PCでは3列になるカードグリッドを作成してください。」と質問してみましょう。"
      },
      {
        type: "code",
        language: "tsx",
        content: "// レスポンシブグリッドの例\n<div className=\"grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4\">\n  {/* カード */}\n</div>"
      }
    ],
    starterFiles: {
      "grid-layout.tsx": `export default function GridLayout() {\n  const items = ['Item 1', 'Item 2', 'Item 3', 'Item 4', 'Item 5', 'Item 6'];\n  \n  return (\n    <div className="container mx-auto p-6">\n      <h1 className="text-3xl font-bold mb-6">カードグリッド</h1>\n      {/* ここにグリッドレイアウトを作成 */}\n    </div>\n  );\n}\n`
    },
    task: {
      goal: "レスポンシブなグリッドレイアウトを実装する",
      hints: [
        "grid-cols-1 で基本は1列",
        "md:grid-cols-2 でタブレットサイズ以上は2列",
        "lg:grid-cols-3 でデスクトップサイズ以上は3列"
      ],
      tests: [
        { type: "dom", selector: ".grid", exists: true },
        { type: "dom", selector: "h1", exists: true }
      ]
    },
    qa: [
      "Q. グリッドが1列のままです A. Tailwindのブレークポイント(md:, lg:)を確認",
      "Q. 隙間がありません A. gap-4などのgapクラスを追加"
    ],
    summary: {
      recap: ["Tailwind のレスポンシブ修飾子", "グリッドレイアウト", "モバイルファースト設計"],
      nextLessonId: "ai05"
    }
  },
  ai05: {
    id: "ai05",
    chapterId: "chapter-ai",
    title: "ヒーローセクションを作成しよう",
    durationMinutes: 22,
    slides: [
      { type: "text", content: "ランディングページのヒーローセクションを作成します。" },
      {
        type: "note",
        content: "🤖AIチャットに、「大きな見出し、サブテキスト、CTAボタンを含むヒーローセクションを作成してください。」と質問してみましょう。"
      },
      {
        type: "image",
        src: "/slides/hero-section.svg",
        alt: "ヒーローセクションのイメージ"
      }
    ],
    starterFiles: {
      "hero.tsx": `export default function Hero() {\n  return (\n    <section className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-500 to-purple-600">\n      {/* ここにヒーローセクションを作成 */}\n    </section>\n  );\n}\n`
    },
    task: {
      goal: "魅力的なヒーローセクションを作成する",
      hints: [
        "h1で大きな見出しを作成",
        "pでサブテキストを追加",
        "buttonでCTA（Call To Action）ボタンを配置",
        "中央揃えと適切な余白を設定"
      ],
      tests: [
        { type: "dom", selector: "section", exists: true },
        { type: "dom", selector: "h1", exists: true },
        { type: "dom", selector: "p", exists: true },
        { type: "dom", selector: "button", exists: true }
      ]
    },
    qa: [
      "Q. 中央に配置できません A. flex、items-center、justify-centerを確認",
      "Q. グラデーションが表示されません A. bg-gradient-toとfrom/toの設定を確認"
    ],
    summary: {
      recap: ["ヒーローセクションの基本構成", "Flexboxによる中央配置", "グラデーション背景"],
      nextLessonId: "ai06"
    }
  },
  ai06: {
    id: "ai06",
    chapterId: "chapter-ai",
    title: "特徴セクションを作成しよう",
    durationMinutes: 25,
    slides: [
      { type: "text", content: "サービスの特徴を紹介するセクションを作成します。" },
      {
        type: "note",
        content: "🤖AIチャットに、「アイコン、見出し、説明文を持つ3つの特徴カードを横並びに配置してください。」と質問してみましょう。"
      },
      {
        type: "code",
        language: "tsx",
        content: "const features = [\n  { icon: '⚡', title: '高速', description: '...'},\n  { icon: '🎨', title: '美しい', description: '...'},\n  { icon: '🔒', title: '安全', description: '...'}\n];"
      }
    ],
    starterFiles: {
      "features.tsx": `export default function Features() {\n  const features = [\n    { icon: '⚡', title: '高速', description: '最新技術で高速な動作を実現' },\n    { icon: '🎨', title: '美しい', description: 'モダンで洗練されたデザイン' },\n    { icon: '🔒', title: '安全', description: 'セキュリティを最優先に設計' }\n  ];\n  \n  return (\n    <section className="py-20 bg-gray-50">\n      <div className="container mx-auto px-6">\n        <h2 className="text-3xl font-bold text-center mb-12">特徴</h2>\n        {/* ここに特徴カードを配置 */}\n      </div>\n    </section>\n  );\n}\n`
    },
    task: {
      goal: "3つの特徴を紹介するセクションを作成する",
      hints: [
        "map関数で配列をループして各カードを生成",
        "gridまたはflexで横並びに配置",
        "各カードに適切な余白とスタイルを適用"
      ],
      tests: [
        { type: "dom", selector: "section", exists: true },
        { type: "dom", selector: "h2", exists: true }
      ]
    },
    qa: [
      "Q. カードが縦に並んでしまいます A. grid-cols-3またはflex flex-rowを確認",
      "Q. mapでエラーが出ます A. 各要素にkey属性を追加"
    ],
    summary: {
      recap: ["配列のmap処理", "特徴セクションのデザインパターン", "アイコンの活用"],
      nextLessonId: "ai07"
    }
  },
  ai07: {
    id: "ai07",
    chapterId: "chapter-ai",
    title: "フッターセクションを作成しよう",
    durationMinutes: 20,
    slides: [
      { type: "text", content: "ランディングページのフッターを作成します。" },
      {
        type: "note",
        content: "🤖AIチャットに、「コピーライト、リンク、SNSアイコンを含むフッターを作成してください。」と質問してみましょう。"
      }
    ],
    starterFiles: {
      "footer.tsx": `export default function Footer() {\n  return (\n    <footer className="bg-gray-900 text-white py-12">\n      <div className="container mx-auto px-6">\n        {/* ここにフッターの内容を作成 */}\n      </div>\n    </footer>\n  );\n}\n`
    },
    task: {
      goal: "コピーライト、ナビゲーションリンク、SNSリンクを含むフッターを作成する",
      hints: [
        "gridまたはflexで複数列に分割",
        "リンクはaタグまたはNext.jsのLinkコンポーネントを使用",
        "コピーライト表記は中央または左端に配置"
      ],
      tests: [
        { type: "dom", selector: "footer", exists: true },
        { type: "dom", selector: "a", exists: true }
      ]
    },
    qa: [
      "Q. リンクの色が見えません A. text-whiteなどで色を設定",
      "Q. レイアウトが崩れます A. containerとpxでコンテンツ幅を制限"
    ],
    summary: {
      recap: ["フッターの基本構成", "ナビゲーションリンク", "コピーライト表記"],
      nextLessonId: undefined
    }
  }
};

export const aiCodingLessons = {
  "ai-basic-01": {
    id: "ai-basic-01",
    title: "AIでボタンコンポーネントを作成",
    prompt: "Reactでクリック可能なボタンコンポーネントを作成してください。青い背景で、ホバー時に濃くなるようにしてください。",
    initialCode: `export default function App() {\n  return (\n    <div>\n      {/* ここにボタンを追加 */}\n    </div>\n  );\n}`,
    targetCode: `export default function App() {\n  const handleClick = () => {\n    alert('クリックされました!');\n  };\n\n  return (\n    <div>\n      <button\n        onClick={handleClick}\n        className="rounded bg-blue-600 px-4 py-2 text-white hover:bg-blue-700"\n      >\n        クリック\n      </button>\n    </div>\n  );\n}`,
    explanation: "AIが生成したコードでは、ボタンのクリックイベントをhandleClick関数で処理し、Tailwind CSSでスタイリングしています。"
  },
  "state01": {
    id: "state01",
    title: "AIでカウンターを実装",
    prompt: "useStateを使ってカウンターを実装してください。+1ボタンと-1ボタンを配置してください。",
    initialCode: `import { useState } from 'react';\n\nexport default function Counter() {\n  return (\n    <div>\n      {/* カウンター実装 */}\n    </div>\n  );\n}`,
    targetCode: `import { useState } from 'react';\n\nexport default function Counter() {\n  const [count, setCount] = useState(0);\n\n  return (\n    <div className="space-y-4">\n      <div className="text-2xl font-bold">Count: {count}</div>\n      <div className="flex gap-2">\n        <button onClick={() => setCount(count - 1)}>-1</button>\n        <button onClick={() => setCount(count + 1)}>+1</button>\n      </div>\n    </div>\n  );\n}`,
    explanation: "useStateフックを使って状態管理を行い、ボタンクリックで状態を更新しています。"
  }
};
