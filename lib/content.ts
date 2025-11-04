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
      title: "AI連携",
      description: "OpenAI APIにリクエストするシンプルなチャットを実装します",
      order: ["ai01"]
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
    title: "AI APIに問い合わせる",
    durationMinutes: 12,
    slides: [
      { type: "text", content: "OpenAIにPOSTリクエストを送ってみましょう" },
      {
        type: "note",
        content: "安全なAPIキーの管理方法を忘れずに"
      }
    ],
    starterFiles: {},
    task: {
      goal: "OpenAI APIとの通信フローを理解する",
      hints: ["環境変数にAPIキーを設定"],
      tests: []
    },
    qa: ["Q. Unauthorizedになります A. APIキーを確認"],
    summary: {
      recap: ["APIキーの扱い", "レスポンス取り扱い"],
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
  }
};
