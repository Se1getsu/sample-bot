import json
import logging
import requests
import sys
from typing import List, TextIO

logger = logging.getLogger()

class LevelFilter(logging.Filter):
    def __init__(self, levels: List[int]):
        self.levels = levels

    def filter(self, record: logging.LogRecord):
        return record.levelno in self.levels

class DiscordHandler(logging.StreamHandler):
    def __init__(self, url: str):
        super().__init__()
        self.url = url

    def emit(self, record: logging.LogRecord):
        self.formatter.format
        msg = self.format(record)
        self.send_message(msg)

    def send_message(self, text):
        data = json.dumps({'content': text})
        headers = {'Content-Type': 'application/json'}
        response = requests.post(self.url, headers=headers, data=data)
        return response

def _default_formatter() -> logging.Formatter:
    fmt = '[{asctime}] {levelname}: {name}: {message}'
    datefmt = '%Y-%m-%d %H:%M:%S'
    return logging.Formatter(fmt, datefmt, style='{')

def _handler(
    url: str,
    levels: List[int],
    formatter: logging.Formatter,
    default_stream: TextIO
) -> logging.StreamHandler:
    if url != "default":
        handler = DiscordHandler(url)
    else:
        handler = logging.StreamHandler(stream=default_stream)
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(formatter)
    handler.addFilter(LevelFilter(levels))
    return handler

def setup_logger(
    info_webhook: str,
    error_webhook: str,
    *,
    formatter: logging.Formatter = None
) -> None:
    if formatter is None: formatter = _default_formatter()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(_handler(info_webhook, [logging.INFO], formatter, sys.stdout))
    logger.addHandler(_handler(error_webhook, [logging.ERROR], formatter, sys.stderr))
