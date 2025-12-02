export function SkeletonCard() {
  return (
    <div className="animate-pulse rounded-xl border border-slate-200 bg-white p-6">
      <div className="h-6 w-3/4 rounded bg-slate-200" />
      <div className="mt-3 h-4 w-full rounded bg-slate-200" />
      <div className="mt-2 h-4 w-5/6 rounded bg-slate-200" />
      <div className="mt-4 flex gap-2">
        <div className="h-8 w-20 rounded bg-slate-200" />
        <div className="h-8 w-20 rounded bg-slate-200" />
      </div>
    </div>
  );
}

export function SkeletonLesson() {
  return (
    <div className="grid h-screen grid-cols-1 md:grid-cols-2 lg:grid-cols-3">
      <div className="animate-pulse border-r border-slate-200 bg-slate-50 p-6">
        <div className="mb-4 h-8 w-2/3 rounded bg-slate-200" />
        <div className="space-y-3">
          <div className="h-4 w-full rounded bg-slate-200" />
          <div className="h-4 w-5/6 rounded bg-slate-200" />
          <div className="h-4 w-4/6 rounded bg-slate-200" />
        </div>
        <div className="mt-8 h-48 w-full rounded bg-slate-200" />
      </div>
      <div className="animate-pulse border-r border-slate-200 p-6">
        <div className="mb-4 h-6 w-32 rounded bg-slate-200" />
        <div className="h-96 w-full rounded bg-slate-200" />
      </div>
      <div className="animate-pulse p-6">
        <div className="mb-4 h-6 w-32 rounded bg-slate-200" />
        <div className="h-96 w-full rounded bg-slate-200" />
      </div>
    </div>
  );
}

export function SkeletonDashboard() {
  return (
    <div className="animate-pulse space-y-6 p-8">
      <div className="h-10 w-64 rounded bg-slate-200" />
      <div className="grid gap-6 md:grid-cols-3">
        <div className="h-32 rounded-xl bg-slate-200" />
        <div className="h-32 rounded-xl bg-slate-200" />
        <div className="h-32 rounded-xl bg-slate-200" />
      </div>
      <div className="h-64 rounded-xl bg-slate-200" />
    </div>
  );
}
