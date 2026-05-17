# OpenClaw Playground

*A public, free, rate-limited OpenClaw instance with no credit card required.*

## What it is

OpenClaw Playground is a lightweight way for people to experience real agents before asking them to self-host, pay, or even create an account.

The goal is simple: let someone try a real agent on a real task in minutes, with almost no setup friction.

## Why this matters

Most people have used chatbots. Far fewer have actually delegated a real task to an agentic system.

A public playground lowers the barrier dramatically:
- no install
- no credit card
- no infra
- no docs-first experience

If the first experience is good, some users will later:
- self-host OpenClaw
- join the community
- pay for hosted usage
- bring their own keys

## Recommended MVP

The best first version is **anonymous guest mode with hard limits**.

Core shape:
- no signup required for first use
- strict per-browser / per-IP / per-day rate limits
- disposable sandbox per task or session
- small default model budget
- restricted tool set
- queue when load is high

Example limits:
- 1 to 3 tasks per anonymous user per day
- 2 to 5 minute max runtime per task
- low output token cap
- one active task at a time per user
- global concurrency cap

## Product shape

### Tier 1: guest playground
- no card
- no account, or optional lightweight email later
- public URL
- canned starter prompts + blank prompt box
- temporary transcript link
- safe tools only

### Tier 2: free account
- more daily tasks
- saved history
- maybe file uploads
- maybe lightweight integrations

### Tier 3: paid / BYOK / hosted
- longer tasks
- private agents
- more tools
- persistent memory
- team or personal workspaces

## Tool policy

Allowed at first:
- web search
- web fetch
- maybe browser in a sandbox
- scratch files in a disposable workspace
- maybe image / PDF reading with tight limits

Disallowed at first:
- shell access on a shared host
- messaging / email / outbound communication
- GitHub writes
- cloud credentials
- long-lived memory
- private connectors

## Current recommendation

Build the guest playground first:
1. anonymous session
2. one active task at a time
3. 3 tasks/day/browser
4. 3 minute timeout
5. safe read-only tools only
6. disposable sandbox
7. cheap fast model by default
8. clear upgrade path to hosted or self-hosted OpenClaw

This keeps the concept legible and cheap while still delivering the core magic.
