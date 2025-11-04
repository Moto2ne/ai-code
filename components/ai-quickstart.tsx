"use client";

import { useEffect, useRef, useState } from "react";
import { Loader2, Sparkles } from "lucide-react";

const GENERATED_CODE = `import { useState } from "react";

export default function MagicButton() {
  const [count, setCount] = useState(0);

  return (
    <button
      onClick={() => setCount((prev) => prev + 1)}
      className="rounded-full bg-indigo-600 px-6 py-3 text-sm font-semibold text-white shadow-lg transition hover:bg-indigo-500"
    >
      クリックした回数: {count}
    </button>
  );
}`;

export function AIQuickStart() {
  const [stage, setStage] = useState<"idle" | "generating" | "done">("idle");
  const [progress, setProgress] = useState(0);
  const timers = useRef<number[]>([]);

  useEffect(() => {
    return () => {
      timers.current.forEach((timerId) => window.clearTimeout(timerId));
      timers.current = [];
    };
  }, []);

  const runDemo = () => {
    timers.current.forEach((timerId) => window.clearTimeout(timerId));
    timers.current = [];
    setStage("generating");
    setProgress(0);

    timers.current.push(
      window.setTimeout(() => {
        setProgress(35);
      }, 350)
    );

    timers.current.push(
      window.setTimeout(() => {
        setProgress(72);
      }, 900)
    );

    timers.current.push(
      window.setTimeout(() => {
        setProgress(100);
        setStage("done");
      }, 1500)
    );
  };

  return (
    <div className="space-y-4 rounded-2xl border border-indigo-200 bg-gradient-to-br from-white via-indigo-50 to-white p-6 shadow-sm">
      <header className="flex items-center gap-2 text-sm font-semibold text-indigo-700">
        <Sparkles className="h-4 w-4" />
        ステップ1: まずはクリックしてみよう
      </header>

      {stage === "idle" && (
        <button
          type="button"
          onClick={runDemo}
          className="w-full rounded-xl border border-indigo-200 bg-white px-6 py-4 text-lg font-semibold text-indigo-700 shadow-sm transition hover:-translate-y-0.5 hover:shadow-md"
        >
          「Reactでボタンを作って」
        </button>
      )}

      {stage === "generating" && (
        <div className="space-y-4 rounded-xl border border-indigo-200 bg-white p-4 shadow-sm">
          <div className="flex items-center gap-3 text-indigo-600">
            <Loader2 className="h-5 w-5 animate-spin" />
            <span className="text-sm font-semibold">コードがシュッと生成される...</span>
          </div>
          <div className="h-2 w-full overflow-hidden rounded-full bg-indigo-100">
            <div
              className="h-full rounded-full bg-indigo-500 transition-all"
              style={{ width: `${progress}%` }}
            />
          </div>
        </div>
      )}

      {stage === "done" && (
        <div className="space-y-4">
          <div className="rounded-xl border border-emerald-200 bg-emerald-50 px-4 py-3 text-sm font-semibold text-emerald-700">
            すごい！AIがコード書いた！
          </div>
          <pre className="overflow-x-auto rounded-xl border border-slate-200 bg-slate-900 p-4 text-xs text-slate-100">
            <code>{GENERATED_CODE}</code>
          </pre>
          <button
            type="button"
            onClick={runDemo}
            className="w-full rounded-lg border border-slate-200 bg-white px-4 py-2 text-sm font-semibold text-slate-600 transition hover:bg-slate-50"
          >
            もう一度体験する
          </button>
        </div>
      )}
    </div>
  );
}
