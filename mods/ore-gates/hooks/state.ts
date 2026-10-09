/** Pure state projection. Never executes commands or writes workspace state. */
export interface Specialist {
  specialist: string;
  department: string;
  domain_lead: string;
  revision: number;
}
export interface Task {
  id: string;
  title: string;
  objective: string;
  status: 'active' | 'blocked' | 'complete';
  revision: number;
  progress: number;
  deliverables: { name: string; weight: number; completion: number; status: string }[];
  gates: Record<string, { required: boolean; status: string }>;
  blockers: string[];
  next_action?: string;
  active_specialist?: Specialist;
  events?: { kind: string; specialist?: string; revision?: number }[];
}
const object = (v: unknown): v is Record<string, unknown> => !!v && typeof v === 'object' && !Array.isArray(v);
export function pointer(raw: string): string | null {
  try {
    const p: unknown = JSON.parse(raw);
    return object(p) && p.schema_version === 1 && typeof p.task_id === 'string' && /^[a-z0-9][a-z0-9-]{0,95}$/.test(p.task_id) ? p.task_id : null;
  } catch { return null; }
}
export function parseTask(raw: string, id: string): Task | null {
  try {
    const t: unknown = JSON.parse(raw);
    if (!object(t) || t.schema_version !== 1 || t.id !== id || !['active','blocked','complete'].includes(String(t.status)) ||
        typeof t.title !== 'string' || typeof t.objective !== 'string' || !Number.isInteger(t.revision) || Number(t.revision) < 1 ||
        !Array.isArray(t.deliverables) || !t.deliverables.length || !object(t.gates) || !Array.isArray(t.blockers) || !t.blockers.every(b => typeof b === 'string')) return null;
    if (!t.deliverables.every(d => object(d) && typeof d.name === 'string' && typeof d.status === 'string' &&
        Number.isInteger(d.weight) && Number(d.weight) > 0 && Number.isInteger(d.completion) && Number(d.completion) >= 0 && Number(d.completion) <= 100)) return null;
    if (t.deliverables.reduce((sum, d) => sum + Number(d.weight), 0) !== 100) return null;
    if (!Object.values(t.gates).every(g => object(g) && typeof g.required === 'boolean' && ['pending','passed','failed','blocked','not_applicable'].includes(String(g.status)))) return null;
    const result = t as unknown as Task;
    // Python round uses ties to even. Use the same summation order as ore_state.py.
    const rawProgress = result.deliverables.reduce((s, d) => s + d.weight * d.completion / 100, 0);
    const floor = Math.floor(rawProgress);
    result.progress = rawProgress - floor === 0.5 ? floor + floor % 2 : Math.round(rawProgress);
    const a = t.active_specialist;
    if (!object(a) || typeof a.specialist !== 'string' || !/^ore-[a-z0-9-]+$/.test(a.specialist) ||
        typeof a.department !== 'string' || typeof a.domain_lead !== 'string' || !Number.isInteger(a.revision) || Number(a.revision) > result.revision || Number(a.revision) < 1) delete result.active_specialist;
    if (!Array.isArray(t.events)) result.events = [];
    else result.events = t.events.filter(object).filter(e => typeof e.kind === 'string') as Task['events'];
    return result;
  } catch { return null; }
}
export function nextDeliverable(t: Task): string {
  return t.deliverables.find(d => d.status === 'in_progress' && d.completion < 100)?.name ??
    t.deliverables.find(d => d.completion < 100)?.name ?? 'None remaining';
}
export function pendingGates(t: Task): string[] {
  return Object.entries(t.gates).filter(([,g]) => g.required && !['passed','not_applicable'].includes(g.status)).map(([n,g]) => `${n}: ${g.status}`);
}
export function handoff(t: Task): string {
  return `${t.title} | ${t.progress}% | Objective: ${t.objective} | Next deliverable: ${nextDeliverable(t)} | Next action: ${t.next_action ?? 'Not recorded'} | Blockers: ${t.blockers.join('; ') || 'None'}`;
}
export function department(t: Task): string {
  const a = t.active_specialist;
  if (!a) return 'ORE lead';
  const history = (t.events ?? []).filter(e => e.kind === 'specialist_changed' && typeof e.specialist === 'string').slice(-5).map(e => `$${e.specialist}`);
  return `${a.department} → $${a.specialist}\nORE lead → ${a.domain_lead} → $${a.specialist}\nRecent: ${history.join(' → ') || `$${a.specialist}`}`;
}
export function revisionChanged(before: Task | null, after: Task | null): boolean {
  return !!before && !!after && (before.id !== after.id || before.revision !== after.revision);
}
