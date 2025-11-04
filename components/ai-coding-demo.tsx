"use client";

import { useState } from "react";
import { Loader2, Sparkles, Code2 } from "lucide-react";

interface AICodingDemoProps {
  prompt: string;
  initialCode: string;
  targetCode: string;
  explanation: string;
}

export function AICodingDemo({ prompt, initialCode, targetCode, explanation }: AICodingDemoProps) {
  const [isGenerating, setIsGenerating] = useState(false);
  const [currentCode, setCurrentCode] = useState(initialCode);
  const [aiOutput, setAiOutput] = useState("");
  const [showExplanation, setShowExplanation] = useState(false);

  const simulateAIGeneration = async () => {
    setIsGenerating(true);
    setAiOutput("");
    setShowExplanation(false);
    
    // AIの思考過程をシミュレート
    const thinkingSteps = [
      "プロンプトを分析しています...",
      "コードの構造を検討中...",
      "最適な実装方法を選択しています...",
      "コードを生成中..."
    ];

    for (const step of thinkingSteps) {
      setAiOutput(step);
      await new Promise(resolve => setTimeout(resolve, 800));
    }

    // コードを段階的に書き換え
    const lines = targetCode.split('\n');
    let buildingCode = '';
    
    for (let i = 0; i < lines.length; i++) {
      buildingCode += lines[i] + '\n';
      setCurrentCode(buildingCode);
      setAiOutput(`コード生成中... (${i + 1}/${lines.length} 行)`);
      await new Promise(resolve => setTimeout(resolve, 300));
    }

    setAiOutput("✓ コード生成完了!");
    await new Promise(resolve => setTimeout(resolve, 500));
    setShowExplanation(true);
    setIsGenerating(false);
  };

  const resetDemo = () => {
    setCurrentCode(initialCode);
    setAiOutput("");
    setShowExplanation(false);
  };

  return (
    <div className="space-y-4">
      {/* プロンプト表示 */}
      <div className="rounded-lg border border-purple-200 bg-purple-50 p-4">
        <div className="flex items-center gap-2 text-sm font-semibold text-purple-900">
          <Sparkles className="h-4 w-4" />
          AIへのプロンプト
        </div>
        <p className="mt-2 text-sm text-purple-800">{prompt}</p>
      </div>

      {/* AI出力状態 */}
      {aiOutput && (
        <div className="rounded-lg border border-blue-200 bg-blue-50 p-4">
          <div className="flex items-center gap-2">
            {isGenerating && <Loader2 className="h-4 w-4 animate-spin text-blue-600" />}
            <span className="text-sm font-medium text-blue-900">{aiOutput}</span>
          </div>
        </div>
      )}

      {/* コードエディタ */}
      <div className="rounded-lg border border-slate-300 bg-slate-900">
        <div className="flex items-center justify-between border-b border-slate-700 px-4 py-2">
          <div className="flex items-center gap-2 text-xs text-slate-400">
            <Code2 className="h-3 w-3" />
            <span>index.tsx</span>
          </div>
          <div className="flex gap-2">
            <button
              onClick={simulateAIGeneration}
              disabled={isGenerating}
              className="rounded bg-brand-600 px-3 py-1 text-xs font-semibold text-white hover:bg-brand-700 disabled:opacity-50"
            >
              {isGenerating ? "生成中..." : "AIで生成"}
            </button>
            <button
              onClick={resetDemo}
              className="rounded bg-slate-700 px-3 py-1 text-xs font-semibold text-slate-300 hover:bg-slate-600"
            >
              リセット
            </button>
          </div>
        </div>
        <pre className="overflow-x-auto p-4 text-sm">
          <code className="text-slate-100">{currentCode}</code>
        </pre>
      </div>

      {/* 解説表示 */}
      {showExplanation && (
        <div className="rounded-lg border border-emerald-200 bg-emerald-50 p-4">
          <div className="text-sm font-semibold text-emerald-900">💡 解説</div>
          <p className="mt-2 text-sm text-emerald-800">{explanation}</p>
        </div>
      )}
    </div>
  );
}