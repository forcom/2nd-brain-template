#!/usr/bin/env python3
"""Validate deterministic wiki gates and stamp shared graph input metadata."""

from __future__ import annotations

import argparse
import ast
import datetime as dt
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


CANONICAL_DIRS = {
    "entities": "entity",
    "concepts": "concept",
    "comparisons": "comparison",
    "queries": "query",
}
REQUIRED_CANONICAL_FIELDS = {
    "title",
    "created",
    "updated",
    "type",
    "tags",
    "sources",
    "confidence",
    "contested",
    "contradictions",
}
ALLOWED_LOG_ACTIONS = {
    "ingest",
    "create",
    "update",
    "query",
    "lint",
    "archive",
    "delete",
    "map",
    "repair",
}
REQUIRED_GRAPH_NODE_FIELDS = {"id", "type", "name", "summary", "tags", "complexity"}
GRAPH_INFRA_FILES = {"index.md", "log.md", "claude.md", "agents.md", "soul.md"}
GRAPH_OUTPUT_PATHS = {
    ".understand-anything/knowledge-graph.json",
    ".understand-anything/meta.json",
}
GRAPH_INPUT_HASH_ALGORITHM = "sha256-path-size-bytes-v1"


def relative(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return str(path)


def result(name: str) -> dict[str, Any]:
    return {"name": name, "ok": True, "errors": [], "warnings": [], "metrics": {}}


def add_error(gate: dict[str, Any], message: str) -> None:
    gate["errors"].append(message)
    gate["ok"] = False


def add_warning(gate: dict[str, Any], message: str) -> None:
    gate["warnings"].append(message)


def read_bytes(path: Path, root: Path, gate: dict[str, Any]) -> bytes | None:
    try:
        data = path.read_bytes()
    except OSError as exc:
        add_error(gate, f"{relative(path, root)}: read failed: {exc}")
        return None
    if data.startswith(bytes((239, 187, 191))):
        add_error(gate, f"{relative(path, root)}: UTF-8 BOM is not allowed")
    if b"\r" in data:
        add_error(gate, f"{relative(path, root)}: non-LF line ending")
    try:
        data.decode("utf-8")
    except UnicodeDecodeError as exc:
        add_error(gate, f"{relative(path, root)}: invalid UTF-8: {exc}")
        return None
    return data


def split_frontmatter(
    data: bytes, path: Path, root: Path, gate: dict[str, Any]
) -> tuple[dict[str, Any] | None, bytes]:
    if not data.startswith(b"---\n"):
        return None, data
    end = data.find(b"\n---\n", 4)
    if end < 0:
        add_error(gate, f"{relative(path, root)}: missing closing frontmatter delimiter")
        return None, b""
    parsed: dict[str, Any] = {}
    active_list: str | None = None
    frontmatter_text = data[4:end].decode("utf-8")
    for line_number, line in enumerate(frontmatter_text.splitlines(), 1):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line.startswith("  - "):
            if active_list is None:
                add_error(
                    gate,
                    f"{relative(path, root)}: frontmatter line {line_number} "
                    "has a list item without a key",
                )
                return None, data[end + 5 :]
            try:
                parsed[active_list].append(parse_yaml_scalar(line[4:]))
            except ValueError as exc:
                add_error(
                    gate,
                    f"{relative(path, root)}: invalid frontmatter line "
                    f"{line_number}: {exc}",
                )
                return None, data[end + 5 :]
            continue
        if line[0].isspace():
            add_error(
                gate,
                f"{relative(path, root)}: unsupported nested frontmatter "
                f"at line {line_number}",
            )
            return None, data[end + 5 :]
        match = re.fullmatch(r"([A-Za-z_][A-Za-z0-9_-]*):(.*)", line)
        if match is None:
            add_error(
                gate,
                f"{relative(path, root)}: malformed frontmatter line {line_number}",
            )
            return None, data[end + 5 :]
        key, raw_value = match.groups()
        if key in parsed:
            add_error(gate, f"{relative(path, root)}: duplicate frontmatter key {key!r}")
            return None, data[end + 5 :]
        raw_value = raw_value.strip()
        if not raw_value:
            parsed[key] = []
            active_list = key
            continue
        try:
            parsed[key] = parse_yaml_scalar(raw_value)
        except ValueError as exc:
            add_error(
                gate,
                f"{relative(path, root)}: invalid frontmatter line "
                f"{line_number}: {exc}",
            )
            return None, data[end + 5 :]
        active_list = None
    return parsed, data[end + 5 :]


def parse_yaml_scalar(value: str) -> Any:
    """Parse the flat YAML scalar/list subset used by this repository."""
    lowered = value.casefold()
    if lowered in {"true", "false"}:
        return lowered == "true"
    if lowered in {"null", "~"}:
        return None
    if value == "[]":
        return []
    if value == "{}":
        return {}
    if value.startswith('"'):
        try:
            parsed = json.loads(value)
        except json.JSONDecodeError as exc:
            raise ValueError(f"invalid double-quoted scalar: {exc.msg}") from exc
        if not isinstance(parsed, str):
            raise ValueError("double-quoted scalar must be a string")
        return parsed
    if value.startswith("'"):
        if not value.endswith("'") or len(value) < 2:
            raise ValueError("unterminated single-quoted scalar")
        return value[1:-1].replace("''", "'")
    if value.startswith("["):
        if not value.endswith("]"):
            raise ValueError("unterminated inline list")
        try:
            parsed = ast.literal_eval(value)
        except (SyntaxError, ValueError):
            inner = value[1:-1].strip()
            return [] if not inner else [parse_yaml_scalar(item.strip()) for item in inner.split(",")]
        if not isinstance(parsed, list):
            raise ValueError("inline collection must be a list")
        return parsed
    if re.fullmatch(r"-?\d+", value):
        return int(value)
    return value


def git_output(root: Path, *args: str) -> str:
    completed = subprocess.run(
        ["git", "-C", str(root), *args],
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode != 0:
        return ""
    return completed.stdout.strip()


def git_succeeds(root: Path, *args: str) -> bool:
    completed = subprocess.run(
        ["git", "-C", str(root), *args],
        check=False,
        capture_output=True,
    )
    return completed.returncode == 0


def git_paths(root: Path, *args: str) -> set[str]:
    completed = subprocess.run(
        ["git", "-C", str(root), *args],
        check=False,
        capture_output=True,
    )
    if completed.returncode != 0:
        return set()
    return {
        value.decode("utf-8", errors="surrogateescape")
        for value in completed.stdout.split(b"\0")
        if value
    }


def repository_candidate_paths(root: Path) -> set[str]:
    return git_paths(
        root,
        "ls-files",
        "-z",
        "--cached",
        "--others",
        "--exclude-standard",
    )


def graph_article_paths(root: Path) -> set[str]:
    paths: set[str] = set()
    for value in repository_candidate_paths(root):
        relative_path = Path(value)
        if relative_path.suffix != ".md" or not (root / relative_path).is_file():
            continue
        if (
            relative_path.parent == Path(".")
            and relative_path.name.casefold() in GRAPH_INFRA_FILES
        ):
            continue
        paths.add(relative_path.as_posix())
    return paths


def graph_source_paths(root: Path) -> set[str]:
    paths: set[str] = set()
    for value in repository_candidate_paths(root):
        relative_path = Path(value)
        if (
            relative_path.parts
            and relative_path.parts[0] == "raw"
            and not relative_path.name.startswith(".")
            and (root / relative_path).is_file()
        ):
            paths.add(relative_path.as_posix())
    return paths


def graph_input_fingerprint(root: Path) -> tuple[str, list[str]]:
    input_paths = graph_article_paths(root) | graph_source_paths(root)
    for infrastructure_file in ("index.md", "log.md"):
        if (root / infrastructure_file).is_file():
            input_paths.add(infrastructure_file)

    digest = hashlib.sha256()
    digest.update(f"{GRAPH_INPUT_HASH_ALGORITHM}\0".encode("utf-8"))
    ordered_paths = sorted(input_paths, key=lambda value: value.encode("utf-8"))
    for relative_path in ordered_paths:
        data = (root / relative_path).read_bytes()
        digest.update(relative_path.encode("utf-8"))
        digest.update(b"\0")
        digest.update(str(len(data)).encode("ascii"))
        digest.update(b"\0")
        digest.update(data)
        digest.update(b"\0")
    return f"sha256:{digest.hexdigest()}", ordered_paths


def write_graph_input_metadata(root: Path) -> dict[str, Any]:
    meta_path = root / ".understand-anything" / "meta.json"
    if not meta_path.is_file():
        raise ValueError("knowledge graph metadata file is missing")
    try:
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"graph metadata parse failed: {exc}") from exc
    if not isinstance(meta, dict):
        raise ValueError("graph metadata must be a JSON object")

    input_hash, input_paths = graph_input_fingerprint(root)
    meta["inputHash"] = input_hash
    meta["inputHashAlgorithm"] = GRAPH_INPUT_HASH_ALGORITHM
    meta["inputFiles"] = len(input_paths)
    meta_path.write_text(
        json.dumps(meta, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return {
        "ok": True,
        "meta": relative(meta_path, root),
        "inputHash": input_hash,
        "inputHashAlgorithm": GRAPH_INPUT_HASH_ALGORITHM,
        "inputFiles": len(input_paths),
    }


def validate_repository_state(
    root: Path,
    gate: dict[str, Any],
    allow_graph_output_changes: bool = False,
) -> None:
    branch = git_output(root, "branch", "--show-current")
    status = git_output(root, "status", "--porcelain", "--untracked-files=all")
    gate["metrics"]["git_branch"] = branch
    gate["metrics"]["git_head"] = git_output(root, "rev-parse", "HEAD")
    if branch != "main":
        add_error(gate, f"automation requires branch 'main'; current branch is {branch!r}")
    if not status:
        return
    if not allow_graph_output_changes:
        add_error(gate, "automation requires a clean worktree")
        return

    changed_paths = set()
    changed_paths.update(git_paths(root, "diff", "--name-only", "-z"))
    changed_paths.update(git_paths(root, "diff", "--cached", "--name-only", "-z"))
    changed_paths.update(
        git_paths(root, "ls-files", "-z", "--others", "--exclude-standard")
    )
    unexpected = sorted(changed_paths - GRAPH_OUTPUT_PATHS, key=str.casefold)
    if unexpected or not changed_paths:
        add_error(
            gate,
            "automation permits dirty state only for versioned graph outputs; "
            f"unexpected={unexpected}",
        )
        return
    gate["metrics"]["allowed_graph_output_changes"] = sorted(changed_paths)


def validate_gate_a(root: Path) -> dict[str, Any]:
    gate = result("A")
    required_data: dict[str, bytes] = {}
    for required in ("SCHEMA.md", "index.md", "log.md"):
        path = root / required
        if not path.is_file():
            add_error(gate, f"missing required wiki file: {required}")
            continue
        data = read_bytes(path, root, gate)
        if data is not None:
            required_data[required] = data
            if not data.endswith(b"\n"):
                add_error(gate, f"{required}: missing final LF")

    raw_root = root / "raw"
    raw_paths = sorted(raw_root.rglob("*.md")) if raw_root.is_dir() else []
    log_text = required_data.get("log.md", b"").decode("utf-8")
    hash_checked = 0
    legacy_gaps = 0
    for path in raw_paths:
        data = read_bytes(path, root, gate)
        if data is None:
            continue
        frontmatter, body = split_frontmatter(data, path, root, gate)
        if frontmatter is None:
            legacy_gaps += 1
            path_value = relative(path, root)
            add_warning(gate, f"{path_value}: legacy record without frontmatter/hash")
            if path_value not in log_text:
                add_error(gate, f"{path_value}: legacy coverage gap is not documented in log.md")
            continue
        recorded_hash = frontmatter.get("sha256")
        if not recorded_hash:
            legacy_gaps += 1
            path_value = relative(path, root)
            add_warning(gate, f"{path_value}: documented hash-coverage gap")
            if path_value not in log_text:
                add_error(gate, f"{path_value}: hash-coverage gap is not documented in log.md")
            continue
        hash_checked += 1
        actual_hash = hashlib.sha256(body).hexdigest()
        if str(recorded_hash) != actual_hash:
            add_error(gate, f"{relative(path, root)}: post-frontmatter sha256 mismatch")
        if not data.endswith(b"\n"):
            add_error(gate, f"{relative(path, root)}: hashed raw record lacks final LF")

    gate["metrics"].update(
        {
            "raw_records": len(raw_paths),
            "raw_hashes_checked": hash_checked,
            "legacy_coverage_gaps": legacy_gaps,
        }
    )
    return gate


def registered_raw_prefixes(schema_text: str) -> tuple[str, ...]:
    paths = re.findall(r"^\| `([^`]+)` \|", schema_text, re.MULTILINE)
    prefixes = []
    for path in paths:
        if path.startswith("raw/") and path.endswith("/") and not path.endswith("/files/"):
            prefixes.append(path)
    return tuple(prefixes)


def is_valid_date(value: Any) -> bool:
    if isinstance(value, dt.date):
        return True
    if isinstance(value, str):
        try:
            dt.date.fromisoformat(value)
            return True
        except ValueError:
            return False
    return False


def validate_gate_b(root: Path) -> dict[str, Any]:
    gate = result("B")
    schema_path = root / "SCHEMA.md"
    index_path = root / "index.md"
    log_path = root / "log.md"
    if not all(path.is_file() for path in (schema_path, index_path, log_path)):
        add_error(gate, "Gate B requires SCHEMA.md, index.md, and log.md")
        return gate

    support_data: dict[Path, bytes] = {}
    for path in (schema_path, index_path, log_path):
        data = read_bytes(path, root, gate)
        if data is None:
            continue
        support_data[path] = data
        if not data.endswith(b"\n"):
            add_error(gate, f"{relative(path, root)}: missing final LF")
    if len(support_data) != 3:
        return gate

    schema_text = support_data[schema_path].decode("utf-8")
    registered_tags = set(re.findall(r"^- `([^`]+)`: ", schema_text, re.MULTILINE))
    source_prefixes = registered_raw_prefixes(schema_text)
    if not source_prefixes:
        add_error(gate, "SCHEMA.md does not register any raw source directory")

    page_data: dict[Path, tuple[dict[str, Any], str]] = {}
    slug_to_path: dict[str, Path] = {}
    source_references = 0
    claim_markers = 0

    for directory, expected_type in CANONICAL_DIRS.items():
        for path in sorted((root / directory).glob("*.md")):
            data = read_bytes(path, root, gate)
            if data is None:
                continue
            if not data.endswith(b"\n"):
                add_error(gate, f"{relative(path, root)}: missing final LF")
            if len(data.decode("utf-8").splitlines()) > 200:
                add_error(gate, f"{relative(path, root)}: exceeds 200 lines")
            frontmatter, body = split_frontmatter(data, path, root, gate)
            if frontmatter is None:
                add_error(gate, f"{relative(path, root)}: canonical frontmatter must start at byte zero")
                continue
            missing = REQUIRED_CANONICAL_FIELDS - set(frontmatter)
            if missing:
                add_error(gate, f"{relative(path, root)}: missing fields {sorted(missing)}")
            if not isinstance(frontmatter.get("title"), str) or not frontmatter.get("title"):
                add_error(gate, f"{relative(path, root)}: title must be a non-empty string")
            if frontmatter.get("type") != expected_type:
                add_error(gate, f"{relative(path, root)}: type must be {expected_type!r}")
            if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*\.md", path.name):
                add_error(gate, f"{relative(path, root)}: invalid canonical filename")
            for field in ("created", "updated"):
                if not is_valid_date(frontmatter.get(field)):
                    add_error(gate, f"{relative(path, root)}: invalid {field}")
            if is_valid_date(frontmatter.get("created")) and is_valid_date(
                frontmatter.get("updated")
            ):
                created = dt.date.fromisoformat(str(frontmatter["created"]))
                updated = dt.date.fromisoformat(str(frontmatter["updated"]))
                if updated < created:
                    add_error(gate, f"{relative(path, root)}: updated precedes created")
            if frontmatter.get("confidence") not in {"high", "medium", "low"}:
                add_error(gate, f"{relative(path, root)}: invalid confidence")
            if not isinstance(frontmatter.get("contested"), bool):
                add_error(gate, f"{relative(path, root)}: contested must be boolean")
            contradictions = frontmatter.get("contradictions")
            if not isinstance(contradictions, list):
                add_error(gate, f"{relative(path, root)}: contradictions must be a list")
            tags = frontmatter.get("tags")
            if not isinstance(tags, list):
                add_error(gate, f"{relative(path, root)}: tags must be a list")
            else:
                for tag in tags:
                    if not isinstance(tag, str) or tag not in registered_tags:
                        add_error(gate, f"{relative(path, root)}: unregistered tag {tag!r}")
                string_tags = [tag for tag in tags if isinstance(tag, str)]
                if len(string_tags) != len(set(string_tags)):
                    add_error(gate, f"{relative(path, root)}: duplicate tags")

            sources = frontmatter.get("sources")
            if not isinstance(sources, list):
                add_error(gate, f"{relative(path, root)}: sources must be a list")
                sources = []
            elif len(sources) != len(set(map(str, sources))):
                add_error(gate, f"{relative(path, root)}: duplicate sources")
            source_references += len(sources)
            for source in sources:
                if not isinstance(source, str):
                    add_error(gate, f"{relative(path, root)}: source must be a string: {source!r}")
                    continue
                source_value = str(source)
                source_path = root / source_value
                source_parts = Path(source_value).parts
                if (
                    Path(source_value).is_absolute()
                    or ".." in source_parts
                    or not source_value.endswith(".md")
                    or not source_value.startswith(source_prefixes)
                    or source_value.startswith("raw/papers/files/")
                    or not source_path.is_file()
                ):
                    add_error(gate, f"{relative(path, root)}: invalid source {source_value!r}")
            if frontmatter.get("confidence") == "high" and len(set(map(str, sources))) < 2:
                add_error(
                    gate,
                    f"{relative(path, root)}: high confidence requires multiple sources",
                )

            body_text = body.decode("utf-8")
            markers = re.findall(r"\^\[(raw/[^\]]+\.md)\]", body_text)
            claim_markers += len(markers)
            for marker in markers:
                if marker not in sources:
                    add_error(gate, f"{relative(path, root)}: marker absent from sources: {marker}")
                if not (root / marker).is_file():
                    add_error(gate, f"{relative(path, root)}: unresolved marker: {marker}")

            if path.stem in slug_to_path:
                add_error(gate, f"duplicate canonical slug: {path.stem}")
            slug_to_path[path.stem] = path
            page_data[path] = (frontmatter, body_text)

    canonical_links = 0
    for path, (frontmatter, body_text) in page_data.items():
        targets: set[str] = set()
        for target in re.findall(r"\[\[([^\]|#]+)", body_text):
            slug = Path(target).name
            if slug == path.stem:
                add_error(gate, f"{relative(path, root)}: self-link {target!r}")
            elif slug not in slug_to_path:
                add_error(gate, f"{relative(path, root)}: broken canonical link {target!r}")
            else:
                targets.add(slug)
        canonical_links += len(targets)
        if len(targets) < 2:
            add_error(gate, f"{relative(path, root)}: fewer than two outbound canonical links")
        contradictions = frontmatter.get("contradictions")
        if isinstance(contradictions, list):
            for slug in contradictions:
                if not isinstance(slug, str) or slug == path.stem or slug not in slug_to_path:
                    add_error(gate, f"{relative(path, root)}: invalid contradiction slug {slug!r}")

    index_text = support_data[index_path].decode("utf-8")
    index_slugs = re.findall(r"^- \[\[([^\]|#]+)", index_text, re.MULTILINE)
    if len(index_slugs) != len(set(index_slugs)):
        add_error(gate, "index.md contains duplicate canonical entries")
    if set(index_slugs) != set(slug_to_path):
        missing = sorted(set(slug_to_path) - set(index_slugs))
        extra = sorted(set(index_slugs) - set(slug_to_path))
        add_error(gate, f"index.md mismatch: missing={missing}, extra={extra}")
    count_match = re.search(r"Total pages: (\d+)", index_text)
    if not count_match or int(count_match.group(1)) != len(page_data):
        add_error(gate, f"index.md total must equal {len(page_data)}")

    section_directories = {
        "Entities": "entities",
        "Concepts": "concepts",
        "Comparisons": "comparisons",
        "Queries": "queries",
    }
    section_entries: dict[str, list[str]] = {section: [] for section in section_directories}
    current_section: str | None = None
    for line in index_text.splitlines():
        heading = re.fullmatch(r"## (.+)", line)
        if heading:
            current_section = heading.group(1) if heading.group(1) in section_directories else None
            continue
        entry = re.match(r"^- \[\[([^\]|#]+)", line)
        if not entry:
            continue
        slug = entry.group(1)
        if current_section is None:
            add_error(gate, f"index.md: entry {slug!r} is outside a canonical type section")
            continue
        section_entries[current_section].append(slug)
        page_path = slug_to_path.get(slug)
        expected_directory = section_directories[current_section]
        if page_path is not None and page_path.parent.name != expected_directory:
            add_error(
                gate,
                f"index.md: {slug!r} is under {current_section} but belongs to {page_path.parent.name}",
            )
    for section, entries in section_entries.items():
        if entries != sorted(entries, key=str.casefold):
            add_error(gate, f"index.md: {section} entries are not alphabetically sorted")

    log_text = support_data[log_path].decode("utf-8")
    log_heading_pattern = re.compile(r"^## \[(\d{4}-\d{2}-\d{2})\] ([a-z]+) \| .+$")
    for line in (value for value in log_text.splitlines() if value.startswith("## [")):
        heading = log_heading_pattern.fullmatch(line)
        if heading is None:
            add_error(gate, f"log.md: malformed operation heading {line!r}")
            continue
        date_value, action = heading.groups()
        if not is_valid_date(date_value):
            add_error(gate, f"log.md: invalid date {date_value!r}")
        if action not in ALLOWED_LOG_ACTIONS:
            add_error(gate, f"log.md: invalid action {action!r}")

    gate["metrics"].update(
        {
            "canonical_pages": len(page_data),
            "index_entries": len(index_slugs),
            "registered_tags": len(registered_tags),
            "source_references": source_references,
            "claim_markers": claim_markers,
            "canonical_link_targets": canonical_links,
        }
    )
    return gate


def validate_gate_c(root: Path) -> dict[str, Any]:
    gate = result("C")
    graph_path = root / ".understand-anything" / "knowledge-graph.json"
    meta_path = root / ".understand-anything" / "meta.json"
    if not graph_path.is_file() or not meta_path.is_file():
        add_error(gate, "knowledge graph or metadata file is missing")
        return gate

    try:
        graph = json.loads(graph_path.read_text(encoding="utf-8"))
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        add_error(gate, f"graph JSON parse failed: {exc}")
        return gate
    if not isinstance(graph, dict) or not isinstance(meta, dict):
        add_error(gate, "graph and metadata must be JSON objects")
        return gate

    if graph.get("kind") != "knowledge":
        add_error(gate, "graph kind must be 'knowledge'")
    nodes = graph.get("nodes")
    edges = graph.get("edges")
    if not isinstance(nodes, list) or not isinstance(edges, list):
        add_error(gate, "graph nodes and edges must be lists")
        return gate
    if not isinstance(graph.get("layers"), list) or not graph.get("layers"):
        add_error(gate, "graph layers must be a non-empty list")
    if not isinstance(graph.get("tour"), list) or not graph.get("tour"):
        add_error(gate, "graph tour must be a non-empty list")

    node_ids: set[str] = set()
    article_node_ids: set[str] = set()
    source_node_ids: set[str] = set()
    for index, node in enumerate(nodes):
        if not isinstance(node, dict):
            add_error(gate, f"node {index}: must be an object")
            continue
        missing = REQUIRED_GRAPH_NODE_FIELDS - set(node)
        if missing:
            add_error(gate, f"node {index}: missing fields {sorted(missing)}")
        node_id = node.get("id")
        if not isinstance(node_id, str) or not node_id:
            add_error(gate, f"node {index}: invalid id")
            continue
        if node_id in node_ids:
            add_error(gate, f"duplicate graph node id: {node_id}")
        node_ids.add(node_id)
        if node.get("type") == "article":
            article_node_ids.add(node_id)
        if node.get("type") == "source":
            source_node_ids.add(node_id)
        if not isinstance(node.get("tags"), list):
            add_error(gate, f"node {node_id}: tags must be a list")

    dangling_edges = 0
    for index, edge in enumerate(edges):
        if not isinstance(edge, dict):
            add_error(gate, f"edge {index}: must be an object")
            continue
        source = edge.get("source")
        target = edge.get("target")
        if not isinstance(source, str) or not isinstance(target, str):
            dangling_edges += 1
            add_error(gate, f"edge {index}: endpoints must be node-id strings")
        elif source not in node_ids or target not in node_ids:
            dangling_edges += 1
            add_error(gate, f"edge {index}: dangling endpoint {source!r} -> {target!r}")

    expected_canonical_ids = {
        f"article:{path.relative_to(root).with_suffix('').as_posix()}"
        for directory in CANONICAL_DIRS
        for path in (root / directory).glob("*.md")
    }
    missing_canonical = sorted(expected_canonical_ids - node_ids)
    if missing_canonical:
        add_error(gate, f"graph is missing canonical article nodes: {missing_canonical}")

    expected_article_ids = {
        f"article:{Path(path).with_suffix('').as_posix()}"
        for path in graph_article_paths(root)
    }
    missing_articles = sorted(expected_article_ids - article_node_ids)
    unexpected_articles = sorted(article_node_ids - expected_article_ids)
    if missing_articles or unexpected_articles:
        add_error(
            gate,
            "graph article coverage mismatch: "
            f"missing={missing_articles}, unexpected={unexpected_articles}",
        )

    expected_source_ids = {
        f"source:{Path(path).relative_to('raw').with_suffix('').as_posix()}"
        for path in graph_source_paths(root)
    }
    missing_sources = sorted(expected_source_ids - source_node_ids)
    unexpected_sources = sorted(source_node_ids - expected_source_ids)
    if missing_sources or unexpected_sources:
        add_error(
            gate,
            "graph source coverage mismatch: "
            f"missing={missing_sources}, unexpected={unexpected_sources}",
        )

    head = git_output(root, "rev-parse", "HEAD")
    graph_base_commit = meta.get("gitCommitHash")
    if (
        not isinstance(graph_base_commit, str)
        or not re.fullmatch(r"[0-9a-f]{40}", graph_base_commit)
        or not git_succeeds(root, "cat-file", "-e", f"{graph_base_commit}^{{commit}}")
    ):
        add_error(gate, f"invalid graph base commit: {graph_base_commit!r}")
    elif head and not git_succeeds(
        root, "merge-base", "--is-ancestor", graph_base_commit, head
    ):
        add_error(
            gate,
            f"graph base commit {graph_base_commit!r} is not an ancestor of HEAD {head!r}",
        )
    graph_project = graph.get("project")
    if (
        not isinstance(graph_project, dict)
        or graph_project.get("gitCommitHash") != graph_base_commit
    ):
        add_error(
            gate,
            "graph project gitCommitHash must equal meta gitCommitHash",
        )

    try:
        expected_input_hash, graph_input_paths = graph_input_fingerprint(root)
    except OSError as exc:
        expected_input_hash, graph_input_paths = "", []
        add_error(gate, f"graph input fingerprint failed: {exc}")
    if meta.get("inputHashAlgorithm") != GRAPH_INPUT_HASH_ALGORITHM:
        add_error(
            gate,
            "graph input hash algorithm mismatch: "
            f"{meta.get('inputHashAlgorithm')!r}",
        )
    if meta.get("inputHash") != expected_input_hash:
        add_error(
            gate,
            f"graph is stale: meta inputHash={meta.get('inputHash')!r}, "
            f"expected={expected_input_hash!r}",
        )
    if meta.get("inputFiles") != len(graph_input_paths):
        add_error(
            gate,
            f"meta inputFiles={meta.get('inputFiles')!r} does not equal "
            f"graph inputs={len(graph_input_paths)}",
        )

    analyzed_files = meta.get("analyzedFiles")
    if analyzed_files != len(article_node_ids):
        add_error(
            gate,
            f"meta analyzedFiles={analyzed_files!r} does not equal "
            f"article nodes={len(article_node_ids)}",
        )
    analyzed_at = meta.get("lastAnalyzedAt")
    normalized_analyzed_at = str(analyzed_at)
    if normalized_analyzed_at.endswith("Z"):
        normalized_analyzed_at = normalized_analyzed_at[:-1] + "+00:00"
    try:
        dt.datetime.fromisoformat(normalized_analyzed_at)
    except ValueError:
        add_error(gate, f"invalid lastAnalyzedAt: {analyzed_at!r}")
    intermediate = root / ".understand-anything" / "intermediate"
    if intermediate.exists():
        add_error(gate, "intermediate graph directory remains after generation")

    gate["metrics"].update(
        {
            "nodes": len(nodes),
            "article_nodes": len(article_node_ids),
            "source_nodes": len(source_node_ids),
            "edges": len(edges),
            "dangling_edges": dangling_edges,
            "layers": len(graph.get("layers", [])),
            "tour_steps": len(graph.get("tour", [])),
            "canonical_nodes_expected": len(expected_canonical_ids),
            "article_nodes_expected": len(expected_article_ids),
            "source_nodes_expected": len(expected_source_ids),
            "graph_input_files": len(graph_input_paths),
            "graph_input_hash": expected_input_hash,
            "graph_base_commit": graph_base_commit,
            "git_head": head,
            "last_analyzed_at": analyzed_at,
        }
    )
    return gate


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--wiki", type=Path, default=Path.cwd(), help="Wiki root")
    parser.add_argument(
        "--gate",
        action="append",
        choices=("a", "b", "c"),
        help="Gate to validate; repeat as needed (default: all)",
    )
    parser.add_argument(
        "--require-clean-main",
        action="store_true",
        help="Require the current branch to be clean main for scheduled automation",
    )
    parser.add_argument(
        "--allow-graph-output-changes",
        action="store_true",
        help=(
            "With --require-clean-main, permit changes only to the two versioned "
            "graph output files"
        ),
    )
    parser.add_argument(
        "--write-graph-input-metadata",
        action="store_true",
        help="Write the current deterministic graph input fingerprint to meta.json",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = args.wiki.expanduser().resolve()
    if args.allow_graph_output_changes and not args.require_clean_main:
        raise SystemExit(
            "--allow-graph-output-changes requires --require-clean-main"
        )
    if args.write_graph_input_metadata:
        try:
            report = write_graph_input_metadata(root)
        except (OSError, ValueError) as exc:
            print(
                json.dumps(
                    {"ok": False, "wiki": str(root), "error": str(exc)},
                    ensure_ascii=False,
                    indent=2,
                )
            )
            return 1
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0

    selected = args.gate or ["a", "b", "c"]
    gates = []
    if "a" in selected:
        gates.append(validate_gate_a(root))
    if "b" in selected:
        gates.append(validate_gate_b(root))
    if "c" in selected:
        gates.append(validate_gate_c(root))
    if args.require_clean_main and gates:
        validate_repository_state(
            root,
            gates[0],
            allow_graph_output_changes=args.allow_graph_output_changes,
        )
    report = {
        "ok": all(gate["ok"] for gate in gates),
        "wiki": str(root),
        "gates": {gate["name"]: gate for gate in gates},
    }
    print(json.dumps(report, ensure_ascii=False, indent=2, default=str))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
