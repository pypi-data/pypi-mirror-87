import unittest
import os
from time import sleep
import HtmlTestRunner

from markipy.basic import Channel


class TestChannel(unittest.TestCase):

    def test_channel_in_out(self):
        var = [10, 20, 30]
        c = Channel()
        c.put(var)
        var_channel = c.get()
        self.assertEqual(var, var_channel)


if __name__ == '__main__':
    unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output='/tmp/markpy_unittest/'))
