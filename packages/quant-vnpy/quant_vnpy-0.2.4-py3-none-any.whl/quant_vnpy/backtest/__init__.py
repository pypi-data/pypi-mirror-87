"""
@author  : MG
@Time    : 2020/10/9 12:00
@File    : __init__.py.py
@contact : mmmaaaggg@163.com
@desc    : 用于
"""
import enum
import time
from threading import Thread


class CrossLimitMethod(enum.Enum):
    open_price = 0
    mid_price = 1
    worst_price = 2


class CleanupOrcaServerProcessIntermittent(Thread):

    def __init__(self, interval=60):
        super().__init__()
        self.is_running = True
        self.interval = interval

    def run(self) -> None:
        from plotly.io._orca import cleanup

        while self.is_running:
            time.sleep(self.interval)
            cleanup()


DEFAULT_STATIC_ITEMS = [
    "available", "info_ratio",
    "max_new_higher_duration", "daily_trade_count", "return_drawdown_ratio",
]
