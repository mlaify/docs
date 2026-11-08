#!/usr/bin/env bash
#
# Assert that the Hugo + Pagefind build produced everything the site needs
# before it is deployed. Run by `npm run build:cf`, which is what Workers Builds
# and the deploy job execute, so a bad build never becomes a deployment.
#
# Broken links between docs pages, and links to headings that don't exist, fail
# the Hugo build itself (layouts/_markup/render-link.html).

set -euo pipefail

fail=0
note() {
	printf '  %s\n' "$1"
	fail=1
}

[ -f public/index.html ] || note "public/index.html missing"
[ -f public/404.html ] || note "public/404.html missing — not_found_handling: 404-page has nothing to serve"
[ -d public/pagefind ] || note "public/pagefind missing — search index not built"
[ -f public/.well-known/security.txt ] || note "public/.well-known/security.txt missing"
[ -s public/llms.txt ] || note "public/llms.txt missing or empty"
[ -s public/llms-full.txt ] || note "public/llms-full.txt missing or empty"

# Cloudflare reads public/_headers and public/_redirects at deploy time and
# does not serve them. If either is absent the deploy still succeeds, silently
# dropping every security header, or breaking every old docs.mlaify.io link.
[ -f public/_headers ] || note "public/_headers missing — static/_headers did not reach the build output"
[ -f public/_redirects ] || note "public/_redirects missing — static/_redirects did not reach the build output"

# Every product page must be in the search index. Pagefind indexes only pages
# with data-pagefind-body, so a layout change could silently drop them.
pages=$(find public -path public/pagefind -prune -o -name index.html -print | grep -c -v '^public/index.html$' || true)
indexed=$(grep -l 'data-pagefind-body' -r public --include=index.html | wc -l | tr -d ' ')
[ "$indexed" -gt 0 ] && [ "$indexed" -eq "$pages" ] || note "$indexed of $pages docs pages carry data-pagefind-body"

# No source maps or unrendered shortcodes in the output.
maps=$(find public -name '*.map' | wc -l | tr -d ' ')
[ "$maps" = "0" ] || note "$maps source map(s) in public/"
if grep -rl '{{[<%]' public --include=*.html >/dev/null; then
	note "unrendered shortcode in: $(grep -rl '{{[<%]' public --include=*.html | tr '\n' ' ')"
fi

if [ "$fail" -ne 0 ]; then
	printf 'Build output is not deployable.\n' >&2
	exit 1
fi

printf 'Build output looks sane (%s files).\n' "$(find public -type f | wc -l | tr -d ' ')"
