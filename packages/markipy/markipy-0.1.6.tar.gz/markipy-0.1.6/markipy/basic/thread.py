import threading

from markipy import DEFAULT_LOG_PATH
from .atom import Performance
from .logger import Logger

_general_thread_ = {'class': 'GeneralThread', 'version': 3}
_consumer_thread_ = {'class': 'ConsumerThread', 'version': 3}
_producer_thread_ = {'class': 'ProducerThread', 'version': 3}


class GeneralThread(Logger, threading.Thread):

    def __init__(self, channel=None, task_name='default', console=False, daemon=False, log_path=DEFAULT_LOG_PATH):
        Logger.__init__(self, console=console, file_log=f'GeneralThread.{task_name}', log_path=log_path)
        self._init_atom_register_class(_general_thread_)
        threading.Thread.__init__(self)
        self.setDaemon(daemon)
        self.channel = channel
        self.finish = False

    def init(self):
        pass

    def task(self):
        pass

    @Performance.collect
    def run(self):
        self.init()
        self.task()
        self.set_finish()

    def set_finish(self):
        self.finish = True
        self.cleanup()

    def cleanup(self):
        pass


class ThreadConsumer(Logger, threading.Thread):

    def __init__(self, channel=None, task_name='default', console=False, daemon=False, log_path=DEFAULT_LOG_PATH):
        Logger.__init__(self, console=console, file_log=f'ConsumerThread.{task_name}', log_path=log_path)
        self._init_atom_register_class(_consumer_thread_)
        threading.Thread.__init__(self)
        self.setDaemon(daemon)
        self.channel = channel
        self.finish = False

    def init(self):
        pass

    def task(self, val):
        pass

    @Performance.collect
    def run(self):
        self.init()
        try:
            while not self.finish:
                val = self.channel.get()
                if val is self.channel.empty:
                    if self.channel.get_finish():
                        self.set_finish()
                else:
                    if val is not None:
                        self.task(val)
                        self.channel.task_done()

        except Exception as e:
            self.log.error(f"Error -> {e}")

    @Performance.collect
    def set_finish(self):
        self.finish = True
        self.cleanup()

    @Performance.collect
    def cleanup(self):
        pass


class ThreadProducer(Logger, threading.Thread):

    def __init__(self, channel=None, task_name='default', console=False, daemon=False, log_path=DEFAULT_LOG_PATH):
        Logger.__init__(self, console=console, file_log=f'ProducerThread.{task_name}', log_path=log_path)
        self._init_atom_register_class(_producer_thread_)
        threading.Thread.__init__(self)
        self.setDaemon(daemon)
        self.channel = channel
        self.finish = False

    def init(self):
        pass

    def task(self):
        pass

    @Performance.collect
    def run(self):
        self.init()
        try:
            while not self.finish:
                self.task()
        except Exception as e:
            self.log.error(f"Error -> {e}")

    def set_finish(self):
        self.channel.wait_completion_task()
        self.finish = True
        self.cleanup()

    def produce(self, val):
        self.channel.put(val)

    def cleanup(self):
        pass


