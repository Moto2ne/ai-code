"use client";

import { useEffect, useMemo, useRef, useState } from "react";
import { CheckCircle2, Loader2, Play } from "lucide-react";

interface PromptConfig {
  id: string;
  title: string;
  code: string;
  explanation: string;
  level: "beginner" | "intermediate" | "advanced";
}

const PROMPTS: PromptConfig[] = [
  {
    id: "todo",
    title: "「TODOアプリを作って」",
    level: "intermediate",
    code: `import { useState } from "react";

export default function TodoApp() {
  const [tasks, setTasks] = useState(["買い物", "学習"]);

  return (
    <div className="space-y-4 rounded-xl border border-slate-200 bg-white p-6">
      <h1 className="text-xl font-bold">今日のTODO</h1>
      <ul className="space-y-2">
        {tasks.map((task) => (
          <li key={task} className="rounded-lg border border-slate-200 bg-slate-50 px-3 py-2">
            {task}
          </li>
        ))}
      </ul>
    </div>
  );
}`,
    explanation: "useStateでTODOを保持し、配列をmapしてリストとして表示します。"
  },
  {
    id: "login",
    title: "「ログイン画面を作って」",
    level: "advanced",
    code: `export default function LoginForm() {
  return (
    <form className="w-full max-w-sm space-y-4 rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
      <h1 className="text-xl font-semibold">ログイン</h1>
      <label className="block text-sm">
        <span className="text-slate-600">メールアドレス</span>
        <input className="mt-1 w-full rounded-lg border border-slate-300 px-3 py-2" type="email" />
      </label>
      <label className="block text-sm">
        <span className="text-slate-600">パスワード</span>
        <input className="mt-1 w-full rounded-lg border border-slate-300 px-3 py-2" type="password" />
      </label>
      <button className="w-full rounded-lg bg-indigo-600 px-4 py-2 text-sm font-semibold text-white">ログイン</button>
    </form>
  );
}`,
    explanation: "フォーム構造を作り、アクセシブルなラベルと入力欄を組み合わせています。"
  },
  {
    id: "calendar",
    title: "「カレンダーを作って」",
    level: "advanced",
    code: `const days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];

export default function MiniCalendar() {
  return (
    <div className="rounded-xl border border-slate-200 bg-white p-6">
      <h2 className="text-lg font-semibold">今週の予定</h2>
      <div className="mt-4 grid grid-cols-7 gap-2 text-center text-sm">
        {days.map((day) => (
          <div key={day} className="rounded-lg border border-slate-200 bg-slate-50 px-2 py-4">
            <div className="font-semibold">{day}</div>
            <div className="mt-1 text-xs text-slate-500">No events</div>
          </div>
        ))}
      </div>
    </div>
  );
}`,
    explanation: "配列を使ったグリッド表示でカレンダー風のUIを生成します。"
  }
];

const LEVEL_LABEL: Record<PromptConfig["level"], string> = {
  beginner: "初級",
  intermediate: "中級",
  advanced: "上級"
};

interface GenerationState {
  status: "idle" | "generating" | "done";
  progress: number;
}

export function AIPromptPlayground() {
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const [state, setState] = useState<GenerationState>({ status: "idle", progress: 0 });
  const timers = useRef<number[]>([]);

  const selectedPrompt = useMemo(() => PROMPTS.find((prompt) => prompt.id === selectedId) ?? null, [selectedId]);

  useEffect(() => {
    return () => {
      timers.current.forEach((timerId) => window.clearTimeout(timerId));
      timers.current = [];
    };
  }, []);

  const startGeneration = (promptId: string) => {
    if (state.status === "generating" && promptId === selectedId) {
      return;
    }
    timers.current.forEach((timerId) => window.clearTimeout(timerId));
    timers.current = [];

    setSelectedId(promptId);
    setState({ status: "generating", progress: 0 });

    timers.current.push(
      window.setTimeout(() => setState((prev) => ({ ...prev, progress: 45 })), 400)
    );

    timers.current.push(
      window.setTimeout(() => setState((prev) => ({ ...prev, progress: 82 })), 1100)
    );

    timers.current.push(
      window.setTimeout(() => setState({ status: "done", progress: 100 }), 1700)
    );
  };

  const reset = () => {
    timers.current.forEach((timerId) => window.clearTimeout(timerId));
    timers.current = [];
    setState({ status: "idle", progress: 0 });
    setSelectedId(null);
  };

  return (
    <div className="space-y-6">
      <div className="grid gap-3 md:grid-cols-3">
        {PROMPTS.map((prompt) => {
          const isActive = prompt.id === selectedId;
          return (
            <button
              key={prompt.id}
              type="button"
              onClick={() => startGeneration(prompt.id)}
              className={`flex items-center justify-between rounded-xl border px-5 py-4 text-left text-base font-semibold shadow-sm transition ${
                isActive
                  ? "border-indigo-400 bg-indigo-50 text-indigo-700"
                  : "border-slate-200 bg-white text-slate-700 hover:-translate-y-0.5 hover:shadow-md"
              }`}
            >
              <span>{prompt.title}</span>
              <span className="text-xs font-normal text-slate-400">{LEVEL_LABEL[prompt.level]}</span>
            </button>
          );
        })}
      </div>

      <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
        {state.status === "idle" && (
          <div className="flex flex-col items-center gap-3 py-10 text-slate-500">
            <Play className="h-6 w-6" />
            <p className="text-sm">人気のプロンプトをクリックして体験を始めましょう。</p>
          </div>
        )}

        {state.status === "generating" && (
          <div className="space-y-4">
            <div className="flex items-center gap-2 text-indigo-600">
              <Loader2 className="h-5 w-5 animate-spin" />
              <span className="text-sm font-semibold">✨ 生成中...</span>
            </div>
            <div className="h-2 w-full overflow-hidden rounded-full bg-indigo-100">
              <div
                className="h-full rounded-full bg-indigo-500 transition-all"
                style={{ width: `${state.progress}%` }}
              />
            </div>
          </div>
        )}

        {state.status === "done" && selectedPrompt && (
          <div className="space-y-4">
            <div className="flex items-center gap-2 text-sm font-semibold text-emerald-600">
              <CheckCircle2 className="h-5 w-5" />
              完成しました！
            </div>
            <div>
              <h3 className="text-xs font-semibold uppercase tracking-wide text-slate-500">生成されたコード</h3>
              <pre className="mt-2 max-h-80 overflow-auto rounded-xl border border-slate-200 bg-slate-900 p-4 text-xs text-slate-100">
                <code>{selectedPrompt.code}</code>
              </pre>
            </div>
            <div>
              <h3 className="text-xs font-semibold uppercase tracking-wide text-slate-500">説明</h3>
              <p className="mt-2 text-sm text-slate-600">{selectedPrompt.explanation}</p>
            </div>
            <button
              type="button"
              className="inline-flex items-center gap-2 rounded-lg bg-emerald-600 px-4 py-2 text-sm font-semibold text-white shadow-sm transition hover:bg-emerald-500"
            >
              👉 実際に動かしてみる
            </button>
            <button
              type="button"
              onClick={reset}
              className="text-xs font-semibold text-slate-400 hover:text-slate-600"
            >
              ほかのプロンプトも試す
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
