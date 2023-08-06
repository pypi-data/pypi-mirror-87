import logging
import multiprocessing
import queue
import sys
import threading
import traceback
from datetime import datetime

from narration.constants import QUEUE_OPEN_SENTINEL, QUEUE_CLOSED_SENTINEL


class ServerHandler(logging.Handler):
    def __init__(
        self,
        name,
        target_handler=None,
        queue=multiprocessing.Queue(-1),
        level="dummy-level",
    ):
        super(ServerHandler, self).__init__(level=target_handler.level)

        if target_handler is None:
            target_handler = logging.StreamHandler()
        self.target_handler = target_handler

        self.setFormatter(self.target_handler.formatter)
        self.filters = self.target_handler.filters

        self.queue = queue
        self._server_closed = False

        self._client_count = 0
        self._max_waiting_time_reading_queue = 5.0  # in seconds
        self._raise_exception_on_server_closed_too_early = False

        # Thread receives records asynchronously.
        self._server_thread = threading.Thread(target=self._receive, name=name)
        self._server_thread.daemon = True
        self._server_thread.start()

    def setFormatter(self, fmt):
        super(ServerHandler, self).setFormatter(fmt)
        self.target_handler.setFormatter(fmt)

    def _receive(self):
        max_read_timeout = 0.2
        max_wait_time = self._max_waiting_time_reading_queue - (max_read_timeout * 2.0)
        start_time = None
        while True:
            try:
                record = self.queue.get(timeout=max_read_timeout)

                # Handle closing of a client handler
                if record == QUEUE_CLOSED_SENTINEL:
                    self._client_count -= 1

                    # Stop receiving anymore message when the last client
                    # handler has closed
                    if self._client_count == 0:
                        break
                # Handle opening of a client handler
                elif record == QUEUE_OPEN_SENTINEL:
                    self._client_count += 1
                # Forward client handler's records
                else:
                    self.target_handler.emit(record)
            except (KeyboardInterrupt, SystemExit):
                raise
            except (BrokenPipeError, EOFError):
                break
            except queue.Empty:
                if not self._server_closed:
                    # Client handlers are not emitting new records, while server handler is trying
                    # to read records
                    pass
                else:
                    # Client handlers are not emitting new records, while server handler is trying
                    # to stop reading records
                    end_time = datetime.now()
                    if start_time is None:
                        start_time = end_time

                    max_wait_time -= (end_time - start_time).total_seconds()
                    start_time = datetime.now()

                    # Force server handler to stop reading records
                    if max_wait_time <= 0:
                        break
            except BaseException:
                traceback.print_exc(file=sys.stderr)

        # At this point the queue may still contain data
        if self._client_count > 0 and self._raise_exception_on_server_closed_too_early:
            raise BaseException(
                f"{self._client_count} were still sending records when the mp-server handler was definitly closed"
            )

        # self.queue.close()
        # self.queue.join_thread()

    def emit(self, record):
        self.target_handler.emit(record)

    def close(self):
        if not self._server_closed:
            self._server_closed = True
            # Waits some time for receive queue to eventually be empty.
            self._server_thread.join(self._max_waiting_time_reading_queue)

            self.target_handler.close()
            super(ServerHandler, self).close()
