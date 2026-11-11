# 个人写作风格档案：收什么、怎么写、怎么提取

问题：给 LLM 写作 skill 用的个人写作风格档案，格式、结构和提取方法怎样做效果最好。对照对象是 `skills/writing-style-setup/SKILL.md` 和 `skills/writing/writing-style-learn/SKILL.md`（均为 0.1.0）。

调研日期：2026-11-05。每条结论后标证据强度：

- 【论文】有实验数据的论文。预印本另注明。
- 【官方】模型厂商文档里的建议，没有公开实验细节。
- 【实践】开源项目或成熟风格指南的做法，不证明效果。
- 【推断】由上面几类证据推出、没有直接实验的判断。

来源编号见文末。

## 结论摘要

1. 只给范文，模型学不像普通作者，尤其是博客、论坛这类随意文体；多给范文帮助很小。Wang et al. 2025 用 400 多位真实作者测试，5 篇范文的输出比 0 篇更接近作者，但从 2 篇加到 10 篇，各项指标几乎不变，输出仍偏向「平均、通用的语气」[P7]。【论文】档案不能只靠范文，也不该靠堆更多范文。
2. 规则描述和范文作用不同，两者合用最好。PROSE 的实验里，范文（ICL）在结构类偏好上更好，文字描述在语气类偏好上更好，两者合用比单用范文高 8.9% [P14]。【论文，模拟用户、摘要和邮件任务】当前「规则 + 片段 + 范文」三层结构与此一致。
3. 从改稿学比从整篇语料归纳更直接。CIPHER 从「模型输出 → 用户改后」的差异推出偏好，用文字存下，按场景检索，改稿量比不学习少 31%–73%，比直接检索过去的改稿便宜得多 [P13]。PROSE 在此基础上加了两步：拿推出的偏好再写一稿和用户原文比、反复修正；把偏好拆成短条目，逐条到用户的其他样本里核对，对不上的删掉 [P14]。【论文】
4. 让 LLM 从样本里归纳风格，得到的描述泛、不稳定。PROSE 指出已有方法常产出「通用的偏好描述」[P14]；PersonalBench 发现同一方法多次抽取的特征清单重合度只有 Jaccard 0.22，并且用 LLM 评委打分时，「先抽特征再照着写」的方法得分比作者本人原文还高，评委量到的是指令遵循，不是像不像作者 [P10]。【论文，预印本】所以规则要有作者原话或手改作依据，校准不能只靠同一个模型对照档案自评。
5. 形容词式描述（「语气温暖」）没有证据支持单独使用。STYLL 把形容词描述和 16 对范文一起用，是低资源风格迁移最强的基线，但作者结论是「还没掌握这个任务」[P5]；PROSE 和 PersonalBench 都把泛化描述列为问题 [P14][P10]。【论文】可执行的规则写成「什么情况下怎么写」，并附原因：Anthropic 文档的例子显示，说明原因后模型能推广到相近情形 [A1]。【官方】
6. 负面规则效果差，应写成正面替代。Anthropic 建议「告诉 Claude 做什么，而不是不做什么」[A1]；早期模型在否定式提示上随规模增大反而变差 [P20]；「别提粉红大象」类指令常让模型照样提到 [P21]。【官方 + 论文，后两篇用的是较早模型】需要保留的禁止项，写明换成什么。
7. 档案越长，单条规则越容易被漏掉；靠前的更容易被执行。IFScale 测到指令数增加时准确率下降，最好的模型在 500 条时约 68%，且偏向执行靠前的指令 [P22]；长上下文里，放在中间的信息最难被用上 [P23]。【论文，任务是关键词包含，不是风格规则】档案规模在几十到一两百条规则时可以全量放进上下文，但要合并重复、把常被违反的放前面；Anthropic 建议长文档放在提示开头、指令和任务放后面 [A1]。【官方】
8. 区分「作者独特写法」和「模型默认写法」要有基线。不同模型的输出能以 97.1% 准确率区分，差异主要在用词分布，改写、翻译后仍保留 [P25]；Kobak et al. 用「LLM 出现前的词频」作基线找出被模型带高的词 [P26]。【论文】对档案的直接做法是：不给档案让模型写同一篇，看它默认怎么写，只把作者和默认不同的地方写成规则。genideva/voice-profile 就是先让 Claude 无风格指令写三稿，再和作者比 [R1]。【实践】

