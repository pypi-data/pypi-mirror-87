import tqdm
from multiprocessing import Pool, cpu_count, RLock
from functools import partial, reduce

MULTI_WORKERS_NUM = cpu_count() - 1


def multi_worker(data, func, workers=MULTI_WORKERS_NUM):
    """
    多进程运行，带进度
    :param data: 数据
    :param func: 处理的func
    :param workers: cpu数量，默认本机cpu数量-1
    :return:
    """
    pool = Pool(workers, initializer=tqdm.tqdm.set_lock, initargs=(RLock(),))
    data_list = list()
    cl = len(data)
    k = int(cl / workers)
    worker_func = partial(_multi_worker_func, func)
    for i in range(workers):
        if i == workers - 1:
            data_list.append(data[i * k : cl])
        else:
            data_list.append(data[i * k : (i + 1) * k])
    else:
        rst = pool.map(worker_func, enumerate(data_list))
        rst = reduce(list.__add__, rst)
        return rst


def _multi_worker_func(func, args):
    _ix, _data = args
    _rst = list()
    for _i in tqdm.tqdm(_data, position=_ix):
        _rst.append(func(_i))
    return _rst
