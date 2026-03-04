# Course Runner

Run through a Dagster University course lesson-by-lesson, following the Markdoc instructions, writing code, executing CLI commands, and verifying results. This surfaces instruction clarity issues and confirms code examples work.

**Usage:** `/course-runner <course_name>`

---

## Course Catalog

Use this table to look up course metadata for `$ARGUMENTS`.

| Course | Project dir | Pages dir | Lessons | Verification |
|--------|-------------|-----------|---------|--------------|
| `dagster_essentials` | `dagster_university/dagster_essentials` | `course/pages/dagster-essentials` | 3–9 | completed_model |
| `dagster_and_dbt` | `dagster_university/dagster_and_dbt` | `course/pages/dagster-dbt` | 2–7 | completed_model |
| `dagster_and_etl` | `dagster_university/dagster_and_etl` | `course/pages/dagster-etl` | 3–7 | completed_model |
| `dagster_testing` | `dagster_university/dagster_testing` | `course/pages/dagster-testing` | 3–6 | defs_model |
| `ai_driven_data_engineering` | — | — | — | skip |

**Verification modes:**

- `completed_model` — student writes code in `defs/`; tests import from `completed/lesson_N/` to validate env health. Assets are in `defs/assets/` (a subdirectory), except `dagster_and_etl` which uses flat files directly in `defs/` (`assets.py`, `jobs.py`, etc.).
- `defs_model` — applies to `dagster_testing` only. Assets are pre-populated in `defs/`; student work is writing tests. Tests import from `defs/` directly, so per-lesson pytest validates the agent's test-writing.
- `skip` — not suitable for the instruction runner (e.g., course teaches AI prompting workflows).

If `verification` is `skip`, stop immediately and explain why.

**Environment variables** (set before running `uv` commands for applicable courses):
- `dagster_essentials`, `dagster_and_dbt`, `dagster_and_etl`: `DUCKDB_DATABASE=data/staging/data.duckdb`

---

## Phase 1: Setup

1. Clone a fresh copy of the repository:
   ```
   git clone git@github.com:dagster-io/project-dagster-university.git
   ```
   All subsequent work happens inside this clone. Keep the path to the clone's root handy — it is the `<repo_root>`.

2. `cd` into `<repo_root>/<project_dir>` and run `uv sync` to install dependencies.

3. Run `uv run dg check defs` to confirm the baseline loads. If it fails, stop and report — do not proceed with a broken baseline.

4. Create a result log file at the **original** working directory (where the skill was invoked) under `course/course_runner/results/<course>_<YYYY-MM-DD>.md` with this header:
   ```
   # Course Runner: <course> — <date>
   ```

---

## Phase 2: Per-Lesson Loop

For each lesson number N in the course's lesson range (from the catalog above), in order:

### Step 1 — Read lesson pages

List all `.md` files in `<repo_root>/<pages_dir>/lesson-N/`. Sort by numeric filename prefix (e.g., `0-overview.md` before `1-setup.md`). Read each file in order.

### Step 2 — Classify each page

- **SKIP** — pure prose overview, recap, or intro with no code to write or commands to run.
- **SKIP** — page's only code references the Dagster UI (mentions "Dagster UI", "click", screenshots, or `dg dev`).
- **ACTIONABLE** — page contains:
  - Bash blocks with CLI commands (`dg scaffold`, `dg check`, `uv add`, etc.)
  - Python code blocks preceded by phrases like "add the following", "replace with", "your code should look like this"
- **REFERENCE** — `coding-practice` or challenge page. Consult `<project_dir>/src/<pkg>/completed/lesson_N/defs/` for the expected solution.

### Step 3 — Execute actionable pages

- **Bash commands:** Prefix Python tool commands with `uv run` (e.g., `uv run dg scaffold defs dagster.asset assets/trips.py`). Run from within `<repo_root>/<project_dir>`.
- **Python code:** Identify the target file from:
  - A `# src/...` comment at the top of the code block, or
  - Surrounding prose ("open `trips.py`", "add to `definitions.py`")

  When a page shows a cumulative "your code should look like this" block, treat it as the full current file content (replace, don't append).

- **After every file write:** Run `uv run dg check defs`. Log any errors. If the check fails and you cannot fix it within two attempts, mark the page `BLOCKED` and continue to the next page — do not loop indefinitely.

### Step 4 — Post-lesson verification

1. Run `uv run dg check defs`. This must pass to mark the lesson PASS, unless the lesson content explicitly introduces a deliberate error as a teaching example.

2. Run `uv run pytest tests/test_lesson_N.py -p no:warnings`:
   - `completed_model` courses: tests run against `completed/lesson_N/`, confirming env health.
   - `defs_model` courses (`dagster_testing`): tests run against the agent's own written tests, validating that work directly.

3. Append to the result log:
   ```markdown
   ## Lesson N
   Status: PASS | FAIL | BLOCKED
   Pages: X processed (Y skipped)
   Files written: <list>
   dg check defs: PASS | FAIL — <error if any>
   pytest test_lesson_N.py: PASS | FAIL — <error if any>
   Notes: <anything unusual or ambiguous in the instructions>
   ```

---

## Phase 3: End-of-Course

1. Run `uv run pytest tests -p no:warnings` (full suite).
2. Run `uv run ruff check`.
3. Append to the result log:
   ```markdown
   ## Summary
   Lessons: X/Y PASS
   Full pytest: PASS | FAIL
   Ruff: PASS | FAIL
   Issues:
   - <list any pages with unclear instructions, broken examples, or unexpected diffs>
   ```
4. Delete the cloned repository created in Phase 1.

---

## Notes

- Always run commands from within `<repo_root>/<project_dir>`, not from the repo root.
- If a page's instructions are ambiguous (unclear which file to write to, conflicting code snippets), make a reasonable choice, proceed, and log the ambiguity in the result file.
- Do not modify anything under `completed/` — it is read-only reference material.
