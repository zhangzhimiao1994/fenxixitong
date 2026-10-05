---
name: zhengliu
description: Use when an agent needs to distill either a person or a book/long-form source into an auditable, executable skill. Require an explicit choice between person distillation and book/content distillation before research; produce grounded SKILL.md outputs, source records, boundaries, links, and test prompts instead of a simple summary or unsupported role-play.
---

# Zhengliu

Turn evidence into reusable reasoning tools. Preserve the source's useful decision logic while making every output executable, attributable, and bounded.

## First: choose the distillation type

Before researching, writing files, or proposing a target, determine exactly one route:

| User choice | Route | Primary output |
| --- | --- | --- |
| 人物 | Perspective | One perspective skill |
| 书 / 长内容 | Method | Several atomic method skills |

If the request does not make the choice explicit, ask only this and wait:

```text
你要蒸馏哪一种？
1. 人物：提炼某人的思维框架与决策方式
2. 书 / 长内容：提炼书、视频、播客、课程或访谈中的可执行方法
```

Do not infer a third route. Do not research, generate a skill, or recommend candidates until the user selects `人物` or `书 / 长内容`. Once selected, ask at most two further questions only when a missing target, source text, intended use, or research permission would materially change the result. For a book or long-form source, require the text, transcript, notes, or a user-approved source location; do not distill from memory.

## Working Directory

Create a self-contained pack named `<slug>-zhengliu/` in the user-approved output location. Keep these files when applicable:

```text
<slug>-zhengliu/
  TARGET_BRIEF.md
  PIPELINE_STATE.md
  sources/
  research/
  candidates/
  rejected/
  skills/
    <skill-slug>/SKILL.md
    <skill-slug>/test-prompts.json
  INDEX.md
  DIGEST.md
  GLOSSARY.md
  test-results.md
```

Record target, use case, evidence mode, source inventory, route, and unresolved questions in `TARGET_BRIEF.md`. Record completed stages, rejected claims, and remaining risks in `PIPELINE_STATE.md`.

## Evidence Rules

1. Prefer user-provided material. Use web research only when needed and permitted.
2. Save every material claim with a URL or local reference, date, and label: `firsthand`, `reliable-secondary`, or `inference`.
3. Separate quoted evidence, interpretation, and recommendation. Never invent quotations, positions, or citations.
4. Preserve meaningful disagreement, evolution, and counterexamples; do not force a clean theory where the evidence is mixed.
5. Do not use low-accountability aggregators as core evidence. Do not expose private material beyond the task scope.

## Extract

### Perspective route

Research six lenses when evidence exists: original writing, conversations, expression patterns, outside criticism, consequential decisions, and timeline. Extract only claims with recurring support.

Build:

- 3-7 mental models, each with evidence, mechanism, use case, and failure mode.
- 5-10 decision heuristics.
- Expression DNA only when the user explicitly needs the voice.
- Values, anti-patterns, intellectual lineage, and honest boundaries.

The generated perspective skill must answer from the distilled framework, not impersonate the person. When facts are current, uncertain, or high stakes, research first and clearly distinguish the framework's view from verified facts.

### Method route

First write `BOOK_OVERVIEW.md`: structure, central argument, context, criticism, and applicability. Then extract candidates in parallel categories: framework, principle, case, counterexample, and glossary.

For each approved atomic skill, write the complete RIA+E+B unit:

- `R` - a short source quote or precise location reference.
- `I` - interpretation in plain language.
- `A1` - a source-grounded application.
- `A2` - a future trigger description.
- `E` - concrete execution steps.
- `B` - boundary, failure mode, or when not to use it.

Do not produce a book review, a generic summary, or an author-role-play skill unless the user separately selects the perspective route.

## Verify Before Synthesis

Approve a candidate only when it passes all applicable checks:

1. **Cross-context evidence**: recurrence across independent source contexts, or explicit single-source limitation.
2. **Generative power**: predicts a decision, diagnosis, or next action better than a slogan.
3. **Distinctiveness**: is not merely generic advice relabeled with the source's name.
4. **Boundary**: has a plausible failure case, contraindication, or uncertainty note.

Write failed candidates and the reason in `rejected/`. Keep uncertainty visible instead of filling gaps with confidence.

## Write Generated Skills

Each generated `SKILL.md` must contain valid `name` and `description` frontmatter, then only the instructions needed to act. Include:

1. A trigger and non-trigger.
2. Inputs and evidence assumptions.
3. The decision model or RIA+E+B method.
4. An execution sequence or decision rules.
5. Boundaries, source traceability, and any freshness requirement.

Keep generated skills self-contained. Use short quotes only when necessary; otherwise cite a source location and paraphrase.

## Link, Test, Deliver

Link related skills in `INDEX.md` with `depends-on`, `contrasts-with`, or `composes-with`. Maintain shared terms in `GLOSSARY.md` and a human-readable synopsis in `DIGEST.md`.

Create `test-prompts.json` for every generated skill:

```json
{
  "should_trigger": ["A request where this skill is the best fit"],
  "should_not_trigger": ["A nearby request better handled by a sibling skill"],
  "edge_cases": ["A case that tests its stated boundary"]
}
```

Run the prompts as a blind check. A skill passes only when it activates for the first class, declines or routes the second class, and states the boundary for the third. Record results and revise unclear triggers before delivery.

## Red Flags

- Do not start costly or long-running research without scope and evidence-mode confirmation.
- Do not treat an author's claim as fact merely because it is in a book.
- Do not turn one memorable quote into a universal mental model.
- Do not hide contradictions, copyright limits, source gaps, or stale information.
- Do not call the result complete without `test-prompts.json` and `test-results.md`.

## Deliverable

Return the pack path, generated skill names, evidence coverage, rejected or unresolved items, and the next required user action. State clearly when the output is source-limited or when a source must be supplied before distillation can continue.
