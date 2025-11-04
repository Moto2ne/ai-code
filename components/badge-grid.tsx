export function BadgeGrid({ badges }: { badges: string[] }) {
  if (badges.length === 0) {
    return (
      <div className="rounded-lg border border-dashed border-slate-200 p-4 text-sm text-slate-500">
        取得したバッジはまだありません。レッスンを進めて獲得しましょう！
      </div>
    );
  }
  return (
    <ul className="flex flex-wrap gap-2">
      {badges.map((badge) => (
        <li key={badge} className="rounded-full border border-amber-200 bg-amber-50 px-3 py-1 text-xs font-semibold text-amber-600">
          {badge}
        </li>
      ))}
    </ul>
  );
}
