# 标点与混合规则

## 全角与半角

- **正文**：全角标点（`，` `。` `：` `；`）
- **代码/命令周围**：半角括号
- 用 `……` 代替 `\ldots`

## LaTeX 混合中文标点规则

绝不要在中文标点前保留英文式的控制空格反斜杠。

### 错误写法

```latex
\LaTeX\，
\locations\。
\indexed\（见下文）
```

### 正确写法

```latex
\LaTeX，
\locations。
\indexed（见下文）
```

### 原因

`\LaTeX\，` 会被解析为未定义的控制序列 `\，`，引发连锁的 `Undefined control sequence` 错误。

若一行以 `\command\` 结尾而下一行以中文标点开头，跨行时也会出现同样的错误。

### 自动检测

```bash
python scripts/find_backslash_before_cjk.py <file.tex>
```

输出所有中文标点前带有 `\` 的行号，直接定位修复。
