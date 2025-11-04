"use client";

import { useState } from "react";
import type { LessonDefinition } from "@/lib/content";

export function HintPanel({ lesson }: { lesson: LessonDefinition }) {
  const [copiedIndex, setCopiedIndex] = useState<number | null>(null);

  const handleCopy = async (text: string, index: number) => {
    try {
      await navigator.clipboard.writeText(text);
      setCopiedIndex(index);
      setTimeout(() => setCopiedIndex(null), 2000);
    } catch (error) {
      console.error("Failed to copy", error);
    }
  };

  const suggestions = lesson.qa.map((entry) => entry.split("A.")[0].trim());

  return (
    <aside className="space-y-4 rounded-lg border border-slate-200 bg-white p-4 shadow-sm">
      <div>
        <h3 className="text-sm font-semibold text-slate-700">AIヒント</h3>
        <p className="mt-1 text-xs text-slate-500">
          質問例をコピーして、お困りごとをAIに相談しましょう。
        </p>
      </div>
      <div>
        <h4 className="text-xs font-semibold uppercase tracking-wide text-slate-500">ヒント</h4>
        <ul className="mt-2 space-y-2">
          {lesson.task.hints.map((hint, index) => (
            <li key={index} className="rounded-md border border-brand-100 bg-brand-50 px-3 py-2 text-xs text-brand-700">
              {hint}
            </li>
          ))}
        </ul>
      </div>
      <div>
        <h4 className="text-xs font-semibold uppercase tracking-wide text-slate-500">質問テンプレ</h4>
        <ul className="mt-2 space-y-2">
          {suggestions.map((suggestion, index) => (
            <li key={index} className="flex items-center justify-between gap-2 rounded-md border border-slate-200 px-3 py-2 text-xs text-slate-600">
              <span className="line-clamp-2">{suggestion}</span>
              <button
                type="button"
                onClick={() => handleCopy(`${suggestion} ${lesson.qa[index]}`, index)}
                className="rounded bg-brand-600 px-2 py-1 text-[10px] font-semibold text-white hover:bg-brand-700"
              >
                {copiedIndex === index ? "コピー済" : "コピー"}
              </button>
            </li>
          ))}
        </ul>
      </div>
    </aside>
  );
}
