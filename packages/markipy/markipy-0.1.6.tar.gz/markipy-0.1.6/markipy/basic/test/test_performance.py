import unittest
import time
import HtmlTestRunner

from markipy.basic import Atom
from markipy.basic import Performance

_Performance_child_ = {'class': 'PerformanceChild', 'version': 2}
_Performance_nephew_ = {'class': 'PerformanceNephew', 'version': 3}


# class PerformanceChild(Atom):
#     def __init__(self):
#         Atom.__init__(self, _Performance_child_['class'], _Performance_child_['version'])
#
#     @Performance.collect
#     def test_performance_child(self):
#         pass
#
#
# class PerformanceNephew(PerformanceChild):
#     def __init__(self):
#         PerformanceChild.__init__(self)
#         Atom.__init__(self, _Performance_nephew_['class'], _Performance_nephew_['version'])
#
#     @Performance.collect
#     def test_performance_nephew(self):
#         pass
#
#
# class TestPerformance(unittest.TestCase):
#
#     def test_performance_child(self):
#         pc = PerformanceChild()
#         pc.test_performance_child()
#         self.assertEqual(pc.performance.stats['test_performance_child'].name, 'test_performance_child')
#
#     def test_performance_nephew(self):
#         pn = PerformanceNephew()
#         pn.test_performance_child()
#         pn.test_performance_nephew()
#         self.assertEqual(pn.performance.stats['test_performance_nephew'].name, 'test_performance_nephew')
#
#
# if __name__ == '__main__':
#     unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output='/tmp/markpy_unittest/'))
