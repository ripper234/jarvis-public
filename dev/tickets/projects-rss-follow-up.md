# Ticket: Projects RSS follow-up

Status: deferred, not now

## Summary

Adding RSS for the projects page is not a zero-effort tweak. It needs follow-up work across pathing, canonical deploy flow, and feed auto-update behavior.

## Issues discovered

1. `jarvis.ripper234.com/feed.xml` is already used by the **ron.build** feed.
   - The projects feed therefore needs its own path, for example `projects-feed.xml`.

2. The current deploy reality is split.
   - There is a Vercel mirror flow.
   - The canonical URLs are under `jarvis.ripper234.com` and `jarvis.ripper234.com/staging`.
   - The canonical domain is not currently being updated by the same path we used for the mirror deploys.

3. Canonical publish is blocked from this runtime.
   - The bot could not create an upstream GitHub issue because `GH_TOKEN` is missing in the current runtime.
   - Direct upstream git push is also blocked by permissions.

4. Auto-update requires more than a static file.
   - We need feed generation on deploy.
   - We need persisted state for detecting meaningful changes over time.
   - The relevant change types are:
     - new project added
     - project maturity/status changed

5. RSS should remain invisible in the UI.
   - Keep it discoverable only via HTML feed metadata.
   - No visible “Follow via RSS” CTA for now.

## What was already done in local / mirror work

- Added a generator script for a projects RSS feed
- Switched the intended path to `projects-feed.xml`
- Kept RSS discoverable only via HTML `<link rel="alternate">`
- Parked Telegram / email / WhatsApp follow options as later work

## Deferred work

- Make `https://jarvis.ripper234.com/projects-feed.xml` live on the canonical domain
- Align canonical hosting/deploy so the feed actually ships there
- Keep feed generation automatic on deploy
- Preserve event/change tracking for new and maturing projects
- Revisit other follow options later:
  - Telegram
  - email
  - WhatsApp

## Recommendation

Treat this as infrastructure + content workflow work, not a quick UI tweak.
