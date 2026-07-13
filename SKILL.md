---
name: tex-manual-translation
description: 将 LaTeX 文档翻译为中文。当用户说"翻译 tex"、"翻译 LaTeX 手册"、"中文化手册"、"translate LaTeX to Chinese"、"把英文文档翻译成中文"时自动触发。
---

# 将英文 LaTeX 文档翻译为中文

目标：$1（若未提供，则询问用户要翻译哪个文件）

这是一项**由 AI 逐字执行的翻译任务**。逐段阅读英文原文，理解含义，用中文重新表达，通过逐行编辑写入译文。不得使用正则替换等自动化批量工具翻译正文，但可使用 `scripts/` 下的检查脚本辅助验证。

## 1. 范围与调查

仅翻译用户手册类的 `.tex` 文档文件。不要翻译宏包实现的源代码（`.sty`、`.ins`、脚本文件）。`.dtx` 文件同时包含实现代码和文档——仅翻译文档部分，绝不要改动宏定义代码。

**仅将待翻译的文件复制到项目根目录，其余文件保持只读。** 若后续发现缺少依赖文件，再将所需文件从原目录复制到根目录。

阅读目标 `.tex` 文件头部，记录引擎、`documentclass`、构建方式。用 `grep` 检索文档中使用的所有代码环境名称——这些环境内的内容一律不翻译。检查文档是否依赖外部文件或预生成的资源。

## 2. 搭建中文环境

1. 将 $1 复制到项目根目录，添加 `-zh` 后缀
2. 在 `\documentclass` 之后插入 `\usepackage{ctex}`（根据系统选择 `fontset`，依次尝试 `fandol`、`ubuntu`、`lxgw`）。检查 `.log` 中是否出现 `Missing character: There is no <glyph> in font` 警告，若有则切换至下一字体设置。检查西文与中文设置是否有冲突，若 `ctex` 在 Unicode 引擎下无法正常编译，改用 `xeCJK` 手动加载方案：`\usepackage{xeCJK}` + `\setCJKmainfont{}`
3. 编译**未翻译的中文版原文**，验证引擎 + CJK + 所有依赖能否共存。默认使用 `lualatex` 编译；若因 `TeX capacity exceeded` 或单次编译超时（>120s）失败，回退至 `xelatex`。`pdflatex` 不适用于 CJK，不作为回退选项
4. 若编译失败，逐个排查宏包冲突：添加一个临时方案，编译，验证，并在注释中标注原因

**关卡：未翻译的中文版能成功编译并生成 PDF。**

## 3. 术语表

为整篇文档创建术语映射表，存储为项目根目录下的 `glossary.md`，以确保全文一致性。判定规则与模板详见 [references/terminology.md](references/terminology.md)。

**保留英文**：工具名、宏包名、文件扩展名、命令名、键名、选项值、代码环境内容

**需翻译**：章节标题、正文段落、表格标题、描述性文字

## 4. 任务分解

使用 todo 工具按 `\chapter` / `\section` 创建任务列表。按顺序推进，每完成一章即标记为已完成。

## 5. 逐字翻译

逐章、逐段、逐句阅读**英文原文**，通过**逐行**编辑替换为**中文译文**。

### 翻译范围

仅翻译正文。语法命令（如 `\cmd{<args>}`）和代码注释维持英文原样。各类 LaTeX 元素（`\index{}`、`\href{}`、`\footnote{}`、`\caption{}` 等）的翻译规则详见 [references/latex-elements.md](references/latex-elements.md)。

### 术语一致性

严格遵循术语表。无对应中文翻译时，保留英文原样。专有名词首次翻译为中文时，以括号补充英文原文，例如「宏(macros)」。

### 标点与编辑规则

- 标点与混合中文标点规则：详见 [references/punctuation.md](references/punctuation.md)
- 编辑黄金法则与行号管理：详见 [references/editing-rules.md](references/editing-rules.md)

## 6. 编译验证

每完成一章后编译一次。编译时**禁止**使用 `--shell-escape`。遇到编译报错时立即停止，逐一排查后方可继续。

若编译失败：

1. 对照英文原文，检查是否丢失了环境标记
2. 运行 `python scripts/check_env_balance.py <file.tex>` 检查 `\begin{X}` / `\end{X}` 配对
3. 若不平衡，根据脚本输出的行号手动恢复缺失的标记
4. 运行 `python scripts/find_backslash_before_cjk.py <file.tex>` 扫描中文标点前的 `\`，删除控制空格反斜杠
5. 运行 `python scripts/find_untranslated.py <file.tex>` 检测疑似遗漏的未翻译段落

完整构建遵循文档原有的编译流程（通常需要多次运行及索引工具）。首次编译出现未定义引用警告属正常现象。若编译失败，**重试前先删除中间文件**。

如果编译仍然报错，全局分析 LaTeX 问题并尝试修复。

## 7. 大文档并行化

按 `\chapter{}` 或 `\section{}` 名称拆分给子代理，每个子代理逐字翻译各自负责的小节。随着上游翻译的推进，行号会不断漂移——子代理必须通过搜索小节标题来定位自己的部分，而非依赖行号。

各子代理应共享同一份 `glossary.md` 术语表以保持翻译一致性。
