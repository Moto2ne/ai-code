import { Metadata } from "next";

export const metadata: Metadata = {
  title: "Publish Guide | Setup Coach"
};

const STEPS = [
  {
    title: "GitHubにプッシュ",
    description: "mainブランチに最新コードをpushし、Vercelと連携させます。"
  },
  {
    title: "Vercelでデプロイ",
    description: "New Project → Import Git Repositoryでリポジトリを選択します。"
  },
  {
    title: "環境変数を設定",
    description: "プロジェクト設定 > Environment VariablesからAPIキーなどを登録します。"
  },
  {
    title: "プレビューリンクを共有",
    description: "DeploymentsからPreview URLをコピーしてメンターに共有しましょう。"
  }
];

export default function PublishPage() {
  return (
    <div className="space-y-8">
      <header className="rounded-2xl border border-slate-200 bg-white p-8 shadow-sm">
        <h1 className="text-3xl font-bold text-slate-900">Vercel公開ガイド</h1>
        <p className="mt-2 text-sm text-slate-600">
          デプロイから共有までの流れをステップで確認できます。各ステップで必要なチェックポイントも用意しました。
        </p>
      </header>
      <section className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
        <ol className="space-y-4">
          {STEPS.map((step, index) => (
            <li key={step.title} className="flex gap-4 rounded-xl border border-slate-200 bg-slate-50 p-5">
              <span className="mt-1 h-8 w-8 rounded-full bg-brand-600 text-center text-sm font-semibold leading-8 text-white">
                {index + 1}
              </span>
              <div>
                <h2 className="text-lg font-semibold text-slate-900">{step.title}</h2>
                <p className="text-sm text-slate-600">{step.description}</p>
              </div>
            </li>
          ))}
        </ol>
      </section>
      <section className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
        <h2 className="text-lg font-semibold text-slate-900">チェックリスト</h2>
        <ul className="mt-3 list-disc space-y-2 pl-5 text-sm text-slate-600">
          <li>環境変数はProductionとPreviewで揃っていますか？</li>
          <li>ビルドコマンドは `next build` ですか？</li>
          <li>CIの結果を確認しましたか？</li>
          <li>公開URLをSlackやメールで共有しましたか？</li>
        </ul>
      </section>
    </div>
  );
}
