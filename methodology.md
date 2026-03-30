# The Jarvis OpenClaw Methodology

> ["Jarvis"](https://www.youtube.com/watch?v=WNu6fRo_7fg) is the name [Ron](http://ripper234.com/) gave to his OpenClaw instance.

*Write the spec, not the code. Let the AI figure out the rest.*

Ron runs an AI agent (Jarvis) as a junior co-founder, not a tool. The methodology: write specs instead of code, protect human attention with a credit system, enforce safety through architecture rather than prompts, and keep the philosophy top-down — spec first, build later. The motto: **"think deeply, output lightly."**

---

## The Agent as Co-Founder

Ron treats his AI agent (Jarvis) like a **junior co-founder**, not a tool. Instead of prompting it with tasks, he writes specifications: what the product should do, how it should behave, what matters and what doesn't. The agent reads these specs and proposes tiny improvements as GitHub pull requests, **1-2 lines at a time**. But PRs are just one output. Jarvis also monitors social media and GitHub activity nightly, evaluates new tools and frameworks, manages research bookmarks, and **surfaces only what matters** each morning.

## Attention as Currency

The workflow protects Ron's scarcest resource: **attention**. An attention credit system (10 free + 20 earnable daily) hard-caps how much the agent can demand. **Capture mode costs zero credits** — Ron fires off ideas via voice without engaging, and the agent files everything for overnight processing. Only the final summary costs credits. Safety rails are **enforced by code**, not by asking the AI to remember rules. The agent has no direct write access to anything, only PRs that Ron approves.

## Safety by Architecture

Most users hand their AI agent root access and full data permissions on day one. Ron does the opposite: **information is need-to-know**, and access is earned incrementally. The agent has **no direct write access** to anything — not repos, not messaging, not external APIs. Every mutation goes through a code-level guard that validates, logs, and can be audited. Rules live in enforced scripts, not in prompts the AI might forget. Trust is earned through structure: the agent proposes, the human approves.

## Operations

**Backups** run at two levels: Railway's built-in backup system on the Pro tier, plus a bidirectional sync to a private GitHub repo. The workspace is the source of truth — if the container dies, everything rebuilds from git.

**Debugging** is deliberately low-tech. When something breaks, Ron copy-pastes state into ChatGPT, asks Jarvis to export logs, searches for how to extract the right diagnostics, and iterates. No custom observability stack — just persistence and multiple AI assistants cross-checking each other. When a bug turns out to be upstream, he opens an issue rather than working around it silently.

## Spec is the Product

The philosophy is top-down: **spec first**, then tests, then architecture, then code. Most of the code doesn't exist yet, and that's intentional. The spec IS the product at this stage. The agent's job is to sharpen the spec until building becomes obvious. Ron calls it **"think deeply, output lightly."**

## References

1. [Jarvis OpenClaw setup guide](https://docs.google.com/document/d/1axF5rnUsIPvD1L-SWltx9iwVpnetcCLs3gBx6C6qvJI/edit?tab=t.0)
2. [OpenSpec](https://openspec.dev/) — a lightweight spec-driven framework for AI coding agents
