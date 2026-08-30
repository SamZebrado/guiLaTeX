"""Regression gate for content intended for the public guiLaTeX repository."""

from __future__ import annotations

import re
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ALLOWED_EMAILS = {
    "audit@guilatex.local",
    "guilatex@users.noreply.github.com",
}


def git(*args: str, binary: bool = False) -> bytes | str:
    return subprocess.check_output(
        ["git", "-C", str(ROOT), *args],
        text=not binary,
    )


def forbidden_patterns() -> list[tuple[str, re.Pattern[bytes]]]:
    mac_home = b"/" + b"Users" + b"/" + b"sam" + b"zebrado" + b"/"
    linux_home = b"/" + b"home" + b"/" + b"sam" + b"zebrado" + b"/"
    nyu_email = b"sz68" + b"@" + b"nyu.edu"
    foxmail = b"sam" + b"zebrado" + b"@" + b"foxmail.com"
    private_project = b"g-p-69db4b7b" + b"b42881918755388dff67857b"
    private_conversation = b"69d0cad8-a3f0-83a5-" + b"b2e5-2ea725dd8394"
    chatgpt_project = b"chatgpt" + b".com/" + b"g/"
    profile_state = b"state/" + b"chrome_" + b"profiles"
    debug_port = b"remote-" + b"debugging-" + b"port"
    return [
        ("private_macos_home", re.compile(re.escape(mac_home), re.I)),
        ("private_linux_home", re.compile(re.escape(linux_home), re.I)),
        ("private_nyu_email", re.compile(re.escape(nyu_email), re.I)),
        ("private_foxmail_email", re.compile(re.escape(foxmail), re.I)),
        ("private_chatgpt_project", re.compile(re.escape(chatgpt_project), re.I)),
        ("private_chatgpt_project_id", re.compile(re.escape(private_project), re.I)),
        ("private_chatgpt_conversation_id", re.compile(re.escape(private_conversation), re.I)),
        ("bridge_profile_state", re.compile(re.escape(profile_state), re.I)),
        ("bridge_debug_port", re.compile(re.escape(debug_port), re.I)),
        ("private_key", re.compile(b"-----BEGIN (?:RSA |OPENSSH |EC |DSA )?PRIVATE KEY-----")),
        ("openai_key", re.compile(b"\\b" + b"s" + b"k-[A-Za-z0-9_-]{20,}\\b")),
        ("github_token", re.compile(b"\\b(?:g" + b"hp_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,})\\b")),
        ("aws_access_key", re.compile(b"\\bA" + b"KIA[0-9A-Z]{16}\\b")),
        ("google_api_key", re.compile(b"\\bA" + b"Iza[0-9A-Za-z_-]{30,}\\b")),
        ("bearer_secret", re.compile(b"\\bBear" + b"er\\s+[A-Za-z0-9._~+\\/-]{20,}=*", re.I)),
    ]


EMAIL = re.compile(rb"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I)


def scan_blob(label: str, data: bytes) -> list[str]:
    findings = [f"{label}: {name}" for name, pattern in forbidden_patterns() if pattern.search(data)]
    for value in EMAIL.findall(data):
        email = value.decode("ascii", errors="ignore").lower()
        if email and email not in ALLOWED_EMAILS:
            findings.append(f"{label}: unapproved_email")
    return findings


def tracked_findings() -> list[str]:
    findings: list[str] = []
    names = bytes(git("ls-files", "-z", binary=True)).split(b"\0")
    for raw_name in filter(None, names):
        relative = raw_name.decode("utf-8", errors="surrogateescape")
        findings.extend(scan_blob(relative, (ROOT / relative).read_bytes()))
    return findings


def history_findings() -> list[str]:
    findings: list[str] = []
    seen: set[str] = set()
    for line in str(git("rev-list", "--objects", "--all")).splitlines():
        object_id, _, object_path = line.partition(" ")
        if object_id in seen:
            continue
        seen.add(object_id)
        if str(git("cat-file", "-t", object_id)).strip() != "blob":
            continue
        data = bytes(git("cat-file", "blob", object_id, binary=True))
        findings.extend(scan_blob(object_path or object_id, data))

    metadata = str(git("log", "--all", "--format=%ae%n%ce"))
    for value in filter(None, (line.strip().lower() for line in metadata.splitlines())):
        if value not in ALLOWED_EMAILS:
            findings.append("commit_metadata: unapproved_email")
    return findings


class PublicPrivacyTest(unittest.TestCase):
    def test_tracked_public_tree_is_private_data_free(self) -> None:
        self.assertEqual(tracked_findings(), [])

    def test_reachable_public_history_is_private_data_free(self) -> None:
        self.assertEqual(history_findings(), [])


if __name__ == "__main__":
    unittest.main()
