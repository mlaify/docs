---
title: "grrclone"
description: "What grrclone is, how to install it, and where to go next."
weight: 0
product: "grrclone"
groups: ["Guide", "Reference"]
---

**A free, open-source macOS menu bar app that connects [rclone](https://rclone.org)
remotes as Finder volumes.** No licence key, no phone-home, no kernel extension, no
root.

grrclone runs one bundled `rclone` daemon, starts an NFS server on loopback for each
connection, and mounts it with options that turn a dead backend into an error instead
of a hung Finder. [How it works](https://mlaify.io/grrclone/how-it-works/) on mlaify.io
explains the design.

<p><img src="/grrclone/img/menu.png" alt="The grrclone menu, listing connected remotes" width="420" loading="lazy"></p>

## Install

Apple Silicon, macOS 14 or later.

```bash
brew install --cask mlaify/tap/grrclone
```

Or download the latest DMG from
[Releases](https://github.com/mlaify/grrclone/releases/latest) and drag it to
Applications. It's signed and notarised. Homebrew owns updates
(`brew update && brew upgrade --cask grrclone`); grrclone can check for new releases
if you ask it to, but never replaces its own bundle.

## First run

grrclone appears in the menu bar, with no Dock icon. It finds the remotes already in
your `rclone.conf` and lists them. Connect one and it appears in Finder, under
`~/grrclone` by default or any folder you choose. It reads `rclone.conf` but never
writes it, so your command-line setup keeps working as before.

<p><img src="/grrclone/img/settings.png" alt="grrclone settings" width="520" loading="lazy"></p>

## Where to go next

- [Limitations](limitations.md): what NFSv3 and the macOS NFS client can't do, and what
  to expect when storage goes away.
- [Benchmarks](benchmarks.md): the throughput numbers and the crash test behind the mount
  options.
- [The usage document](usage-document.md): let your storage server report how much
  space a remote uses.
- [Changelog](https://mlaify.io/grrclone/changelog/) and
  [source](https://github.com/mlaify/grrclone).
