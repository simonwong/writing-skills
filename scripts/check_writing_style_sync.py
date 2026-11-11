#!/usr/bin/env python3
"""Check that the writing skills agree on the writing-style archive format.

Run from the repository root: python3 scripts/check_writing_style_sync.py
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"
WRITERS = {"write-article": ("长文", "article"), "write-tweet": ("推文", "tweet")}
FORMAT_SOURCE = SKILLS / "writing-style-learn" / "references" / "archive-format.md"
FORMAT_COPY = SKILLS / "writing-style-setup" / "references" / "archive-format.md"
CREATED_FILES = [
    "index.md",
    "style.md",
    "genres/article/default.md",
    "genres/tweet/default.md",
    "candidates.md",
]
STYLE_GROUPS = ["作者与读者", "口头习惯", "标点和排版", "讲事和解释", "禁用词表"]
DEFAULT_SECTIONS = ["语气", "结构", "讲事和解释", "排版", "固定表达", "类型", "范文"]
USAGE_SECTIONS = STYLE_GROUPS + ["结构", "排版", "固定表达"]
OLD_NAMES = ["voice.md", "samples.md", "pending.md", "archive.md", "待提炼", "体裁卡", "篇型", "术语表", "常用结构", "标题括号", "history.jsonl", "MUST", "SHOULD", "MAY"]

errors = []


def skill_text(skill):
    return (SKILLS / skill / "SKILL.md").read_text(encoding="utf-8")


def setup_usage():
    match = re.search(r"## 使用说明\n\n(.*?)\n```", skill_text("writing-style-setup"), re.S)
    if not match:
        errors.append("writing-style-setup: index.md template lacks「使用说明」")
        return None
    return match.group(1).strip()


def style_section(skill):
    match = re.search(r"^## 风格档案\n(.*?)(?=^## )", skill_text(skill), re.S | re.M)
    if not match:
        errors.append(f"{skill}: missing「风格档案」section")
        return ""
    return match.group(1)


def check_writers():
    normalized = {}
    for skill, (genre, folder) in WRITERS.items():
        section = style_section(skill)
        if f"genres/{folder}/" not in section:
            errors.append(f"{skill}:「风格档案」does not name genres/{folder}/")
        for name in ["index.md", "「使用说明」", "candidates.md"]:
            if name not in section:
                errors.append(f"{skill}:「风格档案」does not point to {name}")
        if "\n1. " in section:
            errors.append(f"{skill}:「风格档案」copies the usage steps; point to index.md instead")
        normalized[skill] = section.replace(genre, "<体裁>").replace(folder, "<目录>")
    article, tweet = normalized.values()
    if article != tweet:
        for i, (x, y) in enumerate(zip(article.splitlines(), tweet.splitlines()), 1):
            if x != y:
                errors.append(f"「风格档案」differs at line {i}:\n  write-article: {x}\n  write-tweet:   {y}")
                break
        else:
            errors.append("「风格档案」sections differ in length")


def check_setup():
    setup = skill_text("writing-style-setup")
    step3 = setup.split("## 3. 建档案", 1)[-1].split("## 4.", 1)[0]
    for name in CREATED_FILES:
        if name not in step3:
            errors.append(f"writing-style-setup: step 3 does not create {name}")
    if "references/archive-format.md" not in step3:
        errors.append("writing-style-setup: step 3 does not point to references/archive-format.md")


def check_format():
    for path in (FORMAT_SOURCE, FORMAT_COPY):
        if not path.exists():
            errors.append(f"{path.relative_to(ROOT)}: missing")
            return
    source = FORMAT_SOURCE.read_text(encoding="utf-8")
    if FORMAT_COPY.read_text(encoding="utf-8") != source:
        errors.append(
            f"{FORMAT_COPY.relative_to(ROOT)} differs from {FORMAT_SOURCE.relative_to(ROOT)}; "
            "edit the learn copy, then copy it to setup"
        )
    for name in STYLE_GROUPS + DEFAULT_SECTIONS + ["candidates.md"]:
        if f"## {name}" not in source:
            errors.append(f"archive-format.md: lacks「## {name}」")
    for name in USAGE_SECTIONS:
        if re.search(rf"^## {name}\n\n(?!用法：)", source, re.M):
            errors.append(f"archive-format.md:「## {name}」lacks a「用法：」line in a skeleton")


def check_learn():
    learn = skill_text("writing-style-learn")
    for name in ["references/archive-format.md", "candidates.md", "examples/"]:
        if name not in learn:
            errors.append(f"writing-style-learn: does not mention「{name}」")


def check_old_names():
    for skill in list(WRITERS) + ["writing-style-setup", "writing-style-learn"]:
        paths = [SKILLS / skill / "SKILL.md", *(SKILLS / skill).glob("references/*.md")]
        for path in paths:
            text = path.read_text(encoding="utf-8")
            for name in OLD_NAMES:
                if name in text:
                    errors.append(f"{path.relative_to(ROOT)}: still uses old name「{name}」")


usage = setup_usage()
if usage and "「用法」" not in usage:
    errors.append("writing-style-setup:「使用说明」does not point to the「用法」line of each section")
check_writers()
check_setup()
check_format()
check_learn()
check_old_names()

if errors:
    print("\n".join(errors))
    sys.exit(1)
print("writing style format in sync")
