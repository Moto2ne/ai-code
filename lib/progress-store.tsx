"use client";

import { createContext, useContext, useMemo, useState, type ReactNode } from "react";
import type { LessonDefinition, UserProfile } from "./content";

export interface ProgressState {
  profile: UserProfile;
  updateProfile: (updater: (prev: UserProfile) => UserProfile) => void;
  markLessonComplete: (lesson: LessonDefinition) => void;
}

const ProgressContext = createContext<ProgressState | undefined>(undefined);

interface ProgressProviderProps {
  initialProfile: UserProfile;
  children: ReactNode;
}

export function ProgressProvider({ initialProfile, children }: ProgressProviderProps) {
  const [profile, setProfile] = useState(initialProfile);

  const value = useMemo<ProgressState>(
    () => ({
      profile,
      updateProfile: (updater: (prev: UserProfile) => UserProfile) =>
        setProfile((prev: UserProfile) => updater(prev)),
      markLessonComplete: (lesson: LessonDefinition) =>
        setProfile((prev: UserProfile) => {
          if (prev.completedLessons.includes(lesson.id)) {
            return prev;
          }
          const nextXp = prev.xp + 50;
          const badges = new Set(prev.badges);
          if (nextXp >= 500) {
            badges.add("連続学習チャレンジャー");
          }
          return {
            ...prev,
            xp: nextXp,
            badges: Array.from(badges),
            completedLessons: [...prev.completedLessons, lesson.id],
            currentLessonId: lesson.summary.nextLessonId ?? prev.currentLessonId
          };
        })
    }),
    [profile]
  );

  return <ProgressContext.Provider value={value}>{children}</ProgressContext.Provider>;
}

export function useProgress() {
  const ctx = useContext(ProgressContext);
  if (!ctx) {
    throw new Error("useProgress must be used within ProgressProvider");
  }
  return ctx;
}
