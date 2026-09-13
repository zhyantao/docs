# future

`std::future` 是 C++11 提供的异步任务结果容器：把耗时的计算放到后台线程执行，
调用方先继续做别的事情，需要结果时再通过 `future` 获取。它有三种典型的来源：

1. **`std::packaged_task`**：把可调用对象包装成"任务"，`get_future()` 取得对应的 `future`，
   然后手动决定在哪个线程上运行（常用于线程池）；
2. **`std::async`**：最简单的用法，由标准库决定（或通过 `std::launch::async` 强制）在新线程上异步执行；
3. **`std::promise`**：生产端与 `future` 手动配对，可以在任意线程中通过
   `set_value()`（或示例中的 `set_value_at_thread_exit()`）设置结果，控制最灵活。

常用成员函数：

- `get()`：阻塞直到结果就绪，返回结果（只能调用一次，调用后 `future` 失效）；
- `wait()`：阻塞直到结果就绪，不返回结果；
- `wait_for()` / `wait_until()`：限时等待，返回 `std::future_status` 表示就绪/超时。

```cpp
#include <future>
#include <iostream>
#include <thread>

int main() {
    // 来自 packaged_task 的 future
    std::packaged_task<int()> task([]() {
        return 7;
    });                                      // 包装函数
    std::future<int> f1 = task.get_future(); // 获取 future
    std::thread(std::move(task)).detach();   // 在线程上运行

    // 来自 async() 的 future
    std::future<int> f2 = std::async(std::launch::async, []() {
        return 8;
    });

    // 来自 promise 的 future
    std::promise<int> p;
    std::future<int> f3 = p.get_future();
    std::thread([&p] {
        p.set_value_at_thread_exit(9);
    }).detach();

    std::cout << "Waiting..." << std::flush;
    f1.wait();
    f2.wait();
    f3.wait();
    std::cout << "Done!\nResults are: " << f1.get() << ' ' << f2.get() << ' ' << f3.get()
              << '\n';
}
```
