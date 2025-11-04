import Link from "next/link";
import { notFound } from "next/navigation";
import { course, lessons } from "@/lib/content";

interface CoursePageProps {
  params: { courseId: string };
}

export default function CoursePage({ params }: CoursePageProps) {
  if (params.courseId !== course.id) {
    notFound();
  }

  return (
    <div className="space-y-8">
      <header className="rounded-2xl border border-slate-200 bg-white p-8 shadow-sm">
        <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
          <div>
            <h1 className="text-3xl font-bold text-slate-900">{course.title}</h1>
            <p className="mt-2 text-sm text-slate-600">{course.description}</p>
            <div className="mt-4 flex flex-wrap gap-3 text-xs text-slate-500">
              <span className="rounded-full bg-slate-100 px-3 py-1">対象: {course.audience}</span>
              <span className="rounded-full bg-slate-100 px-3 py-1">所要時間: 約 {course.durationMinutes} 分</span>
            </div>
          </div>
          <Link
            href={`/courses/${course.id}/lessons/${course.chapters[0].order[0]}`}
            className="inline-flex items-center justify-center rounded-lg bg-brand-600 px-5 py-2 text-sm font-semibold text-white shadow-sm transition hover:bg-brand-700"
          >
            レッスンに進む
          </Link>
        </div>
      </header>

      <section className="grid gap-6 md:grid-cols-[3fr_2fr]">
        <div className="space-y-4">
          {course.chapters.map((chapter) => (
            <article key={chapter.id} className="rounded-xl border border-slate-200 bg-slate-50 p-6 shadow-sm">
              <div className="flex items-center justify-between">
                <div>
                  <h2 className="text-lg font-semibold text-slate-900">{chapter.title}</h2>
                  <p className="text-sm text-slate-600">{chapter.description}</p>
                </div>
                <span className="text-xs text-slate-400">{chapter.order.length} lessons</span>
              </div>
              <ol className="mt-4 space-y-3">
                {chapter.order.map((lessonId, index) => {
                  const lesson = lessons[lessonId];
                  return (
                    <li key={lessonId} className="rounded-md border border-slate-200 bg-white p-3 text-sm text-slate-700">
                      <div className="flex items-center justify-between gap-3">
                        <div>
                          <div className="text-xs font-semibold uppercase tracking-wide text-slate-400">Lesson {index + 1}</div>
                          <div className="font-semibold text-slate-800">{lesson.title}</div>
                          <div className="text-xs text-slate-500">目安 {lesson.durationMinutes} 分</div>
                        </div>
                        <Link
                          href={`/courses/${course.id}/lessons/${lesson.id}`}
                          className="rounded-md border border-brand-200 px-3 py-1 text-xs font-semibold text-brand-600 hover:bg-brand-50"
                        >
                          開く
                        </Link>
                      </div>
                    </li>
                  );
                })}
              </ol>
            </article>
          ))}
        </div>
        <aside className="space-y-4">
          <div className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
            <h3 className="text-sm font-semibold text-slate-900">学習の柱</h3>
            <ul className="mt-3 space-y-2 text-sm text-slate-600">
              <li>一本道ナビで迷わず進む</li>
              <li>コードを書くたびにライブプレビュー</li>
              <li>AIヒントでいつでも質問</li>
            </ul>
          </div>
          <div className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
            <h3 className="text-sm font-semibold text-slate-900">到達目標</h3>
            <ul className="mt-3 space-y-2 text-sm text-slate-600">
              {course.outcomes.map((outcome) => (
                <li key={outcome}>{outcome}</li>
              ))}
            </ul>
          </div>
        </aside>
      </section>
    </div>
  );
}
