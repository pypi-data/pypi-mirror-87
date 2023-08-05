"""
@author  : MG
@Time    : 2020/10/9 12:01
@File    : run.py
@contact : mmmaaaggg@163.com
@desc    : 用于对策略进行回测
"""
import itertools
import json
import typing
from collections import defaultdict, OrderedDict
from datetime import datetime, date
from multiprocessing import Pool, cpu_count, Manager, Queue, Lock
from queue import Empty

import pandas as pd
from ibats_utils.mess import date_2_str
from tqdm import tqdm
from vnpy.app.cta_strategy import CtaTemplate
from vnpy.trader.constant import Interval

from quant_vnpy.backtest import DEFAULT_STATIC_ITEMS, CrossLimitMethod, CleanupOrcaServerProcessIntermittent
from quant_vnpy.backtest.cta_strategy.engine import BacktestingEngine
from quant_vnpy.config import logging

logger = logging.getLogger()
HAS_PANDAS_EXCEPTION = False


def get_output_file_path(*args, root_folder_name=None):
    import os
    if root_folder_name is None or root_folder_name == "":
        root_folder_name = date_2_str(datetime.now().date())
    file_path = os.path.join('output', root_folder_name, *args)
    dir_path, _ = os.path.split(file_path)
    os.makedirs(dir_path, exist_ok=True)
    return file_path


def run_backtest(
        strategy_class: typing.Type[CtaTemplate],
        vt_symbol: str = "RB9999.SHFE",
        interval: Interval = Interval.MINUTE,
        start: datetime = datetime(2017, 1, 1),
        rate: float = 2.5e-5,
        slippage: float = 1,
        size: float = 10,
        pricetick: float = 1,
        capital: int = 100000,
        end: datetime = datetime(2022, 1, 1),
        cross_limit_method: CrossLimitMethod = CrossLimitMethod.open_price,
        strategy_kwargs: typing.Optional[dict] = None,
        root_folder_name=None,
        file_name_header="",
        engine=None,
        output_available_only=False,
        open_browser_4_charts=False,
        log_statistic_markdown=False,
        show_indexes=None,
        output_statistics=True,
        lock: typing.Optional[Lock] = None,
) -> dict:
    """
    本地化运行策略回测程序
    """
    if file_name_header is None or file_name_header == '':
        file_name_header = date_2_str(end)

    image_file_name = get_output_file_path(
        vt_symbol, cross_limit_method.name, f'{file_name_header}.png', root_folder_name=root_folder_name)
    stat_file_name = get_output_file_path(
        vt_symbol, 'stat', f'{file_name_header}_stat.md', root_folder_name=root_folder_name)
    daily_result_file_name = get_output_file_path(
        vt_symbol, 'data', f'{file_name_header}_result.csv', root_folder_name=root_folder_name)
    param_file_name = get_output_file_path(
        vt_symbol, 'param', f'{file_name_header}_param.json', root_folder_name=root_folder_name)

    # 保存参数
    with open(param_file_name, 'w') as fp:
        json.dump(strategy_kwargs, fp=fp)

    # 初始化引擎
    load_data = True
    if engine is None:
        engine = BacktestingEngine()
    else:
        if engine.vt_symbol == vt_symbol \
                and engine.start == start \
                and engine.end == end \
                and engine.interval == interval:
            load_data = False

        # 清除上一轮测试数据
        engine.clear_data()

    # 设置环境参数
    engine.set_parameters(
        vt_symbol=vt_symbol,
        interval=interval,
        start=start,
        end=end,
        rate=rate,  # 手续费
        slippage=slippage,  # 滑点
        size=size,  # 乘数
        pricetick=pricetick,  # 最小价格变动
        capital=capital,
        cross_limit_method=cross_limit_method,
    )

    # 设置策略参数
    if strategy_kwargs is None:
        logger.warning('%s 回测没有设置参数项，使用默认参数', strategy_class.__name__)
        strategy_kwargs = {}

    engine.add_strategy(strategy_class=strategy_class, setting=strategy_kwargs)
    # 加载历史数据
    if load_data:
        if lock is not None:
            with lock:
                engine.load_data()
        else:
            engine.load_data()

    # 开始回测
    engine.run_backtesting()
    # 统计结果
    df = engine.calculate_result()
    # 统计绩效
    statistics = engine.calculate_statistics(output=output_statistics)

    if output_available_only and not statistics['available']:
        pass
    else:
        if df is not None:
            # engine.output(df)
            df[[_ for _ in df.columns if _ != "trades"]].to_csv(daily_result_file_name)
            # 展示图表
            engine.show_chart(
                image_file_name=image_file_name,
                open_browser_4_charts=open_browser_4_charts,
                show_indexes=show_indexes,
                lock=lock,
            )

        try:
            # 保存绩效结果
            statistics_s = pd.Series(statistics)
            statistics_s.name = file_name_header
            statistics_s.index.rename('item', inplace=True)
            if log_statistic_markdown:
                logger.info("\n:%s", statistics_s.to_markdown())

            with open(stat_file_name, 'w') as f:
                statistics_s.to_markdown(f, 'w')

            logger.info("策略绩效(保存到文件：%s)", stat_file_name)  # , statistics_s.to_markdown()
        except AttributeError:
            global HAS_PANDAS_EXCEPTION
            if not HAS_PANDAS_EXCEPTION:
                logger.warning("pandas 需要 1.0.0 以上版本才能够支持此方法")
                HAS_PANDAS_EXCEPTION = True

    return statistics


