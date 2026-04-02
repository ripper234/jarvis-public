# Long Pages: UX Best Practices

## What's Wrong With a Wall of Text
- **No orientation.** Reader can't see what's ahead or how long the journey is.
- **No escape.** Can't jump to the section they care about.
- **Uniform density.** Every section looks the same -- nothing signals "this is the important part."
- **Scroll fatigue.** After 3+ scrolls, engagement drops sharply on mobile.
- **No scanning.** Power users want to skim, not read linearly.

## Techniques (in order of preference for us)

### 1. Sticky Table of Contents (preferred)
- Anchor links at top, stays visible as you scroll
- Shows full structure at a glance
- Preserves Cmd+F
- Best for: reference docs, guides, long-form content

### 2. Progressive Disclosure
- Show summary, expand on demand (accordions, "Read more")
- Reduces initial cognitive load
- Best for: FAQ, settings, detailed specs

### 3. Chunked Sections with Visual Breaks
- Alternating background colors between sections
- Clear section headers with emoji/icons
- Generous whitespace between blocks
- Best for: landing pages, scrollable single-page sites

### 4. Tabbed Content
- Split page into tabs (e.g. "Overview | Setup | Advanced")
- Good for reducing scroll, bad for discoverability
- Best for: dashboards, product pages with distinct modes

### 5. Multi-Page Split
- Break one long page into multiple focused pages
- Each page is short and complete
- Best for: tutorials, step-by-step guides

## Our Defaults (lesson)
1. **Any page longer than ~4 screen-heights on mobile needs a TOC or split**
2. **Sticky TOC** is default for guides/reference
3. **Chunked sections** with visual variety for landing-style pages
4. **Progressive disclosure** for detail-heavy sections (code examples, config tables)
5. Never create a page that's just section after section of the same visual density
6. Always ask: "Can someone find what they need in 5 seconds?"

## Anti-Patterns
- ❌ Uniform h2 → paragraph → h2 → paragraph for 20 sections
- ❌ No TOC on a page that takes >3 scrolls
- ❌ Walls of bullet lists with no visual hierarchy
- ❌ Code blocks that dominate the page (hide behind expandable sections)
- ❌ "Read from top to bottom" as the only navigation
