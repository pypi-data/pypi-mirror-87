import unittest
from iutils.dict import deep_merge


class TestDeepMerge(unittest.TestCase):
    def test_deep_merge(self):

        # when reaches the max depth, it should return b
        self.assertEqual(
            deep_merge(
                {"0a": {"1a": {"2a": {"3a": {},},}, "1b": 1, "1c": [1],},},
                {
                    "0a": {
                        "1a": {"2a": {"3a": {"4a": (1, "a"),},},},
                        "1b": {"2b": {"3b": [1],},},
                    },
                },
                max_depth=2,
            ),
            {
                "0a": {
                    "1a": {"2a": {"3a": {"4a": (1, "a"),},},},
                    "1b": {"2b": {"3b": [1],},},
                    "1c": [1],
                },
            },
        )

        # when a is not a dict, should return b
        self.assertEqual(deep_merge(None, {"b": 2}), {"b": 2})

        # when b is not a dict, should return b
        self.assertEqual(deep_merge({"a": 1}, None), None)

        # same key overwrites
        self.assertEqual(deep_merge({"a": 1}, {"a": 2}), {"a": 2})
        self.assertEqual(
            deep_merge({"a": {"b": 1, "c": 2,}}, {"a": {"c": 3,}}),
            {"a": {"b": 1, "c": 3}},
        )

        # different keys merge
        self.assertEqual(deep_merge({"a": 1}, {"b": 2}), {"a": 1, "b": 2})

        self.assertEqual(
            deep_merge({"a": {"b": 1, "c": 2,}}, {"a": {"d": 3,}}),
            {"a": {"b": 1, "c": 2, "d": 3,}},
        )
