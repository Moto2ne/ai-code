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
  body { font-family: 'Segoe UI', sans-serif; margin: 0; padding: 24px; background: #f8fafc; color: #0f172a; }
  header, footer { background: #ffffff; border-radius: 12px; padding: 16px; margin-bottom: 12px; box-shadow: 0 1px 3px rgba(15, 23, 42, 0.1); }
  main { background: #ffffff; border-radius: 12px; padding: 16px; box-shadow: 0 1px 3px rgba(15, 23, 42, 0.08); }
  nav a { margin-right: 12px; color: #0ea5e9; text-decoration: none; font-weight: 600; }
</style>
</head>
<body>
${markup}
</body>
</html>`;
}
