---
name: hermes-feishu-streaming-migration-kit
description: Transfer the optimized Hermes Feishu streaming-card workflow to another Hermes repo, with bundled files, upgrade locators, recovery notes, and verification commands.
version: 2.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [hermes, feishu, gateway, streaming, migration, transfer, patch, skill]
    related_skills: [hermes-agent, hermes-feishu-gateway-setup, hermes-gateway-streaming-debugging, systematic-debugging]
---

# Hermes Feishu Streaming Migration Kit

Use this bundle when you need to restore or transfer the **Feishu-specific gateway UX** after a Hermes upgrade or on a new machine.

## Preserved behavior

- Feishu single-card streaming output
- tool progress embedded into the active card
- metadata-only / status-only edits
- Feishu session notices and context-pressure cards
- generic file attachments with caption sent as `text -> native file`

## Suggested workflow

1. Run the locator against the target Hermes repo.
2. Inspect `references/modified-files.md` and `references/upgrade-locator.md`.
3. Apply the bundled files.
4. Run the verification commands from `references/verification.md`.
5. If this is a real environment restore, also follow `docs/feishu-restore-runbook.md` in the standalone repo.

## Acceptance checklist

- Feishu tool execution uses one live card instead of noisy split messages
- tool status clears correctly on completion
- final answer edits back into the same Feishu stream path
- session/context notices render as Feishu cards
- focused pytest suite passes
