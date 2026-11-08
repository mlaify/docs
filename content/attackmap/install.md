---
title: "Install"
description: "Homebrew, uv from pkg.mlaify.io, pipx or pip; the LLM and all-analyzers extras; the macOS app."
weight: 10
group: "Getting started"
---

AttackMap needs **Python 3.11+**. It isn't on PyPI: it installs from the
[Homebrew tap](https://github.com/mlaify/homebrew-tap), the
[M&L AI package index](https://pkg.mlaify.io/) or GitHub.

{{< tabs >}}
{{< tab name="Homebrew" >}}
The CLI and all 15 official analyzer plugins:

```bash
brew install mlaify/tap/attackmap
```
{{< /tab >}}
{{< tab name="uv" >}}
The CLI and all 15 official analyzer plugins, from pkg.mlaify.io:

```bash
uv tool install "attackmap[all]" --index mlaify=https://pkg.mlaify.io/pypi/simple/ --index-strategy first-index
```
{{< /tab >}}
{{< tab name="pipx" >}}
Core only, from GitHub:

```bash
pipx install git+https://github.com/mlaify/AttackMap.git
```
{{< /tab >}}
{{< tab name="pip" >}}
Core only, from GitHub:

```bash
pip install git+https://github.com/mlaify/AttackMap.git
```
{{< /tab >}}
{{< /tabs >}}

## Optional: LLM support

The AI-review modes work through the `claude` / `codex` CLIs with no extra
install. To use the **API backends** instead, add the LLM extra (pulls in the
`anthropic` and `openai` SDKs):

```bash
pip install "attackmap[llm] @ git+https://github.com/mlaify/AttackMap.git"
```

See [AI review](llm.md) for how backends and credentials resolve.

## Optional: everything

The `all` extra adds all 15 official ecosystem analyzer plugins up front, each
pinned to its release on pkg.mlaify.io. Homebrew installs them too. Without
them, a plain `attackmap analyze` never installs plugins; use
`attackmap suggest . --install` or `--module <name>` (see
[Analyzers](analyzers.md#installing-plugins)):

```bash
uv tool install "attackmap[all]" --index mlaify=https://pkg.mlaify.io/pypi/simple/ --index-strategy first-index
```

The plugins are published only on pkg.mlaify.io, not on PyPI, so use uv's
`--index-strategy first-index`, which takes each package from the first index
that has it. Avoid `pip install --extra-index-url`: pip takes the highest
version from any index, so a package with the same name published on PyPI
could be installed instead.

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