## 1. 档案该收哪些维度

### 1.1 计量文体学里最能区分作者的特征

- 高频词（尤其虚词）的相对频率是作者归属最常用的特征。Burrows' Delta 比较的就是最高频词的 z 分数差 [P1]。虚词被认为与话题无关、使用时不自觉，所以能区分作者 [P2][P3]。【论文】
- 中文同样适用。Yu 2012 用 35 个虚词（的、了、就、也、却、把、被等）做现代汉语作者归属：小说平均约 90%、散文 85%、博客 68%；同时发现虚词也区分体裁，作者和体裁混在一起时两者互相干扰 [P3]。【论文】
- 字符 n-gram、句长、词长、标点也常用；不同模型的风格也主要在用词分布上可区分 [P25]。【论文】
- 体裁会盖过作者信号。Eder 2017 指出作者特征有时被体裁、性别、年代、翻译等信号掩盖，有的作者特征明显，有的不明显，最小样本量因作者而异 [P4]。【论文】

对档案的含义：作者最稳定的指纹（虚词频率、句长分布）是不自觉的习惯，写成规则很难执行，也很难让作者认出来；这部分更适合由片段和范文携带。作者能意识到、也能说清的固定用词、标点习惯、段落长度判断，适合写成规则。【推断】

### 1.2 对模型模仿有用的维度

- 结构（怎么开头、怎么推进、怎么收尾）：范文比文字描述更有效 [P14]。【论文】
- 语气、措辞倾向：文字描述比范文更有效 [P14]。【论文】
- 表面特征（标点、符号、口语词）：模型能抓到一部分。Wang et al. 发现某些模型在博客和 Reddit 上的作者归属得分较高，原因是作者间差异明显的 `*`、`#`、`!` 这类表面线索被学到了 [P7]。【论文】
- 选材、立场、对读者的定位：计量文体学把它们当作要排除的「内容」[P4 Wegmann]，但模型默认写法的特征有一部分在内容层面，改写、翻译后仍保留 [P25]；LLM 辅助写作会让不同作者的内容变得相似 [P27]，让非西方作者的写法向西方靠拢 [P28]。【论文】所以对写作 skill 来说，选材和立场要收，否则模型会用自己的默认内容填空。【推断】

### 1.3 基本无效或无证据的维度

- 只写人格或语气形容词（「真诚」「犀利」）：无证据单独有效（见摘要第 5 条）。genideva/voice-profile 收了大五人格分数，但每项要求至少两段原文作证 [R1]。【实践】
- 写成数字目标的统计特征（平均句长 N 字、虚词每千字 M 次）：计量研究表明这些能区分作者，但没有找到「把它们写进提示词能让模型写得更像」的实验。genideva/voice-profile 用数字区间做事后校验而非写作指令 [R1]。【实践】本仓库 ADR 已决定写作规则不设数字阈值（`docs/adr/writing-skills.md`「规则交给模型判断」）。

## 2. 档案格式

### 2.1 规则、范文、抽象描述的效果

| 形式 | 证据 | 适合承载 |
| --- | --- | --- |
| 范文（few-shot） | 0 篇 → 5 篇显著变好，5 篇以上几乎不再提升，随意文体仍学不像 [P7]；few-shot 风格匹配比 zero-shot 最高高 23.5 倍 [P8]；Anthropic 称范文是控制格式、语气、结构「最可靠的方法之一」，建议 3–5 个 [A1] | 结构、段落写法、整体节奏 |
| 改前/改后对 | CIPHER 和 PROSE 都从「模型稿 vs 用户稿」差异中学习 [P13][P14]；直接检索原始改稿（不归纳）在邮件任务上几乎无效，且 token 成本高得多 [P13] | 作为规则的证据和例子，不单独使用 |
| 规则清单 | PROSE 的偏好是有序短条目，与范文合用最好 [P14]；Anthropic 建议说明原因 [A1] | 语气、用词、判断标准 |
| 形容词描述 | STYLL 用但未证明单独有效 [P5]；被指为泛化 [P14] | 不单独使用 |
| 让模型续写作者原文 | 续写式提示与原作者风格一致率 99.9%（作者的验证器口径）[P8]；在提示里放一段作者真实文字，被 GPTZero 判为人写的比例从 9.00% 升到 21.70%（博客）[P7] | 写稿时让作者先写开头或关键句 |