def _test_run_backtest():
    from strategies.trandition.double_ma.double_ma_strategy import DoubleMA
    run_backtest(
        DoubleMA,
        open_browser_4_charts=True
    )


def _process_backtest(strategy_cls, task_queue: Queue, results_dic: dict, lock: Lock,
                      statistic_items, multi_valued_param_name_list, name):
    """
    :param strategy_cls 策略类
    :param task_queue 任务参数队列
    :param results_dic 执行结果队列
    :param name 进程名称
    """
    logger.info("启动子进程 %s 监控任务队列 task_queue,结果返回给 results_dic", name)
    engine = BacktestingEngine()
    job_count = 0
    while True:
        try:
            job_count += 1
            # 阻塞等待消息队列传递参数
            key, backtest_param_kwargs = task_queue.get(block=True, timeout=5)
            logger.debug('process %s %d task| key=%s, backtest_param_kwargs=%s',
                         name, job_count, key, backtest_param_kwargs)
            try:
                statistics_dic = run_backtest(
                    strategy_cls,
                    engine=engine,
                    output_statistics=False,
                    lock=lock,
                    **backtest_param_kwargs
                )
            except Exception:
                logger.exception("%s run_backtest error", name)
                task_queue.task_done()
                continue

            task_queue.task_done()
            strategy_kwargs = backtest_param_kwargs["strategy_kwargs"]
            file_name_header = backtest_param_kwargs["file_name_header"]
            # strategy_kwargs.update({k: v for k, v in statistics_dic.items() if k in statistic_items})
            # 剔除 single_valued_param_name_set
            statistics_dic = OrderedDict([(k, v) for k, v in statistics_dic.items() if k in statistic_items])
            statistics_dic.update({k: v for k, v in strategy_kwargs.items() if k in multi_valued_param_name_list})
            statistics_dic["file_name_header"] = file_name_header
            # key = (
            #     backtest_param_kwargs["vt_symbol"],
            #     backtest_param_kwargs["slippage"],
            #     backtest_param_kwargs["size"],
            #     backtest_param_kwargs["cross_limit_method"],
            # )
            with lock:
                # 多进程 dict 对象只能使用 赋值 操作。不可以使用 [].append 的操作。
                # 因此不可以使用 setdefault(key, []).append()
                if key in results_dic:
                    results = results_dic[key]
                    results.append(statistics_dic)
                else:
                    results = [statistics_dic]

                results_dic[key] = results

            logger.debug('process %s %d task| key=%s finished',
                         name, job_count, key)
        except Empty:
            logger.warning("Process '%s' 没有收到任务信息,结束进程，累计完成 %d 个任务",
                           name, job_count)
            break


def get_param_values_iter(param_values_dic: typing.Union[dict, typing.List[dict]]):
    if isinstance(param_values_dic, dict):
        param_values_dic_list = [param_values_dic]
    elif isinstance(param_values_dic, list):
        param_values_dic_list = param_values_dic
    else:
        raise ValueError(f"param_values_dic {type(param_values_dic)} 参数类型不支持")

    param_name_list = None
    param_values_iter_source = []
    for param_values_dic in param_values_dic_list:
        if param_name_list is None:
            param_name_list = list(param_values_dic.keys())

        param_iter = itertools.product(*[
            param_values_dic[_] if _ in param_values_dic else [None] for _ in param_name_list
        ])
        param_values_iter_source.append(param_iter)

    param_values_iter = itertools.chain(*param_values_iter_source)
    return param_name_list, param_values_iter


