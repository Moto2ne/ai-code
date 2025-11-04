import { clsx } from "clsx";

export function ProgressBar({ value }: { value: number }) {
  return (
    <div className="h-2 w-full rounded-full bg-slate-200">
      <div
        className={clsx("h-2 rounded-full bg-brand-500 transition-all", value >= 100 && "bg-emerald-500")}
        style={{ width: `${Math.min(100, Math.max(0, value))}%` }}
      />
    </div>
  );
}
