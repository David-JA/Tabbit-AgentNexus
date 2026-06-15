from __future__ import annotations

import unittest

from scripts.message_envelope import (
    MessageEnvelope,
    build_envelope,
    validate_envelope,
)
from scripts.relay_constants import (
    COMPLETENESS_COMPLETE,
    COMPLETENESS_INCOMPLETE,
    COMPLETENESS_UNKNOWN,
    DIRECTION_REPO_TO_WEB,
    DIRECTION_WEB_TO_REPO,
    PAYLOAD_ROLE_CONTEXT_PACK,
    PAYLOAD_ROLE_ASSISTANT_REPLY,
)


class MessageEnvelopeTests(unittest.TestCase):
    def test_build_envelope_stores_digest_not_payload(self) -> None:
        payload = b"secret repository content"
        env = build_envelope(
            session_id="n1-test",
            direction=DIRECTION_REPO_TO_WEB,
            target_conversation_url="https://chat.example.com/c/abc",
            payload_role=PAYLOAD_ROLE_CONTEXT_PACK,
            payload=payload,
            round_number=1,
        )
        # payload_digest is a hex string, not the raw payload.
        self.assertIsInstance(env.payload_digest, str)
        self.assertEqual(len(env.payload_digest), 64)  # SHA-256 hex
        self.assertNotEqual(env.payload_digest, payload.decode())

    def test_build_envelope_payload_bytes_matches(self) -> None:
        payload = b"hello world"
        env = build_envelope(
            session_id="n1-test",
            direction=DIRECTION_REPO_TO_WEB,
            target_conversation_url="https://chat.example.com/c/abc",
            payload_role=PAYLOAD_ROLE_CONTEXT_PACK,
            payload=payload,
            round_number=1,
        )
        self.assertEqual(env.payload_bytes, len(payload))

    def test_build_envelope_string_payload(self) -> None:
        env = build_envelope(
            session_id="n1-test",
            direction=DIRECTION_REPO_TO_WEB,
            target_conversation_url="https://chat.example.com/c/abc",
            payload_role=PAYLOAD_ROLE_CONTEXT_PACK,
            payload="a string payload",
            round_number=1,
        )
        self.assertEqual(env.payload_bytes, len("a string payload".encode("utf-8")))

    def test_untrusted_data_always_true(self) -> None:
        env = build_envelope(
            session_id="n1-test",
            direction=DIRECTION_REPO_TO_WEB,
            target_conversation_url="https://chat.example.com/c/abc",
            payload_role=PAYLOAD_ROLE_CONTEXT_PACK,
            payload=b"data",
            round_number=1,
        )
        self.assertTrue(env.untrusted_data)

    def test_validate_valid_envelope_returns_empty(self) -> None:
        env = build_envelope(
            session_id="n1-test",
            direction=DIRECTION_REPO_TO_WEB,
            target_conversation_url="https://chat.example.com/c/abc",
            payload_role=PAYLOAD_ROLE_CONTEXT_PACK,
            payload=b"data",
            round_number=1,
        )
        issues = validate_envelope(env)
        self.assertEqual(issues, [])

    def test_validate_envelope_detects_round_zero(self) -> None:
        env = build_envelope(
            session_id="n1-test",
            direction=DIRECTION_REPO_TO_WEB,
            target_conversation_url="https://chat.example.com/c/abc",
            payload_role=PAYLOAD_ROLE_CONTEXT_PACK,
            payload=b"data",
            round_number=0,
        )
        issues = validate_envelope(env)
        self.assertTrue(any("round" in i.lower() for i in issues))

    def test_validate_envelope_detects_bad_direction(self) -> None:
        env = MessageEnvelope(
            envelope_id="e1",
            session_id="n1-test",
            round=1,
            direction="northbound",
            target_conversation_url="https://chat.example.com/c/abc",
            payload_role=PAYLOAD_ROLE_CONTEXT_PACK,
            payload_digest="a" * 64,
            payload_bytes=100,
        )
        issues = validate_envelope(env)
        self.assertTrue(any("direction" in i.lower() for i in issues))

    def test_validate_envelope_detects_bad_payload_role(self) -> None:
        env = MessageEnvelope(
            envelope_id="e1",
            session_id="n1-test",
            round=1,
            direction=DIRECTION_REPO_TO_WEB,
            target_conversation_url="https://chat.example.com/c/abc",
            payload_role="execute_command",
            payload_digest="a" * 64,
            payload_bytes=100,
        )
        issues = validate_envelope(env)
        self.assertTrue(any("role" in i.lower() for i in issues))

    def test_validate_envelope_detects_bad_payload_digest(self) -> None:
        env = MessageEnvelope(
            envelope_id="e1",
            session_id="n1-test",
            round=1,
            direction=DIRECTION_REPO_TO_WEB,
            target_conversation_url="https://chat.example.com/c/abc",
            payload_role=PAYLOAD_ROLE_CONTEXT_PACK,
            payload_digest="notsha",
            payload_bytes=100,
        )
        issues = validate_envelope(env)
        self.assertTrue(any("payload_digest" in i for i in issues))

    def test_validate_envelope_detects_negative_payload_bytes(self) -> None:
        env = MessageEnvelope(
            envelope_id="e1",
            session_id="n1-test",
            round=1,
            direction=DIRECTION_REPO_TO_WEB,
            target_conversation_url="https://chat.example.com/c/abc",
            payload_role=PAYLOAD_ROLE_CONTEXT_PACK,
            payload_digest="a" * 64,
            payload_bytes=-1,
        )
        issues = validate_envelope(env)
        self.assertTrue(any("payload_bytes" in i for i in issues))

    def test_validate_envelope_detects_negative_redaction_count(self) -> None:
        env = MessageEnvelope(
            envelope_id="e1",
            session_id="n1-test",
            round=1,
            direction=DIRECTION_REPO_TO_WEB,
            target_conversation_url="https://chat.example.com/c/abc",
            payload_role=PAYLOAD_ROLE_CONTEXT_PACK,
            payload_digest="a" * 64,
            payload_bytes=100,
            redaction_count=-3,
        )
        issues = validate_envelope(env)
        self.assertTrue(any("redaction_count" in i for i in issues))

    def test_validate_envelope_detects_invalid_completeness(self) -> None:
        env = MessageEnvelope(
            envelope_id="e1",
            session_id="n1-test",
            round=1,
            direction=DIRECTION_REPO_TO_WEB,
            target_conversation_url="https://chat.example.com/c/abc",
            payload_role=PAYLOAD_ROLE_CONTEXT_PACK,
            payload_digest="a" * 64,
            payload_bytes=100,
            completeness="complete-ish",
        )
        issues = validate_envelope(env)
        self.assertTrue(any("completeness" in i for i in issues))

    def test_validate_envelope_detects_empty_session_id(self) -> None:
        env = MessageEnvelope(
            envelope_id="e1",
            session_id="",
            round=1,
            direction=DIRECTION_REPO_TO_WEB,
            target_conversation_url="https://chat.example.com/c/abc",
            payload_role=PAYLOAD_ROLE_CONTEXT_PACK,
            payload_digest="a" * 64,
            payload_bytes=100,
        )
        issues = validate_envelope(env)
        self.assertTrue(any("session_id" in i for i in issues))

    def test_to_dict_and_json_roundtrip(self) -> None:
        import json

        env = build_envelope(
            session_id="n1-test",
            direction=DIRECTION_WEB_TO_REPO,
            target_conversation_url="https://chat.example.com/c/abc",
            payload_role=PAYLOAD_ROLE_ASSISTANT_REPLY,
            payload=b"response text",
            round_number=2,
            redaction_count=3,
            completeness=COMPLETENESS_COMPLETE,
        )
        d = env.to_dict()
        self.assertEqual(d["session_id"], "n1-test")
        self.assertEqual(d["round"], 2)
        self.assertEqual(d["redaction_count"], 3)
        self.assertEqual(d["completeness"], COMPLETENESS_COMPLETE)
        self.assertTrue(d["untrusted_data"])

        json_str = env.to_json()
        parsed = json.loads(json_str)
        self.assertEqual(parsed["envelope_id"], env.envelope_id)

    def test_envelope_is_immutable(self) -> None:
        env = build_envelope(
            session_id="n1-test",
            direction=DIRECTION_REPO_TO_WEB,
            target_conversation_url="https://chat.example.com/c/abc",
            payload_role=PAYLOAD_ROLE_CONTEXT_PACK,
            payload=b"data",
            round_number=1,
        )
        with self.assertRaises(Exception):
            env.round = 99  # type: ignore[misc]


if __name__ == "__main__":
    unittest.main()
