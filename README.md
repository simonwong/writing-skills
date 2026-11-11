<div align="center">

# simonwong/writing-skills

**一组日常使用的写作 Agent Skills**

小、可编辑、可组合，不接管完整工作流。选择需要的 skill，装进自己的 agent 即可。

[![Spec](https://img.shields.io/badge/Agent_Skills-Specification-6E56CF?style=flat-square)](https://agentskills.io/specification)
[![License](https://img.shields.io/badge/License-MIT-3FB950?style=flat-square)](#license)
[![Author](https://img.shields.io/badge/Author-Simon_Wong-1F6FEB?style=flat-square)](https://github.com/simonwong)

</div>

## 安装

<table>
<tr><td>

**Bun**

```shell
bunx skills add simonwong/writing-skills
```

</td><td>

**npm**

```shell
npx skills@latest add simonwong/writing-skills
```

</td></tr>
</table>

安装器会发现 `skills/` 下的 skills，并让你选择要安装的项目和目标 agent。

## 为什么有这些 Skills

<details open>
<summary><b>英文内容翻成中文总带着翻译腔</b></summary>

<br>

`rewrite-en2zh` 先理解英文原意，再脱离英文外壳用中文重新表达，保留 Markdown 格式和 AI 专有名词。

</details>

## Reference

Skills 分为两种调用方式：

| 调用方式 | 说明 |
| --- | --- |
| 🤖 **Model-invoked** | 任务匹配时，agent 可以自动调用；用户也可以直接调用。 |
| 👤 **User-invoked** | 只有用户显式输入 skill 名称时才调用，适合配置和编排动作。 |

| Skill | 调用方式 | 用途 |
| --- | :---: | --- |
| `rewrite-en2zh` | 👤 | 理解英文原意后，用自然的简体中文重新表达。 |
| `write-article` | 👤 | 从想法、素材或草稿出发协作写文章：定选题方向、补素材、设计提纲与节奏、成文、修改。需要时另行运行 `writing-ai-check`。 |
| `writing-ai-check` | 🤖 | 按 23 条编号痕迹逐段找出 AI 味，直接交付定稿、改动清单和统计，会删掉观点的改动留给作者定，信息不增不减。只管 AI 味，不评内容和个人风格。 |
| `write-tweet` | 👤 | 写 X 推文。按本次要求顺稿、压缩、重组或从素材成文，`short` / `long` 指定长短。需要时另行运行 `writing-ai-check`。 |
| `writing-style-setup` | 👤 | 建写作风格档案，并把档案路径写进当前项目的 AGENTS.md。 |
| `writing-style-learn` | 👤 | 把作者的亲笔稿、改稿和原话提炼成规则、类型和范文写进风格档案，并整理档案。 |
| `codex-cover-gen` | 🤖 | 从文章提取封面关键词，按 playbook 定尺寸和布局、按 style 定视觉风格，用 `image_gen` 生成封面。自带公众号封面 playbook 和流体 shader style。 |
| `wechat-publish` | 👤 | 本地预览 Markdown 文章的公众号排版（含微信暗色模式），上传图片和封面并同步到公众号草稿箱。 |

写作 skill 互不调用，各自独立安装使用。稿件写完后需要清理 AI 味时，单独运行 `writing-ai-check`。

个人风格不写进 skill，放在仓库外的风格档案：先运行 `writing-style-setup` 建档，之后用 `writing-style-learn` 把亲笔稿和改稿写进去。`write-article`、`write-tweet` 写稿时按档案写，没有档案时按通用写法。档案的 index.md 带一份使用说明，其他 agent 读它也能照档案写。`writing-ai-check` 只管 AI 味，不读档案。

<details>
<summary><code>write-article</code> 与 <code>writing-ai-check</code> 的实现参考</summary>

<br>

- [stop-slop](https://github.com/hardikpandya/stop-slop)
- [human-writing](https://github.com/KKKKhazix/human-writing)
- [lieflat-less-ai-tone](https://github.com/larashero3-dotcom/lieflat-less-ai-tone)
- [humanizer](https://github.com/blader/humanizer)
- [Humanizer-zh](https://github.com/op7418/Humanizer-zh)
- [dbskill](https://github.com/dontbesilent2025/dbskill)
- [khazix-writer](https://github.com/KKKKhazix/khazix-skills)
- [Dan Koe 的写作方法](https://thedankoe.com/letters/the-greatest-skill-of-the-21st-century/)
- 影视飓风 Tim 的 HKRR（快乐、知识、共鸣、节奏）
- 潘乱的三种转发动机（对我有用、感同身受、喜闻乐见）
- [宝玉：去掉 AI 味](https://baoyu.io/blog/2026-02-14/remove-ai-writing-flavor)
- [Paul Graham: Write Like You Talk](https://paulgraham.com/talk.html)
- [中文文案排版指北](https://github.com/sparanoid/chinese-copywriting-guidelines/blob/master/README.zh-Hans.md)

</details>

## 仓库结构

```text
skills/
├── codex-cover-gen/
├── rewrite-en2zh/
├── wechat-publish/
├── write-article/
├── write-tweet/
├── writing-ai-check/
├── writing-style-learn/
└── writing-style-setup/
evals/
└── writing-ai-check/
```

`skills/` 下每个目录都是一个可独立安装的 skill。`evals/` 存放 skill 的测试用例，不随 skill 安装。

## 推荐 Skills

工程、编排和其他通用 skill 在 [simonwong/skills](https://github.com/simonwong/skills)。

## Find Me

- [X / Twitter](https://x.com/simon_wong)
- [GitHub](https://github.com/simonwong)

## License

MIT
