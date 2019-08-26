### 1.介绍
python3自带的异步编程模块, 主要支持异步的网络IO操作, 子进程管理等功能;
### 2.使用示例
```python
import asyncio
import time
import sys
import logging

logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)


async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(what)


async def main():
    task1 = asyncio.create_task(
        say_after(1, 'hello'))  # 3.6用ensure_future

    task2 = asyncio.create_task(
        say_after(2, 'world'))
    # time.sleep(1)

    print(f"started at {time.strftime('%X')}")

    await task1
    await task2
    print(f"finished at {time.strftime('%X')}")

asyncio.run(main(), debug=True)  # 3.7
#loop = asyncio.get_event_loop()
#loop.run_until_complete(main())
#loop.close()
```
(1)通过async关键字定义协程;<br>

(2)通过asyncio.create_task()来定义异步任务;<br>

(3)通过await关键字来异步等待;<br>

(4)通过asyncio.run()来启动协程;<br>

#### 2.1 awaitable
可以用在await表达式中的对象, 主要有3种: coroutines, Tasks, 和 Futures.

tasks: asyncio.create_task()返回的对象;

Future是一个特殊的低级别等待对象，它表示异步操作的最终结果。
当等待Future对象时，它意味着协程将会等到Future在其他地方解析。
#### 2.2 task对象
>Tasks are used to run coroutines in event loops. If a coroutine awaits on a Future, the Task suspends the execution of the coroutine and waits for the completion of the Future. When the Future is done, the execution of the wrapped coroutine resumes.

>Use the high-level asyncio.create_task() function to create Tasks, or the low-level loop.create_task() or ensure_future() functions. Manual instantiation of Tasks is discouraged.

task对象用于在事件循环内运行, 管理协程;通常通过asyncio.create_task(),  loop.create_task() 或者 ensure_future()来生成, 具有如下几个方法:
<br>

(1) **cancel()**<br>
取消协程的运行, 会抛出一个CanceldeError;<br>

(2) **canceled()/done()** <br>
task是否取消/完成;<br>

(3) **result()/exception()** <br>
返回task运行异常/结果, 或者CanceledError, InvalidStateError; <br>

(4) **add_done_callback(callback, *, context=None) / remove_done_callback(callback)**<br>
添加/移除回调函数, task运行完成后执行;

(5) **get_stack(\*, limit=None) / print_stack(*, limit=None, file=None)** <br>
>Return the list of stack frames for this Task.
If the wrapped coroutine is not done, this returns the stack where it is suspended. If the coroutine has completed successfully or was cancelled, this returns an empty list. If the coroutine was terminated by an exception, this returns the list of traceback frames.

返回task中协程挂起位置的frame的列表, 如果task已运行结束, 返回空列表;
#### 2.3 future对象
>Future objects are used to bridge low-level callback-based code with high-level async/await code.

是连接底层的基于回调的代码和上层async/await的桥梁, 它代表一个异步操作的最终结果;<br>

(1)result() / exception()
>Return the result of the Future.

获取future中的结果/异常;

(2)set_result(result)<br>
>Mark the Future as done and set its result.

标记future已完成并设置future的结果;

(3)set_exception(exception)
>Mark the Future as done and set an exception.

标记future已完成并设置一个异常;

(4)done() / cancelled()

(5)add_done_callback(callback, \*, context=None) \ remove_done_callback(callback)
添加或移除future完成时执行的回调函数, context参数可指定运行时的上下文;

(6)cancel()
取消future对象的等待并开始运行回调函数;

(7)get_loop()
>Return the event loop the Future object is bound to.

获取future绑定的事件循环对象;

#### 2.4 api
(1)asyncio.run(coro, \*, debug=False)
> This function runs the passed coroutine, taking care of managing the asyncio event loop and finalizing asynchronous generators.

(2)asyncio.create_task(coro)
> Wrap the coro coroutine into a Task and schedule its execution. Return the Task object.

将协程封装成一个task对象<br>

(3)asyncio.sleep(delay, result=None, \*, loop=None)<br>

异步sleep

(4)asyncio.gather(\*aws, loop=None, return_exceptions=False)
>Run awaitable objects in the aws sequence concurrently.

