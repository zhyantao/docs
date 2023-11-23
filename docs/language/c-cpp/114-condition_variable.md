# condition_variable

条件变量（`condition_vatiable`）主要用于线程间同步。

条件变量是同步原语，能用于阻塞一个线程，或同时阻塞多个线程吗，直到另一个线程修改共享变量（条件），并通知条件变量。

有意修改变量的线程必须：

- 获得 `std::mutex`（常通过 `std::lock_guard`）
- 在保有锁时进行修改
- 在 `std::condition_variable` 上执行 `notify_one` 或 `notify_all`（不需要为通知保有锁）

**即使共享变量是原子的，也必须在互斥下修改它，以正确地发布修改到等待的线程。**

任何有意在 `std::condition_variable` 上等待的线程必须：

- 获得用于保护共享变量的 `std::unique_lock<std::mutex>`
- 使用 `wait`、`wait_for` 及 `wait_until` 等待其他线程释放互斥锁

注意事项：

- `std::condition_variable` 只可与 `std::unique_lock<std::mutex>` 一同使用；此限制在一些平台上允许最大效率。
- `std::condition_variable_any` 提供可与任何基础可锁对象，例如 `std::shared_lock` 一同使用的条件变量。
- `condition_variable` 允许 `wait`、`wait_for`、`wait_until`、`notify_one` 及 `notify_all` 被同时调用。

```cpp
#include <iostream>
#include <string>
#include <chrono>
#include <thread>
#include <mutex>
#include <condition_variable>

std::mutex m;
std::condition_variable cv; // 条件变量
std::string data;           // 共享变量

bool ready = false;
bool processed = false;

// >>>> step 2
void worker_thread() // 这个函数什么时候才会被执行？
{
    // 等待直至 main() 发送数据
    std::cout << "Worker: before unique_lock\n";
    std::unique_lock<std::mutex> lk(m);
    cv.wait(lk, []{return ready;});  // ready == true 后继续执行

    // 等待后，我们占有锁
    std::cout << "Worker thread is processing data\n";
    data += " after processing";

    // 发送数据回 main()
    processed = true;
    std::cout << "Worker thread signals data processing compeleted\n";

    // 通知前完成手动解锁，以避免等待线程才被唤醒就阻塞（细节见 notify_one）
    lk.unlock();

    // 发送通知
    cv.notify_one();
}

int main()
{
    // 创建 worker 线程，该线程运行的代码为 worker_thread
    std::thread worker(worker_thread);

    // 睡眠可以保证子线程先运行，否则主线程将先执行
    std::chrono::milliseconds dura(500);
    std::this_thread::sleep_for(dura);

    // >>>> step 1
    data = "Example data";
    // 发送数据到 worker 线程
    {
        std::lock_guard<std::mutex> lk(m);  // lock_guard 离开作用域后自动解锁
        ready = true;
        std::cout << "main() signals data ready for processing\n";
    }
    cv.notify_one();

    // >>>> step 3
    // 等候 worker
    {
        std::unique_lock<std::mutex> lk(m);
        cv.wait(lk, []{return processed;});
    }
    std::cout << "Back in main(), data = " << data << '\n';

    worker.join();  // 等待子线程 worker 退出
}

// 运行： g++ wait_for.cpp --std=c++11 -lpthread
```
