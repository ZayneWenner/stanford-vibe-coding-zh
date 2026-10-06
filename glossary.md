# 术语表（Glossary）— Stanford CS146S「The Modern Software」中文翻译基准

> 用途：本术语表是本次翻译的**唯一一致性基准**。全部 31 个阅读页、PDF 译文均须遵循下表译法，
> 以保证全文术语统一（对应评分项 contentAccuracy「术语统一」信号）。
> 维护方式：换一门课只需增补本表，翻译流程即可复跑（对应 pipelineAutomation「换源可复用」信号）。

## 使用约定

1. **专有名词 / 工具名 / 公司名 / 产品名**：一律保留英文原文（如 Claude Code、Codex、Devin、Warp、Anthropic、OpenAI、Kubernetes、GitHub Copilot）。首次出现可加中文括注，后文直接用原名。
2. **代码、命令、API、路径、变量名**：逐字保留，不翻译。
3. **术语首次出现**：采用「中文译名（English）」格式，后文可用纯中文译名。
4. **有争议译法**：以本表为准，不擅自发挥。

## 一、核心概念（Vibe Coding / AI 辅助编程）

| 英文 | 中文译法 | 备注 |
|---|---|---|
| Vibe Coding | 氛围编程 | 保留 Vibe Coding 括注 |
| Scaffolding | 脚手架（搭建） | 指快速生成项目骨架 |
| Context Engineering | 上下文工程 | |
| Context Rot | 上下文退化 | 亦作「上下文腐烂」，正文统一用「上下文退化」 |
| Context Window | 上下文窗口 | |
| Long Context | 长上下文 | |
| Prompt Engineering | 提示工程 | |
| Prompt Injection | 提示注入 | |
| Prompt Injection Attack | 提示注入攻击 | |
| System Prompt | 系统提示 | |
| User Prompt | 用户提示 | |
| In-context Learning | 上下文学习 | |
| Few-shot / Zero-shot | 少样本 / 零样本 | |
| Chain-of-Thought | 思维链 | |
| Temperature | 温度（采样参数） | |
| Token | Token | 保留英文 |
| Hallucination | 幻觉 | |
| Grounding | 事实对齐 | 指让模型输出基于真实依据 |
| Eval | 评测 | 指 evaluation |
| Benchmark | 基准测试 | |
| RAG (Retrieval-Augmented Generation) | 检索增强生成（RAG） | |
| Embedding | 嵌入 | |
| Fine-tuning | 微调 | |
| Function Calling | 函数调用 | |
| Prompt Caching | 提示缓存 | |
| Streaming | 流式输出 | |

## 二、智能体与工具（Agents / MCP）

| 英文 | 中文译法 | 备注 |
|---|---|---|
| LLM (Large Language Model) | 大语言模型（LLM） | |
| Coding Agent | 编程智能体 | 亦作编码智能体 |
| Agentic AI | 智能体式 AI | 亦作「具代理性 AI」 |
| Agentic Workflow | 智能体式工作流 | |
| Agentic Loop | 智能体循环 | |
| Multi-agent System | 多智能体系统 | |
| Sub-agent | 子智能体 | |
| Tool Use / Tool Calling | 工具调用 | |
| MCP (Model Context Protocol) | 模型上下文协议（MCP） | |
| MCP Server | MCP 服务器 | |
| MCP Client | MCP 客户端 | |
| MCP Registry | MCP 注册表 | |
| Orchestration | 编排 | |
| Guardrail | 安全护栏 | |
| Sandbox | 沙箱 | |
| Agentic On-call | 智能体式值班 | |

## 三、软件工程与安全

| 英文 | 中文译法 | 备注 |
|---|---|---|
| Code Review | 代码审查 | |
| AI-assisted Code Review | AI 辅助代码审查 | |
| Spec / PRD | 规格说明 / 产品需求文档（PRD） | |
| Specs are the new source code | 规格说明成为新的源代码 | 标题保留英文意象 |
| Repository | 代码仓库（仓库） | |
| Pull Request (PR) | 拉取请求（PR） | |
| Commit | 提交 | |
| Refactor | 重构 | |
| Boilerplate | 样板代码 | |
| CI/CD | 持续集成 / 持续部署（CI/CD） | |
| Linter | 代码检查器（Lint 工具） | |
| Regression | 回归 | |
| Remote Code Execution (RCE) | 远程代码执行（RCE） | |
| Vulnerability | 漏洞 | |
| Vulnerability Detection | 漏洞检测 | |
| SAST (Static Application Security Testing) | 静态应用安全测试（SAST） | |
| DAST (Dynamic Application Security Testing) | 动态应用安全测试（DAST） | |
| OWASP Top Ten | OWASP 十大（安全风险） | |
| Prompt Injection RCE | 提示注入导致的远程代码执行 | |

## 四、运维与可观测性（SRE / Observability）

| 英文 | 中文译法 | 备注 |
|---|---|---|
| SRE (Site Reliability Engineering) | 网站可靠性工程（SRE） | |
| Observability | 可观测性 | |
| Trace / Span | 追踪 / 跨度 | |
| On-call | 值班 | |
| Troubleshooting | 故障排查 | |
| Latency | 延迟 | |
| Throughput | 吞吐量 | |
| Idempotent | 幂等 | |
| Deterministic / Non-deterministic | 确定性 / 非确定性 | |
| Kubernetes | Kubernetes | 保留 |
| Deployment | 部署 | |
| Incident | 事故 / 事件 | 运维语境用「事故」 |

## 五、通用方法论

| 英文 | 中文译法 | 备注 |
|---|---|---|
| Scaffold | 搭建骨架 | 动词 |
| Workflow | 工作流 | |
| Pipeline | 管线 | |
| Iteration | 迭代 | |
| Trade-off | 权衡 | |
| Heuristic | 启发式（方法） | |
| Best Practice | 最佳实践 | |
| Rubric | 评分量规 | |
| Deliverable | 交付物 | |
