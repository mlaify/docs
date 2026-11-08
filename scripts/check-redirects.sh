#!/usr/bin/env bash
#
# Check that every URL the old MkDocs docs published (scripts/old-urls.txt)
# still lands on a page in public/: either it exists as is, or a rule in
# public/_redirects sends it to a page that exists. Run after the build.
#
# The old home page (/) is now the docs home, so it needs no redirect. Only the
# exact-match rules are checked here; the one dynamic rule (/img/*) is checked
# against the screenshots that were published.

set -euo pipefail

fail=0
note() {
	printf '  %s\n' "$1"
	fail=1
}

[ -f public/_redirects ] || { echo "public/_redirects missing" >&2; exit 1; }

exists() { # $1 = URL path; true if public/ serves it
	local p=$1
	[ -f "public$p" ] || [ -f "public${p%/}/index.html" ]
}

target_of() { # print the destination of an exact rule for $1, if any
	awk -v src="$1" '$1 == src && $0 !~ /^#/ { print $2; exit }' public/_redirects
}

checked=0
while read -r path; do
	if [ "$path" = "/" ]; then
		checked=$((checked + 1))
		exists / || note "/: the docs home is missing"
		continue
	fi
	# Each old page is listed with and without its trailing slash.
	for p in "$path" "${path%/}"; do
		checked=$((checked + 1))
		dest=$(target_of "$p")
		if [ -z "$dest" ]; then
			note "$p: no redirect rule"
		elif ! exists "$dest"; then
			note "$p redirects to $dest, which is not in the build"
		fi
	done
done < <(grep -v '^#' scripts/old-urls.txt | sed 's|#.*||' | sort -u)

# The old screenshots: /img/<x> -> /attackmap/img/<x>.
for f in static/attackmap/img/screenshots/*; do
	checked=$((checked + 1))
	exists "/attackmap/img/screenshots/$(basename "$f")" || note "/img/screenshots/$(basename "$f"): target missing"
done
grep -q '^/img/\* /attackmap/img/:splat 301$' public/_redirects || note "the /img/* rule is missing from _redirects"

if [ "$fail" -ne 0 ]; then
	printf 'Old docs URLs would break.\n' >&2
	exit 1
fi
printf 'Old docs URLs: %s checked, all resolve.\n' "$checked"
