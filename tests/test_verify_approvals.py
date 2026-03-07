from __future__ import annotations

import copy
import unittest

from _helpers import load_module


def make_accepted_adr() -> dict:
    return {
        "adr": {
            "id": "ADR-1234-accepted-example",
            "status": "accepted",
            "title": "Accepted ADR",
            "summary": "Summary",
            "project": "project-x",
            "component": "auth",
            "priority": "high",
            "decision_type": "security",
            "created_at": "2026-03-01T10:00:00Z",
        },
        "authors": [{"name": "Author", "role": "Architect"}],
        "decision_owner": {"name": "Owner", "role": "Lead", "email": "owner@example.com"},
        "reviewers": [{"name": "Reviewer", "role": "Reviewer"}],
        "approvals": [
            {
                "name": "Approver",
                "role": "Architect",
                "identity": "@approver",
                "approved_at": "2026-03-02T10:00:00Z",
            }
        ],
        "context": {"summary": "Original context"},
        "architecturally_significant_requirements": [],
        "alternatives": [{"name": "Option A"}],
        "decision": {"chosen_alternative": "Option A", "rationale": "Because"},
        "consequences": {"positive": ["good"], "negative": ["bad"]},
        "dependencies": [],
        "references": [],
        "confirmation": {"description": None, "artifact_ids": []},
        "lifecycle": {"review_cycle_months": 12},
        "audit_trail": [{"event": "created", "by": "Author", "at": "2026-03-01T10:00:00Z"}],
    }


class VerifyApprovalsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.module = load_module("verify_approvals", "scripts/verify-approvals.py")

    def test_append_only_audit_trail_allows_append_but_rejects_edits_and_deletes(self):
        old = make_accepted_adr()

        edited = copy.deepcopy(old)
        edited["audit_trail"][0]["by"] = "Someone Else"
        ok, message = self.module.check_append_only_audit_trail(old, edited)
        self.assertFalse(ok)
        self.assertIn("edited or reordered", message)

        deleted = copy.deepcopy(old)
        deleted["audit_trail"] = []
        ok, message = self.module.check_append_only_audit_trail(old, deleted)
        self.assertFalse(ok)
        self.assertIn("deleted", message)

        appended = copy.deepcopy(old)
        appended["audit_trail"].append(
            {"event": "reviewed", "by": "Reviewer", "at": "2026-04-01T10:00:00Z"}
        )
        ok, message = self.module.check_append_only_audit_trail(old, appended)
        self.assertTrue(ok, message)

    def test_immutable_after_acceptance_blocks_decision_core_changes(self):
        old = make_accepted_adr()
        changed = copy.deepcopy(old)
        changed["decision"]["rationale"] = "Changed rationale"

        ok, message = self.module.check_immutable_after_acceptance(
            old,
            changed,
            self.module.DEFAULT_IMMUTABLE_AFTER_ACCEPTANCE_FIELDS,
        )
        self.assertFalse(ok)
        self.assertIn("decision core is immutable", message)
        self.assertIn("decision.rationale", message)

    def test_immutable_after_acceptance_allows_confirmation_updates_and_supersession(self):
        old = make_accepted_adr()

        confirmation = copy.deepcopy(old)
        confirmation["confirmation"] = {
            "description": "Verified in production",
            "artifact_ids": ["PR-42"],
        }
        ok, message = self.module.check_immutable_after_acceptance(
            old,
            confirmation,
            self.module.DEFAULT_IMMUTABLE_AFTER_ACCEPTANCE_FIELDS,
        )
        self.assertTrue(ok, message)

        superseded = copy.deepcopy(old)
        superseded["adr"]["status"] = "superseded"
        superseded["lifecycle"]["superseded_by"] = "ADR-9999-replacement"
        ok, message = self.module.check_immutable_after_acceptance(
            old,
            superseded,
            self.module.DEFAULT_IMMUTABLE_AFTER_ACCEPTANCE_FIELDS,
        )
        self.assertTrue(ok, message)

        invalid_status = copy.deepcopy(old)
        invalid_status["adr"]["status"] = "draft"
        ok, message = self.module.check_immutable_after_acceptance(
            old,
            invalid_status,
            self.module.DEFAULT_IMMUTABLE_AFTER_ACCEPTANCE_FIELDS,
        )
        self.assertFalse(ok)
        self.assertIn("may only remain 'accepted' or transition", message)


if __name__ == "__main__":
    unittest.main()