def get_backtest_params_iter(
        backtest_param_list: typing.Union[dict, typing.List[dict]],
        param_values_dic: typing.Union[dict, typing.List[dict]],
):
    """
    返回参数参数名称列表以及迭代器兑现
    :param backtest_param_list 合约列表(可以是 str 数组,或者 tuple 数组,如果是 tuple 对应 (vt_symbol, slippage, size)
    :param param_values_dic 策略类 参数数组字典,key为参数名称, value 为数组
    """
    param_name_list, param_values_iter = get_param_values_iter(param_values_dic)

    if isinstance(backtest_param_list, dict):
        backtest_param_list = [backtest_param_list]

    backtest_params_iter = itertools.product(backtest_param_list, param_values_iter)
    return param_name_list, backtest_params_iter


def bulk_backtest(
        strategy_cls: typing.Type[CtaTemplate],
        vt_symbol_list: list,
        param_values_dic: typing.Union[typing.Dict[str, list], typing.List[typing.Dict[str, list]]],
        start: datetime = datetime(2017, 1, 1),
        end: datetime = datetime(2022, 1, 1),
        available_backtest_params_check_func: typing.Optional[typing.Callable] = None,
        file_name_func: typing.Optional[typing.Callable] = None,
        statistic_items: typing.Optional[list] = None,
        output_available_only: bool = False,
        open_browser_4_charts: bool = False,
        root_folder_name: typing.Optional[str] = None,
        multi_process: int = 0
):
    """
    :param strategy_cls 策略类
    :param vt_symbol_list 合约列表(可以是 str 数组,或者 tuple 数组,
        如果是 tuple 对应 (vt_symbol, slippage, size, cross_limit_method)
    :param param_values_dic 策略类 参数数组字典,key为参数名称, value 为数组
    :param start 回测日期范围
    :param end 回测日期范围
    :param available_backtest_params_check_func 如果希望忽略部分参数组合，可以自定义函数，对每一个组合进行筛选，False为忽略该参数
    :param file_name_func 自定义文件头名称，默认为None，所有["参数名+参数", ...]用下划线链接
    :param statistic_items 策略类 统计项默认 DEFAULT_STATIC_ITEMS
    :param output_available_only
    :param open_browser_4_charts
    :param root_folder_name 策略类 保存跟目录名称,None 时为当前系统日期
    :param multi_process 0 单进程, -1 为CPU数量,正数为对应的进程数
    """
    # vt_symbol_list = [
    #     # (vt_symbol, slippage, size)
    #     ("RB9999.SHFE", 1, 10, CrossLimitMethod.open_price),
    #     ("I9999.DCE", 0.5, 100, CrossLimitMethod.open_price),
    #     ("HC9999.SHFE", 1, 10, CrossLimitMethod.open_price)
    # ]
    # param_prod_dic = dict(
    #     target_n_bars=[10, 20, 30, 60],
    #     threshold=[0.001, 0.002, 0.003],
    #     method=['svr', 'linear', 'lasso', 'ridge', 'sgd'],
    # )
    if statistic_items is None:
        statistic_items = DEFAULT_STATIC_ITEMS

    if root_folder_name is None:
        root_folder_name = f'bulk_backtest_{date_2_str(date.today())}'

    # 整理参数
    param_name_list, backtest_params_iter = get_backtest_params_iter(vt_symbol_list, param_values_dic)
    # backtest_params_count = len(list(backtest_params_iter))
    params_df = pd.DataFrame([_[1] for _ in backtest_params_iter], columns=param_name_list)
    backtest_params_count = params_df.shape[0]
    # 记录所有 单一值 变量的名字
    single_valued_param_name_set = set()
    for name in param_name_list:
        if params_df[name].unique().shape[0] == 1:
            single_valued_param_name_set.add(name)

    multi_valued_param_name_list = [_ for _ in param_name_list if _ not in single_valued_param_name_set]
    logger.info(f'开始批量运行，包含 {len(vt_symbol_list)} 个合约， {len(param_name_list)} 个参数，总计 {backtest_params_count:,d} 个回测')
    # 再次获得迭代器进行循环
    _, backtest_params_iter = get_backtest_params_iter(vt_symbol_list, param_values_dic)
    backtest_params_iter = tqdm(enumerate(backtest_params_iter), total=backtest_params_count)

    # 多进程情况启动进程池
    if multi_process != 0:
        # 多进程情况下启动子进程,等待消息带回来传递参数
        if multi_process == -1:
            # 默认CPU数量
            multi_process = cpu_count()

        engine = None
        # 首次运行是启动进程池
        logger.info("启动进程池")
        pool = Pool(processes=multi_process)
        manager = Manager()
        # task_queue = JoinableQueue(multi_process * 2)
        task_queue = manager.Queue(multi_process * 2)
        lock = manager.Lock()
        results_dic = manager.dict()
        # 建立子进程实例
        for _ in range(multi_process):
            name = f"process_{_}"
            logger.info("启动子进程 %s", name)

            def print_error(value):
                logger.error("%s 启动 error: %s", name, value)

            pool.apply_async(
                _process_backtest,
                args=(strategy_cls, task_queue, results_dic, lock,
                      statistic_items, multi_valued_param_name_list, name),
                error_callback=print_error
            )

        cleanup_thread = CleanupOrcaServerProcessIntermittent()
        cleanup_thread.start()
    else:
        # 单进程准备好回测引擎
        results_dic = defaultdict(list)
        engine = BacktestingEngine()
        pool = None
        task_queue = None
        cleanup_thread = None

    # 开始对每一种参数组合进行回测
    for n, (backtest_params, param_values) in backtest_params_iter:
        # 参数检查及整理
        cross_limit_method = CrossLimitMethod.open_price
        if isinstance(backtest_params, tuple):
            # vt_symbol 是 tuple 的话,自动拆包
            if len(backtest_params) == 2:
                vt_symbol, slippage = backtest_params
                size = 10
            elif len(backtest_params) == 3:
                vt_symbol, slippage, size = backtest_params
            elif len(backtest_params) == 4:
                vt_symbol, slippage, size, cross_limit_method = backtest_params
            else:
                raise ValueError(f"backtest_params: {backtest_params} 长度不支持")

            backtest_params = vt_symbol, slippage, size, cross_limit_method
        else:
            vt_symbol, slippage, size = backtest_params, 1, 10

        backtest_params_iter.set_description(vt_symbol)

        # 设置参数
        strategy_kwargs = {k: v for k, v in zip(param_name_list, param_values)}
        backtest_param_kwargs = dict(
            vt_symbol=vt_symbol,
            slippage=slippage,
            size=size,
            strategy_kwargs=strategy_kwargs,
            output_available_only=output_available_only,
            open_browser_4_charts=open_browser_4_charts,
            start=start,
            end=end,
            rate=2.5e-5,
            interval=Interval.MINUTE,
            pricetick=1,
            cross_limit_method=cross_limit_method,
        )
        # 检查参数有效性
        if available_backtest_params_check_func is not None and not available_backtest_params_check_func(
                **backtest_param_kwargs):
            continue

        # 设置 root_folder_name, file_name_header 参数
        if file_name_func is None:
            file_name_header = '_'.join([
                f"{k}{v}" for k, v in zip(param_name_list, param_values)
                if k not in single_valued_param_name_set
            ]) + f'_{cross_limit_method.value}{cross_limit_method.name}'
        else:
            file_name_header = file_name_func(single_valued_param_name_set=single_valued_param_name_set,
                                              **backtest_param_kwargs)
            if isinstance(file_name_header, tuple):
                root_folder_name_ret, file_name_header = file_name_header
                if root_folder_name_ret is not None:
                    root_folder_name = root_folder_name_ret

        backtest_param_kwargs["file_name_header"] = file_name_header
        backtest_param_kwargs["root_folder_name"] = root_folder_name
        # 开始回测
        if multi_process != 0:
            logger.debug("put key=%s task=%s in queue", backtest_params, backtest_param_kwargs)
            # 多进程 参数加入队列
            task_queue.put((backtest_params, backtest_param_kwargs), block=True)
        else:
            # 单进程直接调用
            statistics_dic = run_backtest(
                strategy_cls,
                engine=engine,
                output_statistics=False,
                **backtest_param_kwargs
            )
            # strategy_kwargs.update({k: v for k, v in statistics_dic.items() if k in statistic_items})
            # 剔除 single_valued_param_name_set
            statistics_dic = OrderedDict([(k, v) for k, v in statistics_dic.items() if k in statistic_items])
            statistics_dic.update({k: v for k, v in strategy_kwargs.items() if k in multi_valued_param_name_list})
            statistics_dic["file_name_header"] = file_name_header
            results_dic[backtest_params].append(statistics_dic)

    # 如果是多进程，则等待全部进程结束
    if multi_process != 0:
        logger.info("等待所有进程结束")
        task_queue.join()
        logger.info("等待所有进程结束")
        pool.close()
        logger.info("关闭进程池（pool）不再接受新的任务")
        cleanup_thread.is_running = False
        cleanup_thread.join()
        logger.info("关闭 CleanupOrcaServerProcessIntermittent 线程")
        pool.join()
        logger.info("进程池（pool）所有任务结束")

    backtest_params_list = list(results_dic.keys())
    backtest_params_count = len(backtest_params_list)
    logger.info("backtest_params_list %s", backtest_params_list)
    logger.info("param_name_list %s", param_name_list)
    logger.info("multi_valued_param_name_list %s", multi_valued_param_name_list)
    if backtest_params_count == 0:
        result_df = None
    elif backtest_params_count == 1:
        result_df = pd.DataFrame(results_dic[backtest_params_list[0]])
    else:
        try:
            result_df = pd.concat(
                [pd.DataFrame(results_dic[_]).set_index(multi_valued_param_name_list) for _ in backtest_params_list],
                keys=['_'.join([
                    f"{_.value}{_.name}" if isinstance(_, CrossLimitMethod) else str(_) for _ in backtest_params
                ]) for backtest_params in backtest_params_list],
                axis=1,
            )
        except ValueError:
            logger.exception("合并 DataFrame 异常")
            result_df = pd.concat(
                [pd.DataFrame(results_dic[_]).set_index(multi_valued_param_name_list) for _ in backtest_params_list],
            )

    if result_df is not None:
        result_df.drop_duplicates(inplace=True)
        csv_file_path = get_output_file_path(
            f'result_df_{date_2_str(datetime.now())}.csv', root_folder_name=root_folder_name)
        result_df.to_csv(csv_file_path)
        logger.info("总计 %d 条测试记录被保存到 %s", result_df.shape[0], csv_file_path)
        csv_file_path = get_output_file_path(
            f'result_df_grouped_{date_2_str(datetime.now())}.xlsx', root_folder_name=root_folder_name)
        result_df.to_excel(csv_file_path)

    return result_df


