"use client";

import { useEffect, useMemo, useState } from "react";
import type { LessonDefinition, TestCase } from "@/lib/content";

export interface TestRunnerProps {
  lesson: LessonDefinition;
  markup: string;
  onAllPassed: () => void;
}

interface TestResult {
  case: TestCase;
  passed: boolean;
  message: string;
}

function evaluateDomTest(doc: Document, testCase: Extract<TestCase, { type: "dom" }>): TestResult {
  const element = doc.querySelector(testCase.selector);
  if (!element) {
    return {
      case: testCase,
      passed: !testCase.exists,
      message: `${testCase.selector} が見つかりません`
    };
  }
  if (testCase.exists === false) {
    return {
      case: testCase,
      passed: false,
      message: `${testCase.selector} は存在しない必要があります`
    };
  }
  if (testCase.text && element.textContent?.trim() !== testCase.text) {
    return {
      case: testCase,
      passed: false,
      message: `${testCase.selector} のテキストは "${testCase.text}" が必要です`
    };
  }
  return {
    case: testCase,
    passed: true,
    message: "OK"
  };
}

function runTests(markup: string, tests: TestCase[]): TestResult[] {
  if (tests.length === 0) {
    return [];
  }
  const parser = new DOMParser();
  const doc = parser.parseFromString(markup, "text/html");
  return tests.map((testCase) => {
    if (testCase.type === "dom") {
      return evaluateDomTest(doc, testCase);
    }
    return {
      case: testCase,
      passed: false,
      message: "未対応のテストタイプです"
    };
  });
}

export function TestRunner({ lesson, markup, onAllPassed }: TestRunnerProps) {
  const [results, setResults] = useState<TestResult[]>([]);

  const testResults = useMemo(() => runTests(markup, lesson.task.tests), [lesson.task.tests, markup]);

  useEffect(() => {
    setResults(testResults);
  }, [testResults]);

  useEffect(() => {
    if (lesson.task.tests.length === 0) {
      return;
    }
    const allPassed =
      results.length > 0 && results.every((result: TestResult) => result.passed);
    if (allPassed) {
      onAllPassed();
    }
  }, [lesson.task.tests.length, onAllPassed, results]);

  if (lesson.task.tests.length === 0) {
    return (
      <div className="rounded-lg border border-emerald-200 bg-emerald-50 p-4 text-sm text-emerald-700">
        このレッスンでは手動チェックのみが必要です。
      </div>
    );
  }

  return (
    <div className="space-y-3">
      <div className="flex items-center justify-between">
        <span className="text-sm font-semibold text-slate-700">自動チェック</span>
        <span className="text-xs text-slate-500">
          {results.filter((result: TestResult) => result.passed).length} / {results.length} パス
        </span>
      </div>
      <ul className="space-y-2">
  {results.map((result: TestResult, index: number) => (
          <li
            key={index}
            className={`rounded-md border p-3 text-sm ${result.passed ? "border-emerald-200 bg-emerald-50 text-emerald-700" : "border-rose-200 bg-rose-50 text-rose-700"}`}
          >
            <div className="font-medium">{result.case.type === "dom" ? `${result.case.selector} を確認` : "未対応テスト"}</div>
            <div>{result.message}</div>
          </li>
        ))}
      </ul>
    </div>
  );
}
