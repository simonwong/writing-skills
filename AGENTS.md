# AGENTS.md

## Repository

This repository contains Simplified Chinese writing skills. Each skill is standalone; the only shared runtime data is the author's writing-style archive (see 个人风格).

Each skill lives at `skills/<skill-name>/`. Keep its `SKILL.md` and supporting resources together. Test cases live at `evals/<skill-name>/` and are not installed with the skill.

## Working Rules

- Read the target skill and its local instructions before editing it.
- Keep changes scoped to the requested skills. Preserve unrelated work.
- Keep skills self-contained. Add supporting files only when the workflow needs them.
- Preserve explicit-invocation settings in both `SKILL.md` and `agents/openai.yaml` when present.
- Write agent-facing instructions as short, imperative steps. Keep final-state docs free of migration history and discarded approaches.

## Writing Rules

- Write skill instructions and user-facing output in Simplified Chinese.
- Keep `name`, `description`, `license`, `metadata.author`, and `metadata.version` in each `SKILL.md` frontmatter.
- Quote version strings, for example `"1.2.0"`.
- Include concrete Chinese trigger phrases in `description`.
- Bump `metadata.version` whenever a skill's `SKILL.md` changes.

## 个人风格

skill 里只写通用写法，`references/expression.md` 也是通用的。作者的个人风格放在仓库外的风格档案，由 `writing-style-setup` 建立、`writing-style-learn` 维护；接口和理由见 [docs/adr/writing-skills.md](docs/adr/writing-skills.md)。

- 某条写法只有这位作者需要时，写进风格档案，不写进 skill。
- 怎么读和用档案只写在 `writing-style-setup` 第 3 步 index.md 模板的「使用说明」；write-article 和 write-tweet 的「风格档案」一节只指向 index.md，两节除体裁名和体裁目录外保持一致。
- 档案的目录、文件名和 index.md 只在 `writing-style-setup` 定义；各文件的骨架和节名、每节放什么和「用法：」一行、规则格式和放哪、candidates.md 的格式只在 `archive-format.md` 定义；范文的写法只在 `writing-style-learn` 定义。改动这些时，同步：write-article 第 1、3、4、5 步和 `references/review.md`「作者表达」，write-tweet 第 3、4 步，`docs/adr/writing-skills.md`。
- `archive-format.md` 在 learn 和 setup 的 `references/` 下各有一份：改 `skills/writing-style-learn/references/archive-format.md`，再复制到 `skills/writing-style-setup/references/`。
- 改完运行 `python3 scripts/check_writing_style_sync.py`。

## Validation

- Validate every changed `SKILL.md` against the [Agent Skills Specification](https://agentskills.io/specification), allowing documented client-specific frontmatter extensions such as `disable-model-invocation`.
- Check links and paths referenced by changed instructions.
- When a skill has cases under `evals/<skill-name>/`, run them after changing its rules, flow, or output format.
- Run `git diff --check` before committing.

## Agent skills

### Issue tracker

Track maintainer work in Linear. Before creating, reading, or updating tickets, read `docs/agents/issue-tracker.md`.

### Domain docs

Single-context: `CONTEXT.md` at the repo root plus `docs/adr/`. See `docs/agents/domain.md`.