def _test_bulk_backtest():
    from strategies.statistic.rolling_regression.rolling_regression_strategy import RollingRegressionStrategy
    result_df = bulk_backtest(
        RollingRegressionStrategy,
        vt_symbol_list=[
            # (vt_symbol, slippage, size)
            ("RB9999.SHFE", 1, 10),
            ("I9999.DCE", 0.5, 100),
            ("HC9999.SHFE", 1, 10, CrossLimitMethod.open_price),
            ("HC9999.SHFE", 1, 10, CrossLimitMethod.mid_price)
        ],
        param_values_dic=dict(
            target_n_bars=[10, 20, 30, 60],
            threshold=[0.001, 0.002, 0.003],
            method=['svr', 'linear', 'lasso', 'ridge', 'sgd'],
        ),
    )


def _test_bulk_backtest_double_ma():
    from strategies.trandition.double_ma.double_ma_strategy import DoubleMA
    result_df = bulk_backtest(
        DoubleMA,
        vt_symbol_list=[
            # (vt_symbol, slippage, size)
            ("RB9999.SHFE", 1, 10, CrossLimitMethod.open_price),
            ("RB9999.SHFE", 1, 10, CrossLimitMethod.mid_price),
            ("I9999.DCE", 0.5, 100),
            ("HC9999.SHFE", 1, 10)
        ],
        param_values_dic=dict(
            fast_window=[20, 30],
        ),
        multi_process=2
    )


if __name__ == "__main__":
    # _test_run_backtest()
    # _test_bulk_backtest()
    _test_bulk_backtest_double_ma()
