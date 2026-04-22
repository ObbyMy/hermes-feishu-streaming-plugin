# Feishu migration steps

## 1. Locate anchors in the target repo

```bash
python -m hermes_feishu_streaming_plugin locate --target /path/to/hermes-agent
```

## 2. Dry-run the file application

```bash
python -m hermes_feishu_streaming_plugin apply --target /path/to/hermes-agent --dry-run
```

## 3. Apply the bundle

```bash
python -m hermes_feishu_streaming_plugin apply --target /path/to/hermes-agent
```

## 4. Restore current machine Feishu settings if needed

Private restore bundle path on this machine:

`/home/jiangshuo/.hermes/private/feishu_restore_bundle_20260422`

## 5. Run verification

See `references/verification.md`.