【论文 + 官方】

范文的风险：模型会照搬。OpenAI 指出给了示例短语后，模型会逐字使用，读起来重复 [O1]；Anthropic 要求范文足够多样，避免模型学到意外的模式 [A1]。【官方】

### 2.2 规则怎么写才能执行

- 写目标状态，并写何时适用。Anthropic 例：不写「不要用 markdown」，写「回复用连贯的段落」[A1]。【官方】
- 附一句原因。Anthropic 例：「永远不要用省略号」改成「回复会被语音朗读，所以不要用省略号，引擎读不出来」，模型能从原因推广 [A1]。【官方】
- 一条规则一个意思。PROSE 把偏好拆成短条目逐条核对；保持 LLM 原本的措辞和顺序比重新排序好约 11% [P14]。【论文】
- 成熟风格指南的条目格式：GOV.UK A–Z 每条是「词头 + 规则 + 例子，部分附原因」[G3]；Google 开发者风格指南用「Recommended / Not recommended」对照，以及「太随意 / 刚好 / 太正式」三栏表 [G2]；Mailchimp 用「X 但不 Y」限定特质（「weird but not inappropriate」）[G1]。【实践】
- 层级与例外：Google 风格指南规定先按项目专用规范，再按本指南，再按第三方参考，并称「这是指南不是规则，能改善内容时可以偏离」[G2]。【实践】这与本仓库「体裁卡 > voice.md > skill 通用写法」的优先级同构。

### 2.3 负面规则

- 否定式提示在 2022 年的模型上随规模增大表现变差（inverse scaling）[P20]。【论文，较早模型】
- 「不要提到 X」常导致模型提到 X；作者的解决办法是微调，并非提示词 [P21]。【论文】
- Anthropic 官方仍在示例里用「Avoid ...」列出要避开的通用 AI 审美，但同时给出替代方向（「做出出人意料的选择」）[A1]。【官方】

- 开源的去 AI 味 skill 普遍用负面模式清单，但每种模式都配改前改后，等于给出替代写法 [R2]。【实践】

结论：负面规则可以有，但每条要写替代写法；更适合放在专门的检查环节（本仓库的 `writing-ai-check`），而不是作为写作规则的主体。【推断】

## 3. 提取流程

### 3.1 三种来源的比较

| 来源 | 证据 | 局限 |
| --- | --- | --- |
| 从作者改稿学 | CIPHER 改稿量降 31%–73% [P13]；PROSE 比 CIPHER 再好 33% [P14]；DITTO 用不到 10 个作者示范微调，胜率比 few-shot 等基线平均高 19 个百分点（16 人用户实验）[P15] | CIPHER、PROSE 用 GPT-4 模拟用户，偏好较粗（「用 emoji」「短句」），对细粒度个人风格的效果未验证 |
| 从语料自动归纳 | LLM 抽取的特征清单泛、不稳定（Jaccard 0.22）[P10][P14] | 需要人工确认 |
| 访谈作者 | GATE：模型主动提问得到的信息比用户自己写提示或标注更多，用户也觉得更省力 [P19] | 实验任务是邮件验证、内容推荐、道德判断，不是写作风格 |

【论文】

推荐顺序：改稿和原话作主要依据；亲笔语料提供片段、范文和候选规则；用提问补齐语料里看不出的部分（例如「这是一贯写法还是只针对这篇」）。【推断，与 GATE、PROSE 一致】

### 3.2 需要多少语料

- 作者归属（判断是谁写的）：Eder 2015 认为每个样本至少约 5000 词，2017 年的新方法可降到 2000 词以下，但特征不明显的作者需要更长样本 [P4]。【论文，英文和波兰文】
- 少样本风格迁移：STYLL 用每位作者 16 篇、平均约 500 词的帖子 [P5]。【论文】
- 提示词范文：5 篇以上收益很小 [P7]；Anthropic 建议 3–5 个 [A1]。【论文 + 官方】
- 微调：DITTO 不到 10 个示范 [P15]；Panza 用不到 100 封邮件就能仿得很像 [P16]；OpenAI 建议从 50 条精心写的示范开始，最少 10 条 [O2]。【论文 + 官方】
- 从改稿归纳规则需要多少条：没有找到直接研究。PROSE 用「跨多个样本核对」来防止只在一个样本上成立的偏好进入档案 [P14]，这是「同一改法出现两次再升级」的最接近的证据。

