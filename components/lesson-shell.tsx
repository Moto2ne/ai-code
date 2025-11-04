"use client";

import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import type { LessonDefinition } from "@/lib/content";
import { extractMarkupFromSource } from "@/lib/lesson-utils";
import { useProgress } from "@/lib/progress-store";
import { CodeEditor } from "./code-editor";
import { SlidePane } from "./slide-pane";
import { LivePreview } from "./live-preview";
import { TestRunner } from "./test-runner";
import { HintPanel } from "./hint-panel";
import { XPToast } from "./xp-toast";

export function LessonShell({ lesson }: { lesson: LessonDefinition }) {
  const initialSource = useMemo(() => {
    const [firstFile] = Object.values(lesson.starterFiles);
    return firstFile ?? "export default function Result() {\n  return (\n    <main className=\"p-6\">まだコードがありません</main>\n  );\n}";
  }, [lesson.starterFiles]);

  const [source, setSource] = useState(initialSource);
  const markup = useMemo(() => extractMarkupFromSource(source), [source]);
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

  return (
    <div className="space-y-6">
      <div className="grid h-[640px] grid-cols-[minmax(240px,0.95fr)_minmax(320px,1.4fr)_minmax(240px,0.9fr)] gap-4">
        <div className="overflow-y-auto rounded-lg border border-slate-200 bg-slate-50 p-4">
          <div className="mb-3 text-xs font-semibold uppercase tracking-wide text-slate-500">スライド</div>
          <SlidePane slides={lesson.slides} />
        </div>
        <div className="flex flex-col gap-4 overflow-hidden">
          <div className="flex-1 overflow-hidden">
            <div className="mb-2 flex items-center justify-between text-xs font-semibold text-slate-500">
              <span>コードエディタ</span>
              <span className="rounded bg-slate-100 px-2 py-0.5 text-[10px] uppercase">Monaco</span>
            </div>
            <div className="h-full min-h-[280px]">
              <CodeEditor value={source} onChange={setSource} language="javascript" />
            </div>
          </div>
          <div className="flex-1 overflow-hidden">
            <div className="mb-2 flex items-center justify-between text-xs font-semibold text-slate-500">
              <span>ライブプレビュー</span>
              <span className="rounded bg-emerald-100 px-2 py-0.5 text-[10px] uppercase text-emerald-700">Auto Refresh</span>
            </div>
            <div className="h-full min-h-[240px]">
              <LivePreview markup={markup} />
            </div>
          </div>
        </div>
        <div className="overflow-y-auto">
          <HintPanel lesson={lesson} />
        </div>
      </div>
      <div className="rounded-lg border border-slate-200 bg-white p-4 shadow-sm">
        <div className="mb-3 flex items-center justify-between">
          <div>
            <div className="text-sm font-semibold text-slate-700">タスク</div>
            <p className="text-xs text-slate-500">{lesson.task.goal}</p>
          </div>
          <span className="rounded-full bg-brand-50 px-3 py-1 text-xs font-semibold text-brand-600">自動採点</span>
        </div>
        <TestRunner lesson={lesson} markup={markup} onAllPassed={handleAllPassed} />
      </div>
      <XPToast xp={xpTrigger} />
    </div>
  );
}
