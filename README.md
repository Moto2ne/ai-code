# AICode  Web App

AICode  is a Progate-inspired learning experience that combines slide-based explanation, live coding, instant preview, automated checks, and AI coaching prompts. This repository contains a Next.js + TypeScript prototype that follows the provided specification.

## Features

- Guided course flow with a single Next.js course sample
- Lesson shell replicating slide / editor / live preview / test layout
- Monaco editor integration with instant iframe preview
- DOM-based automated test runner for quick feedback
- AI hint panel offering actionable prompts and copy-ready question templates
- Dashboard with XP, streak, badges, and roadmap overview
- Setup checklist and Vercel publish guide pages

## Getting Started

```bash
npm install
npm run dev
```

The development server starts at `http://localhost:3000`.

## Project Structure

- `app/` – App Router pages for home, course, lesson, dashboard, ask-coach, setup, publish
- `components/` – Reusable UI elements including the LessonShell, Monaco wrapper, preview, tests, and hint panel
- `lib/content.ts` – Mock Firestore-like data models for courses, lessons, and user profile
- `lib/progress-store.tsx` – Client-side progress context that simulates XP gain and completion tracking

## Next Steps

- Connect to real Firestore collections via SDKs and server actions
- Expand lesson data and implement JSON-driven course loading
- Replace iframe preview with Sandpack or Next.js local runtime for accurate rendering
- Integrate authentication, billing, and AI API calls according to the roadmap
