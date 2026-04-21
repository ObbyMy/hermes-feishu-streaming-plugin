# Hermes Feishu Streaming Skill Kit

> A transferable skill repository for the **OpenClaw-style optimized Feishu streaming card workflow** in Hermes Agent.
>
> 一个可迁移的技能仓库，用于把 **OpenClaw 风格优化后的飞书流式卡片消息方案** 迁移到其他 Hermes Agent 实例。

<p align="center">
  <a href="#中文说明">中文</a> ·
  <a href="#english">English</a>
</p>

---

# 中文说明

## 快速跳转

- [项目定位](#项目定位)
- [这个仓库解决什么问题](#这个仓库解决什么问题)
- [我到底改了 Hermes 哪些源码](#我到底改了-hermes-哪些源码)
- [如何在 Hermes 更新后重新定位这些修改点](#如何在-hermes-更新后重新定位这些修改点)
- [仓库结构](#仓库结构)
- [命令行用法](#命令行用法)
- [典型迁移流程](#典型迁移流程)
- [验证方式](#验证方式)
- [打包与发布](#打包与发布)

## 项目定位

这不是“一个普通插件示例仓库”，而是一个**可交付、可迁移、可复用的技能仓库**。

它把我在 Hermes Agent 中为飞书 / 微信网关做过的这套关键优化完整沉淀下来：

1. **飞书单卡片流式输出**：避免“小预览气泡 + 工具进度消息 + 最终消息”分裂成多条杂乱消息。  
2. **工具进度嵌入当前流式卡片**：工具调用状态直接显示在当前消息卡片里。  
3. **Weixin 重复气泡抑制**：在不支持真正编辑的通道上关闭重复预览/进度气泡。  
4. **session/context 通知卡片化**：把 session reset / context pressure 等提示也纳入统一风格。  
5. **升级可定位**：不仅保存改后的文件，还提供“以后 Hermes 升级了该去哪里改”的定位清单和 CLI。  

## 这个仓库解决什么问题

如果你只是拷贝一份补丁，短期能用；但一旦上游 Hermes 更新：

- 你会忘记到底改过哪些文件；
- 你会忘记为什么要这么改；
- 你会不知道新版源码里应该去哪里续改；
- 你会很难把同一套体验稳定复用到其他实例。

这个仓库就是为了解决这些问题：

- **资产化**：把源码修改、测试、文档、补丁、技能说明统一封装；
- **可迁移**：可以导出 bundle，交给别的 Hermes 实例直接复用；
- **可定位**：通过 `locators` / `locate` 命令快速定位新版 Hermes 中的改动触点；
- **可审计**：清楚记录“改了什么”“为什么改”“怎么验证”。

## 我到底改了 Hermes 哪些源码

核心改动集中在下面这些文件：

- `gateway/platforms/feishu.py`
- `gateway/run.py`
- `gateway/stream_consumer.py`
- `gateway/config.py`
- `gateway/display_config.py`
- `hermes_cli/gateway.py`
- 对应的 `tests/gateway/*`、`tests/run_agent/*`、`tests/agent/*`

详细说明见：

- `references/modified-files.md`
- `references/upgrade-locator.md`
- `references/modification-map.json`

其中最关键的三处是：

### 1) `gateway/platforms/feishu.py`

这里决定飞书消息到底怎么发、怎么编辑、什么时候走 interactive card、失败时怎样 fallback。

这部分修改主要负责：

- 打开 Feishu 的消息编辑能力；
- 引入 `_hermes_stream` metadata 协议；
- 让流式消息优先走单卡片路径；
- 让 metadata-only 更新也能触发 edit；
- 处理 interactive card 失败回退；
- 保证附件+说明走“先文本后文件”的发送策略。

### 2) `gateway/run.py`

这里负责把 agent commentary / stream delta / tool progress 真正接到平台发送逻辑上。

这部分修改主要负责：

- 定义 tool progress 的传输模式：`embedded` / `standalone` / `off`；
- 在 Feishu 上把工具进度嵌入当前 stream card；
- 在 Weixin 上关闭会造成重复气泡的路径；
- 给 session notice / context pressure 注入 Feishu 所需 metadata。

### 3) `gateway/stream_consumer.py`

这里负责“一个正在流式更新的消息”在运行期如何增量刷新。

这部分修改主要负责：

- 支持 `on_status()` 的临时状态刷新；
- 支持 **只有 metadata 变化也要触发 edit**；
- 支持 `\u200b` placeholder 让 status-only flush 生效；
- 支持 paragraph boundary / inline commentary；
- 避免对 placeholder 错误追加流式光标。

## 如何在 Hermes 更新后重新定位这些修改点

这是这个仓库和“普通补丁仓库”最大的区别之一。

### 方法一：查看定位清单

```bash
python -m hermes_feishu_streaming_plugin locators
```

这个命令会输出 JSON，列出每个目标文件、用途、以及应该搜索的稳定锚点，比如：

- `class FeishuAdapter(BasePlatformAdapter):`
- `async def send(`
- `async def edit_message(`
- `progress_transport`
- `GatewayStreamConsumer(`
- `_STATUS_ONLY_PLACEHOLDER = "\u200b"`

### 方法二：直接扫描目标 Hermes 仓库

```bash
python -m hermes_feishu_streaming_plugin locate --target /path/to/hermes-agent
```

它会返回：

- 哪些文件存在；
- 哪些文件是完整匹配；
- 哪些文件只匹配到一部分锚点；
- 每个锚点在哪一行出现。

这对下面两种情况尤其有用：

1. **上游升级后文件还在，但行号变了**；
2. **上游重构后只能找到部分结构，需要手工续改**。

### 方法三：结合 bundle 内文档手工续改

优先顺序建议：

1. 先跑 `locate`
2. 再看 `references/modified-files.md`
3. 再对照 `references/migration.patch`
4. 最后用 `files/` 目录里的目标文件作为参考真值

## 仓库结构

```text
hermes-feishu-streaming-plugin/
├── README.md
├── pyproject.toml
├── src/hermes_feishu_streaming_plugin/
│   ├── __init__.py
│   ├── __main__.py
│   ├── bundle.py
│   ├── cli.py
│   ├── installer.py
│   ├── locator.py
│   └── assets/
│       └── hermes-feishu-weixin-streaming-migration-kit/
│           ├── SKILL.md
│           ├── README.md
│           ├── files/
│           └── references/
│               ├── modified-files.md
│               ├── upgrade-locator.md
│               ├── modification-map.json
│               ├── migration.patch
│               ├── migration-steps.md
│               ├── verification.md
│               └── feishu-format-calls.md
├── tests/
└── .github/workflows/ci.yml
```

## 命令行用法

### 安装

```bash
pip install -e .[dev]
```

### 查看 bundle 文件清单

```bash
python -m hermes_feishu_streaming_plugin manifest
```

### 导出完整迁移包

```bash
python -m hermes_feishu_streaming_plugin export --output-dir ./dist
```

### 输出“升级定位清单”

```bash
python -m hermes_feishu_streaming_plugin locators
```

### 扫描目标 Hermes 仓库中的改动触点

```bash
python -m hermes_feishu_streaming_plugin locate --target /path/to/hermes-agent
```

### 应用 bundle 内置文件

```bash
python -m hermes_feishu_streaming_plugin apply --target /path/to/hermes-agent
```

### 先 dry-run 再复制

```bash
python -m hermes_feishu_streaming_plugin apply --target /path/to/hermes-agent --dry-run
```

## 典型迁移流程

```bash
# 1) 查看本仓库内置的 bundle 结构
python -m hermes_feishu_streaming_plugin manifest

# 2) 扫描目标 Hermes 仓库，确认改动触点还在不在
python -m hermes_feishu_streaming_plugin locate --target /path/to/hermes-agent

# 3) 导出 bundle，便于审阅或打包发给别人
python -m hermes_feishu_streaming_plugin export --output-dir ./dist

# 4) 先演练复制计划
python -m hermes_feishu_streaming_plugin apply --target /path/to/hermes-agent --dry-run

# 5) 正式应用
python -m hermes_feishu_streaming_plugin apply --target /path/to/hermes-agent
```

## 验证方式

仓库内已经保存了聚焦回归验证命令，见：

- `references/verification.md`

本项目自身的测试：

```bash
pytest
```

构建发行包：

```bash
python -m build
```

## 打包与发布

这个仓库适合直接作为“技能仓库”发布，因为它同时包含：

- 技能说明 `SKILL.md`
- 可迁移文件 `files/`
- 修改说明 `references/modified-files.md`
- 升级定位清单 `references/upgrade-locator.md`
- 机器可读定位图 `references/modification-map.json`
- CLI 工具 `locate / locators / export / apply`

---

# English

## Quick Links

- [Project Goal](#project-goal)
- [What Problem This Repo Solves](#what-problem-this-repo-solves)
- [Which Hermes Source Files Were Actually Changed](#which-hermes-source-files-were-actually-changed)
- [How to Re-locate the Touchpoints After Hermes Updates](#how-to-re-locate-the-touchpoints-after-hermes-updates)
- [Repository Layout](#repository-layout)
- [CLI Usage](#cli-usage)
- [Typical Migration Workflow](#typical-migration-workflow)
- [Verification](#verification)
- [Packaging and Publishing](#packaging-and-publishing)

## Project Goal

This is not just a patch dump.

It is a **transferable skill repository** that packages the OpenClaw-style optimized Feishu streaming-card workflow for Hermes Agent, including:

- the modified source files,
- the migration patch,
- the supporting tests,
- the operational documentation,
- and a locator CLI for future upstream upgrades.

## What Problem This Repo Solves

A one-off patch is never enough once Hermes evolves.

Without a structured migration repository, you quickly lose track of:

- which files were changed,
- why those changes existed,
- where to re-apply the logic after upstream refactors,
- and how to verify that the UX still behaves correctly.

This repository solves that by turning the work into a reusable artifact:

- **portable** — exportable and shareable across Hermes instances;
- **inspectable** — documents the exact source touchpoints and intent;
- **upgradable** — ships locator specs for future Hermes versions;
- **testable** — keeps the regression scope visible.

## Which Hermes Source Files Were Actually Changed

Primary source touchpoints:

- `gateway/platforms/feishu.py`
- `gateway/run.py`
- `gateway/stream_consumer.py`
- `gateway/config.py`
- `gateway/display_config.py`
- `hermes_cli/gateway.py`
- corresponding gateway / run_agent / display tests

See these bundled references for the detailed breakdown:

- `references/modified-files.md`
- `references/upgrade-locator.md`
- `references/modification-map.json`

## How to Re-locate the Touchpoints After Hermes Updates

### 1) Print the locator manifest

```bash
python -m hermes_feishu_streaming_plugin locators
```

This emits a JSON list of target files plus stable anchor patterns such as:

- `class FeishuAdapter(BasePlatformAdapter):`
- `async def send(`
- `async def edit_message(`
- `progress_transport`
- `GatewayStreamConsumer(`
- `_STATUS_ONLY_PLACEHOLDER = "\u200b"`

### 2) Scan a target Hermes repository

```bash
python -m hermes_feishu_streaming_plugin locate --target /path/to/hermes-agent
```

The report tells you:

- which files still exist,
- which files fully match the expected touchpoints,
- which files only partially match,
- and which line numbers contain each anchor.

That makes future manual merges much easier after upstream churn.

### 3) Finish the merge with the bundled references

Recommended order:

1. run `locate`
2. read `references/modified-files.md`
3. compare against `references/migration.patch`
4. use the bundled `files/` tree as the source of truth

## Repository Layout

```text
hermes-feishu-streaming-plugin/
├── src/hermes_feishu_streaming_plugin/
│   ├── bundle.py
│   ├── installer.py
│   ├── locator.py
│   ├── cli.py
│   └── assets/hermes-feishu-weixin-streaming-migration-kit/
│       ├── SKILL.md
│       ├── files/
│       └── references/
├── tests/
├── pyproject.toml
└── README.md
```

## CLI Usage

Install in editable mode:

```bash
pip install -e .[dev]
```

Print bundled manifest:

```bash
python -m hermes_feishu_streaming_plugin manifest
```

Export the migration bundle:

```bash
python -m hermes_feishu_streaming_plugin export --output-dir ./dist
```

Print the locator spec:

```bash
python -m hermes_feishu_streaming_plugin locators
```

Locate the migration touchpoints in a Hermes repo:

```bash
python -m hermes_feishu_streaming_plugin locate --target /path/to/hermes-agent
```

Apply the bundled files:

```bash
python -m hermes_feishu_streaming_plugin apply --target /path/to/hermes-agent
```

Dry run first:

```bash
python -m hermes_feishu_streaming_plugin apply --target /path/to/hermes-agent --dry-run
```

## Typical Migration Workflow

```bash
python -m hermes_feishu_streaming_plugin manifest
python -m hermes_feishu_streaming_plugin locate --target /path/to/hermes-agent
python -m hermes_feishu_streaming_plugin export --output-dir ./dist
python -m hermes_feishu_streaming_plugin apply --target /path/to/hermes-agent --dry-run
python -m hermes_feishu_streaming_plugin apply --target /path/to/hermes-agent
```

## Verification

Run the local test suite:

```bash
pytest
```

Build distribution artifacts:

```bash
python -m build
```

For the original Hermes regression targets, see:

- `references/verification.md`

## Packaging and Publishing

This repository is suitable as a public **skill repository** because it includes:

- the installable `SKILL.md`,
- the modified files under `files/`,
- the migration patch,
- the rationale and touchpoint docs,
- and a CLI that helps future upgrades find the right code again.
