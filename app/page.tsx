import Link from "next/link";
import { courseCatalog, lessons, userProfile } from "@/lib/content";

export default function HomePage() {
  const completedLessons = userProfile.completedLessons.length;
  const totalLessons = Object.keys(lessons).length;
  const completionLabel = `${completedLessons}個 完了レッスン`;

  return (
    <div className="space-y-8">
      <section className="overflow-hidden rounded-3xl border border-slate-300 bg-white shadow-sm">
        <div className="grid grid-cols-[2fr_1fr_1fr] border-b border-slate-200 bg-slate-50 text-xs font-semibold uppercase tracking-wider text-slate-500">
          <div className="px-6 py-3">ユーザー名</div>
          <div className="px-6 py-3">完了レッスン</div>
          <div className="px-6 py-3">バッジ</div>
        </div>
        <div className="grid grid-cols-[2fr_1fr_1fr] items-center gap-4 px-6 py-6 text-sm text-slate-700">
          <div>
            <div className="text-lg font-semibold text-slate-900">{userProfile.name}</div>
            <p className="mt-1 text-xs text-slate-500">現在のプラン: {userProfile.plan.toUpperCase()}</p>
          </div>
          <div className="text-base font-semibold text-slate-800">{completionLabel}</div>
          <div className="flex flex-wrap items-center gap-2">
            {userProfile.badges.length > 0 ? (
              userProfile.badges.map((badge) => (
                <span key={badge} className="rounded-full border border-teal-200 bg-teal-50 px-3 py-1 text-xs font-semibold text-teal-600">
                  {badge}
                </span>
              ))
            ) : (
              <span className="text-xs text-slate-400">バッジはまだありません</span>
            )}
          </div>
        </div>
      </section>

      <section className="overflow-hidden rounded-3xl border border-slate-300 bg-white shadow-sm">
        <header className="border-b border-slate-200 bg-slate-50 px-6 py-4 text-sm font-semibold text-slate-600">コース一覧</header>
        <ul className="divide-y divide-slate-200 text-sm text-slate-700">
          {courseCatalog.map((course) => (
            <li key={course.id} className="flex flex-wrap items-center justify-between gap-4 px-6 py-5">
              <div>
                <div className="text-base font-semibold text-slate-800">{course.title}</div>
                <p className="mt-1 text-xs text-slate-500">{course.description}</p>
              </div>
              <Link
                href={`/courses/${course.id}`}
                className="rounded-full bg-teal-400 px-5 py-2 text-sm font-semibold text-white shadow-sm transition hover:bg-teal-500"
              >
                始める
              </Link>
            </li>
          ))}
        </ul>
      </section>
    </div>
  );
}
