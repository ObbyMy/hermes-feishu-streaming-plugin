# Hermes Feishu Streaming Plugin

A standalone project that packages the Feishu/Weixin gateway streaming migration for Hermes.

## What it includes

- bundled modified Hermes source files
- bundled regression tests
- bundled migration patch
- Feishu `_hermes_stream` metadata contract docs
- CLI to inspect, export, and apply the migration bundle

## Install

```bash
pip install -e .[dev]
```

## CLI

```bash
python -m hermes_feishu_streaming_plugin manifest
python -m hermes_feishu_streaming_plugin export --output-dir ./dist
python -m hermes_feishu_streaming_plugin apply --target /path/to/hermes-repo
```

## Tests

```bash
pytest
```
