import asyncio
import time
import threading
import multiprocessing


# 模拟网络请求
def mock_io(delay, name):
    time.sleep(delay)
    return f"{name}完成"


# 1. 普通顺序执行（慢）
def sync_version():
    start = time.time()
    mock_io(1, "任务1")
    mock_io(1, "任务2")
    print(f"同步: {time.time()-start:.1f}秒")


# 2.多进程（快一点）
def process_version():
    start = time.time()
    # 创建多进程
    p1 = multiprocessing.Process(target=mock_io, args=(1, '进程1'))
    p2 = multiprocessing.Process(target=mock_io, args=(1, '进程2'))
    # 启动多进程
    p1.start()
    p2.start()
    # 注意join和守护线程不一样。守护线程是生命周期机制：被动跟随，主程序结束你也结束，一般用于后台服务
    # join()是同步机制：主动控制，等这个任务干完了，我再继续往下走，一般用于等待结果的场景。
    # 等待结果结束
    p1.join()
    p2.join()
    print(f"进程: {time.time() - start:.1f}秒")


# 3. 多线程执行（快多了）
def thread_version():
    start = time.time()
    t1 = threading.Thread(target=mock_io, args=(1, "线程1"))
    t2 = threading.Thread(target=mock_io, args=(1, "线程2"))
    # 启动线程
    t1.start()
    t2.start()
    # 等待线程执行完
    # 注意join和守护线程不一样。守护线程是生命周期机制：被动跟随，主程序结束你也结束，一般用于后台服务
    # join()是同步机制：主动控制，等这个任务干完了，我再继续往下走，一般用于等待结果的场景。
    t1.join()
    t2.join()
    print(f"线程: {time.time()-start:.1f}秒")


# 4. 协程执行（理论上最快）
async def async_version():
    start = time.time()

    async def async_io(delay, name):
        await asyncio.sleep(delay)
        return f"{name}完成"

    # 并发执行
    task1 = asyncio.create_task(async_io(1, "协程1"))
    task2 = asyncio.create_task(async_io(1, "协程2"))
    await task1
    await task2

    print(f"协程: {time.time()-start:.1f}秒")


if __name__ == '__main__':
    # 运行对比
    print("=== 执行时间对比 ===")
    sync_version()  # 约2秒
    process_version() # 约1秒
    thread_version()  # 约1秒
    asyncio.run(async_version())  # 约1秒