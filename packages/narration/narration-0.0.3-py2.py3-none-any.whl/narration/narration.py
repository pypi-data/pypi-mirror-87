import logging
from typing import Dict

from narration.client_handler import ClientHandler
from narration.server_handler import ServerHandler


def _create_client_handler_factory(kwargs: Dict = {}):
    return ClientHandler(**kwargs)


def _create_server_handler_factory(start_method: str = None, ctx=None, ctx_manager=None, **kwargs):
    """
    Factory to create a multiprocessing aware logging handler instance
    :param kwargs: Keyword arguments:
    {
        name: str
        target_handler: Handler
        queue: Queue (or similar),
        level: int
    }
    :return ServerHandler, {} (Or None,None if no process starting method is identified nor no multiprocessing aware
    handler should be returned)
    """
    if None in [start_method, ctx_manager]:
        return None, {}

    queue = kwargs.get("queue", None)
    queue_missing = queue is None
    if queue_missing:
        queue = ctx_manager.Queue(-1)
        kwargs.update(queue=queue)

    settings = {"queue": queue, "level": kwargs.get("level", logging.DEBUG)}
    return ServerHandler(**kwargs), settings


def setup_client_handlers(
    logger=None,
    handler_name_to_client_handler_settings: Dict = {},
    create_client_handler_factory=_create_client_handler_factory,
):
    for (
        handler_name,
        client_handler_settings,
    ) in handler_name_to_client_handler_settings.items():
        handler = create_client_handler_factory(client_handler_settings)
        handler.name = handler_name
        logger.addHandler(handler)


def setup_server_handlers(
    logger=None,
    ctx=None,
    ctx_manager=None,
    create_server_handler_factory=_create_server_handler_factory,
):
    """Wraps a logger's handlers with ServerHandler instances.
       This utility function will setup the correct inter process communication to retrieve logs from child processes,
       regardless of the process start method used (fork, spawn, forkserver)

    :param logger: Logger whose handlers to wrap. Default: Python root logger.
    :return Tuple[ServerHandler's name, dict of client handler settings]. The dict must be considered opaque.
    """
    if logger is None:
        logger = logging.getLogger()

    settings = {}

    for i, orig_handler in enumerate(list(logger.handlers)):
        handler_name = (
            str(orig_handler.name) if orig_handler.name is not None else f"mp-handler-{i}"
        )
        kwargs = {
            "name": "mp-handler-{0}".format(handler_name),
            "target_handler": orig_handler,
            "level": orig_handler.level if orig_handler.level is not None else logging.DEBUG,
            "start_method": ctx.get_start_method(),
            "ctx": ctx,
            "ctx_manager": ctx_manager,
        }
        server_handler, client_handler_settings = create_server_handler_factory(**kwargs)
        if server_handler is not None:
            logger.removeHandler(orig_handler)
            logger.addHandler(server_handler)
            settings[handler_name] = client_handler_settings

    return settings


def teardown_handlers(logger=None):
    """Unwraps a logger's handlers from their ServerHandler instances

    :param logger: Logger whose handlers to wrap. Default: Python root logger.
    """
    if logger is None:
        logger = logging.getLogger()

    for handler in logger.handlers:
        if isinstance(handler, ServerHandler):
            target_handler = handler.target_handler
            logger.removeHandler(handler)
            logger.addHandler(target_handler)
