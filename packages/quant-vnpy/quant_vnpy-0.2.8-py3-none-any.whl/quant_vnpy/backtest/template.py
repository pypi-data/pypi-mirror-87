"""
@author  : MG
@Time    : 2020/10/26 13:53
@File    : template.py
@contact : mmmaaaggg@163.com
@desc    : 用于对vnpy元 template对象继续增强
"""
import json
import logging
from collections import defaultdict
from ibats_utils.mess import date_2_str
from vnpy.app.cta_strategy import TargetPosTemplate as TargetPosTemplateBase
from vnpy.trader.object import BarData


class TargetPosTemplate(TargetPosTemplateBase):
    # 熔断机制，避免出现某一日频繁交易的情况，设定每天最多交易次数上限。
    # 默认值 0 不做限制
    circuit_breaker = 0

    def __init__(self, cta_engine, strategy_name, vt_symbol, setting):
        """实例函数"""
        super().__init__(cta_engine, strategy_name, vt_symbol, setting)
        self._date_trade_count_dic = defaultdict(lambda: 0)
        self._current_bar = None  # 记录当前bar实例
        self.logger = logging.getLogger(self.__class__.__name__)
        self.write_log(f"{strategy_name} on {vt_symbol} setting=\n{json.dumps(setting, indent=4)}")

    def write_log(self, msg: str):
        super().write_log(msg)
        self.logger.info(msg)

    def on_bar(self, bar: BarData):
        """
        Callback of new bar data update.
        """
        super().on_bar(bar)
        self._current_bar = bar

    def set_target_pos(self, target_pos):
        """在函数功能基础上增加熔断机制"""
        cur_date = self._current_bar.datetime.date()
        count = self._date_trade_count_dic[cur_date] + 1
        # 即使没有发出交易请求也记录交易次数，便于日后统计每日熔断次数
        self._date_trade_count_dic[cur_date] = count
        if 0 < self.circuit_breaker < self._date_trade_count_dic[cur_date]:
            self.logger.error("%s 当日第 %d 次交易 > %d 上限，触发熔断", date_2_str(cur_date), count, self.circuit_breaker)
            return None
        else:
            super().set_target_pos(target_pos)
            return target_pos


if __name__ == "__main__":
    pass
