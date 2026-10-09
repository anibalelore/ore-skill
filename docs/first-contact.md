# First Contact: evidence before claims

`skills/ore/scripts/ore_first_contact.py` implements a bounded Playwright
adapter and a read-only scenario/evidence interface. It never writes `.ore/`.
The host imports a redacted result through the sole ORE state writer.

## Reproducible local demonstration

```sh
python -m pip install -r requirements.txt
python -m playwright install chromium
python skills/ore/scripts/ore_first_contact.py demo
# Optional screenshots from the explicitly synthetic demo:
python skills/ore/scripts/ore_first_contact.py demo --artifact-directory /tmp/ore-replays
```

The demo starts a temporary loopback-only HTTP server, opens the synthetic fixture,
discovers the visible Support button, and independently checks its visible result.
It shuts down the server afterward. Playwright and its matching Chromium binaries
are required ORE dependencies for browser execution and full validation. The Python
version is pinned in `skills/ore/requirements.txt` and bundled with runtime adapters.
For a standalone skill install, run `python -m pip install -r requirements.txt`
from the installed `ore` skill directory, then `python -m playwright install chromium`.
For a standalone mod, use its bundled `requirements.txt` with the same Python interpreter
configured for that mod. Without either dependency the adapter
reports blocked; it does not fabricate interactions or successful outcomes.
The browser acceptance test fails instead of skipping when dependencies are missing.

## Scenario contract

```json
{
  "url": "http://127.0.0.1:8080",
  "goal": "Find support and open the help page",
  "environment": "isolated_test",
  "isolated_environment_confirmed": true,
  "synthetic_accounts_confirmed": true,
  "authorized": true,
  "profile": "new",
  "max_actions": 12,
  "timeout_seconds": 30,
  "retention_hours": 24
}
```

```sh
python skills/ore/scripts/ore_first_contact.py validate scenario.json
python skills/ore/scripts/ore_first_contact.py prepare scenario.json
python skills/ore/scripts/ore_first_contact.py run scenario.json --success-visible "Support available"
python skills/ore/scripts/ore_first_contact.py summary evidence.json
```

`--success-visible` is an evaluator criterion. It never reaches the exploration
policy. The explorer receives the end-user goal, visible roles/names, and optional
synthetic field values keyed by visible labels. Source, selectors, internal routes,
answer keys, and step lists are rejected. Imported observations are labeled external
assertions and must not be presented as independently executed local tests.

## Profiles and limits

Profiles set budgets, viewport, and interaction delay. They are simulation parameters,
not claims about demographic groups. `limited_connectivity` adds delay; it does not
claim to simulate packet loss. `accessibility` uses accessible roles but does not
constitute a full accessibility audit. `unauthorized` is an exploration preset,
not proof of comprehensive authorization coverage.

The explorer is deterministic and limited: lexical relevance of visible actions,
unvisited actions, bounded recovery after an interaction failure, and visible goal
verification. It is not a model of human behavior or a replacement for human tests.
Without an independent visible criterion, results remain unverified. Retests run
the original scenario afresh and must be compared by the caller; no prior action
history or implementation answer is fed to the next exploration.

## Security and evidence

Only loopback HTTP(S) is accepted. Explicit isolation, synthetic accounts, and
authorization confirmations are required. All off-origin browser traffic is blocked,
including redirects; service workers are disabled. Only GET/HEAD traffic is allowed;
mutation requests and WebSockets are blocked, and popups are closed. This means
server-backed form writes are deliberately unsupported; synthetic client-side forms
can be explored. Playwright must support WebSocket routing. Visible actions for purchases,
payments, messages, deployment, publishing, deletion, and transfers are excluded.
These heuristics are not a sandbox or a guarantee about application-side effects:
the confirmations are operator trust assertions, not independently proven isolation.
The target **must** be an actually isolated synthetic application, never a local
proxy to production. External/staging URLs and real credentials are not supported.

Results contain up to 30 redacted actions, failures, observations, labeled
interpretations, and elapsed time. Known secret keys, email addresses, credential
assignments, and long numeric identifiers are redacted. Do not use real private
data: automated redaction is not exhaustive. Video is not recorded; screenshots are
disabled by default. Optional `artifact_directory` must resolve outside `.ore/`;
`capture_screenshots: true` additionally requires explicit
`synthetic_screen_capture_confirmed: true`. All inputs, textareas and editable fields
are masked in viewport PNGs. This is not general pixel PII redaction: remaining page
content must be synthetic, and production screenshots are not supported.

When exports are enabled, the adapter writes a redacted action JSON manifest and
bounded screenshot files with actual action references. Each export has a unique
`ore-first-contact-<random-id>` prefix and an expiry of at most 24 hours. Before the
next export, expired manifests and only their matching owned PNGs are removed;
unrelated files, symlinks and corrupt manifests are preserved. No recursive deletion
is used. Run cleanup independently when no further session is scheduled:

```sh
python skills/ore/scripts/ore_first_contact.py cleanup /tmp/ore-replays
```

There is no resident cleanup process: callers must schedule cleanup to enforce
expiry when idle, secure access to the directory, and manage any copies themselves.
Without `artifact_directory`, evidence is returned on stdout and not persisted.

Interfaces: `validate_scenario(data) -> list[str]`,
`prepare_session(scenario) -> dict`, `summarize_session(evidence) -> dict`, and
`run_session(scenario, success_visible=None) -> dict`.
