"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { FormEvent } from "react";

const hints = [
  "レッスンの進捗は自動保存されます",
  "AIチャットでいつでも質問できます",
  "ブラウザだけで学習・実装・チェックが完了"
];

export default function LoginPage() {
  const router = useRouter();

  const handleSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    router.push("/");
  };

  return (
    <div className="flex flex-1 flex-col gap-8 lg:flex-row">
      <section className="flex flex-1 flex-col justify-center rounded-2xl border border-slate-200 bg-white px-8 py-10 shadow-sm">
        <header className="mb-8">
          <h1 className="text-3xl font-bold text-slate-900">ログイン</h1>
          <p className="mt-2 text-sm text-slate-500">
            AICodeにサインインして、スライド学習とライブコーディングを再開しましょう。
          </p>
        </header>
  <form className="flex flex-col gap-6" onSubmit={handleSubmit}>
          <label className="flex flex-col gap-2 text-sm font-medium text-slate-700">
            メールアドレス
            <input
              type="email"
              name="email"
              required
              placeholder="you@example.com"
              className="w-full rounded-lg border border-slate-200 px-3 py-2 text-base text-slate-900 focus:border-brand-500 focus:outline-none focus:ring-2 focus:ring-brand-200"
            />
          </label>
          <label className="flex flex-col gap-2 text-sm font-medium text-slate-700">
            パスワード
            <input
              type="password"
              name="password"
              required
              placeholder="パスワードを入力"
              className="w-full rounded-lg border border-slate-200 px-3 py-2 text-base text-slate-900 focus:border-brand-500 focus:outline-none focus:ring-2 focus:ring-brand-200"
            />
          </label>
          <div className="flex items-center justify-between text-sm text-slate-600">
            <label className="flex items-center gap-2">
              <input type="checkbox" name="remember" className="h-4 w-4 rounded border-slate-300 text-brand-600 focus:ring-brand-500" />
              ログイン情報を保存
            </label>
            <Link href="#" className="font-medium text-brand-600 hover:text-brand-500">
              パスワードをお忘れの方
            </Link>
          </div>
          <button
            type="submit"
            className="w-full rounded-lg bg-brand-600 px-4 py-3 text-base font-semibold text-white transition hover:bg-brand-500"
          >
            サインイン
          </button>
        </form>
        <p className="mt-8 text-center text-sm text-slate-600">
          初めての方は <Link href="/setup" className="font-semibold text-brand-600 hover:text-brand-500">セットアップ</Link> からはじめましょう。
        </p>
      </section>
      <aside className="flex flex-1 flex-col justify-center gap-6 rounded-2xl border border-dashed border-slate-300 bg-slate-100 px-8 py-10 text-slate-700">
        <h2 className="text-xl font-semibold text-slate-800">AICodeでできること</h2>
        <ul className="flex flex-col gap-4">
          {hints.map((hint) => (
            <li key={hint} className="flex items-start gap-3">
              <span className="mt-1 inline-flex h-6 w-6 items-center justify-center rounded-full bg-brand-100 text-sm font-semibold text-brand-600">✓</span>
              <span className="text-sm leading-relaxed">{hint}</span>
            </li>
          ))}
        </ul>
        <div className="rounded-xl bg-white p-6 text-sm shadow-sm">
          <h3 className="font-semibold text-slate-800">まだアカウントがありませんか？</h3>
          <p className="mt-2 text-slate-600">
            無料トライアルでスライドとライブプレビューを体験できます。セットアップページから環境情報を登録してください。
          </p>
          <Link
            href="/setup"
            className="mt-4 inline-flex items-center justify-center rounded-lg border border-brand-600 px-4 py-2 font-semibold text-brand-600 transition hover:bg-brand-50"
          >
            セットアップへ進む
          </Link>
        </div>
      </aside>
    </div>
  );
}
