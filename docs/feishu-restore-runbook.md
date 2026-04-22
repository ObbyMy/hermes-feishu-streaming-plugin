# Feishu 恢复操作手册

目标：在 **更新 Hermes** 或 **更换电脑** 后，重新恢复当前这套 Feishu 网关使用体验。

> 若把本仓库交给另一个 Hermes 智能体，优先让它先读 `AGENTS.md`、`README.md`，并执行 `python -m hermes_feishu_streaming_plugin agent-handoff`。

## 当前机器上的恢复材料

私密恢复包：

`~/.hermes/private/feishu_restore_bundle_20260422/`

其中包括：

- `env.feishu.sh`：当前 FEISHU_* 实际配置
- `config.session_reset.yaml`：当前 session reset 配置片段
- `hermes-gateway.service`：当前 systemd 用户服务文件
- `status_snapshot.json`：当前 Feishu home channel / bot 标识摘要

## A. 同机更新 Hermes 后恢复

1. 备份当前源码目录。
2. 获取新的 Hermes 源码。
3. 在新源码目录中应用本仓库 bundle：

```bash
cd /path/to/hermes-feishu-streaming-plugin
PYTHONPATH=src python3 -m hermes_feishu_streaming_plugin apply --target /path/to/hermes-agent
```

4. 恢复 Feishu 环境变量：

```bash
set -a
source ~/.hermes/private/feishu_restore_bundle_20260422/env.feishu.sh
set +a
```

5. 检查 `~/.hermes/config.yaml` 中的 `session_reset` 是否与私密恢复包一致。
6. 恢复或覆盖用户服务文件：

```bash
cp ~/.hermes/private/feishu_restore_bundle_20260422/hermes-gateway.service ~/.config/systemd/user/hermes-gateway.service
systemctl --user daemon-reload
systemctl --user restart hermes-gateway
```

7. 验证：

```bash
hermes status --all
hermes gateway status
```

## B. 更换电脑后的恢复

1. 新机器安装 Python / git / node（按 Hermes 官方要求）。
2. 克隆 Hermes 新版源码。
3. 克隆本仓库。
4. 把旧机器的私密恢复包安全复制到新机器 `~/.hermes/private/feishu_restore_bundle_20260422/`。
5. 在新 Hermes 源码目录应用 bundle。
6. 写回 FEISHU_* 环境变量、`config.yaml` 片段、systemd service。
7. 启动并验证 gateway。

## C. 本机验证结论

已经在最新上游源码上做过一次恢复演练：

- 上游克隆：`/home/jiangshuo/.hermes/projects/hermes-agent-upstream-check`
- 应用后仓库：`/home/jiangshuo/.hermes/projects/hermes-agent-upstream-applied`
- 关键测试：通过

所以当前结论是：

- **直接更新不会自动保留当前飞书优化状态**
- 但**可以通过本仓库 + 私密恢复包稳定恢复**
