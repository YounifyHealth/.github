# Natalyx MVP Fixes planning package

> Drive-first review package. No implementation, PR closure, branch cleanup, schema change, deployment, payment activation, real-user use or PHI processing is authorized until Luke and Alan jointly approve the plan.

## Review delivery

- [MVP Fixes folder](https://drive.google.com/drive/folders/1fWFyWPcFMEm15BbHXngBH4NzqAaIf2yR)
- [Consolidated plan overview PDF](https://drive.google.com/file/d/1It9TNlHX63A6xmdLXtN9_Nzv30Ey-8qY/view?usp=drivesdk)
- [Markdown work packages](https://drive.google.com/drive/folders/1eKIbuD0lWabm55ZbH3pAv1x-0_Wd3aH3)
- [PDF work packages](https://drive.google.com/drive/folders/1FtZIYVD0y7OmhO7WJmJpJS-ulxesxtU1)

The Drive package contains exactly fourteen Markdown plans, fourteen matching PDF plans, and one consolidated overview PDF. Alan has inherited writer access through the existing MVP folder permissions.

## Review state

The GitHub Project is closed and benched pending this review. Its 106 planning items are retained for possible later reactivation, but all local filesystem plan paths and draft-body references have been removed. `scripts/sync_project.py --apply` is intentionally blocked while `PROJECT_BENCHED` is true.

The current evidence baseline remains:

- The inspected dev endpoint returned ALB 503; Gate A0 is not passed.
- The exact running ECS revision was not independently verified because local AWS SSO was expired.
- PR 122 contains useful invitation/case-shell hardening but is not the final architecture.
- PR 124 should not merge unchanged because it creates paid-case-shaped state too early and weakens access/authorship boundaries.

## Proposed ownership split

This is a review proposal, not a compulsory assignment:

| Lead | Work packages | Reciprocal review |
| --- | --- | --- |
| Luke | WP00, WP05, WP07, WP08, WP11, WP12 | Alan reviews technical architecture, migration, security and failure behavior. |
| Alan | WP01, WP02, WP03, WP04, WP06, WP09, WP10, WP13 | Luke reviews product, privacy, commercial, role, truth and release acceptance. |

External payment, finance, legal, security, privacy, accessibility or provider review remains required where a package names it.

## Local package layout

```text
output/drive/MVP Fixes/
├── MD Work Packages/          # 14 clean Markdown review plans
├── PDF Work Packages/         # 14 matching LuaLaTeX PDFs
└── Natalyx MVP Fixes - Consolidated Plan Overview.pdf
```

The PDFs deliberately follow the earlier AWS migration-plan convention: a restrained highlighted title, serif body, bold sans-serif hierarchy, numbered sections, compact ruled tables and centered page numbers. Dense transition tables are emitted as readable Markdown records instead of unreadable nine-column portrait tables.

## Regeneration and validation

Generate the clean Markdown and overview source:

```bash
python scripts/build_drive_package.py
```

Render all PDFs with Quarto's bundled Pandoc and LuaLaTeX:

```bash
./scripts/render_drive_package.sh
```

Validate counts, names, links, local-path removal, PDF metadata, page size and extracted text:

```bash
python scripts/validate_drive_package.py
```

Bench/clean Project 3 again if a future accidental active sync reintroduces local paths:

```bash
python scripts/bench_project.py
```

Do not reactivate the GitHub Project until Alan's amendments are incorporated and Luke and Alan explicitly accept the Drive plan.
