import Link from "next/link";
import { course, lessons, userProfile } from "@/lib/content";
import { ProgressBar } from "@/components/progress-bar";

function calculateProgress(): number {
  const completed = userProfile.completedLessons.length;
  const total = Object.keys(lessons).length;
  if (total === 0) {
    return 0;
  }
  return Math.round((completed / total) * 100);
}

export default function HomePage() {
  const nextLessonId = userProfile.currentLessonId;
  const totalMinutes = course.chapters.reduce((sum, chapter) => sum + chapter.order.length * 8, 0);

  return (
    <div className="space-y-8">
      <section className="rounded-2xl border border-slate-200 bg-gradient-to-br from-brand-50 via-white to-white px-8 py-10 shadow-sm">
        <div className="flex flex-col gap-6 md:flex-row md:items-center md:justify-between">
          <div className="max-w-2xl space-y-4">
            <p className="text-sm font-semibold uppercase tracking-wide text-brand-600">未経験者でも迷わない</p>
            <h1 className="text-3xl font-bold text-slate-900 md:text-4xl">スライド学習と実装体験を1つの画面で</h1>
            <p className="text-sm text-slate-600">
              Progateの分かりやすさにAIコーチと実行環境を組み合わせたNext.js学習コースです。一本道のナビと即時フィードバックで、無理なく進捗を積み上げましょう。
            </p>
          </div>
          <div className="w-full max-w-sm rounded-xl border border-brand-100 bg-white p-5 shadow-md">
            <div className="text-xs font-semibold uppercase tracking-wide text-slate-500">現在の進捗</div>
            <div className="mt-3 text-3xl font-bold text-brand-600">{userProfile.xp} XP</div>
            <p className="mt-2 text-sm text-slate-500">あと {Math.max(0, 500 - userProfile.xp)} XP で次のバッジ</p>
            <div className="mt-4 space-y-2">
              <ProgressBar value={calculateProgress()} />
              <div className="flex items-center justify-between text-xs text-slate-500">
                <span>{calculateProgress()}%</span>
                <span>{userProfile.completedLessons.length} / {Object.keys(lessons).length} Lessons</span>
              </div>
            </div>
            <Link
              href={`/courses/${course.id}/lessons/${nextLessonId}`}
              className="mt-6 inline-flex w-full items-center justify-center rounded-lg bg-brand-600 px-4 py-2 text-sm font-semibold text-white shadow-sm transition hover:bg-brand-700"
            >
              続きを学習する
            </Link>
          </div>
        </div>
      </section>

      <section className="grid gap-6 md:grid-cols-[2fr_1fr]">
        <div className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-lg font-semibold text-slate-900">{course.title}</h2>
              <p className="text-sm text-slate-500">所要時間: 約 {totalMinutes} 分</p>
            </div>
            <Link href={`/courses/${course.id}`} className="text-sm font-semibold text-brand-600 hover:text-brand-700">
              コース詳細へ
            </Link>
          </div>
          <p className="mt-4 text-sm text-slate-600">{course.description}</p>
          <div className="mt-6 space-y-4">
            {course.chapters.map((chapter) => (
              <div key={chapter.id} className="rounded-lg border border-slate-200 bg-slate-50 p-4">
                <div className="flex items-center justify-between">
                  <div>
                    <h3 className="text-sm font-semibold text-slate-800">{chapter.title}</h3>
                    <p className="text-xs text-slate-500">{chapter.description}</p>
                  </div>
                  <span className="text-xs text-slate-400">{chapter.order.length} レッスン</span>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="flex flex-col gap-6">
          <div className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
            <h3 className="text-sm font-semibold text-slate-800">AIコーチがサポート</h3>
            <p className="mt-2 text-sm text-slate-600">
              各レッスンの右下から「質問テンプレ」をコピーして、最適な聞き方でAsk Coachに相談できます。
            </p>
            <Link href="/ask-coach" className="mt-4 inline-flex items-center text-sm font-semibold text-brand-600 hover:text-brand-700">
              Ask Coachを開く →
            </Link>
          </div>
          <div className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
            <h3 className="text-sm font-semibold text-slate-800">セットアップをチェック</h3>
            <p className="mt-2 text-sm text-slate-600">VS CodeやNode.jsの環境準備が完了しているか、チェックリストで確認しましょう。</p>
            <Link href="/setup" className="mt-4 inline-flex items-center text-sm font-semibold text-brand-600 hover:text-brand-700">
              Setup手順を見る →
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
}
