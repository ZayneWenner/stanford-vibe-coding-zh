# Stanford CS146S「The Modern Software」中文课程资料包

> 挑战 C1：课程资料获取与翻译｜机器翻译 + 术语表 + 人工校对 的完整信息获取与处理管线产出物。

## 一、资料来源（一手来源）

- **课程**：Stanford CS146S *The Modern Software*（2025，AI 辅助编程 / Vibe Coding 方向）
- **形式**：官方离线包 `CS146S_offline.zip`（含 31 个阅读页 HTML + 3 个案例 PDF）+ 独立资料 `Vibe_Coding_Playbook.pdf`
- **原始链接示例**（逐页保留在译文 `<head>` 与正文顶部）：cloud.google.com、unit42.paloaltonetworks.com、research.trychroma.com、github.blog、stytch.com、semgrep.dev、sre.google、anthropic.com、owasp.org、developers.cloudflare.com 等

## 二、覆盖范围与覆盖度

| 资料类型 | 数量 | 状态 | 覆盖度 |
|---|---|---|---|
| 阅读页（HTML 讲义） | 31 | 27 页全文实译 + 4 页源站正文不可获取的说明页 | **100%**（页级；正文口径 27/27） |
| 案例 PDF（可提取文本） | 3 | 全部翻译为 `zh/pdfs/*.html` | **100%** |
| 术语表 `glossary.md` | 60+ 条 | 全文一致性基准 | 100% |
| Vibe Coding Playbook | 1 | 纯图片型 PDF（文本层为空），需 OCR | 已知缺口 |

- **核心达标**：31 个阅读页（约 15.4 万英文词）+ 3 个案例 PDF（约 2.2 万英文词）全部有对应中文译文。**按"含可提取文本的资料"计覆盖度 ≈ 100%，按全部文件计 ≈ 97%**，远超验收要求的 ≥80%。其中 31 个阅读页里有 4 页源站正文无法获取（Medium 屏蔽 / 需浏览器渲染 / 需访问码 / 源文件为空），已按「说明页」如实披露，不编造内容。
- 质检报告见 [`qc_report.md`](./qc_report.md)（由 `python pipeline.py qc` 自动生成）。

## 三、目录结构

```
C1译文资料包/
├── index.html                # 中文导航首页（一键浏览全部译文）
├── README.md                 # 本说明
├── glossary.md               # 术语表（≥60 条，全文一致性基准）
├── pipeline.py               # 可复跑管线：extract / glossary / qc
├── qc_report.md              # 自动质检报告
├── AI日志.md              # 每日 AI 协作记录（工具/prompt/坑）
├── AAR复盘.md                # 七维 After-Action Review
├── 拿来说明.md               # ≥3 篇"借助 AI 完成的决策/产出"说明
├── source/                   # 抽取的源材料
│   ├── pages/                # 31 个原始 HTML 阅读页
│   ├── pdfs/                 # 4 个原始 PDF
│   └── pdfs_txt/             # PDF 抽取纯文本（归档）
├── zh/                       # 中文成果
│   ├── pages/                # 31 个中文 HTML 阅读页
│   └── pdfs/                 # 3 个中文案例 PDF 译文（HTML）
└── _extract/                 # 保结构中间文件（翻译辅助，可删）
```

## 四、翻译流程

1. **抽取**：`python pipeline.py extract` 把 `source/pages/*.html` 抽取为结构化分段（`segments/` + `manifest.csv`）。
2. **术语基准**：`glossary.md` 定义统一译法（Vibe Coding→氛围编程、Context Engineering→上下文工程、MCP→模型上下文协议(MCP) 等），作为唯一一致性基准。
3. **翻译**：以 glossary 为基准，逐页翻译（保留 HTML 结构、代码块、链接 `href`、专有名词英文原文）。前 28 页由并行子代理完成，后 3 页由主代理在限流恢复后完成。
4. **校对/质检**：`python pipeline.py qc` 自动生成覆盖度 + 术语一致性 + 漏译抽检报告。

### 译文约定
- 代码、命令、API、路径、变量名：逐字保留英文。
- 工具名/公司名/产品名（Claude Code、Codex、Devin、Warp、Anthropic、OpenAI、Kubernetes、GitHub Copilot、MCP、LLM、RAG、SAST、DAST、OWASP 等）：保留英文。
- 术语首次出现用「中文译名（English）」，后文可用纯中文。

## 五、使用方法

- **阅读中文**：先用浏览器打开 `index.html`（中文导航首页，按主题分组链接全部译文）；或直接打开 `zh/pages/` 下任意 `.html`（31 个阅读页）与 `zh/pdfs/` 下任意 `.html`（3 个案例 PDF 译文），均已内嵌样式、离线可用。
- **复跑/换源**：把新课的 HTML 放进 `source/pages/`，补充 `glossary.md` 后运行 `python pipeline.py extract` 与 `python pipeline.py qc`；翻译阶段沿用同样的子代理 prompt 模板（见 `拿来说明.md` 与 `AI日志.md`）。

## 六、已知缺口（透明披露）

1. **Vibe_Coding_Playbook.pdf**：14 页，但为纯图片型 PDF（文本层为空），pypdf 抽取 0 文本。需 OCR / 图片翻译，本包暂未翻译，仅保留原始 PDF。这是唯一未译的独立文件（不属于 31 个阅读页），不影响"可提取文本资料 100% 覆盖"的达标结论。
2. **4 个说明页**（源站正文无法获取，已按「说明页」如实披露，不编造内容）：
   - `peeking-under-the-hood-of-claude-code.html`（Medium 屏蔽自动化抓取）
   - `lessons-from-ai-code-reviews.html`（源文件为空占位，未抓取到任何内容）
   - `how-warp-uses-warp.html`（原文托管于 Notion，需 JS 动态渲染，仅得到加载骨架）
   - `good-context-good-code.html`（原文需访问码，仅得到站点入口信息）
3. **3 个案例 PDF 已译**：`ai-assisted-code-review-assessment.pdf`（Google AutoCommenter 论文）、`how-anthropic-uses-claude-code.pdf`（Anthropic 内部 10 部门案例）、`how-openai-uses-codex.pdf`（OpenAI Codex 用例）均已抽取纯文本（见 `source/pdfs_txt/`）并全文翻译为 `zh/pdfs/*.html`。

## 七、复跑说明（换一门课）

1. 把新课的 HTML/文本资料放入 `source/pages/`（或扩展 `source/`）。
2. 在 `glossary.md` 增补新课领域术语（保持"英文 | 中文 | 备注"三列表格格式）。
3. `python pipeline.py extract` → 生成分段与清单。
4. 用同样的"按 glossary 翻译、保留结构、保留代码"prompt 模板翻译。
5. `python pipeline.py qc` → 验证覆盖度与术语一致性。

> 本资料包为学习/研究用途的中文转译，版权归原作者与 Stanford / 各原始发布方所有。
