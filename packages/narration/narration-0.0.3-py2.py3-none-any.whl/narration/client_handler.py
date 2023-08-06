import logging

from narration.constants import QUEUE_CLOSED_SENTINEL, QUEUE_OPEN_SENTINEL


class ClientHandler(logging.Handler):
    def __init__(self, queue=None, level=None):
        super(ClientHandler, self).__init__(level)
        self.queue = queue
        self._server_notified = False

    def emit(self, record):
        try:
            # Notify server handler a new client handler wants to emit records
            if not self._server_notified:
                self._emit(QUEUE_OPEN_SENTINEL)
                self._server_notified = True

            # Send application's regular record
            s = self._format_record(record)
            self._emit(s)
        except (KeyboardInterrupt, SystemExit):
            raise
        except BaseException:
            self.handleError(record)

    def close(self):
        # Notify server the client handler will not be emitting more records
        self._emit(QUEUE_CLOSED_SENTINEL)
        # Wait for queue data to be flushed out via the IPC pipe.
        # The following code happens automatically when the queue is garbage collected (eg: the client process is about to end)
        # self.queue.close()
        # self.queue.join_thread()
        super(ClientHandler, self).close()

    def _emit(self, s):
        self.queue.put_nowait(s)

    def _format_record(self, record):
        # ensure that exc_info and args
        # have been stringified. Removes any chance of
        # unpickleable things inside and possibly reduces
        # message size sent over the pipe.
        if record.args:
            record.msg = record.msg % record.args
            record.args = None
        if record.exc_info:
            self.format(record)
            record.exc_info = None

        return record
