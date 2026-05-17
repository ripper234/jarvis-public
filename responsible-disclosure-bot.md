# Responsible Disclosure Bot

*A privacy safety bot for people who accidentally self-doxx their Bitcoin ownership.*

## One sentence

This bot watches for public posts that leak wallet ownership, identifies the likely on-chain transaction behind the post, and sends a private warning to the author telling them to remove the identifying information.

## The problem

Bitcoin gives you pseudonymity, not automatic privacy.

People regularly post things like:
- screenshots of wallet balances
- transaction screenshots with timestamps and amounts
- "finally got to 1 BTC" style milestone posts
- partial addresses, explorer links, or withdrawal confirmations

They often do this casually, without realizing that the combination of amount + timing + screenshot details can strongly implicate them as the owner of a specific wallet.

Once that leak is public, the damage compounds:
- the wallet becomes targetable
- their identity may get tied to future activity
- old posts can remain searchable forever
- attackers now know this person may be worth phishing, sim-swapping, or extorting

## What the bot does

1. Monitors public Reddit posts in places like `r/Bitcoin`
2. Detects likely privacy leaks using text + image clues
3. Extracts amount, timestamp, wallet UI hints, and any partial address / tx hints
4. Searches the blockchain for the most likely matching transaction
5. Scores confidence
6. If confidence is high, sends a private Reddit DM to the author
7. Optionally posts a generic public comment with zero identifying details, to normalize better privacy practices and make the bot visible

## The DM

The bot sends a calm, non-judgmental message like:

> Hey, quick heads up: your post may expose enough information to link you to a specific wallet or transaction. You may want to edit or delete the post if privacy matters to you.

The message should be:
- private
- short
- practical
- non-threatening
- non-accusatory

## Optional public thread comment

After the private DM, the bot can optionally leave a generic public comment such as:

> Friendly privacy reminder: milestone posts, wallet screenshots, timestamps, and transaction details can expose more than people expect. If privacy matters to you, think twice before posting wallet evidence publicly.

Rules for the public comment:
- no mention of the specific leak details
- no claim that the author owns a specific wallet
- no transaction hash, amount, address, or timing details
- framed as a general safety reminder for everyone reading the thread
- used carefully, because overuse will feel spammy

## Important boundaries

This project should have strong limits.

### In scope
- helping people undo accidental self-disclosure
- warning the original poster privately
- optionally leaving a generic public safety reminder with zero identifying detail
- operating only on already-public self-posted data
- high-confidence matching only

### Out of scope
- public callouts
- naming or exposing wallet owners
- building a deanonymization database
- helping third parties track people
- low-confidence guessing

## Safety rules

- **Private first**: DM the author first; public comments must stay generic and reveal nothing new
- **High confidence threshold**: if the match is weak, do nothing
- **Minimal retention**: do not store leaked personal linkage data longer than needed
- **No enrichment creep**: do not combine with social graph, brokered personal data, or off-platform stalking
- **Rate limited**: avoid spammy or repetitive messages
- **Human-review mode** at the beginning is probably wise

## Why this is interesting

This is one of those rare tools that is simultaneously:
- deeply Bitcoin-native
- socially useful
- technically hard enough to matter
- ethically constrained in an interesting way

It sits at the intersection of:
- open-source intelligence
- blockchain analysis
- privacy UX
- agentic outreach
- responsible disclosure norms

## Hard parts

### 1. False positives
Many transactions can match an amount and rough time window. The bot needs to be conservative.

### 2. Screenshot parsing
Wallet screenshots vary by app, theme, language, and crop. Vision models help, but they will be noisy.

### 3. Reddit messaging limits
DM delivery, anti-spam protections, and API rules may constrain the workflow.

### 4. Ethics drift
Without careful limits, this can slowly turn from a safety tool into a surveillance product. The boundary has to stay sharp.

## Difficulty estimate

### Concept demo
**3-5 days, difficulty 4/10**

A fake or semi-manual demo is easy:
- monitor one subreddit
- detect obvious leak posts with simple heuristics
- show likely tx matches in a dashboard
- no automatic DMs

### Useful MVP
**2-4 weeks, difficulty 7/10**

A real MVP is meaningfully harder:
- Reddit ingestion
- leak scoring
- image OCR / vision extraction
- blockchain matching
- confidence scoring
- human review queue
- DM sending with rate limits

### Production-worthy system
**6-10 weeks, difficulty 8.5/10**

The hard part is not the API plumbing. The hard part is getting:
- low false positives
- safe behavior under ambiguity
- good auditability
- clean data minimization
- platform-safe outbound messaging behavior

## How I'd build it

### Phase 1: Human-reviewed text MVP
- Monitor `r/Bitcoin` only
- Score posts for likely privacy leaks using rules + LLM classification
- Extract amount / timing / explicit claims from text only
- Search for candidate transactions in a bounded time window
- Present candidates to a review UI
- Human clicks approve before any DM goes out

### Phase 2: Add screenshots
- OCR wallet screenshots
- Use a vision model to detect wallet app, amount, and transaction cues
- Merge image evidence with text evidence into a single confidence score

### Phase 3: Narrow automation
- Auto-send only for extremely high-confidence cases
- Keep a per-author cooldown
- Keep a full audit trail of why a message was sent

## Best architecture

Prefer a **scored pipeline with review queue**.

### Core components
1. **Reddit ingestor**
   - Pull new posts/comments from a narrow allowlist of subreddits
   - Store raw post metadata and media references

2. **Leak detector**
   - Fast heuristics first: amount language, milestone language, screenshot presence, explorer links, partial addresses
   - LLM/ML classifier second: “is this likely a self-doxx?”

3. **Evidence extractor**
   - Text extraction: amount, timing, self-ownership claims
   - Image extraction: OCR + wallet UI hints + tx details if visible

4. **Chain matcher**
   - Query mempool/explorer APIs first
   - Optional own Bitcoin node later for privacy and better matching control
   - Return a ranked set of candidate transactions with confidence

5. **Decision engine**
   - Combine signal scores into one conservative confidence score
   - Drop weak/ambiguous cases
   - Queue strong cases for review

6. **Review UI**
   - Show post, extracted clues, likely tx match, and proposed DM
   - Approve / reject / snooze

7. **DM sender**
   - Rate-limited
   - Private only
   - Per-user cooldowns
   - Templated but gentle language

8. **Audit + retention layer**
   - Log why a case was flagged and what was sent
   - Expire sensitive linkages quickly

### Suggested stack
- **Python** for ingestion / scoring / workers
- **Postgres** for cases, scores, and audit trail
- **Redis** or a simple job queue for asynchronous pipeline steps
- **Small web admin** for review queue
- **Explorer API first**, own Bitcoin node later if the project proves out
- **Vision/OCR as a subsystem**, not the whole brain

## MVP shape

A good MVP would be:
- Reddit posts only
- text-first, screenshots second
- Bitcoin only
- one subreddit first
- private warning only
- human review before sending

That keeps the blast radius small.

## My take

As Jarvis, I like the project.

It has real utility, a clear user benefit, and a memorable hook. The strongest version is a **privacy guardian** for people making an honest mistake.

The biggest risk is posture. If it feels creepy, overconfident, or exploitative, people will hate it instantly. If it feels like a quiet seatbelt for Bitcoiners, it could resonate.

## Working title ideas

- Responsible Disclosure Bot
- Wallet Leak Guardian
- Bitcoin Privacy Guardian
- Proof-of-Wealth Warning Bot
- Self-Doxx Rescue Bot
