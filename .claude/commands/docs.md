---
description: Generate or update project documentation in Russian and English.
  Creates a comprehensive set of markdown files covering deployment, usage,
  architecture, and user flows.
  $ARGUMENTS: optional flags — "rus" (Russian only), "eng" (English only), "update" (refresh existing)
---

# /docs $ARGUMENTS

## Purpose

Generate professional, bilingual project documentation from source code,
existing docs, and development insights. Output: `README/rus/` and `README/eng/`.

## Step 1: Gather Context

Read all available sources to build comprehensive understanding:

### Primary sources (project documentation):
```
docs/PRD.md (or docs/*.md)          — product requirements, features
docs/Architecture.md                 — system architecture, tech stack
docs/Specification.md                — API, data model, user stories
docs/Completion.md                   — deployment, environment setup
docs/features/                       — feature-specific documentation
docs/plans/                          — implementation plans
CLAUDE.md                            — project overview, commands, agents
DEVELOPMENT_GUIDE.md                 — development workflow
INSTALL.md                           — installation instructions
docker-compose.yml                   — infrastructure services
.env.example                         — environment variables
```

### Secondary sources (knowledge base):
```
myinsights/1nsights.md               — development insights index
myinsights/details/                   — detailed insight files
.claude/feature-roadmap.json          — feature list and statuses
```

### Tertiary sources (code analysis):
```
Source code structure                 — actual implementation
requirements.txt / pyproject.toml    — dependencies
README.md (existing, if any)         — current documentation
```

## Step 2: Determine Scope

```
IF $ARGUMENTS contains "rus":  languages = ["rus"]
ELIF $ARGUMENTS contains "eng": languages = ["eng"]
ELSE: languages = ["rus", "eng"]

IF $ARGUMENTS contains "update":
    mode = "update"  — read existing README/ files, update only changed sections
ELSE:
    mode = "create"  — generate from scratch
```

## Step 3: Generate Documentation Set

For EACH language in languages, generate these files:

### File 1: `deployment.md`
- System requirements (OS, runtime, Docker)
- Quick start (clone → configure → run)
- Production deployment with TLS
- Database initialization and migrations
- Update and rollback procedures

### File 2: `admin-guide.md`
- User management and roles
- System configuration
- Monitoring and logging
- Backup and restore
- Troubleshooting

### File 3: `user-guide.md`
- Getting started
- Feature-by-feature walkthrough
- Common usage scenarios
- FAQ

### File 4: `infrastructure.md`
- Minimum and recommended hardware
- Network requirements and ports
- External service dependencies
- License requirements

### File 5: `architecture.md`
- High-level system diagram (Mermaid)
- Technology stack with rationale
- Component descriptions
- Data model overview
- Security and scalability approach

### File 6: `ui-guide.md`
- Interface structure and navigation
- Key screens description
- UI patterns and controls

### File 7: `user-flows.md`
- User registration and first login
- Primary user journeys
- Admin setup and management flows
- Monitoring workflows

## Step 4: Generate Output

1. Create directory structure:
```bash
mkdir -p README/rus README/eng
```

2. Generate files for each language:
   - Russian files go to `README/rus/`
   - English files go to `README/eng/`
   - Use proper language throughout (not machine-translated fragments)

3. Generate `README/index.md` — table of contents linking both languages

## Step 5: Commit and Report

```bash
git add README/
git commit -m "docs: generate project documentation (RU/EN)"
git push origin HEAD
```

Report generated files with per-language breakdown.

## Update Mode

When `$ARGUMENTS` contains "update":
1. Read existing files in `README/rus/` and `README/eng/`
2. Compare with current project state
3. Update only sections that have changed
4. Preserve any manual additions (sections not in template)
5. Commit: `git commit -m "docs: update project documentation"`

## Notes

- Documentation is generated from ACTUAL project state, not assumptions
- Mermaid diagrams are used for architecture and flow visualizations
- If UI doesn't exist yet, ui-guide.md notes this and describes planned UI
- If some information is unavailable, the section notes what's missing
- myinsights/ is checked for gotchas and important notes to include