异步执行多个task, 返回一个执行结果的列表; return_exceptions决定是否返回抛出的异常;
```python
import asyncio

async def factorial(name, number):
    f = 1
    for i in range(2, number + 1):
        print(f"Task {name}: Compute factorial({i})...")
        await asyncio.sleep(1)
        f *= i
    print(f"Task {name}: factorial({number}) = {f}")

async def main():
    # Schedule three calls *concurrently*:
    await asyncio.gather(
        factorial("A", 2),
        factorial("B", 3),
        factorial("C", 4),
    )

asyncio.run(main())

# Expected output:
#
#     Task A: Compute factorial(2)...
#     Task B: Compute factorial(2)...
#     Task C: Compute factorial(2)...
#     Task A: factorial(2) = 2
#     Task B: Compute factorial(3)...
#     Task C: Compute factorial(3)...
#     Task B: factorial(3) = 6
#     Task C: Compute factorial(4)...
#     Task C: factorial(4) = 24
```
(5)asyncio.shield(aw, \*, loop=None)
> Protect an awaitable object from being cancelled.

```python
res = await shield(something())
```
避免任务被取消;
用于需要取消协程的情况,如果主协程被取消,那么shield可以避免内部的任务被取消;

(6)asyncio.wait_for(aw, timeout, \*, loop=None)
>Wait for the aw awaitable to complete with a timeout.

异步执行的超时控制, 当超时发生将抛出异常;
```python
async def eternity():
    # Sleep for one hour
    await asyncio.sleep(3600)
    print('yay!')

async def main():
    # Wait for at most 1 second
    try:
        await asyncio.wait_for(eternity(), timeout=1.0)
    except asyncio.TimeoutError:
        print('timeout!')

asyncio.run(main())

# Expected output:
#
#     timeout!
```
(7)asyncio.wait(aws, \*, loop=None, timeout=None, return_when=ALL_COMPLETED)
>Run awaitable objects in the aws set concurrently and block until the condition specified by return_when.<br>
Returns two sets of Tasks/Futures: (done, pending).

运行多个task并且在满足给定条件或达到time out时返回已完成和未完成task的集合;<br>

return_when参数:<br>

Constant | Description
 -------------|------------
FIRST_COMPLETED | The function will return when any future finishes or is cancelled.
FIRST_EXCEPTION | The function will return when any future finishes by raising an exception. If no future raises an exception then it is equivalent to ALL_COMPLETED.
ALL_COMPLETED | The function will return when all futures finish or are cancelled.

```python
async def foo():
    return 42

async def main():
    task = asyncio.create_task(foo())
    done, pending = await asyncio.wait({task})

    if task in done:
        # do something

asyncio.run(main(), debug=True)
```
(8)asyncio.as_completed(aws, \*, loop=None, timeout=None)
>Run awaitable objects in the aws set concurrently. Return an iterator of Future objects. Each Future object returned represents the earliest result from the set of the remaining awaitables.

并发执行多个任务,并返回future对象的迭代器;<br>

(9)asyncio.run_coroutine_threadsafe(coro, loop)
>Submit a coroutine to the given event loop. Thread-safe.<br>
Return a concurrent.futures.Future to wait for the result from another OS thread.

在不同线程中把协程放入给定的事件循环;

(10)asyncio.current_task(loop=None)
>Return the currently running Task instance, or None if no task is running.

返回当前正在运行的task对象;

(11)asyncio.all_tasks(loop=None)
>Return a set of not yet finished Task objects run by the loop.

返回事件循环中所有的task对象;

(12)asyncio.iscoroutine(obj)<br>
判断一个对象是否是协程对象

(13)asyncio.iscoroutinefunction(func)<br>
判断一个对象是否是协程函数(async def 或者 @asyncio.coroutine)

#### 2.5 Generator-based Coroutines
```python
import asyncio
import time


@asyncio.coroutine
def say_after(delay, what, task=0):
    yield from asyncio.sleep(delay)
    print(what)

@asyncio.coroutine
def main():
    task1 = asyncio.create_task(
        say_after(1, 'hello'))

    task2 = asyncio.create_task(
        say_after(2, 'world', task1))
    print(f"started at {time.strftime('%X')}")
    yield from task1
    yield from task2
    print(f"finished at {time.strftime('%X')}")
    return 123

#a = asyncio.run(main())
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
```