### 3.3 区分作者写法和模型默认写法

- 基线对比：见摘要第 8 条 [P25][P26][R1]。
- 内容和风格要分开：只按「同一作者」训练的风格表示会混入话题；用对话或领域标签控制内容后，风格表示更干净 [P4 Wegmann]。【论文】对档案的含义：一种写法只在一个题材里出现时，可能是题材造成的，升级为规则前要在不同题材的稿件里再次看到。【推断】
- 体裁会干扰作者信号 [P3][P4]，所以体裁内的差异和作者的差异要分开记。【论文】

### 3.4 校准和验证

- 自动指标：研究普遍用作者归属、作者验证模型（如 LUAR）、风格嵌入、AI 检测器组合评估 [P7][P9][P10]。这些对中文个人档案的可用性未验证；AI 检测器对不同模型有偏差 [P7]。【论文】
- LLM 评委有循环问题：抽特征和评分是同一类操作，评分奖励的是「照着特征清单写」[P10]。【论文，预印本】
- 用模型的写法冒充作者，在作者验证系统面前仍会被识破，部分原因是 LLM 文本词汇多样性和熵更高 [P9]。【论文】
- PROSE 的「写一稿、和作者原文比、修正描述」循环，平均带来 14.8% 提升，是改进幅度最大的一步 [P14]。【论文】
- 作者盲测（把重写稿和原文混在一起让作者或熟悉作者的读者辨认）：没有找到针对档案校准的一手研究，属于【实践】。

## 4. 长度、组织和放入上下文的方式

### 4.1 长度

- 指令越多遵循率越低，且偏向靠前的指令 [P22]；放在长上下文中间的信息利用率最低 [P23]。【论文】
- 多样本 ICL（数百到上千例）在多类任务上有显著提升 [P24]，但个人风格任务上 5 篇以上几乎不再提升 [P7]。【论文】两者不矛盾：个人作者可用的高质量范文本来就少，瓶颈在模型能否抓到隐性风格，不在数量 [P7]。

没有找到「风格档案多长最好」的直接研究。【证据缺失】

### 4.2 跨体裁 vs 体裁卡

- Mailchimp 区分 voice（不变）和 tone（随场景变）[G1]。【实践】
- CIPHER 按场景（文档类型）存偏好并检索，同一用户对新闻摘要和对邮件的偏好不同 [P13]。【论文】
- 中文虚词同时反映体裁和作者 [P3]；模型在新闻、邮件上学得像，在博客、论坛上学不像 [P7]。【论文】
- genideva/voice-profile 每种写作模式单独建档，理由是对所有文体取平均会描述出作者从没写过的风格 [R1]。【实践】

结论：「跨体裁规则 + 体裁卡」的分层有依据。【论文 + 实践】

### 4.3 全量 vs 检索

- LaMP：从用户历史中检索相关条目放进提示，对个性化有效 [P11]。【论文】
- 先离线生成「任务相关的用户摘要」再配合检索，用的检索数据少 75%，效果持平或更好 [P12]。【论文，4 页 workshop 论文】
- CIPHER 检索的是推出的偏好，不是原始改稿；检索原始改稿成本高、在邮件任务上几乎无效 [P13]。【论文】
- Anthropic：超过约 2 万 token 的长文档放在提示开头，问题放末尾，测试中质量最多提升 30% [A1]。【官方】

结论：规则（相当于摘要）全量读；片段和范文在规模变大后再按体裁、篇型、题材检索。【推断】

## 5. 对照当前设计

### 5.1 已经符合的

