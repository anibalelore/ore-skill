/** Pure presentation contracts. Never grants native permissions or mutates input. */
export type Approval = {
  action: string; reason: string; platform: string; project: string; environment: string;
  resources: string[]; risk: 'Bajo' | 'Medio' | 'Alto' | 'Crítico'; impact: string;
  reversal: string; permissions: string; checks: string[]; exact: string;
  critical: string; blocked: string | null;
};
export const APPROVE = 'Aprobar una vez';
export const REJECT = 'Rechazar';
export const DETAILS = 'Revisar detalles';
export const MAX_PRESENTATION = 12000;

export function prose(value: string): string {
  // Only prose: command/SQL/input bytes are never normalized.
  return value.replace(/\\r\\n|\\n/g, '\n').replace(/\r\n/g, '\n');
}
function block(value: string, language = ''): string {
  const runs = value.match(/`+/g) ?? [];
  const fence = '`'.repeat(Math.max(3, ...runs.map(r => r.length + 1)));
  return `${fence}${language}\n${value}\n${fence}`;
}
function label(value: string): string {
  // Metadata cannot insert terminal escapes or spoof another summary field.
  return JSON.stringify(value).slice(1, -1).replace(/[\u202a-\u202e\u2066-\u2069]/g, c => `\\u${c.charCodeAt(0).toString(16)}`);
}
function strings(value: unknown): string[] {
  if (typeof value === 'string') return [value];
  if (Array.isArray(value)) return value.flatMap(strings);
  return value && typeof value === 'object' ? Object.values(value).flatMap(strings) : [];
}
function sensitive(value: unknown): boolean {
  if (Array.isArray(value)) return value.some(sensitive);
  if (value && typeof value === 'object') return Object.entries(value).some(([key, v]) =>
    /^(?:password|secret|token|api[_-]?key|authorization|access_token)$/i.test(key) && v != null || sensitive(v));
  return typeof value === 'string' && /(?:\b(?:password|secret|token|api[_-]?key|authorization)\s*[:=]\s*\S+|Bearer\s+\S+|postgres(?:ql)?:\/\/[^\s/]+:[^\s@]+@)/i.test(value);
}

export function summarize(tool: string, input: unknown, project: string, reason?: string): Approval {
  const exact = JSON.stringify(input, null, 2);
  if (typeof exact !== 'string') throw new Error('No exact action');
  const data = input && typeof input === 'object' ? input as Record<string, unknown> : {};
  // Descriptions, reasons and instructions do not determine risk or destination.
  const executable: Record<string, unknown> = {};
  for (const [key, value] of Object.entries(data)) if (!['description', 'reason', 'instructions', 'evidence', 'owner'].includes(key)) executable[key] = value;
  const text = strings(executable).join('\n');
  const sql = typeof data.sql === 'string' ? data.sql : typeof data.query === 'string' ? data.query : '';
  const command = typeof data.command === 'string' ? data.command : '';
  const target = [data.environment, data.target, data.project_id, data.project_ref, data.context, data.cluster].filter(v => typeof v === 'string').join(' ');
  const production = /\bprod(?:uction)?\b|--prod\b/i.test(`${target} ${command} ${sql}`);
  const destructive = /\b(?:DROP\s+(?:TABLE|DATABASE|SCHEMA)|TRUNCATE|DELETE\s+FROM|terraform\s+destroy|rm\s+[^\n]*(?:-[a-z]*[rf]|--recursive|--force)|Remove-Item|rmdir\s+\/s|del\s+\/[sq]|git\s+reset\s+--hard|git\s+push[^\n]*(?:--force|-f\b|\s\+\S+)|kubectl\s+delete)\b/i.test(text);
  const permissionChange = /\b(?:GRANT|REVOKE|chmod|chown|create-access-key|delete-access-key)\b|\b(?:disable|bypass)[\s\S]{0,80}\b(?:rls|security|permissions)\b|\bDISABLE\s+ROW\s+LEVEL\s+SECURITY\b/i.test(text);
  const schema = /\b(?:CREATE|ALTER)\s+(?:TABLE|INDEX|SCHEMA)|\b(?:migrate|migration)\b/i.test(text);
  const cloud = /\b(?:deploy|publish|terraform|kubectl|supabase|aws|gcloud|az|vercel|helm)\b/i.test(`${tool} ${command}`);
  const git = /\bgit\s+(?:push|merge|commit|rebase|tag)\b/i.test(command);
  const metadata = ['model-policy', 'model-decision', 'approval', 'revoke-approval', 'scope', 'rule', 'exception', 'revoke-rule'].includes(String(data.action));
  const fileEdit = /^(?:Write|Edit)$/i.test(tool);
  const knownReadOnly = /^(?:Read|Grep|Glob)$/i.test(tool) || /^(?:git\s+(?:status|diff|log)|pwd|Get-Location)(?:\s+[^;&|\n]*)?$/i.test(command.trim());
  const resources = [data.file_path, data.path, data.table, data.project_id, data.project_ref].filter((v): v is string => typeof v === 'string' && !!v);
  const table = /\b(?:CREATE|ALTER|DROP)\s+TABLE\s+(?:IF\s+(?:NOT\s+)?EXISTS\s+)?((?:"[^"]+"|[a-z_][\w]*)(?:\.(?:"[^"]+"|[a-z_][\w]*))?)/i.exec(sql || command);
  if (table) resources.push(table[1]!);
  if (metadata) resources.push('.ore/governance.json');
  const environment = production ? 'Producción (declarada; verificar destino)' : metadata || fileEdit ? 'Proyecto local' : target ? `${target} (declarado; sin verificar)` : 'Detectar y verificar; destino no identificado';
  const risk = destructive ? 'Crítico' : production || permissionChange || cloud || (!metadata && !fileEdit && (!target || !knownReadOnly && !schema && !git)) ? 'Alto' : schema || fileEdit || git || metadata ? 'Medio' : 'Bajo';
  const action = destructive ? 'Ejecutar una operación destructiva' : permissionChange ? 'Modificar permisos o controles de acceso' : table && /^\s*CREATE\s+TABLE/i.test(sql || command) ? /(?:^|[."])activity_log"?$/i.test(table[1]!) ? 'Crear tabla de auditoría' : 'Crear tabla de datos' : schema ? 'Modificar la estructura de datos' : metadata ? 'Guardar la decisión o política de ORE' : fileEdit ? 'Modificar archivos del proyecto' : git ? 'Actualizar el repositorio Git' : cloud ? 'Ejecutar una operación de publicación o infraestructura' : 'Ejecutar la acción indicada';
  const checks = schema || sql ? ['Verificar RLS, privilegios, autoría, integridad y protección frente a modificaciones; no se han probado estos controles.'] : [];
  if (!resources.length) checks.push('Recursos no identificados: revisar la operación exacta y verificar el alcance.');
  if (metadata) checks.push('La política o aprobación registra metadatos; no concede permisos nativos ni ejecuta cambios de modelo.');
  if (data.permissions_sufficient === false) checks.push('Permisos insuficientes: corregir el acceso antes de continuar.');
  let blocked: string | null = exact.length > MAX_PRESENTATION ? 'La operación supera el límite de presentación completa. Divídela y vuelve a solicitar aprobación; no se ha truncado ni ejecutado.' : sensitive(input) ? 'La operación contiene posibles credenciales. Revisa el contenido exacto en el control seguro del host y utiliza referencias a secretos; ORE no la mostrará ni aprobará con contenido oculto.' : data.permissions_sufficient === false ? 'Permisos insuficientes; el resumen no puede otorgarlos.' : null;
  if (/[\u0000-\u0008\u000b\u000c\u000e-\u001f\u007f\u001b\u202a-\u202e\u2066-\u2069]/.test(text)) blocked = 'Caracteres de control impiden presentar fielmente la acción; revisa el contenido en el host.';
  const result: Approval = { action, reason: prose(reason ?? 'La acción requiere revisar su alcance antes de continuar.'), platform: /supabase/i.test(tool + ' ' + command) ? 'Supabase' : label(tool),
    project: label(project), environment: label(environment), resources: [...new Set(resources)].map(label), risk,
    impact: destructive ? 'Posible pérdida de datos, archivos o historial.' : permissionChange ? 'Cambian quién puede acceder o modificar recursos.' : schema ? 'Nueva estructura de datos o cambio de esquema.' : 'Afecta únicamente el alcance declarado; los efectos indirectos no están verificados.',
    reversal: destructive ? 'No garantizada; verificar copias y recuperación antes de aprobar.' : metadata || fileEdit ? 'Requiere un cambio explícito o restauración; no se revierte automáticamente.' : 'No verificada; revisar rollback y efectos externos.',
    permissions: metadata ? 'Consentimiento para guardar metadatos del proyecto; restricciones nativas intactas.' : 'Permisos de la herramienta y del destino; el host sigue siendo la autoridad.',
    checks, exact: blocked ? '' : exact,
    critical: blocked ? '' : command ? block(command, 'text') : sql ? block(sql, 'sql') : '', blocked };
  if (!result.blocked && renderApproval(result, true).length > MAX_PRESENTATION) {
    result.blocked = 'Los detalles completos superan el límite de presentación. Divide la operación; no se ha truncado ni ejecutado.';
    result.exact = ''; result.critical = '';
  }
  return result;
}

export function renderApproval(value: Approval, details = false): string {
  if (value.blocked) return `ORE · Solicitud bloqueada\n${value.blocked}\n¿Rechazar esta solicitud?`;
  const summary = `ORE · Solicitud de permiso\nAcción: ${value.action}\nMotivo: ${value.reason}\nPlataforma: ${value.platform}\nProyecto: ${value.project}\nEntorno: ${value.environment}\n\nImpacto: ${value.impact}\nRecursos: ${value.resources.join(', ') || 'No identificados'}\nRiesgo: ${value.risk}\nReversión: ${value.reversal}\nPermisos: ${value.permissions}\n${value.checks.join('\n')}\nEstado: Pendiente de aprobación`;
  const full = details || value.risk === 'Alto' || value.risk === 'Crítico';
  return `${summary}${full ? `\n\nDetalles técnicos completos (sin modificar):\n${value.critical}\n${block(value.exact, 'json')}` : '\nDetalles técnicos completos disponibles en «Revisar detalles».'}\n\n¿Aprobar únicamente esta operación?`;
}
