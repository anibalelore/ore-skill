# Host matrix — documentation checked 2026-10-09

| Host | Documented controls | Shipped execution / verification |
| --- | --- | --- |
| Claude Code | /model, --model, model setting; /effort; subagent model/effort | Experimental mod observes session model/usage and persists metadata; manual selection; local contract tests |
| Codex | config.toml model/model_reasoning_effort; custom agent TOML model/effort | Pure evaluator with supplied observations; no config writer or active-session switch; local contract tests |
| ChatGPT | Host model picker where available | Recommendation and manual selection only; no UI automation or verified conversation-switch API |
| Gemini, DeepSeek, local, compatible API | Extension seam only | Unsupported until real adapter tests; no fictional compatibility |

[Claude model configuration](https://code.claude.com/docs/en/model-config) documents
aliases, availableModels organizational restrictions, effort caps and environment
precedence. [Claude subagents](https://code.claude.com/docs/en/sub-agents) documents
model/effort fields, inheritance, invocation overrides and substitution observation
with /tasks. Aliases are not exact versions; do not infer API IDs or entitlements.
Relevant variables include ANTHROPIC_MODEL, ANTHROPIC_DEFAULT_OPUS_MODEL,
ANTHROPIC_DEFAULT_SONNET_MODEL, ANTHROPIC_DEFAULT_HAIKU_MODEL,
CLAUDE_CODE_SUBAGENT_MODEL and CLAUDE_CODE_EFFORT_LEVEL. Inspect only authorized
configuration keys, never secrets. Opus/Sonnet/Haiku versions require actual
account/host observation even when official documentation names them.

[Codex configuration](https://developers.openai.com/codex/config-reference) and
[subagents](https://developers.openai.com/codex/multi-agent) document model settings
and agent definitions. Model and reasoning compatibility must come from the installed
host interface and account; commercial aliases are not automatically API IDs.
GPT-6 family identifiers are accepted only with verified inventory entries.
File configuration for a future task is distinct from changing an active task.

The repository SDK types are Claude Code 2.1.295; mods require 2.1.287+.
Installed native version and live launch are checked in the acceptance report.
Offline type checking/mocks do not establish a live compatible adapter. No new
provider calls, account credentials or global setting writes are performed.
