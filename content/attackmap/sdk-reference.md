---
title: "SDK reference"
description: "Every public name in attackmap.sdk at v0.6.2: the analyzer protocol, the signal models and their fields, the allowed values, and the filesystem helpers."
weight: 110
group: "Extending"
source: "https://github.com/mlaify/AttackMap/tree/v0.6.2/src/attackmap/sdk"
---

{{< callout type="note" >}}
Generated from `attackmap.sdk` at [v0.6.2](https://github.com/mlaify/AttackMap/tree/v0.6.2/src/attackmap/sdk) by
`scripts/gen-attackmap-sdk-reference.py`. Anything importable from `attackmap.sdk` is
the stable analyzer contract; anything else in `attackmap` is internal. The
[Analyzer SDK](sdk.md) guide explains how the pieces fit together.
{{< /callout >}}

## Analyzer contract

### `AnalyzerResult` {#analyzerresult}

*Model* (pydantic). Module `attackmap.models`.

| Field | Type | Default |
|---|---|---|
| `root` | `str` | required |
| `languages` | `list[str]` | `list()` |
| `routes` | `list[Route]` | `list()` |
| `external_calls` | `list[ExternalCall]` | `list()` |
| `databases` | `list[DatabaseHint]` | `list()` |
| `auth_hints` | `list[AuthHint]` | `list()` |
| `service_hints` | `list[ServiceHint]` | `list()` |
| `edge_hints` | `list[EdgeHint]` | `list()` |
| `entrypoint_hints` | `list[EntrypointHint]` | `list()` |
| `protocol_hints` | `list[ProtocolHint]` | `list()` |
| `framework_hints` | `list[FrameworkHint]` | `list()` |
| `secret_hints` | `list[SecretHint]` | `list()` |
| `taint_chains` | `list[TaintChain]` | `list()` |
| `dependencies` | `list[DependencyHint]` | `list()` |
| `vulnerabilities` | `list[Vulnerability]` | `list()` |
| `authz_candidates` | `list[BolaCandidate]` | `list()` |
| `crypto_weaknesses` | `list[CryptoWeakness]` | `list()` |
| `web_hardening_issues` | `list[WebHardeningIssue]` | `list()` |
| `code_weaknesses` | `list[CodeWeakness]` | `list()` |
| `workflow_issues` | `list[WorkflowIssue]` | `list()` |
| `supply_chain_issues` | `list[SupplyChainIssue]` | `list()` |
| `cloud_misconfigs` | `list[CloudMisconfig]` | `list()` |
| `app_surface_issues` | `list[AppSurfaceIssue]` | `list()` |
| `secret_history` | `list[SecretHistoryHit]` | `list()` |
| `anomalies` | `list[Anomaly]` | `list()` |
| `limitations` | `list[str]` | `list()` |
| `analyzer_errors` | `list[AnalyzerError]` | `list()` |
| `files_scanned` | `int` | `0` |

### `AnalyzerMetadata` {#analyzermetadata}

*Model* (pydantic). Module `attackmap.analyzer_contracts`.

Static, self-describing metadata every analyzer exposes.

Every analyzer plugin ships a `metadata: AnalyzerMetadata` attribute so
core (and future tooling) can reason about the plugin without loading
or running it. The field set is stable: adding fields is safe on a
minor release, removing or renaming is a major-version break.

| Field | Type | Default |
|---|---|---|
| `name` | `str` | required |
| `display_name` | `str` | `''` |
| `version` | `str` | `'0.1.0'` |
| `description` | `str` | `''` |
| `scope` | `str` | `''` |
| `targets` | `list[str]` | `list()` |
| `languages` | `list[str]` | `list()` |
| `priority` | `int` | `100` |
| `experimental` | `bool` | `True` |
| `enabled_by_default` | `bool` | `False` |

### `AnalyzerRepositoryModule` {#analyzerrepositorymodule}

*Model* (pydantic). Module `attackmap.analyzer_contracts`.

| Field | Type | Default |
|---|---|---|
| `analyzer_name` | `str` | required |
| `repo_name` | `str` | required |
| `web_url` | `str` | required |

### `AnalyzerProtocol` {#analyzerprotocol}

*Protocol*.

Members:

- `metadata: AnalyzerMetadata`
- `name` (property)
- `detect(self, root: str | Path) -> bool`
- `analyze(self, root: str | Path) -> ScanResult`

### `normalize_analyzer_metadata` {#normalize_analyzer_metadata}

```python
def normalize_analyzer_metadata(value: object) -> AnalyzerMetadata
```

## Signal models

### `Route` {#route}

*Model* (pydantic). Module `attackmap.models`.

| Field | Type | Default |
|---|---|---|
| `path` | `str` | required |
| `method` | `str` | `'ANY'` |
| `file` | `str` | required |
| `line` | `int \| None` | `None` |
| `source_analyzer` | `str \| None` | `None` |
| `auth` | `Literal['required', 'anonymous', 'unknown']` | `'unknown'` |
| `guards` | `list[str]` | `list()` |
| `guard_evidence` | `str \| None` | `None` |

### `ExternalCall` {#externalcall}

*Model* (pydantic). Module `attackmap.models`.

| Field | Type | Default |
|---|---|---|
| `target` | `str` | required |
| `file` | `str` | required |
| `line` | `int \| None` | `None` |
| `method` | `str \| None` | `None` |
| `evidence_text` | `str \| None` | `None` |
| `source_analyzer` | `str \| None` | `None` |

### `DatabaseHint` {#databasehint}

*Model* (pydantic). Module `attackmap.models`.

| Field | Type | Default |
|---|---|---|
| `kind` | `str` | required |
| `file` | `str` | required |
| `line` | `int \| None` | `None` |
| `evidence_text` | `str \| None` | `None` |
| `source_analyzer` | `str \| None` | `None` |

### `AuthHint` {#authhint}

*Model* (pydantic). Module `attackmap.models`.

| Field | Type | Default |
|---|---|---|
| `hint` | `str` | required |
| `file` | `str` | required |
| `line` | `int \| None` | `None` |
| `evidence_text` | `str \| None` | `None` |
| `confidence` | `float` | `0.7` |
| `source_analyzer` | `str \| None` | `None` |

### `ServiceHint` {#servicehint}

*Model* (pydantic). Module `attackmap.models`.

| Field | Type | Default |
|---|---|---|
| `hint` | `str` | required |
| `file` | `str` | required |
| `line` | `int \| None` | `None` |
| `evidence_text` | `str \| None` | `None` |
| `confidence` | `float` | `0.7` |
| `source_analyzer` | `str \| None` | `None` |

### `EdgeHint` {#edgehint}

*Model* (pydantic). Module `attackmap.models`.

| Field | Type | Default |
|---|---|---|
| `hint` | `str` | required |
| `file` | `str` | required |
| `line` | `int \| None` | `None` |
| `evidence_text` | `str \| None` | `None` |
| `confidence` | `float` | `0.7` |
| `source_analyzer` | `str \| None` | `None` |

### `EntrypointHint` {#entrypointhint}

*Model* (pydantic). Module `attackmap.models`.

| Field | Type | Default |
|---|---|---|
| `hint` | `str` | required |
| `file` | `str` | required |
| `line` | `int \| None` | `None` |
| `evidence_text` | `str \| None` | `None` |
| `confidence` | `float` | `0.7` |
| `source_analyzer` | `str \| None` | `None` |

### `ProtocolHint` {#protocolhint}

*Model* (pydantic). Module `attackmap.models`.

| Field | Type | Default |
|---|---|---|
| `hint` | `str` | required |
| `file` | `str` | required |
| `line` | `int \| None` | `None` |
| `evidence_text` | `str \| None` | `None` |
| `confidence` | `float` | `0.7` |
| `source_analyzer` | `str \| None` | `None` |

### `FrameworkHint` {#frameworkhint}

*Model* (pydantic). Module `attackmap.models`.

| Field | Type | Default |
|---|---|---|
| `hint` | `str` | required |
| `file` | `str` | required |
| `line` | `int \| None` | `None` |
| `evidence_text` | `str \| None` | `None` |
| `confidence` | `float` | `0.7` |
| `source_analyzer` | `str \| None` | `None` |

### `SecretHint` {#secrethint}

*Model* (pydantic). Module `attackmap.models`.

| Field | Type | Default |
|---|---|---|
| `name` | `str` | required |
| `file` | `str` | required |
| `line` | `int \| None` | `None` |
| `evidence_text` | `str \| None` | `None` |
| `confidence` | `float` | `0.85` |
| `source_analyzer` | `str \| None` | `None` |
| `kind` | `str` | `'env_reference'` |

### `ScanResult` {#scanresult}

The same class as [`AnalyzerResult`](#analyzerresult), exported under a second name.

### `DependencyHint` {#dependencyhint}

*Model* (pydantic). Module `attackmap.models`.

A single third-party dependency declared in a manifest or lockfile.

Manifests (#48) carry version *ranges* verbatim (`^4.16.0`, `>=2,<3`,
`latest`) and only direct dependencies. Lockfiles (#143) carry *exact*
resolved versions and the full transitive tree — those hints set
`resolved=True` and populate `direct` / `via`.

| Field | Type | Default |
|---|---|---|
| `name` | `str` | required |
| `version` | `str` | required |
| `ecosystem` | `str` | required |
| `file` | `str` | required |
| `line` | `int \| None` | `None` |
| `dev` | `bool` | `False` |
| `resolved` | `bool` | `False` |
| `direct` | `bool` | `True` |
| `via` | `str \| None` | `None` |
| `evidence_text` | `str \| None` | `None` |
| `source_analyzer` | `str \| None` | `None` |

### `CloudMisconfig` {#cloudmisconfig}

*Model* (pydantic). Module `attackmap.models`.

A cloud, IaC or container-runtime misconfiguration (terraform#4, iac#1).

Emitted by IaC plugins (Terraform, Kubernetes / Helm, compose,
Dockerfile). Like the other issue families, each one is a
positively-present setting (or a documented insecure default that the
file leaves in place) at a file and line. Core turns each `kind` into
findings, one per (kind, severity) tier, so a low `/var/log` mount never
inherits the severity of a `docker.sock` mount of the same kind.

- `kind`: one of `CLOUD_MISCONFIG_KINDS`. Typed `str` so a plugin built
  against a newer core still validates here; core drops records with a
  kind it doesn't know (noted under `analyzer_errors`) and keeps the rest
  of the plugin's result.
- `resource`: what the setting belongs to, e.g. `aws_eks_cluster.main`,
  `Deployment/web container app`, `module.vpc`.
- `platform`: one of `CLOUD_MISCONFIG_PLATFORMS`.
- `context`: how the resource is instantiated — `for_each`/`count`,
  the calling module of a local module, a Helm template.
- `escalation_path`: what an attacker gets from it, in one line, e.g.
  `hostPath / → node root → kubelet credentials`.

The free-text fields are redacted, folded to one line and capped.

| Field | Type | Default |
|---|---|---|
| `kind` | `str` | required |
| `file` | `str` | required |
| `line` | `int \| None` | `None` |
| `resource` | `str \| None` | `None` |
| `platform` | `Literal['aws', 'azure', 'gcp', 'kubernetes', 'helm', 'compose', 'docker', 'terraform'] \| None` | `None` |
| `context` | `str \| None` | `None` |
| `escalation_path` | `str \| None` | `None` |
| `evidence_text` | `str \| None` | `None` |
| `severity` | `Literal['low', 'medium', 'high']` | `'medium'` |
| `confidence` | `float` | `0.8` |
| `source_analyzer` | `str \| None` | `None` |

### `AppSurfaceIssue` {#appsurfaceissue}

*Model* (pydantic). Module `attackmap.models`.

A mobile/desktop app attack-surface issue emitted by a platform plugin
(#188, #190): the Apple analyzers (Swift, Objective-C) report App Transport
Security exceptions, custom URL-scheme handlers, weakening entitlements,
WKWebView script built from strings, secrets in UserDefaults or on the
pasteboard, unvalidated XPC peers, and classes, selectors or libraries
resolved from runtime strings. Native format-string and command-exec
constructs are `CodeWeakness` kinds shared with the C/C++ plugins.

Core owns the findings: one aggregated finding per kind (rule id = the
kind, dashed), at the most severe instance's severity. Like the other
issue families, every instance is a positively-present construct, never
an absence.

`kind` is one of `APP_SURFACE_ISSUE_KINDS` but typed `str`, so a
plugin built against a newer core still validates: core drops records
with a kind it doesn't know (noted under `analyzer_errors`) and keeps
the rest of the plugin's result.

| Field | Type | Default |
|---|---|---|
| `kind` | `str` | required |
| `file` | `str` | required |
| `line` | `int \| None` | `None` |
| `evidence_text` | `str \| None` | `None` |
| `severity` | `Literal['low', 'medium', 'high']` | `'medium'` |
| `confidence` | `float` | `0.8` |
| `source_analyzer` | `str \| None` | `None` |

### `CodeWeakness` {#codeweakness}

*Model* (pydantic). Module `attackmap.models`.

A novel vulnerability-class weakness in source (#77).

Emitted by the built-in `weaknesses` finder — bug classes beyond the
taint/crypto/web-hardening families, detected from concrete risky
constructs (not absence).

| Field | Type | Default |
|---|---|---|
| `kind` | `str` | required |
| `file` | `str` | required |
| `line` | `int \| None` | `None` |
| `evidence_text` | `str \| None` | `None` |
| `severity` | `Literal['low', 'medium', 'high']` | `'medium'` |
| `confidence` | `Literal['low', 'medium', 'high'] \| None` | `None` |
| `source_kind` | `str \| None` | `None` |
| `source_line` | `int \| None` | `None` |
| `source_analyzer` | `str \| None` | `None` |

### `SupplyChainIssue` {#supplychainissue}

*Model* (pydantic). Module `attackmap.models`.

A dependency supply-chain risk beyond CVEs (#247).

Emitted by the built-in, offline `supply_chain` pass over manifests,
lockfiles and package-manager configs: dependency confusion, typosquat
candidates, mutable VCS/URL dependencies, install scripts, unlocked
manifests and insecure registries.

| Field | Type | Default |
|---|---|---|
| `kind` | `Literal['dependency_confusion', 'typosquat_candidate', 'mutable_vcs_dependency', 'install_script', 'unlocked_manifest', 'insecure_registry']` | required |
| `file` | `str` | required |
| `line` | `int \| None` | `None` |
| `package` | `str \| None` | `None` |
| `ecosystem` | `str \| None` | `None` |
| `evidence_text` | `str \| None` | `None` |
| `severity` | `Literal['low', 'medium', 'high']` | `'medium'` |
| `source_analyzer` | `str \| None` | `None` |

## Allowed values

### `DependencyEcosystem` {#dependencyecosystem}

*Type*: one of `'pypi'`, `'npm'`, `'go'`, `'cargo'`, `'composer'`, `'swiftpm'`, `'maven'`, `'nuget'`, `'conan'`, `'vcpkg'`, `'cmake'`, `'gem'`, `'cocoapods'`, `'carthage'`, `'hex'`, `'pub'`.

### `DEPENDENCY_ECOSYSTEMS` {#dependency_ecosystems}

tuple of 16: `pypi`, `npm`, `go`, `cargo`, `composer`, `swiftpm`, `maven`, `nuget`, `conan`, `vcpkg`, `cmake`, `gem`, `cocoapods`, `carthage`, `hex`, `pub`

### `CloudMisconfigKind` {#cloudmisconfigkind}

*Type*: one of `'iac_module_unpinned'`, `'public_network_access'`, `'public_cluster_endpoint'`, `'plaintext_listener'`, `'api_no_authorizer'`, `'unencrypted_storage'`, `'public_data_access'`, `'public_invoker'`, `'privileged_container'`, `'privilege_escalation_allowed'`, `'container_runs_as_root'`, `'missing_security_context'`, `'host_path_mount'`, `'host_namespace_shared'`, `'dangerous_capability'`, `'security_profile_disabled'`, `'exposed_service'`, `'unpinned_container_image'`, `'dockerfile_remote_add'`, `'dockerfile_curl_pipe_shell'`, `'rbac_wildcard'`, `'rbac_escalation'`, `'rbac_secret_access'`, `'cluster_admin_binding'`.

### `CLOUD_MISCONFIG_KINDS` {#cloud_misconfig_kinds}

tuple of 24: `iac_module_unpinned`, `public_network_access`, `public_cluster_endpoint`, `plaintext_listener`, `api_no_authorizer`, `unencrypted_storage`, `public_data_access`, `public_invoker`, `privileged_container`, `privilege_escalation_allowed`, `container_runs_as_root`, `missing_security_context`, `host_path_mount`, `host_namespace_shared`, `dangerous_capability`, `security_profile_disabled`, `exposed_service`, `unpinned_container_image`, `dockerfile_remote_add`, `dockerfile_curl_pipe_shell`, `rbac_wildcard`, `rbac_escalation`, `rbac_secret_access`, `cluster_admin_binding`

### `CloudMisconfigPlatform` {#cloudmisconfigplatform}

*Type*: one of `'aws'`, `'azure'`, `'gcp'`, `'kubernetes'`, `'helm'`, `'compose'`, `'docker'`, `'terraform'`.

### `CLOUD_MISCONFIG_PLATFORMS` {#cloud_misconfig_platforms}

tuple of 8: `aws`, `azure`, `gcp`, `kubernetes`, `helm`, `compose`, `docker`, `terraform`

### `AppSurfaceIssueKind` {#appsurfaceissuekind}

*Type*: one of `'apple_ats_insecure_loads'`, `'apple_custom_url_scheme'`, `'apple_webview_js_injection'`, `'apple_insecure_secret_storage'`, `'apple_pasteboard_secret'`, `'apple_hardened_runtime_exception'`, `'apple_debuggable_entitlement'`, `'apple_xpc_unvalidated_peer'`, `'apple_dynamic_dispatch'`.

### `APP_SURFACE_ISSUE_KINDS` {#app_surface_issue_kinds}

tuple of 9: `apple_ats_insecure_loads`, `apple_custom_url_scheme`, `apple_webview_js_injection`, `apple_insecure_secret_storage`, `apple_pasteboard_secret`, `apple_hardened_runtime_exception`, `apple_debuggable_entitlement`, `apple_xpc_unvalidated_peer`, `apple_dynamic_dispatch`

### `CODE_WEAKNESS_KINDS` {#code_weakness_kinds}

tuple of 26: `prototype_pollution`, `mass_assignment`, `jwt_weakness`, `jwt_alg_confusion`, `jwt_unverified_decode`, `jwt_claims_unchecked`, `jwt_header_trust`, `jwt_weak_secret`, `oauth_missing_state`, `oauth_implicit_flow`, `oauth_redirect_uri_loose`, `oauth_missing_pkce`, `session_fixation`, `session_weak_secret`, `xxe`, `redos`, `insecure_upload`, `graphql_exposure`, `graphql_no_query_limits`, `graphql_batching`, `prompt_injection_attempt`, `unbounded_copy`, `format_string`, `native_command_exec`, `tainted_copy_length`, `alloc_size_overflow`

## Filesystem helpers

### `walk_repo` {#walk_repo}

```python
def walk_repo(root: str | Path, *, prune: Callable[[str], bool] | None = None, on_symlink: Callable[[Path], None] | None = None) -> Iterator[Path]
```

Yield regular files under `root` (depth-first, sorted per directory).

Symlinks are skipped — symlinked files are not yielded and symlinked
directories are not descended — and `on_symlink(path)` is called for
each. With `ATTACKMAP_FOLLOW_SYMLINKS=1` symlinks whose target resolves
inside `root` are followed (cycle-safe); ones pointing outside are still
skipped. `prune(dirname)` returning True skips descending into a
directory.

### `is_contained` {#is_contained}

```python
def is_contained(root: str | Path, path: str | Path) -> bool
```

True when `path` is inside `root` and is not reached via a symlink.

Every component between `root` and `path` is checked with `lstat` —
a symlinked directory in the middle of the path disqualifies it just like
a symlinked file. With `ATTACKMAP_FOLLOW_SYMLINKS=1` symlinks are allowed
as long as the fully resolved path stays inside `root`.

### `contained_file` {#contained_file}

```python
def contained_file(root: str | Path, rel: str | Path) -> Path | None
```

Resolve a repo-relative path from untrusted text (evidence, plugin
output) to a regular file inside `root`, or `None`.

Absolute paths and paths with `..` components are rejected outright.

### `read_repo_text` {#read_repo_text}

```python
def read_repo_text(root: str | Path, path: str | Path, *, encoding: str = 'utf-8', errors: str = 'strict') -> str
```

`Path.read_text` that refuses paths outside `root` or behind a symlink.

### `DEFAULT_SKIP_DIRS` {#default_skip_dirs}

frozenset of 18: `.attackmap`, `.attackmap-gui`, `.git`, `.mypy_cache`, `.next`, `.pytest_cache`, `.tox`, `.turbo`, `.venv`, `__pycache__`, `bower_components`, `build`, `dist`, `node_modules`, `out`, `target`, `vendor`, `venv`

### `iter_repo_files` {#iter_repo_files}

```python
def iter_repo_files(root: str | Path, *, suffixes: Collection[str] | None = None, names: Collection[str] | None = None, skip_dirs: Collection[str] = frozenset({'.git', '.venv', 'out', '__pycache__', '.attackmap', 'bower_components', 'dist', '.tox', 'node_modules', '.attackmap-gui', '.mypy_cache', '.turbo', 'venv', 'vendor', '.pytest_cache', 'build', 'target', '.next'}), max_bytes: int | None = None, include_tests: bool = True, on_skip: Callable[[Path, str], None] | None = None) -> Iterator[Path]
```

Yield the repo's regular files, sorted and depth-first.

- `suffixes` (e.g. `{".go"}`, case-insensitive) and `names` (exact
  file names, e.g. `{"go.mod"}`) filter the files; a file matching
  either is yielded. With neither, every file is.
- `skip_dirs` are matched against directory *names inside the repo* and
  pruned, so the walk never enters them, and directories above `root`
  never count.
- Files larger than `max_bytes` (default: the core per-file cap,
  `ATTACKMAP_MAX_FILE_BYTES`) are skipped.
- `include_tests=False` drops test/spec/fixture files (see
  `ATTACKMAP_INCLUDE_TESTS`).
- `on_skip(path, reason)` is called for each skipped symlink or
  oversized file, so a plugin can report what it didn't analyze.

### `read_source` {#read_source}

```python
def read_source(path: str | Path, *, root: str | Path | None = None) -> str | None
```

Read a source file as text, or return None if it can't be read.

Decodes UTF-8 (with or without a BOM), then falls back to cp1252 and finally
latin-1, so legacy-encoded sources are analyzed rather than dropped.
Returns None for unreadable files (`OSError`), binary files (a NUL byte
in the first 8 KiB) and, when `root` is given, paths outside it.

### `rel` {#rel}

```python
def rel(path: str | Path, root: str | Path) -> str
```

`path` relative to `root`, POSIX-style (`src/app.py`).

### `line_of` {#line_of}

```python
def line_of(content: str, offset: int) -> int
```

1-indexed line of a character offset (e.g. `match.start()`).

### `line_snippet` {#line_snippet}

```python
def line_snippet(content: str, line: int, max_len: int = 200) -> str
```

The stripped text of 1-indexed `line`, truncated to `max_len`.

    Lines are split on `
` only, matching `line_of`; `str.splitlines`
    would also break on form feeds and other separators common in legacy C and
    put the snippet on the wrong line.
    

## Taint sink plugins

### `TAINT_SINK_PLUGIN_GROUP` {#taint_sink_plugin_group}

`'attackmap.taint_sinks'`

### `TAINT_SINK_KINDS` {#taint_sink_kinds}

tuple of 19: `sql_execute`, `subprocess_shell`, `eval`, `exec`, `dynamic_open`, `path_traversal`, `zip_slip`, `unsafe_deserialization`, `ssti`, `ssrf`, `nosql_injection`, `open_redirect`, `code_injection`, `expression_injection`, `jndi_injection`, `ldap_injection`, `xpath_injection`, `header_injection`, `regex_injection`

### `validate_taint_sink` {#validate_taint_sink}

```python
def validate_taint_sink(entry: Any, kinds: dict[str, KindMeta] | None = None, *, source: str = 'core') -> SinkSpec
```

Validate one registry entry and compile it. Raises SinkRegistryError.

Every sink must name a known `kind`, at least one language, a compiling
`regex` and a `cwe` — a sink without a CWE can't be tagged or mapped,
so it is rejected outright.
