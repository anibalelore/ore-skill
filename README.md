# ORE — Orchestrated Runtime Engineering

> One request. The right engineering workflow. Evidence before completion.

[![Version](https://img.shields.io/badge/version-1.4.0-6f42c1)](./CHANGELOG.md)
[![Agent Skill](https://img.shields.io/badge/Agent%20Skill-compatible-0a7ea4)](./SKILL.md)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-compatible-D97757)](https://code.claude.com/docs/en/skills)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue)](./LICENSE)

ORE is an installable Agent Skill that turns a coding agent into an adaptive software-engineering agency. It scopes the request, selects only the specialists the work needs, keeps context focused, applies risk-based quality gates, and repeats only failed or invalidated work.

Use ORE when you want more than code generation: you want repository-aware execution, disciplined verification, and a defensible definition of done.

## Why ORE?

- **One-command execution** — describe the outcome once; ORE builds the workflow.
- **Adaptive specialist routing** — architecture, frontend, backend, QA, security, release, forms, and other roles are selected only when relevant.
- **Repository-first decisions** — ORE inspects existing architecture and conventions before changing them.
- **Focused context** — specialists receive only the context they need.
- **Targeted repair loops** — failed gates are repaired without restarting the entire pipeline.
- **Quality gates** — testing, build, security, data integrity, accessibility, release confidence, and other checks scale with risk.
- **Project memory** — compact `.ore/` artifacts can preserve verified architecture, progress, workflows, and lessons.
- **Flexible execution** — real subagents when supported; structured single-agent orchestration everywhere else.

## Install

ORE includes a canonical root `SKILL.md`, a portable plugin manifest, an OpenAI compatibility manifest, and a packaged skill under `skills/ore/`.

### Codex CLI or Codex coding agent

macOS or Linux:

```bash
mkdir -p ~/.codex/skills
git clone https://github.com/anibalelore/ore-skill.git ~/.codex/skills/ore
```

Windows PowerShell:

```powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE\.codex\skills" | Out-Null
git clone https://github.com/anibalelore/ore-skill.git "$env:USERPROFILE\.codex\skills\ore"
```

Start a new Codex session, then invoke the skill with `$ore` or a request beginning with `ORE:`.

### Claude Code

macOS or Linux:

```bash
mkdir -p ~/.claude/skills
git clone https://github.com/anibalelore/ore-skill.git ~/.claude/skills/ore
```

Windows PowerShell:

```powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE\.claude\skills" | Out-Null
git clone https://github.com/anibalelore/ore-skill.git "$env:USERPROFILE\.claude\skills\ore"
```

Start a new Claude Code session, then invoke `/ore` or describe a matching engineering task. Claude Code supports personal skills at `~/.claude/skills/<skill-name>/SKILL.md` and can load them automatically when relevant.

### ChatGPT and Codex Desktop

ORE is packaged as a skills-only plugin and includes a Git-backed marketplace catalog.

1. Add the marketplace from a terminal with Codex installed:

   ```bash
   codex plugin marketplace add anibalelore/ore-skill
   ```

2. Restart the ChatGPT desktop app.
3. Open the **Plugins Directory**.
4. Select the **ORE Skills** marketplace and install **ORE**.
5. Start a new conversation with the plugin enabled.

Local plugin availability can depend on the ChatGPT/Codex client, account, workspace policy, and developer settings. Public discovery in the universal Plugins Directory requires a separate OpenAI submission and review; publishing the GitHub repository alone does not create a public directory listing.

### Other Agent Skills hosts

Download or clone the complete repository into the directory where the host discovers Agent Skills. The host must support a folder containing `SKILL.md`; plugin-aware hosts may instead use `plugin.json` and `skills/ore/SKILL.md`.

Consult the host's documentation for its exact install directory, reload behavior, permissions, and invocation syntax. ORE does not claim compatibility with a host that does not support Agent Skills or equivalent instruction bundles.

> Review third-party skills before installation. Skills instruct an agent and operate within the tools, permissions, and approval boundaries provided by the host.

## Quick start

```text
$ore Add Stripe subscriptions with monthly and annual plans, a customer portal,
webhook reconciliation, persistence, regression tests, and deployment checks.
```

```text
/ore Diagnose the checkout regression. Reproduce it first, preserve the current
architecture, add regression coverage, and report validation evidence.
```

```text
ORE: Review this release for security, data migration risk, test coverage, and
rollback readiness.
```

Invocation varies by host: Codex recognizes `$ore`; Claude Code exposes `/ore`; `ORE:` is a portable textual convention.

## How it works

```text
Request
  → scope and risk classification
  → relevant specialists + minimum sufficient context
  → implementation or analysis
  → risk-based quality gates
  → targeted repair loop when needed
  → evidence-based completion report
```

Small tasks stay small. Complex or high-risk work receives deeper review and stronger validation.

## Good use cases

- Build a feature across frontend, backend, database, and integrations.
- Diagnose and repair a difficult regression.
- Review a pull request or release candidate.
- Plan and execute a migration with rollback protection.
- Improve security, accessibility, performance, or reliability.
- Design role-aware forms and connected business workflows.
- Investigate a production incident and prevent recurrence.
- Bootstrap a new application without skipping engineering foundations.

## Core capabilities

ORE v1.4 covers:

- product planning and specification fidelity;
- architecture and domain-flow coherence;
- frontend, backend, API, database, and integrations;
- testing, synthetic-user validation, and proactive bug discovery;
- security, compliance, resilience, accessibility, and localization;
- DevOps, deployment, release evidence, and rollback readiness;
- form intelligence and controlled reference data;
- learning from verified failures and user corrections;
- progress tracking and defensible token-efficiency reporting.

See the [changelog](./CHANGELOG.md) for release details.

## Update

Codex on macOS or Linux:

```bash
git -C ~/.codex/skills/ore pull --ff-only
```

Claude Code on macOS or Linux:

```bash
git -C ~/.claude/skills/ore pull --ff-only
```

Windows PowerShell:

```powershell
git -C "$env:USERPROFILE\.codex\skills\ore" pull --ff-only
# Or, for Claude Code:
git -C "$env:USERPROFILE\.claude\skills\ore" pull --ff-only
```

For the ChatGPT/Codex plugin route, refresh or upgrade the `ore-skills` marketplace, reinstall/update ORE when prompted, and start a new conversation.

## Uninstall

Remove the installed `ore` directory from the host's skills folder, then start a new session. In ChatGPT/Codex Desktop, uninstall ORE from the Plugins Directory.

Removing the installed skill does not remove `.ore/` project-memory folders that may exist inside software projects.

## Repository contents

| Path | Purpose |
| --- | --- |
| [`SKILL.md`](./SKILL.md) | Canonical entry point for direct skill installation |
| [`skills/ore/SKILL.md`](./skills/ore/SKILL.md) | Self-contained ORE workflow packaged for plugin hosts |
| [`plugin.json`](./plugin.json) | Portable Agent Plugin manifest |
| [`.codex-plugin/plugin.json`](./.codex-plugin/plugin.json) | OpenAI compatibility manifest |
| [`.agents/plugins/marketplace.json`](./.agents/plugins/marketplace.json) | Git-backed marketplace catalog |
| [`CHANGELOG.md`](./CHANGELOG.md) | Release history |

## Contributing

Issues and pull requests are welcome. Particularly useful contributions include realistic workflow evaluations, reproducible failures, stack-specific guidance, routing improvements, and documentation fixes.

When reporting a problem, include the host, request, expected behavior, observed behavior, and enough non-sensitive evidence to reproduce it.

## License

Licensed under the [Apache License 2.0](./LICENSE).

---

**ORE brings agency-style engineering discipline to the coding agent you already use.**
