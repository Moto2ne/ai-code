import "./globals.css";
import type { Metadata } from "next";
import { ReactNode } from "react";
import { Providers } from "./providers";

export const metadata: Metadata = {
  title: "AICode",
  description: "Slide-led learning with live coding and AI support"
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="ja">
      <body className="flex min-h-screen flex-col bg-slate-50 text-slate-900">
        <Providers>
          <div className="flex flex-1 flex-col">
            <header className="shrink-0 border-b border-slate-200 bg-white">
              <div className="mx-auto flex w-full max-w-6xl items-center justify-between px-6 py-1">
                <div className="flex items-center gap-2">
                  <span className="text-2xl font-bold text-brand-600">AICode</span>
                </div>
{/*                 <nav className="flex items-center gap-4 text-sm font-medium text-slate-600">
                  <a href="/dashboard" className="hover:text-brand-600">ダッシュボード</a>
                  <a href="/ask-coach" className="hover:text-brand-600">Ask Coach</a>
                  <a href="/setup" className="hover:text-brand-600">Setup</a>
                  <a href="/publish" className="hover:text-brand-600">Publish</a>
                </nav> */}
              </div>
            </header>
            <main className="mx-auto flex w-full max-w-6xl flex-1 min-h-0 flex-col px-6 py-6">{children}</main>
            <footer className="shrink-0 border-t border-slate-200 bg-white">
              <div className="mx-auto flex w-full max-w-6xl items-center justify-between px-6 py-4 text-xs text-slate-500">
                <span>© {new Date().getFullYear()} AICode</span>
                <span>Made for guided web dev onboarding</span>
              </div>
            </footer>
          </div>
        </Providers>
      </body>
    </html>
  );
}
