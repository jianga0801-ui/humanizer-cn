#!/usr/bin/env python3
"""检查 humanizer-cn 的打包文件是否自洽，无外部依赖。"""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


def read_package_file(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError as error:
        raise SystemExit(f"无法读取 {path.relative_to(ROOT)}：{error}")


SKILL_PATH = ROOT / "SKILL.md"
SKILL = read_package_file(SKILL_PATH)
README = read_package_file(ROOT / "README.md")
try:
    PLUGIN = json.loads(read_package_file(ROOT / ".claude-plugin" / "plugin.json"))
except json.JSONDecodeError as error:
    raise SystemExit(f"修正 .claude-plugin/plugin.json 里的 JSON：{error}")


def require_match(match: "re.Match[str] | None", message: str) -> "re.Match[str]":
    if match is None:
        raise SystemExit(message)
    return match


# 1. YAML 元数据必须存在
yaml_metadata = require_match(
    re.match(r"\A---\n(.*?)\n---\n", SKILL, re.DOTALL),
    "SKILL.md 必须以 YAML 元数据开头",
).group(1)

# 2. cn 保留 allowed-tools（与英文 humanizer 相反），必须声明
if not re.search(r"(?m)^allowed-tools:", yaml_metadata):
    raise SystemExit("SKILL.md 的 YAML 里缺少 allowed-tools 声明")

# 3. 三处版本号必须一致：SKILL metadata.version / README 首条 / plugin.json
skill_version = require_match(
    re.search(r'(?m)^\s+version:\s*["\']?([0-9]+\.[0-9]+\.[0-9]+)["\']?\s*$', yaml_metadata),
    "在 SKILL.md 的 metadata.version 写一个三段式版本号",
).group(1)
readme_version = require_match(
    re.search(r"(?m)^- \*\*([0-9]+\.[0-9]+\.[0-9]+)\*\*", README),
    "在 README.md 的版本历史里加一条版本记录",
).group(1)
package_versions = {skill_version, readme_version, str(PLUGIN.get("version", ""))}
if len(package_versions) != 1:
    raise SystemExit(f"三个文件里的版本号必须一致：{sorted(package_versions)}")

# 4. 根目录只能有一个常规 SKILL.md
skill_files = {path.relative_to(ROOT) for path in ROOT.rglob("SKILL.md")}
if SKILL_PATH.is_symlink() or skill_files != {Path("SKILL.md")}:
    raise SystemExit("根目录只能保留一个常规的 SKILL.md")
if PLUGIN.get("skills") != ["./"]:
    raise SystemExit("Claude 插件的 skill 加载路径必须指向仓库根目录 ./")

# 5. 模式必须从 1 连续编号、无缺口（cn 用 #### 作为模式标题）
pattern_numbers = [int(n) for n in re.findall(r"(?m)^#### ([0-9]+)\. ", SKILL)]
pattern_count = len(pattern_numbers)
if pattern_count == 0 or pattern_numbers != list(range(1, pattern_count + 1)):
    raise SystemExit(f"SKILL.md 的模式必须从 1 连续编号、无缺口：{pattern_numbers}")

# 6. 反编造铁律必须在场（这是 cn 的核心修复，不能被人误删）
if "不编造" not in SKILL:
    raise SystemExit("SKILL.md 丢失了'不编造'铁律，这是本 skill 的核心，禁止删除")

print(f"humanizer-cn v{skill_version} 打包校验通过（{pattern_count} 个模式）")
