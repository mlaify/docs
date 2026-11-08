#!/usr/bin/env bash
#
# Check that every heading anchor the old MkDocs docs published
# (scripts/old-urls.txt, e.g. /scanning/#recall-mode) still exists on the page
# it moved to (/attackmap/scanning/), so links into the middle of a page keep
# working. Run after the build.
#
# Heading ids follow Hugo's "blackfriday" style, which matches MkDocs for
# almost every heading. Where they differ (an apostrophe or a dot in the
# heading), the page pins the old id: `## Listing what's installed {#listing-whats-installed}`.

set -euo pipefail

fail=0
checked=0
while read -r url; do
	case $url in '' | '#'*) continue ;; esac
	[[ $url == *'#'* ]] || continue
	path=${url%%#*}
	id=${url#*#}
	file="public/attackmap${path}index.html"
	checked=$((checked + 1))
	if [ ! -f "$file" ]; then
		printf '  %s: %s missing\n' "$url" "$file"
		fail=1
	elif ! grep -Eq "[[:space:]]id=(\"$id\"|$id[[:space:]>])" "$file"; then
		printf '  %s: no id "%s" on /attackmap%s\n' "$url" "$id" "$path"
		fail=1
	fi
done < scripts/old-urls.txt

if [ "$fail" -ne 0 ]; then
	printf 'Old heading links would break.\n' >&2
	exit 1
fi
printf 'Old heading anchors: %s checked, all present.\n' "$checked"
