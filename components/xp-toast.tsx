"use client";

import { createPortal } from "react-dom";
import { useEffect, useRef, useState } from "react";

export function XPToast({ xp }: { xp: number }) {
  const [isMounted, setIsMounted] = useState(false);
  const [visible, setVisible] = useState(false);
  const [count, setCount] = useState(0);
  const didMountRef = useRef(false);

  useEffect(() => {
    setIsMounted(true);
  }, []);

  useEffect(() => {
    if (!didMountRef.current) {
      didMountRef.current = true;
      return;
    }
    setCount((prev: number) => prev + 1);
    setVisible(true);
    const timer = window.setTimeout(() => setVisible(false), 2000);
    return () => window.clearTimeout(timer);
  }, [xp]);

  if (!isMounted || !visible) {
    return null;
  }

  return createPortal(
    <div className="fixed bottom-6 right-6 z-50 flex flex-col gap-2">
      <div className="rounded-lg border border-amber-200 bg-amber-50 px-4 py-3 text-sm font-semibold text-amber-700 shadow-lg">
        +50 XP 獲得！ ({count})
      </div>
    </div>,
    document.body
  );
}
