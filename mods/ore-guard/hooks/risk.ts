/** Configurable pattern matching, not a shell interpreter or remote dry run. */
const DEFAULTS = [
  ['Mass deletion', String.raw`\b(?:rm\s+(?:-[a-zA-Z]*[rf][a-zA-Z]*|--recursive|--force)|Remove-Item\b[\s\S]*-Recurse|rmdir\s+/s|del\s+/[sq])`],
  ['Destructive database operation', String.raw`\b(?:DROP\s+(?:TABLE|DATABASE|SCHEMA|INDEX)|TRUNCATE\b|(?:prisma|alembic|knex|sequelize)\b[\s\S]*(?:reset|drop|downgrade|rollback)|migrate\b[\s\S]*(?:reset|drop|destructive))`],
  ['Force push', String.raw`\bgit\b[\s\S]*\bpush\b[\s\S]*(?:--force\b|--force-with-lease\b|(?:\s|\")-f(?:\s|\"|$)|\s\+\S+)`],
  ['Production deployment', String.raw`\b(?:deploy|deployment|release|vercel|terraform\s+(?:apply|destroy)|kubectl\s+(?:apply|delete)|helm\s+(?:upgrade|uninstall))\b[\s\S]*(?:\bprod(?:uction)?\b|--prod\b)|\b(?:terraform\s+destroy|deploy_production)\b`],
  ['Credential rotation', String.raw`\b(?:rotate|rotation|revoke|regenerate|reset|create-access-key|delete-access-key)\b[\s\S]*(?:credential|secret|token|key|password)|\b(?:credential|secret|token|key|password)\b[\s\S]*\b(?:rotate|rotation|revoke|regenerate)\b`],
  ['Package publication', String.raw`\b(?:npm|pnpm|yarn|bun|cargo|poetry|twine|dotnet|gem)\s+(?:publish|push|upload)\b|\b(?:publish_package|package_publish)\b`],
];
export function classify(tool: string, input: unknown, configured: unknown): string | null {
  let patterns = DEFAULTS;
  if (typeof configured === 'string' && configured.trim()) {
    try {
      const value: unknown = JSON.parse(configured);
      if (!Array.isArray(value) || value.length > 50 || !value.every(v => typeof v === 'string' && v.length <= 500)) return 'Invalid guard pattern configuration';
      patterns = value.map(v => ['Configured high-impact operation', v]);
    } catch { return 'Invalid guard pattern configuration'; }
  }
  // Bound input and patterns. Regular expressions remain trusted plugin options.
  const serialized = JSON.stringify(input);
  if (serialized.length > 65536) return 'Action arguments exceed the guard review limit';
  // Preserve actual whitespace inside argument strings, including shell newlines.
  const text = `${tool} ${serialized} ${argumentStrings(input).join(' ')}`;
  try {
    for (const [label, expression] of patterns) {
      if (expression && new RegExp(expression, 'i').test(text)) return label ?? 'High-impact operation';
    }
  } catch { return 'Invalid guard pattern configuration'; }
  return null;
}
function argumentStrings(input: unknown): string[] {
  if (typeof input === 'string') return [input];
  if (Array.isArray(input)) return input.flatMap(argumentStrings);
  if (input && typeof input === 'object') return Object.values(input).flatMap(argumentStrings);
  return [];
}
export function preview(input: unknown): string {
  // Never persist action arguments. Mask common inline secret representations.
  return JSON.stringify(input).replace(/((?:password|secret|token|api[_-]?key)\s*[=:]\s*)[^\s,;"}]+/gi, '$1[redacted]')
    .replace(/("(?:password|secret|token|api[_-]?key)"\s*:\s*")[^"]*/gi, '$1[redacted]')
    .slice(0, 2000);
}
