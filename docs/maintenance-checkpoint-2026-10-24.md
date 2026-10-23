# Web maintenance checkpoint — 2026-10-24

Web v1 remains feature-frozen. This checkpoint records local integration of existing
geometry and draft-recovery work; it is not a publication or release approval.

## Verified inputs

- Public main: `ca4cd630a4bf8928c53368b8d5ee404f5e2bfa0b`.
- Main includes the unittest discovery fix `9d8fbd41fbd78aefeb805886eb69c7d3c268b50a`
  and the standard-library Web contract CI workflow. Do not recreate that fix.
- Existing local candidate: `53dbec91ea9e79cd4a0fb47c2de413250a07d74c`, including
  Letter export, canonical millimetre conversion, explicit legacy geometry choice,
  Qt A4 compatibility, and local draft recovery including title/author elements.
- Local integration: `baae6b87b38a6367f24fb3f705511a1f4dbfe080`.

## Integration completed

Merged public main into the existing candidate in an isolated checkout. The sole
conflict was `tests/test_web_conforming_roundtrip.py`: preserve main's discoverable
`unittest.TestCase` while retaining the candidate's Letter page-contract assertion
and x/y/width/height roundtrip checks. Main's README posture and CI were retained.

The runtime trees (`web_prototype`, `export_core`, `src`) are byte-for-byte unchanged
from candidate `53dbec9`; no new product feature was implemented.

## Validation

`python3 -m unittest discover -s tests -p 'test_web_*.py' -v`

Result: **54 tests passed**, including both conforming roundtrip cases through the
normal discovery entry point, page geometry/Qt A4 compatibility, legacy conversion,
and draft source-contract guards. `git diff --check --cached` passed before commit.

The public-main CI run [37035052594](https://github.com/SamZebrado/guiLaTeX/actions/runs/37035052594)
was separately verified successful. It covers public main, not this local integration.
Historical candidate Chromium evidence remains historical; this session did not run
Chromium, native Qt GUI tests, or publish/deploy the result. Runtime byte identity
is why those previously completed browser tests were not repeated for this merge.

## Resume

Use branch `codex/continue-existing-fixes-20261024`. The old STATUS/PLAN sections
remain archival context, not the active Web backlog. Inspect this integration and
its two parents before choosing additional work. The next bounded step is a review
of the integrated diff and existing exact-candidate browser evidence, followed by
an explicit publication decision if desired. Do not interpret this checkpoint as
permission to push, publish, run Bridge, or enable project automation.

Work was checkpointed before the requested Shanghai 01:00 stop. Further development
is paused pending continuation after the requested return to Sol High; this task
has not changed or verified the model setting.
