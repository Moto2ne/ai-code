import "./globals.css";
import type { Metadata } from "next";
import { ReactNode } from "react";
import { Providers } from "./providers";

export const metadata: Metadata = {
  title: "Setup Coach",
  description: "Slide-led learning with live coding and AI support"
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="ja">
      <body className="min-h-screen bg-slate-50 text-slate-900">
        <Providers>
          <div className="flex min-h-screen flex-col">
            <header className="border-b border-slate-200 bg-white">
              <div className="mx-auto flex w-full max-w-6xl items-center justify-between px-6 py-4">
                <div className="flex items-center gap-2">
                  <span className="text-2xl font-bold text-brand-600">Setup Coach</span>
                  <span className="rounded-full bg-brand-50 px-2 py-1 text-xs font-semibold text-brand-600">
                    beta
                  </span>
                </div>
                <nav className="flex items-center gap-4 text-sm font-medium text-slate-600">
                  <a href="/dashboard" className="hover:text-brand-600">
                    ダッシュボード
                  </a>
                  <a href="/ask-coach" className="hover:text-brand-600">
                    Ask Coach
                  </a>
                  <a href="/setup" className="hover:text-brand-600">
                    Setup
                  </a>
                  <a href="/publish" className="hover:text-brand-600">
                    Publish
                  </a>
                </nav>
              </div>
            </header>
            <main className="mx-auto w-full max-w-6xl flex-1 px-6 py-8">{children}</main>
            <footer className="border-t border-slate-200 bg-white">
              <div className="mx-auto flex w-full max-w-6xl items-center justify-between px-6 py-4 text-xs text-slate-500">
                <span>© {new Date().getFullYear()} Setup Coach</span>
                <span>Made for guided web dev onboarding</span>
              </div>
            </footer>
          </div>
        </Providers>
      </body>
    </html>
  );
}
