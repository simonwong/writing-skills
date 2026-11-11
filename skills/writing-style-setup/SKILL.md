---
name: writing-style-setup
description: 建写作风格档案，并把档案路径写进项目配置，供写作 skill 读取。用于“建风格档案”“初始化写作风格”。
license: MIT
disable-model-invocation: true
metadata:
  author: simonwong
  version: "0.3.0"
---

# 写作风格档案设置

风格档案存放作者的个人写法。index.md 列出档案里的文件，并带一份使用说明：写稿的 agent 只要读到 index.md，就知道读哪些文件、怎么用。

## 1. 定位置

问用户档案放在哪，给一个具体的默认路径：有笔记库时用 `<笔记库里存写作资料的目录>/writing-style/`，没有时用 `~/writing-style/`。用户给的目录本身或其下的 `writing-style/` 里已有 index.md 时，那就是现成的档案：沿用它，按第 3 步补上缺少的文件、换上新的使用说明，再到第 4 步。

完成标准：档案目录的绝对路径已经用户确认。

## 2. 定体裁

把第 3 步的文件清单给用户看，每个文件用一句话说明放什么，问：「除了长文和推文，你还写别的体裁吗？每种体裁发在哪里？」

长文的目录是 `genres/article/`，推文是 `genres/tweet/`，write-article 和 write-tweet 按这两个路径找文件。加体裁时用 `genres/<英文短名>/`，在 index.md「文件」一节加一项，并告诉用户：write-article 只读长文，write-tweet 只读推文，新体裁由 writing-style-learn 维护，供其他 agent 按使用说明读。

类型文件、范文由 writing-style-learn 在入档时加，这一步不建。

完成标准：体裁和每种体裁发在哪里已经用户确认。

## 3. 建档案

在档案目录建下面的文件。已存在的文件保留原内容，只建缺少的。已有 index.md 时，把它的「使用说明」一节换成下面模板里的这一节，其余不动；已有的 style.md、default.md 和类型文件里，哪一节缺「用法：」一行，或和 archive-format.md 骨架里的不一样，照骨架补上或换掉。

- index.md：照下面的模板。
- style.md：照 [archive-format.md](references/archive-format.md)「style.md」一节的骨架，去掉花括号占位的行，「用法：」一行留着。
- genres/article/default.md、genres/tweet/default.md 和用户加的体裁：照 archive-format.md「default.md」一节，只写一级标题和「适用」。一级标题写长文、推文或用户给的体裁名，「适用」写第 2 步用户说的发在哪里。其余各节有内容时由 writing-style-learn 建。
- candidates.md：照 archive-format.md「candidates.md」一节的开头，花括号照写。已有的 candidates.md 开头缺这段格式说明时补上，条目不动。

index.md：

```markdown
# 写作风格档案

## 文件

- [个人风格](style.md)：每句话怎么说，所有体裁通用。
- 长文
  - [default](genres/article/default.md)：长文的语气、结构、排版、固定表达和类型。
- 推文
  - [default](genres/tweet/default.md)：推文的语气、结构、排版、固定表达和类型。
- [候选](candidates.md)：还没定的写法。

## 使用说明

1. 写稿前读 style.md 和本体裁的 default.md；按 default.md「类型」一节选一个类型，再读它的类型文件，没有合适的类型时只用 default.md。default.md 和类型文件「范文」一节链接的范文也读。
2. 先按类型文件和 default.md 定整体结构，再按 style.md 定每句话怎么说。
3. 说法冲突时按这个顺序取前者：用户本次的要求和所用工具的基本约定、类型文件、default.md、style.md、通用写法。
4. 节标题下的「用法」写这一节怎么用，照它用。
5. 规则的「适用」写这条规则用在哪里，只在这些地方用。
6. 规则下的例子和范文示范语气和句子的写法，照着学；事实、经历和数据来自本次材料，不搬例子里的句子。例子里的标点、大小写和错字以「标点和排版」为准；范文开头「不照搬」列出的写法不学。
7. candidates.md 是还没定的写法，不用于写稿。
```

完成标准：上面的文件都已存在；style.md 的节名、顺序和每节的「用法：」同 archive-format.md，default.md 有一级标题和「适用」；index.md 的「使用说明」和模板一字不差；candidates.md 开头有格式说明。

## 4. 写指向

默认写进当前项目，用户也可以指定别的项目。写在项目根目录的 AGENTS.md；只有 CLAUDE.md 时写 CLAUDE.md。两个都没有时，问用户平时用 Claude Code 还是 Codex：只用 Claude Code 建 CLAUDE.md；只用 Codex 建 AGENTS.md；两个都用建 AGENTS.md，再建一份只有一行 `@AGENTS.md` 的 CLAUDE.md。放在 `## Agent skills` 下，没有这一节就在文件末尾加上：

```markdown
### Writing style profile

`<档案目录的绝对路径>/index.md`. Read it before writing any article or post, and follow its 使用说明.
```

已有 `### Writing style profile` 时只改路径和说明。写进 AGENTS.md 时，看同目录的 CLAUDE.md 有没有 `@AGENTS.md`；没有时告诉用户 Claude Code 读不到这个指向，问要不要在 CLAUDE.md 加一行 `@AGENTS.md`。`git remote -v` 有远端时，问用户仓库是否公开；公开的话提醒这个路径会随提交公开，可以改写进 CLAUDE.local.md（确认 .gitignore 里有它），代价是 Codex 读不到。写入前把内容和目标文件给用户看，用户同意后再写。

完成标准：目标文件里恰有一节 `### Writing style profile`，路径指向的 index.md 存在。

## 5. 交付

告诉用户档案位置和改过的配置文件，再说明：

- 新建的档案是空的。之后用 `/write-article`、`/write-tweet` 写稿时，作者改过的句子和说过的写作偏好会记进 candidates.md，攒下一些后运行 `/writing-style-learn` 提炼成规则。
- 手上已有亲笔稿、改稿记录或旧的风格文件，现在就可以运行 `/writing-style-learn` 入档；认可的整篇亲笔稿可以收作范文。
- 在其他项目写稿时，在那个项目运行 `/writing-style-setup`，给出这份档案的路径。

完成标准：用户已知道档案路径、改过的配置文件和上面三条。
