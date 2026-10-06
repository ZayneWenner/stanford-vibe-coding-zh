# AI 协作日志（AI 日志）

> 记录本次 C1 挑战中"人 + AI"协作的全过程：用了什么工具、什么 prompt、踩了什么坑、怎么解决。
> 时间跨度：2026-10-06（单日集中攻坚）。

---

## 阶段 0｜摸清材料与范围

**目标**：确认挑战要求与源材料规模，避免盲目开工。
**动作**：
- 读取 `CHALLENGE.md` / `rubric.json` / `challenge.yaml` / `README.md` / `materials/`。
- 用 Python 解析 `CS146S_offline.zip`：31 个 HTML 阅读页 + 3 个案例 PDF；外加独立 `Vibe_Coding_Playbook.pdf`。
- 统计阅读页正文约 15.4 万英文词（注意：首次从 zip 直接读偏低，以磁盘为准）。

**坑**：
- 首次用 Bash 的 `unzip -l`、PowerShell 的 `Shell.Application` COM 对象在 Windows 沙箱里都不好用 → 改用 Python `zipfile` 模块，稳定可靠。
- 词数统计两次不一致（zip 内读 8 万 vs 磁盘 15.4 万）→ 以"抽取到磁盘后的真实文件"为准，避免报告写错数字。

**启发**：任何"规模数字"都要从最终处理的真实文件复核，不要信中间产物。

---

## 阶段 1｜搭建管线与抽取

**工具**：Python `zipfile` + `re`（自写 `pipeline.py`）。
**关键 prompt（抽取思路，给自己）**：
> 抽取 HTML 正文时：去 `<script>/<style>`，块级标签换换行，`<[^>]+>` 去标签，保留链接 `href` 与代码；统计英文词数。

**产出**：`pipeline.py`（子命令 `extract` / `glossary` / `qc`）、`source/pages/`、`source/pdfs/`、`source/pdfs_txt/`。

**坑**：
- 临时文件 `_specs_body.html` 误入 `source/pages/` → 清理后重算缺失清单，避免污染覆盖率统计。
- `pipeline.py` 的 `glossary` 强制替换命令是为"原始机翻稿"设计的（会把 `LLM` 等整体替换），**不能**直接跑在我手工校对的成品页上 → 成品页的术语一致性靠"翻译时遵循 glossary"保证，而非事后强替。

---

## 阶段 2｜构建术语表（60+ 条）

**方法**：先让 AI 基于 Vibe Coding / AI 辅助编程领域草拟一份术语表草案（英文 | 中文 | 备注），再人工确认译法、补充分组与约定。
**关键决策**（见 `拿来说明.md` 第 1 篇）：
- Vibe Coding → **氛围编程**（保留英文括注）
- Context Engineering → **上下文工程**；Context Rot → **上下文退化**
- MCP → **模型上下文协议（MCP）**；Code Review → **代码审查**
- 规则：代码/命令/API/路径/变量名逐字保留；工具名/公司名保留英文。

**价值**：术语表成为后续 31 页翻译的"唯一一致性基准"，也是换课复跑时唯一需要改动的配置。

---

## 阶段 3｜并行翻译 31 页（前 28 页）

**工具**：9 个并行子代理（Agent），按术语表翻译、保留结构与代码、专有名词保留英文。
**关键 prompt 模板**（每个子代理）：
> 你是 CS146S 课程中文翻译员。先读 `glossary.md` 作为唯一术语基准；翻译指定 HTML 为干净中文 HTML，保留 h1-h6/段落/列表/表格/引用/链接(href 保留)、代码块与行内代码逐字保留英文；专有名词保留英文；输出自包含 HTML5（内嵌样式）；正文顶部加来源说明。忠实完整，不删减。

**分批**：
- A：prompt-engineering-overview（大页）
- B：agentic-ai-threats + context-rot
- C：how-to-review-code-effectively + mcp-introduction + finding-vulnerabilities-claude-codex
- D：sre + writing-tools + devin
- E：sast + owasp + mcp-auth + specs
- F：multi-agent + ai-review + code-review-essentials + observability
- G：claude-code + long-context + kubernetes + copilot-rce
- H：code-reviews + benefits-oncall + mcp-food + mcp-registry
- I：warp + prompt-guide + good-context + how-warp + peeking + lessons（小页/占位）

**坑（重要）**：
- 部分子代理因后端网络抖动返回 502（copilot.tencent.com 不可达）→ 实际未丢失，重算发现 28 页已产出，仅 3 页缺失。
- 重试时触发 **429 频率限制**（重置时间 2026-10-06 22:09 UTC+8）→ 子代理通道被限流。

**对策**：暂停子代理，改为"主代理直接翻译"补齐缺失 3 页；限流恢复后再视情况补跑。

---

## 阶段 4｜补齐缺失 3 页（主代理直译）

**工具**：主代理 + Python 保结构抽取（`_extract/*.md`：标题/链接/代码块/列表标记化）。
**动作**：逐页读中间文件 → 译为中文 HTML → 写 `zh/pages/`。
- `specs-are-the-new-source-code.html`（Substack 博文，丢弃评论/页脚噪声）
- `mcp-server-authentication.html`（Cloudflare 文档，26 个代码块全部保留）
- `finding-vulnerabilities-claude-codex.html`（Semgrep 研究，2 张结果表 + 命令 + 附录 prompt 保留）

**坑**：源 HTML 编码有 mojibake（Â、â€" 等）→ 在译文中直接清理，不带入成品。

---

## 阶段 5｜PDF 处理

**工具**：`pypdf`（装在受管 venv `python/envs/default`）抽取文本。
**发现**：
- `Vibe_Coding_Playbook.pdf`：14 页，**0 文本**（纯图片型）→ 列为已知缺口，需 OCR。
- 3 个案例 PDF 文本可提取（2k–10.6k 词），已归档到 `source/pdfs_txt/`，中文译文补齐中。

**坑**：基础 Python 没有 pypdf → 必须调用 venv 的 `python.exe`（`.../envs/default/Scripts/python.exe`），否则 `import pypdf` 失败。

---

## 阶段 6｜质检与交付

**工具**：`python pipeline.py qc` → `qc_report.md`。
**结果**：覆盖度 100%；"可见英文词"告警均为刻意保留的专有名词/工具名（符合术语表约定），非漏译。
**产出交付文档**：`README.md`、`AI日志.md`、`AAR复盘.md`、`拿来说明.md`、`glossary.md`、`pipeline.py`、`qc_report.md` + 31 个中文页。

---

## 经验速记（给下次）

1. Windows 沙箱里优先用 Python（zipfile/re）而非 shell 的 unzip/PowerShell COM。
2. 规模数字从"最终磁盘文件"复核，别信中间统计。
3. 翻译类并行任务：子代理便宜但需要限流兜底方案（主代理直译）。
4. 术语表前置，是全文一致 + 换源复跑的关键资产。
5. 图片型 PDF 提前识别，避免在"抽不到文本"上浪费时间，尽早列为缺口。
