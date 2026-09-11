import unittest

ALLOWED_CHANGE_ACTIONS = {
    "ADD", "AMEND", "DEPRECATE", "RETRACT", "ERRATA",
    "CONFLICT_LINK", "ADVERSE_LINK", "VERIFY", "UNVERIFY",
    "PROMOTE_TO_EXHIBIT", "DEMOTE_FROM_EXHIBIT",
}


def source_can_close(coverage_complete, qa_pass, open_items):
    return bool(coverage_complete and qa_pass and not open_items)


class ReviewControlContractTests(unittest.TestCase):
    def test_delete_is_not_allowed_change_action(self):
        self.assertNotIn("DELETE", ALLOWED_CHANGE_ACTIONS)

    def test_open_items_block_closeout(self):
        self.assertFalse(source_can_close(True, True, ["gap-1"]))

    def test_complete_clean_source_can_close(self):
        self.assertTrue(source_can_close(True, True, []))


if __name__ == "__main__":
    unittest.main()
