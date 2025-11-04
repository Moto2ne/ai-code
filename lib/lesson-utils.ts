export function extractMarkupFromSource(source: string): string {
  const cleaned = source.replace(/\{\/\*[^]*?\*\/\}/g, "");
  const match = cleaned.match(/return\s*\(([^]*?)\);?/);
  if (match && match[1]) {
    return match[1]
      .replace(/^\s*<Fragment>/, "")
      .replace(/<\/Fragment>\s*$/, "")
      .trim();
  }
  return cleaned.trim();
}

export function buildPreviewDocument(markup: string): string {
  return `<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Live Preview</title>
<style>
  body { font-family: 'Noto Sans JP', 'Segoe UI', sans-serif; margin: 0; padding: 24px; background: #ffffff; color: #1f2937; }
  h1, h2, h3 { margin: 0 0 12px; }
  p { margin: 0 0 12px; line-height: 1.6; }
  ul { margin: 0 0 12px; padding-left: 20px; }
  li { margin-bottom: 6px; }
</style>
</head>
<body>
${markup}
</body>
</html>`;
}
