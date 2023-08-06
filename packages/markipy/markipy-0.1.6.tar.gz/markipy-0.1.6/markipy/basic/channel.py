from queue import Queue
from threading import Lock


class Channel:

    def __init__(self, size=12500, n_producer=1):
        self.queue_size = size
        self.finish = False
        self.channel = Queue(self.queue_size)
        self.empty = Queue.empty
        self.n_producer = n_producer
        self.producer_completed = 0
        self.channel_lock = Lock()

    def get(self, timeout=5):
        try:
            return self.channel.get(block=True, timeout=timeout)
        except Exception:
            return self.empty

    def put(self, var):
        self.channel.put(var, block=True)

    def task_done(self):
        self.channel.task_done()

    def set_finish(self):
        with self.channel_lock:
            self.producer_completed += 1
            if self.n_producer == self.producer_completed:
                self.finish = True

    def get_finish(self):
        return self.finish

    def wait_completion_task(self):
        self.channel.join()
        self.set_finish()

    def is_full(self):
        return self.channel.full()

    def is_empty(self):
        return self.channel.empty()
