import Image from "next/image";
import type { SlideBlock } from "@/lib/content";

export function SlidePane({ slides }: { slides: SlideBlock[] }) {
  return (
    <div className="space-y-4">
      {slides.map((slide, index) => {
        if (slide.type === "text" || slide.type === "note") {
          return (
            <div
              key={index}
              className={slide.type === "note" ? "rounded-md border border-brand-200 bg-brand-50 p-4" : "rounded-md bg-white p-4 shadow-sm"}
            >
              <p className="whitespace-pre-wrap text-sm leading-relaxed text-slate-700">{slide.content}</p>
            </div>
          );
        }
        if (slide.type === "code") {
          return (
            <pre key={index} className="overflow-x-auto rounded-md bg-slate-900 p-4 text-xs text-slate-100">
              <code>{slide.content}</code>
            </pre>
          );
        }
        if (slide.type === "image") {
          return (
            <div key={index} className="overflow-hidden rounded-md border border-slate-200 bg-white p-2">
              <Image
                src={slide.src}
                alt={slide.alt ?? "スライド画像"}
                width={320}
                height={180}
                className="h-auto w-full rounded"
              />
            </div>
          );
        }
        return null;
      })}
    </div>
  );
}
