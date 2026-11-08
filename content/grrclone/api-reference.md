---
title: "API reference"
description: "The Swift API of grrclone's two packages, RcloneRC and GrrCloneCore, generated with DocC from the v0.9.5 release."
weight: 40
group: "Reference"
---

The logic of grrclone lives in two Swift packages that build and test without Xcode.
Their API reference is generated with DocC from the
[v0.9.5](https://github.com/mlaify/grrclone/tree/v0.9.5/Sources) release:

- **[GrrCloneCore](/grrclone/reference/grrclonecore/documentation/grrclonecore/)**: the
  connection lifecycle (start the daemon, serve, mount, unmount, reconcile after a crash),
  the registry of mounts grrclone made, mount health, the stored connections, and the
  rclone config password and encryption.
- **[RcloneRC](/grrclone/reference/rclonerc/documentation/rclonerc/)**: the client for
  rclone's remote-control API over a unix socket, with serving, config, providers,
  bandwidth limits and deadlines for calls that can't be cancelled.

These are the packages' public and internal declarations as the code documents them; the app
target and `grrclonectl` aren't included. [How it works](https://mlaify.io/grrclone/how-it-works/)
on mlaify.io describes how the parts fit together.

{{< callout type="note" >}}
Generated on a macOS runner by the `grrclone-reference` workflow in this repository and
committed under `static/grrclone/reference/`. After a grrclone release, run the workflow with
the new tag and replace that directory with its output.
{{< /callout >}}
