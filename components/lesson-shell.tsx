"use client";

import { useCallback, useDeferredValue, useEffect, useMemo, useRef, useState } from "react";
import { course, type LessonDefinition } from "@/lib/content";
import { extractMarkupFromSource } from "@/lib/lesson-utils";
import { useProgress } from "@/lib/progress-store";
import { CodeEditor } from "./code-editor";
import { SlidePane } from "./slide-pane";
import { LivePreview } from "./live-preview";
import { TestRunner } from "./test-runner";
import { XPToast } from "./xp-toast";
import { AIChatPanel } from "./ai-chat-panel";

export function LessonShell({ lesson }: { lesson: LessonDefinition }) {
  const defaultSource = `export default function Result() {\n  return (\n    <main className="p-6 space-y-4">\n      <p data-placeholder="ai-response">AIチャットの回答をここに貼り付けましょう。</p>\n    </main>\n  );\n}`;

  const initialSource = useMemo(() => {
    const [firstFile] = Object.values(lesson.starterFiles);
    return firstFile ?? defaultSource;
  }, [defaultSource, lesson.starterFiles]);

  const [source, setSource] = useState(initialSource);
  const deferredSource = useDeferredValue(source);
  const markup = useMemo(() => extractMarkupFromSource(deferredSource), [deferredSource]);
  const { profile, markLessonComplete } = useProgress();
  const [xpTrigger, setXpTrigger] = useState(profile.xp);
  const completionRef = useRef(profile.completedLessons.includes(lesson.id));
  const prevXpRef = useRef(profile.xp);

  useEffect(() => {
    setSource(initialSource);
  }, [initialSource, lesson.id]);

  useEffect(() => {
    if (profile.xp > prevXpRef.current) {
      setXpTrigger(profile.xp);
    }
    prevXpRef.current = profile.xp;
  }, [profile.xp]);

  const handleAllPassed = useCallback(() => {
    if (completionRef.current) {
      return;
    }
    completionRef.current = true;
    markLessonComplete(lesson);
  }, [lesson, markLessonComplete]);

  const breadcrumb = useMemo(() => {
    const chapterTitle = course.chapters.find((chapter) => chapter.id === lesson.chapterId)?.title ?? lesson.chapterId;
    return ["AIコーディング初級編", chapterTitle, lesson.title];
  }, [lesson.chapterId, lesson.title]);

  const handleApplyAIResponse = useCallback((htmlSnippet: string) => {
    setSource((prev) => {
      const placeholderPattern = /<p\s+data-placeholder="ai-response">[\s\S]*?<\/p>/;
      if (placeholderPattern.test(prev)) {
        return prev.replace(placeholderPattern, htmlSnippet);
      }
      return `${prev.trim()}\n\n${htmlSnippet}`;
    });
  }, []);

  return (
    <div className="flex h-full min-h-[640px] flex-col overflow-hidden rounded-3xl border border-slate-300 bg-white">
      <header className="border-b border-slate-200 bg-slate-50 px-6 py-4">
        <nav className="flex flex-wrap items-center gap-2 text-xs text-slate-500">
          {breadcrumb.map((item, index) => (
            <span key={`${item}-${index}`} className="flex items-center gap-2">
              {index > 0 && <span className="text-slate-300">&gt;</span>}
              <span className={index === breadcrumb.length - 1 ? "font-semibold text-slate-700" : ""}>{item}</span>
            </span>
          ))}
        </nav>
      </header>
      <div className="grid flex-1 min-h-0 grid-cols-[260px_minmax(420px,1fr)_300px] divide-x divide-slate-200">
        <section className="flex min-h-0 flex-col px-6 py-6">
          <SlidePane slides={lesson.slides} />
        </section>
        <section className="flex min-h-0 flex-col">
          <header className="flex items-center justify-between border-b border-slate-200 px-6 py-3 text-xs font-semibold text-slate-500">
            <span>コード</span>
          </header>
          <div className="flex-1 min-h-0 px-6 py-4">
            <div className="h-full min-h-0 overflow-hidden rounded-2xl border border-slate-200">
              <CodeEditor value={source} onChange={setSource} language="javascript" />
            </div>
          </div>
        </section>
        <section className="flex min-h-0 flex-col">
          <div className="flex basis-1/2 flex-col border-b border-slate-200 px-6 py-4">
            <header className="mb-3 text-xs font-semibold text-slate-500">プレビュー</header>
            <div className="flex-1 min-h-0 overflow-hidden rounded-lg border border-slate-200 bg-white">
              <LivePreview markup={markup} />
            </div>
          </div>
          <div className="flex basis-1/2 flex-col px-6 py-4">
            <header className="mb-3 text-xs font-semibold text-slate-500">🤖 AIチャット</header>
            <AIChatPanel lesson={lesson} onGenerateResponse={handleApplyAIResponse} />
          </div>
        </section>
      </div>
      <footer className="flex items-center justify-between border-t border-slate-200 bg-slate-50 px-6 py-4">
        <div>
          <div className="text-xs font-semibold text-slate-500">タスク</div>
          <p className="text-sm text-slate-700">{lesson.task.goal}</p>
        </div>
        <TestRunner lesson={lesson} markup={markup} onAllPassed={handleAllPassed} variant="compact" />
      </footer>
      <XPToast xp={xpTrigger} />
    </div>
  );
}
