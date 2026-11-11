# 风格档案的规则强度：分几档、叫什么、用量写在哪

问题：风格档案里每条规则标一个强度，原来分「要求 / 习惯 / 手法」三档。这三档按什么分、叫什么名字，人和模型才不会读错；限制用量的规则（口头禅、强表态词）该算一档，还是另写。

调研日期：2026-11-09。每条结论后标证据强度：

- 【标准】成熟规范体系的条文。
- 【论文】有实验数据的论文。预印本另注明。
- 【官方】模型厂商文档里的建议，没有公开实验细节。
- 【实践】风格指南和检查工具的做法，不证明效果。
- 【推断】由上面几类证据推出、没有直接实验的判断。

来源编号见文末。

## 结论

1. 分三档：MUST（必须）、SHOULD（应该）、MAY（可选）。档位只回答一件事：在「适用」范围内不这么写，算不算错。
2. 位置和用量不是一档，是每条规则自己的参数，写进「适用」，三档都可以写。MAY 必须写「适用」。写稿时用在「适用」以外的位置，或者超过写的用量，算错。
3. 用量写成「最多 N 处」，不写「少用」「偶尔」，也不写「恰好 N 处」。
4. 口头禅、表态词、语气词这类规则定 MAY，不定 SHOULD。
5. 规则里不用全大写、「务必」「绝不」之类的强调词。

## 1. 成熟体系都按「能不能偏离」分档

- RFC 2119 分三级：MUST 是绝对要求；SHOULD 是在特定情况下可以有正当理由不照做，但要先权衡后果；MAY 是真正可选 [S1]。RFC 8174 补充规定，这几个词只有全大写时才是这个意思 [S2]。【标准】
- ISO/IEC Directives Part 2 分 shall、should、may、can。requirement 客观可验证，不允许偏差；recommendation 指特别合适，但不排除别的做法 [S3]。【标准】
- GB/T 1.1-2020 规定：要求用「应 / 不应」，推荐用「宜 / 不宜」，允许用「可 / 不必」（附录 C）。「通常」「一般」「原则上」只能和「宜」连用，不能和「应」连用（9.4.2.3）。条件直接写进条文，例如「……情况下应……」（9.4.2.4）[S4]。【标准】
- GitLab 文档风格按违反的后果分档：error 让 CI 失败，warning 不阻断，suggestion 只在编辑器里显示 [S5]。【实践】

这几个体系没有一个按频率分档。GB/T 1.1 里，频率词是降档的信号，本身不是一档。原来的「手法」把「位置和用量」放进了档位定义，混进了第二个维度。

## 2. 用量是规则的参数，和强度分开

- Vale 的 occurrence 检查用 max、min 限定一个词在一句或一段里出现几次，严重度（level）另外配置 [S6]。Vale 还有 consistency 检查，专抓同一个词混用两种写法 [S7]。【实践】
- ESLint 的规则配置里，第一项是严重度，后面是选项；只改严重度时，选项不用动 [S8]。【实践】
- Microsoft 风格指南写的是「Use exclamation points sparingly」，用量直接写在规则里，不单独分档 [S9]。【实践】

## 3. 模型照着做的是条件和上限，档位名作用有限

- 规则里声明了优先级，也压不住模型对某类约束的固有偏好 [P1]。【论文，预印本】
- 指令冲突时，模型常把两条看成同级，或者两条各照做一半 [P2]。【论文】
- 新模型照字面执行，一条指令适用到哪里，它不会自己往外推，范围要写明 [A1]。【官方】
- 规则一多，模型主要是漏掉，而且靠前的规则执行得更好 [P3]。【论文，预印本】
- 按条件选分支的约束是第二难的一类，嵌套越深越差 [P4]。【论文】

档位名也有用：它告诉检查和维护档案的 AI 什么算错、该报错还是只提示，以及「适用」没写到的情况怎么处理。【推断】

## 4. 「默认照做」用在口头禅上会用过头

- Anthropic 指出，「Default to using X」「If in doubt, use X」这类写法会过度触发，建议改成「在……时用 X」[A2]。【官方】
- OpenAI 指出，「always」类指令会带来副作用；给了示例短语，模型会原样照搬，读起来重复 [A3]。【官方】
- 模型模仿某种风格时，会把表层标记放大，用量达到真人的 10 到 15 倍 [P5]。【论文，预印本】

所以口头禅、表态词、语气词定 MAY，并写明上限。【推断】

## 5. 用量写「最多 N 处」

- 「稍微」这类模糊程度词，模型理解成多少会偏离人类，只有大致的高低顺序比较稳 [P6]。【论文，预印本】
- 计数类约束是最难执行的一类，模型自己核对计数时还会算错 [P7]。【论文】
- 「恰好 N」最难做到，「最多 N」好一些 [P8]。【论文】

