# docs

Documentation for M&L AI's products, published at **[docs.mlaify.io](https://docs.mlaify.io)**.
Each product has its own section: [AttackMap](https://docs.mlaify.io/attackmap/) now, grrclone next.

This repo was `mlaify/attackmap-docs` (MkDocs Material, AttackMap only) until 2026-11-08.
It is now a Hugo site that shares mlaify.io's theme, and covers every product. The three
public sites split the work:

| Site | Repo | Job |
|---|---|---|
| [mlaify.io](https://mlaify.io) | `mlaify/mlaify.github.io` | The products: what each one is, how it works, install |
| **docs.mlaify.io** | **`mlaify/docs`** (this repo) | How to use them: guides and reference |
| [matthewd.xyz](https://matthewd.xyz) | `mlaifyxyz/mlaifyxyz.github.io` | Personal site and writing |

> [!IMPORTANT]
> **Active development, slow pace.** Help is welcome with the docs, the products, or both:
> open an issue on the product's repository (for AttackMap,
> [mlaify/AttackMap](https://github.com/mlaify/AttackMap/issues)) to say hello. Security
> reports are welcome at [security@mlaify.io](mailto:security@mlaify.io).

## Writing docs

Pages are Markdown under `content/<product>/`. A page's front matter places it in the nav:

```yaml
---
title: "Install"
description: "One line, used in search results, llms.txt and the page's meta description."
weight: 10            # order within its group
group: "Getting started"  # one of the groups listed in content/<product>/_index.md
---
```

- **Links between pages** are relative file links, `[Install](install.md)` or
  `[Recall mode](scanning.md#recall-mode)`, so they also work on GitHub. The build fails if
  the page or the heading doesn't exist (`layouts/_markup/render-link.html`).
- **Callouts:** `{{< callout type="note|warn|security" title="..." >}} ... {{< /callout >}}`.
- **Tabs:** `{{< tabs >}}{{< tab name="pipx" >}} ... {{< /tab >}}{{< tab name="pip" >}} ... {{< /tab >}}{{< /tabs >}}`.
- **Code block titles:** ```` ```python {title="my_package/analyzer.py"} ````. Every code block gets
  a copy button.
- **Images** go in `static/<product>/img/` and are linked as `/<product>/img/...`.
- **Heading ids** are Hugo's `blackfriday` style, which matches the old MkDocs ids. If a heading
  has an apostrophe or a dot, pin the old id: `## Listing what's installed {#listing-whats-installed}`.

### Adding a product

1. Add it to `products` in [`config/_default/params.toml`](config/_default/params.toml).
2. Create `content/<slug>/_index.md` with `title`, `description`, `product` and `groups`.
3. Add pages with a `group` from that list. The home page, the product switcher, search, the nav,
   `llms.txt` and `llms-full.txt` pick it up.

## Local development

Needs Hugo extended 0.162.1 and Node 24 (`.nvmrc`).

```bash
npm ci
npm run dev           # live preview at http://localhost:1313 (no search: Pagefind runs at build)
npm run build:cf      # the production build: Hugo, Pagefind, scripts/check-build.sh
npm run check         # after a build: old URLs, old heading anchors, build sanity
npm run preview       # serve public/ through wrangler's real asset router
```

`tests/` checks that the AttackMap pages still match AttackMap itself: the Analyzer SDK example
is extracted from `content/attackmap/sdk.md` and run, the analyzers table is compared with
`attackmap modules --json`, and the CLI reference with the real CLI. It needs AttackMap with every
official plugin; `[all]` pins the plugins' releases, which are on pkg.mlaify.io:

```bash
pip install pytest --extra-index-url https://pkg.mlaify.io/pypi/simple/ \
  "attackmap[all] @ git+https://github.com/mlaify/AttackMap.git"
pytest tests/
```

## Checks

[`docs-ci`](.github/workflows/docs-ci.yml) runs on every pull request; its `build-and-test` job is
the required check.

| Check | What it catches |
|---|---|
| Hugo build | A link to a page or heading that doesn't exist |
| [`scripts/check-build.sh`](scripts/check-build.sh) | Missing search index, `_headers`, `_redirects`, `security.txt`, `llms.txt`; a page left out of search; an unrendered shortcode |
| [`scripts/check-redirects.sh`](scripts/check-redirects.sh) | An old docs.mlaify.io URL that no longer lands on a page |
| [`scripts/check-anchors.sh`](scripts/check-anchors.sh) | An old heading link (`/scanning/#recall-mode`) whose heading is gone |
| lychee `--offline` | Any broken link inside the built site |
| `pytest tests/` | AttackMap pages that drifted from the CLI or SDK |

[`links`](.github/workflows/links.yml) checks external links weekly.

### Old URLs

The MkDocs site served AttackMap's pages at the root (`/install/`, `/scanning/`, ...). They moved
to `/attackmap/...`, and [`static/_redirects`](static/_redirects) sends each old URL there with a
301. [`scripts/old-urls.txt`](scripts/old-urls.txt) lists every URL and heading anchor the old site
published; the two scripts above check each one on every build. Never remove a line from it or a
rule from `_redirects`.

## Deploy

**The operator approves every production deploy.** A push to `main` starts
[`.github/workflows/deploy.yml`](.github/workflows/deploy.yml) in the `production` environment,
which waits for its required reviewer; once approved it runs the same build (`npm run build:cf`)
and `npx wrangler deploy`. Cloudflare **Workers Builds** still clones and builds every push, but
only uploads a version (`npx wrangler versions upload`), so nothing goes live without the
approval. This is the same setup as mlaify.io.

| | |
|---|---|
| Worker | `docs-mlaify-io` |
| Config | [`wrangler.jsonc`](wrangler.jsonc) |
| Production | `main` → `https://docs.mlaify.io` after approval (also served, not redirected, at `docs.fhrp.org`, `docs.mldavis.me` and `docs.tffhrtp.org`; `docs.matthewd.xyz` was dropped on 2026-11-08) |
| Any other branch | built and uploaded as a version; no public preview URL, not promoted to production |

### Build settings (Cloudflare dashboard)

Workers & Pages → `docs-mlaify-io` → Settings → Build:

| Setting | Value |
|---|---|
| Build command | `npm run build:cf` |
| Deploy command | `npx wrangler versions upload` (the approved GitHub job deploys) |
| Non-production deploy command | `npx wrangler versions upload` |
| Root directory | *(blank)* |
| Variable `HUGO_VERSION` | `0.162.1` (without it the build image uses its default Hugo) |

### Toolchain pinning

| Tool | Pinned to | Where |
|---|---|---|
| Hugo extended | 0.162.1 | `HUGO_VERSION` in the workflows and the Workers Builds variable |
| Node | 24 | [`.nvmrc`](.nvmrc) |
| Tailwind, Pagefind, wrangler | see `package-lock.json` | [`package.json`](package.json) |

### Headers

[`static/_headers`](static/_headers) is the single source of truth for security and cache headers.
Hugo copies it to `public/_headers`; Cloudflare reads it at deploy time and does not serve it. If a
Cloudflare Transform Rule also sets these headers, remove one side.

## Theme

The look is mlaify.io's: `tailwind.config.js`, `assets/css/app.css` (the part above the "Docs"
marker), the icon set, the dark-mode toggle (same `localStorage` key) and the search dialog are
copied from `mlaify/mlaify.github.io`. Keep them in step when the theme changes there. The docs
layout itself (nav, table of contents, previous/next, tabs, code blocks) is in `layouts/` and the
"Docs" part of `app.css`.
