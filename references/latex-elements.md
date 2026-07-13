# LaTeX 元素翻译规则

## `\index{}` 索引条目

保留英文原文。如需中文索引，另建独立索引体系，不修改原 `\index{}` 条目。

## `\href{url}{显示文本}`

- URL 不翻译
- 显示文本按正文翻译

## `\footnote{}`

按正文翻译，标点规则同正文。

## `\texttt{}` / `\verb||`

一律不翻译，视为代码。

## `\caption{}`

- 短标签形式 `\caption[short]{long}`：`short` 不翻译（用于目录和列表），`long` 翻译
- 无短标签 `\caption{text}`：`text` 翻译

## `\section{}` / `\chapter{}` 等标题

标题文本翻译。若使用 `\texorpdfstring{PDF文本}{书签文本}`，两部分均需翻译为中文。

## BibTeX 条目

- `title` 字段：可翻译，原文保留于 `note` 字段
- 其余字段（`author`、`journal`、`year` 等）：不翻译

## `\label{}` / `\ref{}` / `\eqref{}`

标签名不翻译。引用编号由 LaTeX 自动生成，无需处理。

## `\cmd{<args>}` 语法占位符

命令语法中的占位符（如 `<args>`、`<key>`）不翻译，维持英文原样。

## 代码注释

LaTeX 源代码中的注释（`%` 开头）不翻译，维持原样。
