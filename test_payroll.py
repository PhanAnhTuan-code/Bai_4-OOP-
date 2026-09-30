import unittest

from cases import CASES


class PayrollCases(unittest.TestCase):
    def test_all_cases(self):
        for case_id, desc, expected, func in CASES:
            with self.subTest(case=case_id, desc=desc):
                self.assertEqual(func(), expected)


if __name__ == "__main__":
    unittest.main(verbosity=2)