- 依据只收手改、原话、亲笔，AI 写的只作线索：与 CIPHER/PROSE 从用户改稿学习、PersonalBench 对 LLM 抽取不稳定的发现一致 [P13][P14][P10]。
- 「规则只收作者和模型默认不同的地方」：方向和基线对比研究一致 [P25][P26]。
- 规则 + 片段（改前改后）+ 范文三层：与 PROSE+ICL 合用最好一致 [P14]，也与 GOV.UK、Google 的「规则 + 对照例子」条目格式一致 [G2][G3]。
- 规则写成改完后的样子、冒号后写适用条件和原因：符合 Anthropic「说做什么」「说明原因」[A1]。
- 「观察中」要再次出现才升级，且出现在不同稿件里：对应 PROSE 的跨样本核对 [P14]，也部分处理了题材混入（3.3）。
- 跨体裁 voice.md + 体裁卡，体裁卡优先：有论文和实践支持（4.2）。
- 每体裁 3–5 篇、题材各不相同的范文：与 [A1] 的数量和多样性建议、[P7] 的收益曲线一致。
- 范文的「不照搬」：针对 [O1] 所说的逐字照搬风险。
- 档案是作者可读可改的纯文本，冲突由作者定：PRELUDE 也把「偏好是文本、用户可查看修改」作为设计目标 [P13]。
- 校准流程「列素材 → 子代理重写 → 对比原文 → 归类」：与 PROSE 的「写一稿和原文比、修正描述」同构 [P14]，且用素材清单隔离了内容差异，符合 3.3 的内容/风格分离。

### 5.2 建议调整

按影响排序。

1. 校准加一路无档案基线。第 2 步同时开一个不读档案的子代理，用同一份素材清单写一稿。对比时分三类：档案稿和无档案稿一样、都偏离原文的（档案没写到，或写了没起作用）；档案稿比无档案稿更接近原文的（规则有效）；无档案稿本来就和原文一致的（对应规则可能是模型默认写法，按「规则只收不同的地方」考虑删）。依据：[P25][P26][R1]，以及摘要第 8 条。
2. 校准结果不只由本会话判断。现在第 3 步由写档案的同一模型在本会话对比，存在 [P10] 指出的循环问题。可选做法：把档案稿、无档案稿和原文去掉标记交给作者，让作者标出「不像我」的句子；作者的标注作为第 4 步归类的主依据。证据强度：循环问题是【论文，预印本】，作者盲测本身是【实践】。
3. 「观察中」升级条件加上「不同题材」。现在要求出现在不同稿件里；建议明确是题材不同的稿件，或至少在升级时看一眼两处是否只因题材相同才这样写。依据：[P4 Wegmann]、[P3]。
4. 固定用词和口头禅写明密度。规则里已允许「作者固定用的一组词」，建议同一条写清「一篇里偶尔用」或「只在 X 处用」，避免模型逐字高频复用 [O1]。写成判断，不写次数，符合本仓库 ADR 的「不设数字阈值」。
5. 负面规则一律写替代写法。现在规则格式要求写改完的样子，已基本覆盖；建议在「规则」一节补一句：作者的原话是「不要 X」时，问作者换成什么，写成正面规则，问不出时记进「观察中」。依据：[A1][P20][P21]。
6. 档案读入顺序（涉及 write-article / write-tweet 的「风格档案」一节，非本两个 skill）：范文较长时，先读范文和片段，再读 voice.md 和体裁卡，让规则离任务最近。依据：[A1] 的长文档在前、指令在后；[P22] 的靠前偏好与此方向相反，所以把最常被违反的规则放在各组开头，两者兼顾。证据强度【官方 + 推断】，收益幅度不确定，可在 evals 里试。
7. 规模变大后的检索。规则全量读不变；片段每条规则只留少数几组（现设计已有）；某体裁范文超过当前上限、或片段文件明显变长时，再考虑按篇型或题材只读相关的。现阶段不需要改。依据：[P11][P12][P13]。
8. 整理时做一次去重压缩。现设计在「整理」时合并重复；建议把「规则条数明显增长」也作为提醒作者整理的时机，依据 [P22] 的指令密度下降。不设条数阈值。
9. 写稿侧可选：让作者先写开头或关键句，再由模型续写。依据：续写和真实片段对风格一致性的提升 [P7][P8]。这属于 write-article / write-tweet 的流程，不改档案格式。

不建议的方向：

