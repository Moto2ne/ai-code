"use client";

import { useMemo } from "react";
import { buildPreviewDocument } from "@/lib/lesson-utils";

export function LivePreview({ markup }: { markup: string }) {
  const srcDoc = useMemo(() => buildPreviewDocument(markup), [markup]);

  return <iframe title="Live preview" srcDoc={srcDoc} className="h-full w-full border-0 bg-white" />;
}
