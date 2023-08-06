#!/usr/bin/env python3

import unittest

from dezimal import Dec


class DecTest(unittest.TestCase):

    def test_construct_from_int(self):
        self.assertEqual("194", str(Dec(194)))
        self.assertEqual("-194", str(Dec(-194)))

    def test_construct_from_str(self):
        self.assertEqual("1", str(Dec("1")))
        self.assertEqual("1", str(Dec("1.0")))
        self.assertEqual("1.01", str(Dec("1.01")))
        self.assertEqual("1", str(Dec("+1")))
        self.assertEqual("1", str(Dec("+1.0")))
        self.assertEqual("1.01", str(Dec("+1.01")))
        self.assertEqual("-1", str(Dec("-1")))
        self.assertEqual("-1", str(Dec("-1.0")))
        self.assertEqual("-1.01", str(Dec("-1.01")))
        self.assertEqual("0", str(Dec("0")))
        self.assertEqual("0", str(Dec("0.0")))
        self.assertEqual("0.01", str(Dec("0.01")))
        self.assertEqual("0", str(Dec("+0")))
        self.assertEqual("0", str(Dec("+0.0")))
        self.assertEqual("0.01", str(Dec("+0.01")))
        self.assertEqual("0", str(Dec("-0")))
        self.assertEqual("0", str(Dec("-0.0")))
        self.assertEqual("-0.01", str(Dec("-0.01")))

    def test_construct_from_str_scifi_notation(self):
        self.assertEqual("1", str(Dec("1e0")))
        self.assertEqual("1", str(Dec("1e+0")))
        self.assertEqual("1", str(Dec("1e-0")))
        self.assertEqual("-1", str(Dec("-1e0")))
        self.assertEqual("-1", str(Dec("-1e+0")))
        self.assertEqual("-1", str(Dec("-1e-0")))
        self.assertEqual("1", str(Dec("1.0e0")))
        self.assertEqual("1", str(Dec("1.0e+0")))
        self.assertEqual("1", str(Dec("1.0e-0")))
        self.assertEqual("-1", str(Dec("-1.0e0")))
        self.assertEqual("-1", str(Dec("-1.0e+0")))
        self.assertEqual("-1", str(Dec("-1.0e-0")))

        self.assertEqual("10", str(Dec("1e1")))
        self.assertEqual("10", str(Dec("1e+1")))
        self.assertEqual("0.1", str(Dec("1e-1")))
        self.assertEqual("-10", str(Dec("-1e1")))
        self.assertEqual("-10", str(Dec("-1e+1")))
        self.assertEqual("-0.1", str(Dec("-1e-1")))
        self.assertEqual("10", str(Dec("1.0e1")))
        self.assertEqual("10", str(Dec("1.0e+1")))
        self.assertEqual("0.1", str(Dec("1.0e-1")))
        self.assertEqual("-10", str(Dec("-1.0e1")))
        self.assertEqual("-10", str(Dec("-1.0e+1")))
        self.assertEqual("-0.1", str(Dec("-1.0e-1")))

    def test_add(self):
        self.assertEqual(Dec("103.03"), Dec("100") + Dec("3.03"))

    def test_sub(self):
        self.assertEqual(Dec("96.97"), Dec("100") - Dec("3.03"))

    def test_mul(self):
        self.assertEqual(Dec("1.26"), Dec("1.2") * Dec("1.05"))

    def test_div(self):
        self.assertEqual("0.33333333333333333", str(Dec(1) / Dec(3)))


if __name__ == '__main__':
    unittest.main()
