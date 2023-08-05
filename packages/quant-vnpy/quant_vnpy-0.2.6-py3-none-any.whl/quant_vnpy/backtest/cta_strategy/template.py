"""
@author  : MG
@Time    : 2020/11/16 10:20
@File    : template.py
@contact : mmmaaaggg@163.com
@desc    : 用于
"""
import pandas as pd
from ibats_utils.mess import datetime_2_str
from vnpy.app.cta_strategy import TargetPosTemplate as TargetPosTemplateBase
from vnpy.trader.constant import Offset
from vnpy.trader.object import OrderData, BarData

from quant_vnpy.backtest.cta_strategy.run import get_output_file_path
from quant_vnpy.config import logging
from quant_vnpy.db.orm import StrategyStatusEnum, StrategyStatusMonitorThread


class TargetPosTemplate(TargetPosTemplateBase):

    def __init__(self, cta_engine, strategy_name, vt_symbol, setting):
        super().__init__(cta_engine, strategy_name, vt_symbol, setting)
        self.logger = logging.getLogger(strategy_name)
        self.orders = []
        self.current_bar = None
        self.bar_count = 0
        self._strategy_status = StrategyStatusEnum.Created
        self._strategy_status_monitor = StrategyStatusMonitorThread(
            self.__class__.__name__ if self.strategy_name is None else self.strategy_name,
            self._get_strategy_status,
            self._set_strategy_status,
            self.vt_symbol,
        )
        self._lock = self._strategy_status_monitor.lock

    def _set_strategy_status(self, status: StrategyStatusEnum):
        if self._strategy_status == status:
            return

        if status == StrategyStatusEnum.RunPending and self._strategy_status not in (
                StrategyStatusEnum.Created, StrategyStatusEnum.Running
        ):
            # StrategyStatusEnum.RunPending 状态只从数据库端发起
            if self._lock is not None:
                self._lock.acquire()

            try:
                # 保险起见，为防止出现死循环调用，在 on_start 先把状态调整过来
                self._strategy_status = status
                self.write_log(f"策略 {self.strategy_name}[{self.vt_symbol}] 状态 {status.name} 被远程启动")
            finally:
                if self._lock is not None:
                    self._lock.release()

            self.on_start()

        elif status == StrategyStatusEnum.StopPending and self._strategy_status == StrategyStatusEnum.Running:
            # StrategyStatusEnum.StopPending 状态只从数据库端发起
            if self._lock is not None:
                self._lock.acquire()

            try:
                # 保险起见，为防止出现死循环调用，在 on_stop 先把状态调整过来
                self._strategy_status = status
                self.write_log(f"策略 {self.strategy_name}[{self.vt_symbol}] 状态 {status.name} 被远程停止")
            finally:
                if self._lock is not None:
                    self._lock.release()

            self.on_stop()
        else:
            self.write_log(f"策略 {self.strategy_name}{self.vt_symbol} 状态 {status.name}")
            self._strategy_status = status

    def _get_strategy_status(self) -> StrategyStatusEnum:
        return self._strategy_status

    def on_init(self) -> None:
        super().on_init()
        self.bar_count = 0
        self._set_strategy_status(StrategyStatusEnum.Initialized)
        self._strategy_status_monitor.start()

    def on_start(self) -> None:
        super().on_start()
        self._set_strategy_status(StrategyStatusEnum.Running)
        # 整理持仓信息
        self.write_log(f"策略启动，当前初始持仓： {self.vt_symbol} {self.pos}")
        self.put_event()

    def on_bar(self, bar: BarData):
        super().on_bar(bar)
        self.current_bar = bar
        self.bar_count += 1

    def on_order(self, order: OrderData):
        super().on_order(order)
        self.write_log(
            f"{order.direction.value} {order.offset.value} {order.price:.1f}"
            if order.datetime is None else
            f"{datetime_2_str(order.datetime)} {order.direction.value} {order.offset.value} {order.price:.1f}"
        )
        current_pos = int(self.pos)
        order_datetime = order.datetime
        if order.offset == Offset.OPEN:
            self.write_log(
                f"{order.vt_symbol:>11s} {order.direction.value} {order.offset.value:4s} "
                f"{order.price:.1f} {current_pos:+d} {order.volume:+.0f} "
                if order_datetime is None else
                f"{datetime_2_str(order_datetime)} {order.vt_symbol} {order.direction.value} {order.offset.value:4s} "
                f"{order.price:.1f} {current_pos:+d} {order.volume:+.0f}"
            )
        else:
            self.write_log(
                f"{order.vt_symbol:>11s} {order.direction.value} {order.offset.value:4s} "
                f"{order.price:.1f}       {current_pos:+d} {order.volume:+.0f} "
                if order_datetime is None else
                f"{datetime_2_str(order_datetime)} {order.vt_symbol} {order.direction.value} {order.offset.value:4s} "
                f"{order.price:.1f}       {current_pos:+d} {order.volume:+.0f}"
            )

        self.orders.append(order)

    def on_stop(self):
        super().on_stop()
        order_df = pd.DataFrame([{
            "datetime": _.datetime,
            "symbol": _.symbol,
            "direction": _.direction.value,
            "offset": _.offset.value,
            "price": _.price,
            "volume": _.volume,
            "order_type": _.type.value,
        } for _ in self.orders])
        file_path = get_output_file_path(
            "data", "orders.csv",
            root_folder_name=self.strategy_name,
        )
        order_df.to_csv(file_path)
        self.logger.info('运行期间下单情况明细：\n%s', order_df)
        self._set_strategy_status(StrategyStatusEnum.Stopped)
        self.put_event()

    def write_log(self, msg: str):
        msg = f"{self.strategy_name} {msg}"
        super().write_log(msg)
        self.logger.info(msg)


if __name__ == "__main__":
    pass
