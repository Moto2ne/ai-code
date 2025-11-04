"use client";

import { useCallback, useMemo, useState } from "react";
import type { LessonDefinition } from "@/lib/content";

interface AIChatPanelProps {
  lesson: LessonDefinition;
  onGenerateResponse: (htmlSnippet: string) => void;
}

type ChatMessage = {
  id: string;
  role: "user" | "assistant";
  content: string;
};

function createAssistantSummary(lesson: LessonDefinition) {
  const [firstSlide] = lesson.slides;
  if (firstSlide && "content" in firstSlide && typeof firstSlide.content === "string") {
    return firstSlide.content.split("。")[0]?.trim() ?? "";
  }
  return "レッスンのポイントを復習しましょう";
}

const PRESET_QUESTION = "AIコーディングについて教えてください。";
const PRESET_RESPONSE = `AIコーディングは、AIチャットや生成系APIを活用して要件整理やコードのたたき台作成を効率化し、人間がレビューと仕上げを行う開発スタイルです。ポイントは「目的を具体的に伝える」「生成結果を検証する」「学んだ内容を自分の言葉でまとめる」の3つです。`;

const PRESET_HTML = `<section className="space-y-4">
  <h1 className="text-2xl font-semibold">AIコーディングとは？</h1>
  <p>${PRESET_RESPONSE}</p>
  <ul className="list-disc space-y-2 pl-5">
    <li>ゴールを明確にし、AIへ丁寧に指示する</li>
    <li>生成コードを読み解き、必要な修正を自分で加える</li>
    <li>完成した内容をまとめて次のステップに共有する</li>
  </ul>
</section>`;

export function AIChatPanel({ lesson, onGenerateResponse }: AIChatPanelProps) {
  const intro = useMemo(() => createAssistantSummary(lesson), [lesson]);
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: "assistant-intro",
      role: "assistant",
      content: `こんにちは！レッスンのゴールは「${lesson.task.goal}」です。気になったことはAIに聞いてみましょう。`
    }
  ]);
  const [hasResponded, setHasResponded] = useState(false);

  const handleAsk = useCallback(() => {
    if (hasResponded) {
      return;
    }
    const newMessages: ChatMessage[] = [
      { id: "user-question", role: "user", content: PRESET_QUESTION },
      {
        id: "assistant-answer",
        role: "assistant",
        content: `${PRESET_RESPONSE}\n\n${intro}`.trim()
      }
    ];
    setMessages((prev) => [...prev, ...newMessages]);
    setHasResponded(true);
    onGenerateResponse(PRESET_HTML);
  }, [hasResponded, intro, onGenerateResponse]);

  return (
    <div className="flex h-full min-h-0 flex-col gap-3">
      <div className="flex-1 min-h-0 rounded-lg border border-slate-200 bg-white p-3">
        <ul className="flex h-full min-h-0 flex-col gap-3 overflow-y-auto">
          {messages.map((message) => (
            <li key={message.id} className={`flex ${message.role === "user" ? "justify-start" : "justify-end"}`}>
              <div
                className={`max-w-[85%] rounded-lg px-3 py-2 text-xs leading-relaxed ${
                  message.role === "user" ? "bg-slate-100 text-slate-700" : "bg-teal-400 text-white"
                }`}
              >
                <span className="mb-1 block text-[10px] font-semibold uppercase tracking-wide">
                  {message.role === "user" ? "You" : "AI Coach"}
                </span>
                <span className="whitespace-pre-wrap">{message.content}</span>
              </div>
            </li>
          ))}
        </ul>
      </div>
      <button
        type="button"
        onClick={handleAsk}
        className="self-start rounded-full bg-teal-400 px-4 py-2 text-xs font-semibold text-white shadow-sm transition hover:bg-teal-500 disabled:cursor-not-allowed disabled:bg-slate-300"
        disabled={hasResponded}
      >
        「AIコーディングについて教えてください」と質問する
      </button>
    </div>
  );
}
