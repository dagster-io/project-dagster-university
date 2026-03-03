# Course Pages: Conventions

## Frontmatter

Every lesson file requires these fields:

```yaml
---
title: "Lesson X: Page Title"
module: 'module_slug'
lesson: 'X'
---
```

Module slugs:
- `dagster-essentials` → `dagster_essentials`
- `dagster-dbt` → `dbt_dagster`
- `dagster-etl` → `dagster_etl`
- `dagster-testing` → `dagster_testing`
- `ai-driven-data-engineering` → `ai_driven_data_engineering`

`lesson` must be a string (e.g., `'3'`, not `3`).

## File Naming

`{number}-{kebab-case-title}.md`, e.g., `3-asset-materialization.md`

Numbers start at 0 (overview). Numbers establish navigation order within a lesson directory.

## Writing Style

- Concise, direct prose — no filler
- Short paragraphs
- `##` for section headers, `###` for subsections
- No emojis, no em dashes
- Active voice

## Markdoc Syntax

- Triple-backtick code blocks with language tag
- Prefer CommonMark tables; Markdoc `{% table %}` available for complex tables

## Pages

The first sub lesson in lesson-1 should be `0-about-this-course.md`

Examples:
- course/pages/dagster-etl/lesson-1/0-about-this-course.md
- course/pages/dagster-testing/lesson-1/0-about-this-course.md

In all other lessons, the first sub lesson should be `0-overview.md`

Examples:
- course/pages/dagster-essentials/lesson-3/0-overview.md

## Images

The images are contained within `course/public/images` which is organized by courses and lesson numbers. All images should be:

```
![Image description](/images/{course name}/{lesson number}/{image name}.png)
```

## Validation

Run `yarn linkcheck` from `course/` to verify internal and external links before finalizing.

## Index files

When a new lesson is added or a lesson number is updated, update the corresponding index `.md` file.

Examples
- course/pages/dagster-essentials.md
- course/pages/dagster-etl.md