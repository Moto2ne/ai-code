"use client";

import Link from "next/link";
import { BadgeGrid } from "@/components/badge-grid";
import { ProgressBar } from "@/components/progress-bar";
import { course, lessons } from "@/lib/content";
import { useProgress } from "@/lib/progress-store";

export default function DashboardPage() {
  const { profile } = useProgress();
  const completedSet = new Set(profile.completedLessons);
  const totalLessons = Object.keys(lessons).length;
  const progressValue = totalLessons === 0 ? 0 : Math.round((completedSet.size / totalLessons) * 100);

  const nextLesson = course.chapters
    .flatMap((chapter) => chapter.order)
    .map((lessonId) => lessons[lessonId])
    .find((lesson) => !completedSet.has(lesson.id));

  return (
    <div className="space-y-8">
      <header className="rounded-2xl border border-slate-200 bg-white p-8 shadow-sm">
        <div className="flex flex-col gap-8 md:flex-row md:items-center md:justify-between">
          <div>
            <p className="text-xs font-semibold uppercase tracking-wide text-brand-600">ダッシュボード</p>
            <h1 className="text-3xl font-bold text-slate-900">ようこそ {profile.name} さん</h1>
            <p className="mt-2 text-sm text-slate-600">今日で連続 {profile.streakDays} 日目。継続するほどXPボーナスが増えます。</p>
          </div>
          <div className="rounded-xl border border-emerald-200 bg-emerald-50 px-6 py-4 text-sm text-emerald-700">
            <div className="font-semibold">現在のプラン: {profile.plan}</div>
            <p className="text-xs">ProプランはAIヒントが無制限になります。</p>
          </div>
        </div>
      </header>

      <section className="grid gap-6 md:grid-cols-[2fr_1fr]">
        <div className="space-y-6">
          <div className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
            <div className="flex items-center justify-between">
              <h2 className="text-lg font-semibold text-slate-900">進捗サマリ</h2>
              <span className="rounded-full bg-brand-50 px-3 py-1 text-xs font-semibold text-brand-600">{profile.xp} XP</span>
            </div>
            <div className="mt-4 space-y-2">
              <ProgressBar value={progressValue} />
              <div className="flex items-center justify-between text-xs text-slate-500">
                <span>{progressValue}% 完了</span>
                <span>{completedSet.size} / {totalLessons} Lessons</span>
              </div>
            </div>
            {nextLesson && (
              <Link
                href={`/courses/${course.id}/lessons/${nextLesson.id}`}
                className="mt-4 inline-flex items-center rounded-md bg-brand-600 px-4 py-2 text-sm font-semibold text-white hover:bg-brand-700"
              >
                次は「{nextLesson.title}」へ →
              </Link>
            )}
          </div>

          <div className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
            <h2 className="text-lg font-semibold text-slate-900">完了済みレッスン</h2>
            {profile.completedLessons.length === 0 ? (
              <p className="mt-3 text-sm text-slate-500">まだレッスンは完了していません。ホームから最初のレッスンを開始しましょう。</p>
            ) : (
              <ul className="mt-4 space-y-2 text-sm text-slate-600">
                {profile.completedLessons.map((lessonId) => (
                  <li key={lessonId} className="flex items-center justify-between rounded-md border border-slate-200 bg-slate-50 px-3 py-2">
                    <span>{lessons[lessonId].title}</span>
                    <span className="text-xs text-slate-400">{lessons[lessonId].durationMinutes} 分</span>
                  </li>
                ))}
              </ul>
            )}
          </div>
        </div>

        <aside className="space-y-6">
          <div className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
            <h3 className="text-sm font-semibold text-slate-900">バッジ</h3>
            <BadgeGrid badges={profile.badges} />
          </div>
          <div className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
            <h3 className="text-sm font-semibold text-slate-900">ロードマップ</h3>
            <ul className="mt-3 space-y-2 text-xs text-slate-500">
              <li>Day 1-14: Lesson Shell + スキーマ + 3課題</li>
              <li>Day 15-30: テスト / XP / 課金 / 公開</li>
              <li>Day 31-60: AIヒント強化・診断</li>
              <li>Day 61-90: 作品投稿・Python/DB拡張</li>
            </ul>
          </div>
        </aside>
      </section>
    </div>
  );
}
