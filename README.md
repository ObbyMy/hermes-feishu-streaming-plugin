# Hermes Feishu Streaming Plugin

> **Bilingual standalone migration toolkit for Hermes Feishu / Weixin streaming fixes**  
> **Hermes 飞书 / 微信流式消息修复的独立双语迁移工具包**

A modern, production-friendly plugin project that packages the verified Feishu/Weixin streaming gateway migration into a reusable Python distribution.

这是一个面向生产环境的现代化独立插件项目，用于把已经验证过的 Hermes 飞书 / 微信流式网关迁移方案打包成可复用的 Python 发行包。

---

## ✨ Highlights | 核心亮点

- **Standalone packaging** — install and distribute the migration kit without copying an entire working repository.  
  **独立封装**——无需复制整个工作仓库，即可安装和分发迁移工具包。
- **Verified migration assets** — includes modified source files, regression tests, patch references, and implementation notes.  
  **已验证迁移资产**——内置修改后的源码文件、回归测试、补丁参考和实施说明。
- **Simple CLI workflow** — inspect, export, and apply the bundle with a small command surface.  
  **简洁 CLI 流程**——通过少量命令即可查看、导出并应用迁移包。
- **Repo-friendly structure** — designed for GitHub publishing, versioning, and future iterative maintenance.  
  **仓库友好结构**——适合发布到 GitHub、版本管理以及后续持续维护。

---

## 🧭 What this project is for | 这个项目解决什么问题

When the Hermes Feishu / Weixin gateway needs streaming-card behavior fixes, manual patch transfer is error-prone and hard to repeat.

当 Hermes 的飞书 / 微信网关需要修复流式卡片行为时，手工迁移补丁通常容易出错，也难以重复执行。

This project turns that migration into a portable plugin-style package so you can:

本项目把该迁移方案整理成可移植的插件式工具包，使你可以：

1. inspect the bundled manifest before changes are applied;  
   在真正修改前先检查内置文件清单；
2. export the full migration kit for review or archival;  
   导出完整迁移包以便审阅或归档；
3. apply the bundled files directly into a target Hermes repository.  
   将内置文件直接应用到目标 Hermes 仓库中。

---

## 📦 Included in the bundle | 内含内容

The package currently bundles the following migration assets:

当前软件包内置以下迁移资产：

- updated Hermes gateway source files  
  更新后的 Hermes 网关源码文件
- Feishu-related regression tests  
  飞书相关回归测试
- migration patch reference files  
  迁移补丁参考文件
- verification and implementation notes  
  验证说明与实施文档
- metadata contract documentation for streaming messages  
  流式消息元数据约定文档
- a Python CLI for export / apply operations  
  用于导出 / 应用操作的 Python CLI

---

## 🗂 Project structure | 项目结构

```text
hermes-feishu-streaming-plugin/
├── src/hermes_feishu_streaming_plugin/
│   ├── bundle.py            # Bundle manifest + export helpers
│   ├── installer.py         # Apply bundled files into a Hermes repo
│   ├── cli.py               # Command-line interface
│   └── assets/
│       └── hermes-feishu-weixin-streaming-migration-kit/
│           ├── files/       # Source files and tests to copy into Hermes
│           ├── references/  # Patch, verification, migration notes
│           ├── README.md
│           └── SKILL.md
├── tests/
├── dist/
├── pyproject.toml
└── README.md
```

---

## 🚀 Quick start | 快速开始

### 1) Install | 安装

```bash
pip install -e .[dev]
```

### 2) View the manifest | 查看清单

```bash
python -m hermes_feishu_streaming_plugin manifest
```

### 3) Export the bundled migration kit | 导出迁移包

```bash
python -m hermes_feishu_streaming_plugin export --output-dir ./dist
```

### 4) Apply to a Hermes repository | 应用到 Hermes 仓库

```bash
python -m hermes_feishu_streaming_plugin apply --target /path/to/hermes-repo
```

### 5) Dry run before copy | 复制前先演练

```bash
python -m hermes_feishu_streaming_plugin apply --target /path/to/hermes-repo --dry-run
```

---

## 🖥 CLI reference | CLI 命令说明

### `manifest`
Print the bundled file manifest as JSON.  
以 JSON 形式输出内置文件清单。

```bash
python -m hermes_feishu_streaming_plugin manifest
```

### `export --output-dir <dir>`
Copy the bundled migration kit into a target directory.  
将内置迁移包复制到指定目录。

```bash
python -m hermes_feishu_streaming_plugin export --output-dir ./dist
```

### `apply --target <repo> [--dry-run]`
Copy the bundled files into a target Hermes repository.  
把内置文件复制到目标 Hermes 仓库。

```bash
python -m hermes_feishu_streaming_plugin apply --target /path/to/hermes-repo
python -m hermes_feishu_streaming_plugin apply --target /path/to/hermes-repo --dry-run
```

---

## 🧪 Development | 开发与测试

Install the development dependencies first:

先安装开发依赖：

```bash
pip install -e .[dev]
```

Run the test suite:

运行测试：

```bash
pytest
```

Build distribution artifacts if needed:

如需构建发行包：

```bash
python -m build
```

---

## ✅ Typical workflow | 典型使用流程

```bash
# 1. inspect what will be shipped
python -m hermes_feishu_streaming_plugin manifest

# 2. export the bundle for review
python -m hermes_feishu_streaming_plugin export --output-dir ./dist

# 3. validate target changes first
python -m hermes_feishu_streaming_plugin apply --target /path/to/hermes-repo --dry-run

# 4. perform the actual copy
python -m hermes_feishu_streaming_plugin apply --target /path/to/hermes-repo
```

---

## 🎯 Use cases | 适用场景

- packaging a proven Feishu streaming fix into a reusable deliverable  
  将已验证的飞书流式修复方案打包成可复用交付物
- shipping migration bundles between environments or teams  
  在不同环境或团队之间分发迁移包
- preserving a tested gateway patch set outside the main Hermes repository  
  在主 Hermes 仓库之外保留一套经过测试的网关补丁
- preparing a clean public repository for documentation and versioned releases  
  为文档展示和版本发布准备一个整洁的公共仓库

---

## 📌 Notes | 说明

- This repository packages **migration assets**, not a full standalone Hermes runtime.  
  本仓库打包的是**迁移资产**，不是完整独立运行版 Hermes。
- Always run a dry run and review copied files before applying changes in production.  
  在生产环境应用修改前，建议先执行 dry run 并审查即将复制的文件。
- The bundled assets can be versioned and released independently from the main Hermes repository.  
  内置迁移资产可以独立于主 Hermes 仓库进行版本管理与发布。

---

## 🛣 Roadmap | 路线图

- [ ] add release automation for GitHub publishing  
      增加 GitHub 发布自动化
- [ ] support selective file application  
      支持按文件选择性应用
- [ ] add richer validation output and diff previews  
      增加更丰富的校验输出与差异预览
- [ ] publish versioned migration bundles with changelogs  
      发布带变更日志的版本化迁移包

---

## 📄 License | 许可证

MIT License.

---

## 🤝 Contributing | 参与贡献

Issues and pull requests are welcome. If you plan to publish or adapt this package for your own Hermes deployment workflow, document your changes clearly and keep migration references in sync.

欢迎提交 Issue 和 Pull Request。如果你计划将本项目用于自己的 Hermes 部署流程，请清晰记录修改内容，并保持迁移参考资料同步更新。
