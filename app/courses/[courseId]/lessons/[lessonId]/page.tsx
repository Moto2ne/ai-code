"use client";

import { useParams } from "next/navigation";
import { lessons } from "@/lib/content";
import { LessonShell } from "@/components/lesson-shell";

export default function LessonPage() {
  const params = useParams();
  const lessonId = params.lessonId as string;
  const lesson = lessons[lessonId];

  if (!lesson) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <p className="text-slate-600">レッスンが見つかりません</p>
      </div>
    );
  }

  return (
    <div className="flex h-full min-h-0 flex-1 flex-col overflow-hidden">
      <LessonShell lesson={lesson} />
    </div>
  );
}
