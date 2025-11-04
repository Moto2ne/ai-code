"use client";

import { useMemo } from "react";
import { buildPreviewDocument } from "@/lib/lesson-utils";

export function LivePreview({ markup }: { markup: string }) {
  const srcDoc = useMemo(() => buildPreviewDocument(markup), [markup]);

  return (
    <div className="h-full overflow-hidden rounded-lg border border-slate-200 bg-white shadow-sm">
      <iframe title="Live preview" srcDoc={srcDoc} className="h-full w-full bg-white" />
    </div>
  );
}
