"use client";

import { useMemo, useState } from "react";

const ISSUE_OPTIONS = [
  "エラーの原因がわからない",
  "テストが通らない",
  "プレビューが更新されない",
  "要件を満たしたか不安" 
];

const DETAIL_OPTIONS = [
  "コンソールの赤いメッセージ",
  "実装したコード",
  "期待する結果",
  "試したこと"
];

export default function AskCoachPage() {
  const [issue, setIssue] = useState(ISSUE_OPTIONS[0]);
  const [detailSelections, setDetailSelections] = useState<string[]>([DETAIL_OPTIONS[0], DETAIL_OPTIONS[1]]);
  const [message, setMessage] = useState("console.error('TypeError: Cannot read properties of undefined')");

  const prompt = useMemo(() => {
  const details = detailSelections.map((item: string) => `- ${item}`).join("\n");
    return `以下の状況で${issue}のでサポートしてください。\n${details}\n補足:\n${message}`;
  }, [detailSelections, issue, message]);

  const handleToggle = (item: string) => {
    setDetailSelections((prev: string[]) =>
      prev.includes(item) ? prev.filter((value: string) => value !== item) : [...prev, item]
    );
  };

  return (
    <div className="space-y-8">
      <header className="rounded-2xl border border-slate-200 bg-white p-8 shadow-sm">
        <h1 className="text-3xl font-bold text-slate-900">Ask Coach</h1>
        <p className="mt-2 text-sm text-slate-600">
          コンテキストと質問テンプレをワンクリックで用意して、AIコーチに貼り付けましょう。
        </p>
      </header>

      <section className="grid gap-6 md:grid-cols-[1.2fr_1fr]">
        <div className="space-y-6">
          <div className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
            <h2 className="text-lg font-semibold text-slate-900">質問の組み立て</h2>
            <div className="mt-4 space-y-4">
              <div>
                <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">困っていること</p>
                <div className="mt-2 flex flex-wrap gap-2 text-sm">
                  {ISSUE_OPTIONS.map((option) => (
                    <button
                      key={option}
                      type="button"
                      onClick={() => setIssue(option)}
                      className={`rounded-full border px-3 py-1 ${issue === option ? "border-brand-400 bg-brand-50 text-brand-700" : "border-slate-200 bg-white text-slate-600"}`}
                    >
                      {option}
                    </button>
                  ))}
                </div>
              </div>

              <div>
                <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">共有する情報</p>
                <div className="mt-2 flex flex-wrap gap-2 text-sm">
                  {DETAIL_OPTIONS.map((option) => (
                    <button
                      key={option}
                      type="button"
                      onClick={() => handleToggle(option)}
                      className={`rounded-full border px-3 py-1 ${detailSelections.includes(option) ? "border-brand-400 bg-brand-50 text-brand-700" : "border-slate-200 bg-white text-slate-600"}`}
                    >
                      {option}
                    </button>
                  ))}
                </div>
              </div>

              <div>
                <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">補足情報</p>
                <textarea
                  value={message}
                  onChange={(event) => setMessage(event.target.value)}
                  rows={6}
                  className="mt-2 w-full rounded-md border border-slate-200 bg-white p-3 text-sm text-slate-700 focus:border-brand-400 focus:outline-none focus:ring-2 focus:ring-brand-200"
                />
              </div>
            </div>
          </div>

          <div className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
            <h2 className="text-lg font-semibold text-slate-900">質問テンプレ</h2>
            <pre className="mt-3 whitespace-pre-wrap rounded-md bg-slate-900 p-4 text-xs text-slate-100">{prompt}</pre>
          </div>
        </div>

        <aside className="space-y-6">
          <div className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
            <h3 className="text-sm font-semibold text-slate-900">よくあるつまずき</h3>
            <ul className="mt-3 space-y-2 text-sm text-slate-600">
              <li>Node.jsのバージョンが古い → LTSを使用</li>
              <li>importパスのtypo → VS Codeのインテリセンスを利用</li>
              <li>npm run devが起動しない → ポート競合をチェック</li>
            </ul>
          </div>
          <div className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
            <h3 className="text-sm font-semibold text-slate-900">Ask Coachの使い方</h3>
            <ol className="mt-3 list-decimal space-y-2 pl-4 text-sm text-slate-600">
              <li>レッスン画面で「質問テンプレをコピー」をクリック</li>
              <li>こちらで補足情報を整えてAIチャットに貼り付け</li>
              <li>回答を基に再実行 → テストで確認</li>
            </ol>
          </div>
        </aside>
      </section>
    </div>
  );
}
