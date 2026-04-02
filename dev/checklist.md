# Pre-Ship Checklist

Run through this before every push to staging or production.

## Required (every change)

### Performance
- [ ] No animations on layout properties (width, height, top, left, margin, padding)
- [ ] Animations use only `transform` and `opacity`
- [ ] `prefers-reduced-motion` respected for all animations
- [ ] No new JS added (or justified if so)
- [ ] Images compressed (< 200KB for hero, < 100KB for thumbnails)
- [ ] Images have explicit width/height or aspect-ratio (CLS prevention)
- [ ] No blocking resources added

### Visual
- [ ] Tested on mobile viewport (375px wide)
- [ ] Tested on desktop (1440px wide)
- [ ] All content above fold on desktop is actually above fold
- [ ] No horizontal scroll on any viewport
- [ ] Consistent with existing style (colors, fonts, spacing)
- [ ] Dark text on light background readable (contrast ratio >= 4.5:1)

### Links & Content
- [ ] No 404s — all links resolve (use "Coming soon" placeholders)
- [ ] External links open correctly
- [ ] Internal navigation works (back links, home links)
- [ ] No placeholder text left in

### Staging/Prod
- [ ] Change is on staging first
- [ ] Version number updated if promoting to prod
- [ ] Old URLs redirect if renamed

## Recommended (major changes)

- [ ] Run Lighthouse audit (Chrome DevTools)
- [ ] Test on slow 3G (Chrome Network throttling)
- [ ] Check LCP < 2.5s, CLS < 0.1
- [ ] Review on actual phone (not just responsive mode)
- [ ] Screenshot before/after for comparison
