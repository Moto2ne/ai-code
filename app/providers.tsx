"use client";

import { ThemeProvider } from "next-themes";
import type { ReactNode } from "react";
import { ProgressProvider } from "@/lib/progress-store";
import { userProfile } from "@/lib/content";

export function Providers({ children }: { children: ReactNode }) {
  return (
    <ThemeProvider attribute="class" defaultTheme="light" enableSystem>
      <ProgressProvider initialProfile={userProfile}>{children}</ProgressProvider>
    </ThemeProvider>
  );
}
