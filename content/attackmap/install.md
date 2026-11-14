---
title: "Install"
description: "PyPI (uv, pipx or pip) or Homebrew; the LLM and all-analyzers extras; the macOS app."
weight: 10
group: "Getting started"
---

AttackMap needs **Python 3.11+**. It's on [PyPI](https://pypi.org/project/attackmap/)
with all 15 official analyzer plugins, and in the
[Homebrew tap](https://github.com/mlaify/homebrew-tap). The same release files are
also on the [M&L AI package index](https://pkg.mlaify.io/) and GitHub.

{{< tabs >}}
{{< tab name="Homebrew" >}}
The CLI and all 15 official analyzer plugins:

```bash
brew install mlaify/tap/attackmap
```
{{< /tab >}}
{{< tab name="uv" >}}
The CLI and all 15 official analyzer plugins, from PyPI:

```bash
uv tool install "attackmap[all]"
```
{{< /tab >}}
{{< tab name="pipx" >}}
From PyPI, with all 15 analyzer plugins (drop `[all]` for core only):

```bash
pipx install "attackmap[all]"
```
{{< /tab >}}
{{< tab name="pip" >}}
From PyPI, into a virtualenv (drop `[all]` for core only):

```bash
pip install "attackmap[all]"
```
{{< /tab >}}
{{< /tabs >}}

## Optional: LLM support

The AI-review modes work through the `claude` / `codex` CLIs with no extra
install. To use the **API backends** instead, add the LLM extra (pulls in the
`anthropic` and `openai` SDKs):

```bash
pip install "attackmap[llm]"
```

See [AI review](llm.md) for how backends and credentials resolve.

## Optional: everything

The `all` extra adds all 15 official ecosystem analyzer plugins up front, each
pinned to its release on PyPI. Homebrew installs them too. Without
them, a plain `attackmap analyze` never installs plugins; use
`attackmap suggest . --install` or `--module <name>` (see
[Analyzers](analyzers.md#installing-plugins)):

```bash
uv tool install "attackmap[all]"
```

A single plugin also installs on its own and pulls in AttackMap with it, for
example `uv tool install attackmap --with attackmap-analyzer-go`.

To install from the [M&L AI package index](https://pkg.mlaify.io/) instead (the
same files), point uv at it with `--index-strategy first-index`. Don't mix it
in with `pip --extra-index-url`: pip takes the highest version from any index.

## macOS app

Prefer a GUI? The native macOS front end drives the same CLI. The cask installs
the CLI too:

```bash
brew install --cask mlaify/tap/attackmap-app
```

Or build it from source: [mlaify/AttackMap-mac](https://github.com/mlaify/AttackMap-mac).

See [macOS app](gui.md).

## Verify

```bash
attackmap --help
attackmap modules        # list installed analyzer modules
```
