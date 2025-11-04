import Link from "next/link";
import { notFound } from "next/navigation";
import type { LessonDefinition } from "@/lib/content";
import { course, lessons } from "@/lib/content";
import { LessonShell } from "@/components/lesson-shell";

interface LessonPageProps {
  params: { courseId: string; lessonId: string };
}

function findLessonNavigation(lessonId: string): { previous?: LessonDefinition; next?: LessonDefinition } {
  const chapterOrder = course.chapters.flatMap((chapter) => chapter.order);
  const index = chapterOrder.indexOf(lessonId);
  if (index === -1) {
    return {};
  }
  const previousId = chapterOrder[index - 1];
  const nextId = chapterOrder[index + 1];
  return {
    previous: previousId ? lessons[previousId] : undefined,
    next: nextId ? lessons[nextId] : undefined
  };
}

export default function LessonPage({ params }: LessonPageProps) {
  if (params.courseId !== course.id) {
    notFound();
  }
  const lesson = lessons[params.lessonId];
  if (!lesson) {
    notFound();
  }
  const navigation = findLessonNavigation(lesson.id);

  return (
    <div className="space-y-6">
      <header className="flex flex-wrap items-center justify-between gap-4 rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
        <div>
          <p className="text-xs font-semibold uppercase tracking-wide text-brand-600">{course.title}</p>
          <h1 className="text-xl font-bold text-slate-900">{lesson.title}</h1>
          <p className="text-sm text-slate-500">目安 {lesson.durationMinutes} 分 / チャプター {lesson.chapterId}</p>
        </div>
        <div className="flex items-center gap-2 text-xs">
          {navigation.previous && (
            <Link
              href={`/courses/${course.id}/lessons/${navigation.previous.id}`}
              className="rounded-md border border-slate-200 px-3 py-1 font-semibold text-slate-600 hover:bg-slate-50"
            >
              ← {navigation.previous.title}
            </Link>
          )}
          {navigation.next && (
            <Link
              href={`/courses/${course.id}/lessons/${navigation.next.id}`}
              className="rounded-md border border-brand-200 bg-brand-50 px-3 py-1 font-semibold text-brand-600 hover:bg-brand-100"
            >
              {navigation.next.title} →
            </Link>
          )}
        </div>
      </header>
      <LessonShell lesson={lesson} />
    </div>
  );
}
