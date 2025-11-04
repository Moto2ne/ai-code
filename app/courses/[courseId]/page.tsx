import Link from "next/link";
import { notFound } from "next/navigation";
import { courseCatalog } from "@/lib/content";

interface CoursePageProps {
  params: { courseId: string };
}

export default function CoursePage({ params }: CoursePageProps) {
  const course = courseCatalog.find((entry) => entry.id === params.courseId);

  if (!course) {
    notFound();
  }

  return (
    <div className="space-y-6">
      <section className="overflow-hidden rounded-3xl border border-slate-300 bg-white shadow-sm">
        <header className="border-b border-slate-200 bg-slate-50 px-6 py-4 text-sm font-semibold text-slate-600">
          {course.title}
        </header>
        <p className="px-6 py-5 text-sm leading-relaxed text-slate-600">{course.description}</p>
      </section>

      <section className="overflow-hidden rounded-3xl border border-slate-300 bg-white shadow-sm">
        <ul className="divide-y divide-slate-200">
          {course.modules.map((module, index) => (
            <li key={module.id} className="flex flex-wrap items-center justify-between gap-6 px-8 py-6">
              <div>
                <div className="text-[11px] font-semibold uppercase tracking-wide text-slate-400">コース {index + 1}</div>
                <div className="mt-1 text-lg font-semibold text-slate-800">{module.title}</div>
                {module.description && <p className="mt-2 text-sm text-slate-500">{module.description}</p>}
              </div>
              {module.lessonId ? (
                <Link
                  href={`/courses/${course.id}/lessons/${module.lessonId}`}
                  className="rounded-full bg-teal-400 px-5 py-2 text-sm font-semibold text-white shadow-sm transition hover:bg-teal-500"
                >
                  始める
                </Link>
              ) : (
                <span className="rounded-full bg-slate-200 px-5 py-2 text-sm font-semibold text-slate-500">近日公開</span>
              )}
            </li>
          ))}
        </ul>
      </section>

      <Link href="/" className="inline-flex items-center gap-1 text-sm font-semibold text-slate-500 transition hover:text-slate-700">
        ← 戻る
      </Link>
    </div>
  );
}
