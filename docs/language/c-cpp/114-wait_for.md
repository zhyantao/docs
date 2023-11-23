# wait_for

```cpp
#include <iostream>
#include <string>
#include <chrono>
#include <thread>
#include <mutex>
#include <condition_variable>

std::mutex m;
std::condition_variable cv;
std::string data;

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
