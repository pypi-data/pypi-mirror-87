#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author: zhangkai
Last modified: 2020-06-29 10:18:14
'''
import asyncio
from concurrent.futures._base import CancelledError
from functools import partial
from signal import SIGINT
from signal import SIGTERM

from utils import Request

from .log_utils import Logger


class Processor:

    def __init__(self, workers=10):
        self.loop = asyncio.get_event_loop()
        self.http = Request(lib='tornado')
        self.queue = asyncio.Queue()
        self.result = asyncio.Queue()
        self.logger = Logger()
        self.workers = workers
        self.init()

    def init(self):
        pass

    async def producer(self):
        raise NotImplementedError

    async def consumer(self, args):
        raise NotImplementedError

    async def collector(self):
        raise NotImplementedError

    async def _consumer(self):
        while True:
            try:
                args = await self.queue.get()
                self.logger.info(f'queue size: {self.queue.qsize()}')
                if isinstance(args, (tuple, list)):
                    ret = await self.consumer(*args)
                else:
                    ret = await self.consumer(args)
                if ret is not None:
                    await self.result.put(ret)
                self.queue.task_done()
            except CancelledError:
                return self.logger.error('Cancelled consumer')
            except Exception as e:
                self.logger.exception(e)
                self.queue.task_done()

    async def finish(self):
        await self.queue.join()
        if self.result.qsize() > 0:
            await self.collector()

    async def shutdown(self, sig):
        self.logger.warning(f'caught signal {sig.name}')
        tasks = list(filter(lambda task: task is not asyncio.tasks.Task.current_task(), asyncio.Task.all_tasks()))
        self.logger.info(f'cancell tasks: {len(tasks)}')
        list(map(lambda task: task.cancel(), tasks))
        self.loop.stop()

    def start(self):
        for sig in (SIGINT, SIGTERM):
            self.loop.add_signal_handler(sig, partial(self.loop.create_task, self.shutdown(sig)))

        self.loop.run_until_complete(self.producer())
        for _ in range(self.workers):
            self.loop.create_task(self._consumer())
        self.loop.run_until_complete(self.finish())
