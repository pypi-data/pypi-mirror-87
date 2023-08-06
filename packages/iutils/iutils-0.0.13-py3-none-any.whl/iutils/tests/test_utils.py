import unittest
from iutils.utils import two_level_split


class TestTwoLevelSplit(unittest.TestCase):
    def test_two_level_split(self):
        self.assertEqual(two_level_split('a "b c" "d"'), ["a", "b c", "d"])

        # multiple spaces with quotes
        self.assertEqual(
            two_level_split('a "b c" "d" "ef  gh"'), ["a", "b c", "d", "ef  gh"]
        )

        self.assertEqual(
            two_level_split('a "b c d"e f g" h'), ["a", 'b c d"e f g', "h"]
        )

        self.assertRaises(ValueError, two_level_split, 'a "b c "d"')

        self.assertRaises(ValueError, two_level_split, 'a "b c" d"')

        self.assertRaises(ValueError, two_level_split, 'a "b "e f" g" h "i j"')

        self.assertEqual(two_level_split("a, b, c ", sep=","), ["a", " b", " c "])

        self.assertEqual(two_level_split('a,"b,c",d', sep=","), ["a", "b,c", "d"])
