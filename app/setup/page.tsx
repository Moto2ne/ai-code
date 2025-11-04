import { Metadata } from "next";

export const metadata: Metadata = {
  title: "Setup Checklist | Setup Coach"
};

const CHECKLIST = [
  {
    title: "VS Code",
    steps: [
      "公式サイトから最新版をインストール",
      "推奨拡張機能: ESLint, Prettier, Tailwind CSS IntelliSense",
      "設定同期をオンにして複数環境で統一"
    ]
  },
  {
    title: "Node.js",
    steps: [
      "LTS版 (18+) をインストール",
      "PowerShellで node -v / npm -v を確認",
      "npx create-next-app が実行できることを確認"
    ]
  },
  {
    title: "Git",
    steps: [
      "公式サイトからインストール",
      "git config --global user.name を設定",
      "GitHubアカウントとSSH鍵を登録"
    ]
  }
];

export default function SetupPage() {
  return (
    <div className="space-y-8">
      <header className="rounded-2xl border border-slate-200 bg-white p-8 shadow-sm">
        <h1 className="text-3xl font-bold text-slate-900">Setup Checklist</h1>
        <p className="mt-2 text-sm text-slate-600">
          まずは環境構築から。以下のチェックが完了すると本編のレッスンがスムーズになります。
        </p>
      </header>
      <section className="grid gap-6 md:grid-cols-3">
        {CHECKLIST.map((item) => (
          <article key={item.title} className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
            <h2 className="text-lg font-semibold text-slate-900">{item.title}</h2>
            <ul className="mt-4 space-y-2 text-sm text-slate-600">
              {item.steps.map((step) => (
                <li key={step} className="flex items-start gap-2">
                  <span className="mt-1 h-2 w-2 rounded-full bg-brand-500" />
                  <span>{step}</span>
                </li>
              ))}
            </ul>
          </article>
        ))}
      </section>
      <section className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
        <h2 className="text-lg font-semibold text-slate-900">トラブルシューティング</h2>
        <ul className="mt-3 list-disc space-y-2 pl-5 text-sm text-slate-600">
          <li>PowerShellでスクリプトがブロックされる → `Set-ExecutionPolicy RemoteSigned` を実行</li>
          <li>npm installで失敗する → プロキシ設定やVPNを一時停止</li>
          <li>Gitで認証エラー → `git credential-manager` の設定を確認</li>
        </ul>
      </section>
    </div>
  );
}