- 不建议加形容词式「风格总述」作为主体（摘要第 5 条）。voice.md「作者与读者」一组写身份和读者定位是具体信息，不属于此类。
- 不建议把句长、虚词频率写成写作规则（1.3）。如果以后想做自动核对，可以像 genideva/voice-profile 那样作为事后检查的数字区间 [R1]，与写作规则分开。

## 6. 证据薄弱的地方

- 「规则 + 范文合用最好」的直接证据只有 PROSE [P14]，用的是 GPT-4 模拟用户、摘要和邮件任务、偏好较粗；对中文长文、真实作者的细粒度风格未验证。
- 「从改稿学优于从语料归纳」：CIPHER、PROSE 同样是模拟用户；DITTO 有真人（16 人），但方法是微调，不是提示词档案。
- 访谈作者的效果：GATE [P19] 的任务不是写作风格。
- 作者盲测作为校准方法：没有找到一手研究。
- 档案长度上限：IFScale [P22] 的指令是「包含某关键词」，与风格规则差别大；没有风格档案长度的直接研究。
- 负面规则：两篇论文用的是 2022–2024 年的模型 [P20][P21]，现代模型的程度可能不同；结论主要依赖 Anthropic 官方建议。
- STYLL 里形容词描述的消融结果在附录 D，本次没有读到，不能说明描述在范文之外有无增益 [P5]。
- PersonalBench [P10] 是 2026 年 8 月的单作者预印本；Zeng & Nini [P9] 是 2026 年 3 月预印本。
- 中文：只找到计量文体学的虚词研究 [P3]，没有找到中文个人风格 LLM 模仿的实验。
- Google Gemini 官方文档中关于风格示例的建议本次未查。
- Burrows' Delta 原文 [P1] 未读全文，只引其公认的方法定义；样本量结论引自 Eder [P4]。

## 参考来源

### 模型厂商文档

- [A1] Anthropic, Prompting best practices（含 Use examples effectively、Add context、Long context prompting、Control the format of responses 各节）. https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices
- [O1] OpenAI, GPT-4.1 Prompting Guide. https://developers.openai.com/cookbook/examples/gpt4-1_prompting_guide
- [O2] OpenAI, Supervised fine-tuning guide. https://developers.openai.com/api/docs/guides/supervised-fine-tuning

### 论文

