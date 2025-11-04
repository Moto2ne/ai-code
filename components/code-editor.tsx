"use client";

import Editor from "@monaco-editor/react";

export interface CodeEditorProps {
  value: string;
  language?: string;
  onChange: (value: string) => void;
}

export function CodeEditor({ value, language = "javascript", onChange }: CodeEditorProps) {
  return (
    <div className="h-full overflow-hidden rounded-lg border border-slate-200">
      <Editor
        height="100%"
        defaultLanguage={language}
        value={value}
        onChange={(nextValue: string | undefined) => onChange(nextValue ?? "")}
        theme="vs-dark"
        options={{
          fontSize: 14,
          minimap: { enabled: false },
          scrollBeyondLastLine: false,
          automaticLayout: true
        }}
      />
    </div>
  );
}
