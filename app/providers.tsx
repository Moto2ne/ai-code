"use client";

import { ThemeProvider } from "next-themes";
import type { ReactNode } from "react";
import { ProgressProvider } from "@/lib/progress-store";
import { AuthProvider } from "@/lib/auth-context";
import { Toaster } from "sonner";
import { userProfile } from "@/lib/content";

export function Providers({ children }: { children: ReactNode }) {
  return (
    <ThemeProvider attribute="class" defaultTheme="light" enableSystem>
      <AuthProvider>
        <ProgressProvider initialProfile={userProfile}>
          {children}
          <Toaster position="top-right" richColors />
        </ProgressProvider>
      </AuthProvider>
    </ThemeProvider>
  );
}