- [P1] Burrows, J. 2002. 'Delta': a Measure of Stylistic Difference and a Guide to Likely Authorship. Literary and Linguistic Computing 17(3): 267–287. https://doi.org/10.1093/llc/17.3.267
- [P2] Kestemont, M. 2014. Function Words in Authorship Attribution: From Black Magic to Theory? CLfL@EACL. https://aclanthology.org/W14-0908/
- [P3] Yu, B. 2012. Function Words for Chinese Authorship Attribution. CLfL@NAACL-HLT. https://aclanthology.org/W12-2506/
- [P4] Eder, M. 2017. Short Samples in Authorship Attribution: A New Approach. DH2017. https://dh2017.adho.org/abstracts/341/341.pdf ；Wegmann, A., Schraagen, M., Nguyen, D. 2022. Same Author or Just Same Topic? Towards Content-Independent Style Representations. RepL4NLP@ACL. https://arxiv.org/abs/2204.04907 （正文中写作 [P4 Wegmann]）
- [P5] Patel, A., Andrews, N., Callison-Burch, C. 2022. Low-Resource Authorship Style Transfer: Can Non-Famous Authors Be Imitated? https://arxiv.org/abs/2212.08986
- [P7] Wang, Z. et al. 2025. Catch Me If You Can? Not Yet: LLMs Still Struggle to Imitate the Implicit Writing Styles of Everyday Authors. Findings of EMNLP 2025. https://arxiv.org/abs/2509.14543
- [P8] Jemama, R., Kumar, R. 2025. How Well Do LLMs Imitate Human Writing Style? https://arxiv.org/abs/2509.24930
- [P9] Zeng, B., Nini, A. 2026. Authorship Impersonation via LLM Prompting does not Evade Authorship Verification Methods. 预印本. https://arxiv.org/abs/2603.29454
- [P10] Sawant, Y. G. 2026. PersonalBench: Measuring the Authorship Gap in LLM Personalization. 预印本. https://arxiv.org/abs/2608.19746
- [P11] Salemi, A. et al. 2023. LaMP: When Large Language Models Meet Personalization. https://arxiv.org/abs/2304.11406
- [P12] Richardson, C. et al. 2023. Integrating Summarization and Retrieval for Enhanced Personalization via Large Language Models. https://arxiv.org/abs/2310.20081
- [P13] Gao, G. et al. 2024. Aligning LLM Agents by Learning Latent Preference from User Edits（PRELUDE / CIPHER）. https://arxiv.org/abs/2404.15269
- [P14] Aroca-Ouellette, S. et al. 2025. Aligning LLMs by Predicting Preferences from User Writing Samples（PROSE）. ICML 2025. https://arxiv.org/abs/2505.23815
- [P15] Shaikh, O. et al. 2024. Aligning Language Models with Demonstrated Feedback（DITTO）. ICLR 2025. https://arxiv.org/abs/2406.00888
- [P16] Nicolicioiu, A. et al. 2024. Panza: Design and Analysis of a Fully-Local Personalized Text Writing Assistant. https://arxiv.org/abs/2407.10994
- [P17] Horvitz, Z. et al. 2024. TinyStyler: Efficient Few-Shot Text Style Transfer with Authorship Embeddings. https://arxiv.org/abs/2406.15586 （800M 参数小模型加作者嵌入，在作者风格迁移上胜过 GPT-4 等方法；说明作者嵌入可作风格信号，对提示词档案无直接结论）
- [P18] Hallinan, S. et al. 2023. STEER: Unified Style Transfer with Expert Reinforcement. https://arxiv.org/abs/2311.07167 （训练式风格迁移，对提示词档案无直接结论）
- [P19] Li, B. Z. et al. 2023. Eliciting Human Preferences with Language Models（GATE）. https://arxiv.org/abs/2310.11589
- [P20] Jang, J., Ye, S., Seo, M. 2022. Can Large Language Models Truly Understand Prompts? A Case Study with Negated Prompts. https://arxiv.org/abs/2209.12711
- [P21] Castricato, L. et al. 2024. Suppressing Pink Elephants with Direct Principle Feedback. https://arxiv.org/abs/2402.07896
- [P22] Jaroslawicz, D. et al. 2025. How Many Instructions Can LLMs Follow at Once?（IFScale）. https://arxiv.org/abs/2507.11538
- [P23] Liu, N. F. et al. 2023. Lost in the Middle: How Language Models Use Long Contexts. TACL. https://arxiv.org/abs/2307.03172
- [P24] Agarwal, R. et al. 2024. Many-Shot In-Context Learning. NeurIPS 2024. https://arxiv.org/abs/2404.11018
- [P25] Sun, M. et al. 2025. Idiosyncrasies in Large Language Models. ICML 2025. https://arxiv.org/abs/2502.12150
- [P26] Kobak, D. et al. 2024. Delving into LLM-assisted writing in biomedical publications through excess vocabulary. Science Advances 2025. https://arxiv.org/abs/2406.07016
- [P27] Padmakumar, V., He, H. 2023. Does Writing with Language Models Reduce Content Diversity? ICLR 2024. https://arxiv.org/abs/2309.05196
- [P28] Agarwal, D., Naaman, M., Vashistha, A. 2024. AI Suggestions Homogenize Writing Toward Western Styles and Diminish Cultural Nuances. CHI 2025. https://arxiv.org/abs/2409.11360

### 风格指南（组织方式参考）

- [G1] Mailchimp Content Style Guide, Voice and Tone. https://styleguide.mailchimp.com/voice-and-tone/
- [G2] Google developer documentation style guide：Voice and tone https://developers.google.com/style/tone ；来源层级与「指南不是规则」https://developers.google.com/style
- [G3] GOV.UK, A to Z style guide. https://guidance.publishing.service.gov.uk/writing-to-gov-uk-standards/style-guides/a-to-z-style-guide/

### 开源实践（不是研究结论）

- [R1] genideva/voice-profile：按写作模式分别建档，10 项计量特征给区间，人格分数要求引原文，先让模型无风格指令写三稿作基线，附草稿校验脚本。https://github.com/genideva/voice-profile
- [R2] blader/humanizer：基于 Wikipedia「Signs of AI writing」的 26 种模式、每种附改前改后，可贴作者两三段文字作语气校准。https://github.com/blader/humanizer
