import sys
import asyncio
import signal

from . import core


def main(path):

    loop = asyncio.get_event_loop()

    coroutine = core.load(path)
    task = loop.create_task(coroutine)

    event = asyncio.Event(loop = loop)

    @task.add_done_callback
    def done_callback(task):
        if not task.exception():
            return
        event.set()

    loop.add_signal_handler(signal.SIGINT, event.set)

    coroutine = event.wait()
    loop.run_until_complete(coroutine)

    task.result()

    coroutine = core.drop(path)
    loop.run_until_complete(coroutine)


def serve():

    args = sys.argv[1:]

    main(*args)
