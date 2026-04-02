# Animation Guidelines

## Principles
1. **Elements inside the image should move, not the image itself** — floating the whole image looks cheap
2. **Subtle > dramatic** — animations should feel alive, not distracting
3. **Performance first** — only `transform` and `opacity`, never layout properties
4. **Respect user preferences** — always include `prefers-reduced-motion: reduce`

## Recommended Techniques for Hero Image

### Floating particles/orbs overlay (preferred)
Small translucent circles positioned over the image with different drift paths.
- Use `position: absolute` divs inside a container
- Animate with `transform: translate()` on different durations (8-15s)
- Varying opacity (0.3-0.6) and sizes (4-12px)
- Colors from our palette: indigo (#4f46e5), cyan (#06b6d4), emerald (#10b981)
- 5-8 particles max (more = GPU cost)

### Glow pulse
Subtle box-shadow or radial-gradient overlay that breathes.
- `box-shadow` animation: expand/contract glow radius over 4-6s
- Or: pseudo-element with radial gradient, animate opacity
- Keep it barely noticeable — the eye should sense it, not track it

### Light shimmer/sweep
Diagonal light band crossing the image.
- Use `::after` pseudo-element with linear-gradient
- `transform: translateX()` from -100% to 100%
- Duration: 3-4s, delay: 6-10s between sweeps
- Very low opacity (0.1-0.15)

### What NOT to do
- ❌ Float/bob the entire image (looks like a loading animation)
- ❌ Rotate the image
- ❌ Scale pulse the image (feels like a heartbeat monitor)
- ❌ Animate `filter` properties (expensive, triggers repaint)
- ❌ Use more than ~8 animated elements (GPU memory)

## Accessibility
```css
@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
    }
}
```

## Implementation Template
```css
.hero-container {
    position: relative;
    overflow: hidden;
}
.hero-img {
    display: block;
    width: 100%;
}
.particle {
    position: absolute;
    border-radius: 50%;
    opacity: 0;
    will-change: transform, opacity;
    animation: particleDrift var(--duration) ease-in-out infinite;
    animation-delay: var(--delay);
}
@keyframes particleDrift {
    0%, 100% { opacity: 0; transform: translate(0, 0); }
    25% { opacity: var(--max-opacity); }
    50% { opacity: var(--max-opacity); transform: translate(var(--dx), var(--dy)); }
    75% { opacity: var(--max-opacity); }
}
```
