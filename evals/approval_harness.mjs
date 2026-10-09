import { readFileSync } from 'node:fs';
import { summarize, renderApproval, prose } from '../mods/sdk/approval.ts';
const input = JSON.parse(readFileSync(0, 'utf8'));
const summary = summarize(input.tool ?? 'Bash', input.action, input.project ?? 'Test project', input.reason);
process.stdout.write(JSON.stringify({ summary, text: renderApproval(summary, input.details), prose: input.prose ? prose(input.prose) : null }));
