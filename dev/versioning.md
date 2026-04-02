# Versioning Policy

## Scheme: Semantic Versioning (SemVer)

Format: `MAJOR.MINOR.PATCH` (e.g., v0.3.0)

### What each number means

- **MAJOR (X)**: Breaking changes, complete redesigns, major pivots. Still 0 while in early development.
- **MINOR (Y)**: New features, pages, or significant visual changes. Bumped when pushing staging to prod.
- **PATCH (Z)**: Bug fixes, copy tweaks, small styling adjustments.

### Rules

1. **Production version** = the latest git tag on `main` (e.g., `v0.3.0`)
2. **Staging version** = next planned minor above prod (e.g., if prod is `v0.3.0`, staging is `v0.4.0-dev`)
3. **On promote to prod**: tag the commit, bump staging to next minor
4. **Patch releases**: increment Z directly on main, no staging cycle needed for small fixes
5. **Footer tag**: always show the version in the site footer (e.g., `v0.3.0`)

### Why SemVer over X.Y?

- Industry standard, instantly understood
- PATCH level allows small fixes without implying a feature release
- Tooling and git tags work naturally with it
- Pre-release suffixes (`-dev`, `-rc.1`) are built into the spec

### Workflow

```
staging (v0.4.0-dev) --> promote --> main (v0.4.0) --> tag v0.4.0
                                     staging bumps to v0.5.0-dev
```

### Current state

- Production: `v0.3.0`
- Staging: `v0.3.0` (just promoted, next staging work will be `v0.4.0-dev`)
