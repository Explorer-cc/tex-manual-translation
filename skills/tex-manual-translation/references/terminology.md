# 术语判定规则

## 保留英文（不翻译）

以下内容维持英文原样：

- 工具名（如 `latexmk`、`biber`）
- 宏包名（如 `ctex`、`hyperref`）
- 文件扩展名（如 `.tex`、`.sty`）
- 命令名（如 `\documentclass`、`\usepackage`）
- 键名与选项值（如 `fontset=fandol`）
- 代码环境内的所有内容

## 需翻译

- 章节标题文本
- 正文段落
- 表格标题（`\caption` 的长文本部分）
- 描述性文字

## 专有名词首次出现格式

翻译为中文后，以括号补充英文原文：

```
宏(macros)
环境(environments)
浮动体(floats)
```

若找不到合适的中文翻译，保留英文原样。

## 术语表模板

为整篇文档创建术语映射表，存储为项目根目录下的 `glossary.md`：

| 英文 | 中文 | 备注 |
|---|---|---|
| macro | 宏 | 首次出现写「宏(macros)」 |
| environment | 环境 | |
| float | 浮动体 | |
| preamble | 导言区 | |
| counter | 计数器 | |
| box | 盒子 | |

翻译过程中持续维护此表，确保全文一致。子代理共享同一份 `glossary.md`。
