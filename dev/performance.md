# Performance Best Practices

## Core Web Vitals Targets
- **LCP** (Largest Contentful Paint): < 2.5s
- **CLS** (Cumulative Layout Shift): < 0.1
- **INP** (Interaction to Next Paint): < 200ms

## Images
- Use WebP/AVIF over PNG/JPG (we use WebP for hero)
- Set explicit `width` and `height` attributes to prevent CLS
- Use `loading="lazy"` for below-fold images, `loading="eager"` for hero
- Compress: aim for < 200KB per image on mobile
- Our hero.webp is 1.36MB — **should be compressed** (target: ~200-300KB)
- Consider `srcset` for responsive image sizes

## CSS
- Inline critical CSS or keep stylesheet small (ours is ~5KB, fine)
- Avoid `@import` chains — we use one Google Fonts import (acceptable)
- Minimize reflows: don't animate `width`, `height`, `top`, `left`, `margin`, `padding`
- **Only animate**: `transform`, `opacity` (GPU-composited, no reflow/repaint)
- Use `will-change: transform` sparingly (on animated elements only)

## Fonts
- We load Inter + JetBrains Mono via Google Fonts
- Use `font-display: swap` (Google Fonts does this by default)
- Consider self-hosting fonts if latency becomes an issue

## CSS Animations — Performance Rules
1. **Only animate `transform` and `opacity`** — everything else triggers layout/paint
2. **Use `will-change`** on elements you'll animate (but remove when done)
3. **Prefer `translate3d(0,0,0)`** over `translate()` to promote to GPU layer
4. **Limit animated elements** — each creates a compositor layer (memory cost)
5. **Use `prefers-reduced-motion`** media query to disable for accessibility
6. **No animation on page-blocking elements** — hero image should load first, animate after

## Static Site Specifics (GitHub Pages)
- GitHub Pages CDN caches aggressively (2-3 min propagation)
- No server-side optimization available — all client-side
- Minimize HTTP requests (inline small CSS, avoid unnecessary JS)
- We use zero JavaScript — keep it that way unless essential
- `defer` / `async` any future JS

## Testing
- **PageSpeed Insights**: https://pagespeed.web.dev/
- **Lighthouse** in Chrome DevTools (Ctrl+Shift+I → Lighthouse tab)
- Test on real mobile (Ron browses on phone)
- Test on slow 3G in DevTools Network throttling

## Current Status
- Zero JS ✅
- Single CSS file (~5KB) ✅
- Google Fonts (1 request) ✅
- Hero image needs compression ⚠️ (1.36MB → target 200KB)
- No explicit image dimensions ⚠️ (CLS risk)
- No `prefers-reduced-motion` handling ⚠️
