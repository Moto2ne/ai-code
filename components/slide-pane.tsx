"use client";

import Image from "next/image";
import type { SlideBlock } from "@/lib/content";

function renderSlideContent(slide: SlideBlock) {
  if (slide.type === "text") {
    return <p className="whitespace-pre-wrap text-sm leading-relaxed text-slate-700">{slide.content}</p>;
  }

  if (slide.type === "note") {
    return (
      <div className="rounded-lg border border-sky-200 bg-sky-50 p-4 text-sm leading-relaxed text-slate-700">
        {slide.content}
      </div>
    );
  }

  if (slide.type === "code") {
    return (
      <pre className="overflow-x-auto rounded-lg bg-slate-900 p-4 text-xs text-slate-100">
        <code>{slide.content}</code>
      </pre>
    );
  }

  if (slide.type === "image") {
    return (
      <figure className="overflow-hidden rounded-lg border border-slate-200 bg-white p-2">
        <Image src={slide.src} alt={slide.alt ?? "スライド画像"} width={320} height={200} className="h-auto w-full rounded" />
        {slide.alt && <figcaption className="mt-2 text-center text-[11px] text-slate-400">{slide.alt}</figcaption>}
      </figure>
    );
  }

  return null;
}

export function SlidePane({ slides }: { slides: SlideBlock[] }) {
  return (
    <div className="flex h-full flex-col">
      <h2 className="text-xs font-semibold uppercase tracking-wide text-slate-500">手順</h2>
      <div className="mt-3 flex-1 overflow-y-auto">
        <ol className="space-y-3 text-sm leading-relaxed text-slate-700">
          {slides.map((slide, index) => (
            <li key={index} className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm">
              <div className="mb-2 text-[11px] font-semibold uppercase tracking-wider text-slate-400">STEP {index + 1}</div>
              <div className="space-y-3">{renderSlideContent(slide)}</div>
            </li>
          ))}
        </ol>
      </div>
    </div>
  );
}