上限是固定说法时，检查时直接在原文里搜索计数，不让模型自己数。【推断】

## 6. 不用强调词

- Anthropic 建议把「CRITICAL: You MUST」改成平常语气，否则新模型会执行过头 [A2]。【官方】
- OpenAI 认为全大写没有必要，还会让模型执行得过严 [A3][A4]。【官方】
- 全大写的实测结果不一致，有一项测试里完全没有效果 [P9]。【论文，预印本】

MUST、SHOULD、MAY 是档位标签，写在规则标题后的括号里，不在正文里用来加重语气。

## 7. 命名

- 「习惯」「手法」讲的是规则属于哪一类：档案里每条都是作者的习惯，看名字判断不出不照做算不算错。
- 「偶尔」本身是模糊的频率词，会和规则里写的上限打架，还容易被读成「要找机会用几次」。【推断】
- 「应」在口语里常表示推测（「应该是」），「宜」日常很少用，两者都要先给定义才靠得住。GB/T 1.1 不用「必须」，是为了和法律这类外部约束分开，个人档案没有这个顾虑 [S4]。
- MUST、SHOULD、MAY 在 RFC 和各类技术规范里大量出现，模型在预训练里见过，入口一句定义就够。中文写作「必须、应该、可选」。【推断】

## 定档

| 强度 | 定义 | 定档时问 |
| --- | --- | --- |
| MUST（必须） | 照做，不符合就是错 | 能指出哪一句违反了，而且想不出正当的例外吗？ |
| SHOULD（应该） | 照做；材料需要时可以偏离，偏离时说得出原因 | 不这么写，需要给理由吗？ |
| MAY（可选） | 不用不算错；必须写「适用」 | 整篇都不用，也没问题吗？ |

用现有规则演示：

- 一个对象全文一个叫法 → MUST：可以逐个对象核对，客观可验证。
- 直接说结论和做法 → SHOULD：「直截了当」要靠判断，没法逐句判对错。想保留硬约束的话，拆出一条能逐句判的，如「引出案例的第一句就说案例是什么、能做什么」，定为 MUST。
- 讲自己的看法用「我觉得」起句 → MAY：原来定为习惯，补充却写「少用」，两处意思相反。
- 画外音放进括号 → MAY：原来定为习惯，补充写「很偶尔用」，矛盾相同。

## 来源

标准

- [S1] RFC 2119: https://www.rfc-editor.org/rfc/rfc2119
- [S2] RFC 8174: https://www.rfc-editor.org/rfc/rfc8174
- [S3] ISO/IEC Directives Part 2 (2021), 3.3.3–3.3.5、第 7 章: https://www.iso.org/sites/directives/current/part2/index.xhtml
- [S4] GB/T 1.1-2020《标准化工作导则 第 1 部分：标准化文件的结构和起草规则》，附录 C、9.4.2.3、9.4.2.4

实践

- [S5] GitLab, Vale documentation tests: https://docs.gitlab.com/development/documentation/testing/vale/
- [S6] Vale, occurrence: https://docs.vale.sh/checks/occurrence
- [S7] Vale, styles: https://docs.vale.sh/topics/styles
- [S8] ESLint, configure rules: https://eslint.org/docs/latest/use/configure/rules
- [S9] Microsoft Writing Style Guide, exclamation points: https://learn.microsoft.com/en-us/style-guide/punctuation/exclamation-points

官方文档

- [A1] Anthropic, Prompting Claude Opus 4.8: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-4-8
- [A2] Anthropic, Prompting best practices: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices
- [A3] OpenAI, GPT-4.1 Prompting Guide: https://developers.openai.com/cookbook/examples/gpt4-1_prompting_guide
- [A4] OpenAI, GPT-5 Prompting Guide: https://developers.openai.com/cookbook/examples/gpt-5/gpt-5_prompting_guide

论文

- [P1] Geng et al., Control Illusion, 2025（预印本）: https://arxiv.org/abs/2502.15851
- [P2] IHEval, NAACL 2025: https://aclanthology.org/2025.naacl-long.425.pdf
- [P3] IFScale, 2025（预印本）: https://arxiv.org/abs/2507.11538
- [P4] ComplexBench, NeurIPS 2024: https://github.com/thu-coai/complexbench
- [P5] Generative Exaggeration in LLM Social Agents, 2025（预印本）: https://arxiv.org/abs/2507.00657
- [P6] Does Slightly Mean Somewhat?, 2026（预印本）: https://arxiv.org/abs/2605.21827
- [P7] Divide-Verify-Refine, ACL Findings 2025: https://aclanthology.org/2025.findings-acl.709.pdf
- [P8] LIFEBench, NeurIPS 2025: https://arxiv.org/abs/2505.16234
- [P9] IssueTrojanBench, 2026（预印本）: https://arxiv.org/abs/2607.20759
