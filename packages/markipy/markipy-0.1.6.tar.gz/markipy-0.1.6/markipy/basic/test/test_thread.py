import unittest
import os
from time import sleep
import HtmlTestRunner

from markipy.basic import Channel
from markipy.basic import ThreadConsumer, ThreadProducer, GeneralThread

_producer_ = {'class': 'Producer', 'version': 1}
_consumer_ = {'class': 'Consumer', 'version': 1}


class Producer(ThreadProducer):
    def __init__(self, channel):
        ThreadProducer.__init__(self, channel=channel, task_name='Unittest.Thread.Producer')
        self._init_atom_register_class(_producer_)
        self.produced = []

    def task(self):
        for x in range(0, 100):
            self.produced.append(x)
            self.produce(x)
            sleep(0.0001)
        self.set_finish()


class Consumer(ThreadConsumer):
    def __init__(self, channel):
        ThreadConsumer.__init__(self, channel=channel, task_name='Unittest.Thread.Consumer')
        self._init_atom_register_class(_producer_)
        self.consumed = []

    def task(self, var):
        self.consumed.append(var)


class TestThreads(unittest.TestCase):

    def test_thread_producer_consumer(self):
        c = Channel()
        p = Producer(channel=c)
        c = Consumer(channel=c)
        p.start()
        c.start()
        p.join()
        c.join()
        self.assertListEqual(p.produced, c.consumed)


if __name__ == '__main__':
    unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output='/tmp/markpy_unittest/'))
