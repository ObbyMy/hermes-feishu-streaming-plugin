# Hermes Feishu Streaming Skill Kit

一个**只面向飞书渠道**的 Hermes Agent 迁移仓库，用来沉淀并复用飞书单卡片流式输出、工具进度嵌入、会话提示卡片化、附件说明发送顺序等优化。

## 现在这个仓库负责什么

- 保存 Feishu 体验优化所需的 Hermes 源码片段
- 提供 `manifest / export / locators / locate / verify / apply / agent-handoff` CLI
- 在 Hermes 升级后帮助重新定位并恢复飞书相关改动
- 配套当前机器的 Feishu 恢复说明，方便更新软件或更换电脑后快速恢复
- 让另一个 Hermes 智能体**只拿到本仓库地址**时，也能知道该怎么应用和验证

## 给 Hermes 智能体的最短用法

如果你把这个仓库地址发给另一个 Hermes 智能体，它在克隆仓库后应优先看：

- `AGENTS.md`
- `README.md`
- `docs/feishu-restore-runbook.md`

然后执行：

```bash
pip install -e .[dev]
python -m hermes_feishu_streaming_plugin agent-handoff
python -m hermes_feishu_streaming_plugin locate --target /path/to/hermes-agent
python -m hermes_feishu_streaming_plugin apply \
  --target /path/to/hermes-agent \
  --verify \
  --python /path/to/hermes-agent/venv/bin/python
```

这样它就能直接得到：

- 要修改哪些文件
- 如何复制 bundle
- 如何执行验证
- 需要向用户汇报哪些结果

> 注意：如果任务还包括恢复某台机器上的真实 `FEISHU_*` 凭据、`config.yaml` 片段和 systemd 服务文件，仍需要那台机器自己的私密恢复包；这些敏感信息不会放进 Git 仓库。

## 作用边界

- 本仓库仅关注 Feishu 渠道体验恢复与迁移
- 其他平台不作为此仓库的目标范围

## 核心迁移文件

当前 bundle 主要包含：

- `gateway/platforms/feishu.py`
- `gateway/run.py`
- `gateway/stream_consumer.py`
- `gateway/display_config.py`
- `tests/gateway/test_stream_consumer.py`
- `tests/gateway/test_feishu.py`
- `tests/gateway/test_feishu_session_notices.py`
- `tests/agent/test_display.py`
- `tests/run_agent/test_context_pressure.py`
- `website/docs/user-guide/messaging/feishu.md`

## 命令

```bash
pip install -e .[dev]
python -m hermes_feishu_streaming_plugin manifest
python -m hermes_feishu_streaming_plugin export --output-dir ./dist
python -m hermes_feishu_streaming_plugin locators
python -m hermes_feishu_streaming_plugin locate --target /path/to/hermes-agent
python -m hermes_feishu_streaming_plugin verify --target /path/to/hermes-agent --python /path/to/hermes-agent/venv/bin/python
python -m hermes_feishu_streaming_plugin apply --target /path/to/hermes-agent --dry-run
python -m hermes_feishu_streaming_plugin apply --target /path/to/hermes-agent --verify --python /path/to/hermes-agent/venv/bin/python
python -m hermes_feishu_streaming_plugin agent-handoff
```

## 更新后的恢复流程

详细步骤见：

- `docs/feishu-restore-runbook.md`
- `src/hermes_feishu_streaming_plugin/assets/hermes-feishu-streaming-migration-kit/references/migration-steps.md`

## 当前结论

已经用最新上游 Hermes 源码做过一次恢复演练：

- 上游检查仓库：`/home/jiangshuo/.hermes/projects/hermes-agent-upstream-check`
- 将本 bundle 应用到演练仓库后
- 运行 `pytest tests/gateway/test_stream_consumer.py tests/gateway/test_feishu.py tests/gateway/test_feishu_session_notices.py -q`
- 结果通过

这说明：**Hermes 更新后，不一定能直接保留当前飞书体验，但可以通过本仓库重新应用并恢复。**
