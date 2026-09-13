# \_\_thread

`__thread` 是 GCC 提供的一个线程局部存储 (TLS) 的修饰符。

在 C 语言中，如果一个变量被 `__thread` 修饰，那么这个变量就可以被每个线程单独拥有一份实例，各个线程对这个变量的操作不会影响到其他线程。这种变量也被称为线程局部存储变量。

`__thread` 变量的生命周期是与线程相同的，当线程开始时创建，在线程结束时销毁。这意味着，对于每一个线程来说，所有使用了 `__thread` 修饰的变量都拥有一个独立的实例。

需要注意的是，`__thread` 只能用于修饰全局变量或静态变量，不能用于函数内部的局部变量。

## 示例

```cpp
#include <pthread.h>
#include <stdio.h>

__thread int tls_counter = 0;

void* worker(void* arg) {
    for (int i = 0; i < 3; i++) {
        tls_counter++;
        printf("thread %d: counter = %d\n", *(int*)arg, tls_counter);
    }
    return NULL;
}

int main() {
    pthread_t t1, t2;
    int id1 = 1, id2 = 2;
    pthread_create(&t1, NULL, worker, &id1);
    pthread_create(&t2, NULL, worker, &id2);
    pthread_join(t1, NULL);
    pthread_join(t2, NULL);
    // 两个线程各自打印 1、2、3，互不影响
    return 0;
}
```

## C++11 的替代：thread_local

C++11 引入了标准的 `thread_local` 关键字，功能与 `__thread` 类似，且是标准语法、跨编译器：

```cpp
#include <iostream>
#include <thread>

thread_local int tls_counter = 0; // 每个线程拥有独立的副本

void worker() {
    tls_counter++;
    std::cout << "counter = " << tls_counter << std::endl;
}
```

新代码推荐使用 `thread_local`；`__thread` 主要用于兼容旧代码或 GCC 特有的 C 代码。

参考文献：

1. <https://gcc.gnu.org/onlinedocs/gcc-3.3.1/gcc/Thread-Local.html>
2. <https://stackoverflow.com/questions/28523480/what-does-gcc-thread-do>
