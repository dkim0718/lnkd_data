from unittest import TestCase

import lnkd_data

class TestJoke(TestCase):
    def test_is_string(self):
        s = lnkd_data.joke()
        self.assertTrue(isinstance(s, basestring))