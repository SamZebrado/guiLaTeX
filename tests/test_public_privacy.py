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
    "samzebrado@foxmail.com",
    "noreply@github.com",
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


# Include atom punctuation so another local part cannot become an approved suffix.
EMAIL = re.compile(
    rb"(?<![A-Z0-9.!#$%&'*+/=?^_`{|}~-])"
    rb"(?:[A-Z0-9.!#$%&'*+/=?^_`{|}~-]+|\"(?:[^\"\\\r\n]|\\.)*\")"
    rb"@[A-Z0-9.-]+\.[A-Z]{2,}\b",
    re.I,
)
BRACKETED_DOMAIN = re.compile(rb"@\[(?:[^\]\\\r\n]|\\.)*\]")
QUOTED_LOCAL_PART = re.compile(rb"\"(?:[^\"\\\r\n]|\\.)*\"@")
# A terminal prose period is a delimiter; a following domain label is not.
DOMAIN_CONTINUATION = re.compile(rb"(?:[A-Z0-9_\x80-\xff-]|\.+[A-Z0-9_\x80-\xff-])", re.I)


def scan_blob(label: str, data: bytes) -> list[str]:
    email_matches = list(EMAIL.finditer(data))
    enclosing_tokens = [match.span() for pattern in (BRACKETED_DOMAIN, QUOTED_LOCAL_PART)
                        for match in pattern.finditer(data)]
    allowed_email_spans = {
        match.span() for match in email_matches
        if match.group().lower() in {email.encode("ascii") for email in ALLOWED_EMAILS}
        and not (match.start() and data[match.start() - 1] >= 128)
        and not DOMAIN_CONTINUATION.match(data, match.end())
        and not any(start < match.start() and match.end() < end
                    for start, end in enclosing_tokens)
    }
    findings = [
        f"{label}: {name}" for name, pattern in forbidden_patterns()
        if any(not (name == "private_foxmail_email" and match.span() in allowed_email_spans)
               for match in pattern.finditer(data))
    ]
    for match in email_matches:
        if match.span() not in allowed_email_spans:
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


class PublicPrivacyPolicyTest(unittest.TestCase):
    def test_owner_approved_addresses_are_allowed_in_content(self) -> None:
        for email in ("samzebrado@foxmail.com", "noreply@github.com"):
            with self.subTest(email=email):
                self.assertEqual(scan_blob("fixture", email.encode()), [])

    def test_approved_addresses_are_case_insensitive(self) -> None:
        self.assertEqual(scan_blob("fixture", b"SAMZEBRADO@FOXMAIL.COM"), [])

    def test_address_prefix_and_domain_suffix_are_not_allowlisted(self) -> None:
        email = b"samzebrado@foxmail.com"
        for value in (b"other" + email, email + b".attacker.test"):
            with self.subTest(value=value):
                self.assertIn("fixture: unapproved_email", scan_blob("fixture", value))
                self.assertIn("fixture: private_foxmail_email", scan_blob("fixture", value))

    def test_other_addresses_on_approved_domains_are_rejected(self) -> None:
        for domain in (b"foxmail.com", b"github.com"):
            self.assertIn("fixture: unapproved_email",
                          scan_blob("fixture", b"unapproved" + b"@" + domain))

    def test_punctuation_prefixed_addresses_are_not_allowlisted(self) -> None:
        for email in (b"samzebrado@foxmail.com", b"noreply@github.com"):
            for prefix in b".!#$%&'*+-/=?^_`{|}~":
                value = bytes([prefix]) + email
                with self.subTest(value=value):
                    self.assertIn("fixture: unapproved_email", scan_blob("fixture", value))

    def test_unapproved_address_before_sentence_punctuation_is_rejected(self) -> None:
        email = b"unapproved" + b"@" + b"example.com"
        for suffix in (b".", b",", b";", b")"):
            with self.subTest(suffix=suffix):
                self.assertIn("fixture: unapproved_email", scan_blob("fixture", email + suffix))

    def test_approved_addresses_before_sentence_punctuation_are_allowed(self) -> None:
        for email in (b"samzebrado@foxmail.com", b"noreply@github.com"):
            for suffix in (b".", b",", b";", b")"):
                with self.subTest(value=email + suffix):
                    self.assertEqual(scan_blob("fixture", email + suffix), [])

    def test_domain_continuations_are_not_allowlisted(self) -> None:
        for email in (b"samzebrado@foxmail.com", b"noreply@github.com"):
            for suffix in (b"-evil", b".attacker123", b".x", b".123"):
                with self.subTest(value=email + suffix):
                    self.assertIn("fixture: unapproved_email", scan_blob("fixture", email + suffix))

    def test_non_ascii_address_parts_are_not_allowlisted(self) -> None:
        extra = "é".encode("utf-8")
        for email in (b"samzebrado@foxmail.com", b"noreply@github.com"):
            for value in (extra + email, email + extra, email + b"." + extra):
                with self.subTest(value=value):
                    self.assertIn("fixture: unapproved_email", scan_blob("fixture", value))

    def test_approved_substring_inside_another_address_is_rejected(self) -> None:
        for email in (b"samzebrado@foxmail.com", b"noreply@github.com"):
            values = (b'"' + email + b'"' + b"@" + b"attacker.test",
                      b'"' + email + b'"' + b"@" + "é.test".encode("utf-8"),
                      b"other" + b"@" + b"[" + email + b"]",
                      b"other" + b"@" + b"[escaped\\] " + email + b"]")
            for value in values:
                with self.subTest(value=value):
                    self.assertIn("fixture: unapproved_email", scan_blob("fixture", value))

    def test_allowed_email_does_not_hide_a_secret_in_the_same_blob(self) -> None:
        for prefix, category in ((b"s" + b"k-", "openai_key"),
                                 (b"g" + b"hp_", "github_token")):
            value = b"noreply@github.com " + prefix + b"a" * 32
            self.assertIn("fixture: " + category, scan_blob("fixture", value))

    def test_allowed_email_does_not_hide_a_private_path(self) -> None:
        value = b"noreply@github.com /" + b"Users" + b"/sam" + b"zebrado/"
        self.assertIn("fixture: private_macos_home", scan_blob("fixture", value))


class PublicPrivacyTest(unittest.TestCase):
    def test_tracked_public_tree_is_private_data_free(self) -> None:
        self.assertEqual(tracked_findings(), [])

    def test_reachable_public_history_is_private_data_free(self) -> None:
        self.assertEqual(history_findings(), [])


if __name__ == "__main__":
    unittest.main()
