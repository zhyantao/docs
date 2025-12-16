# 多线程编程实践：覆盖 80% 的应用场景

## 1. 线程创建与销毁（2 个）

### `pthread_create()`

```c
int pthread_create(pthread_t *thread, const pthread_attr_t *attr,
                   void *(*start_routine)(void *), void *arg);
```

**功能**：创建新线程  
**特点**：

- 新线程立即开始执行 `start_routine`
- `arg` 传递给线程函数的参数
- 线程属性 `attr` 通常设为 NULL 使用默认值

**示例**：

```c
void* thread_func(void* arg) {
    int* num = (int*)arg;
    printf("Thread received: %d\n", *num);
    return NULL;
}

int main() {
    pthread_t tid;
    int value = 42;
    pthread_create(&tid, NULL, thread_func, &value);
    // ...
}
```

### `pthread_join()`

```c
int pthread_join(pthread_t thread, void **retval);
```

**功能**：等待线程结束并回收资源  
**特点**：

- 阻塞调用线程直到目标线程结束
- 可以获取线程的返回值
- 必须调用，否则可能产生僵尸线程

**注意事项**：

- 每个线程只能被 join 一次
- 不 join 会导致内存泄漏
- 分离线程不需要 join

**示例**：

```c
void* thread_func(void* arg) {
    int* result = malloc(sizeof(int));
    *result = 100;
    return result;
}

int main() {
    pthread_t tid;
    pthread_create(&tid, NULL, thread_func, NULL);

    void* retval;
    pthread_join(tid, &retval);
    printf("Thread returned: %d\n", *(int*)retval);
    free(retval);
}
```

## 2. 互斥锁操作（4 个）

### `pthread_mutex_init()`

```c
int pthread_mutex_init(pthread_mutex_t *mutex,
                       const pthread_mutexattr_t *attr);
```

**功能**：初始化互斥锁  
**特点**：

- 静态初始化可用 `PTHREAD_MUTEX_INITIALIZER`
- 属性 `attr` 通常设为 NULL

### `pthread_mutex_destroy()`

```c
int pthread_mutex_destroy(pthread_mutex_t *mutex);
```

**功能**：销毁互斥锁  
**注意事项**：

- 确保没有线程持有锁
- 不能销毁已初始化的锁再次使用

### `pthread_mutex_lock()` / `pthread_mutex_unlock()`

```c
int pthread_mutex_lock(pthread_mutex_t *mutex);
int pthread_mutex_unlock(pthread_mutex_t *mutex);
```

**功能**：加锁和解锁

**示例**：

```c
pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;
int shared_data = 0;

void* increment(void* arg) {
    for (int i = 0; i < 100000; i++) {
        pthread_mutex_lock(&mutex);
        shared_data++;
        pthread_mutex_unlock(&mutex);
    }
    return NULL;
}
```

**注意事项**：

1. **锁顺序**：避免死锁，按固定顺序加锁
2. **锁粒度**：锁的粒度要合适，太细增加开销，太粗降低并发
3. **RAII 模式**：C++ 中使用 `std::lock_guard`

## 3. 条件变量操作（5 个）

### `pthread_cond_init()` / `pthread_cond_destroy()`

```c
int pthread_cond_init(pthread_cond_t *cond,
                      const pthread_condattr_t *attr);
int pthread_cond_destroy(pthread_cond_t *cond);
```

**功能**：初始化/销毁条件变量  
**特点**：

- 静态初始化可用 `PTHREAD_COND_INITIALIZER`

### `pthread_cond_wait()`

```c
int pthread_cond_wait(pthread_cond_t *cond, pthread_mutex_t *mutex);
```

**功能**：等待条件变量  
**特点**：

- 原子地释放锁并进入等待
- 被唤醒时重新获得锁

### `pthread_cond_signal()` / `pthread_cond_broadcast()`

```c
int pthread_cond_signal(pthread_cond_t *cond);
int pthread_cond_broadcast(pthread_cond_t *cond);
```

**功能**：唤醒等待的线程  
**区别**：

- `signal` 唤醒至少一个线程
- `broadcast` 唤醒所有等待线程

**经典生产者-消费者示例**：

```c
pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;
pthread_cond_t cond = PTHREAD_COND_INITIALIZER;
queue_t queue;

// 生产者
void producer() {
    pthread_mutex_lock(&mutex);
    // 生产数据
    queue_push(&queue, data);
    pthread_cond_signal(&cond);  // 通知消费者
    pthread_mutex_unlock(&mutex);
}

// 消费者
void consumer() {
    pthread_mutex_lock(&mutex);
    while (queue_empty(&queue)) {  // 必须用 while，防止虚假唤醒
        pthread_cond_wait(&cond, &mutex);
    }
    data = queue_pop(&queue);
    pthread_mutex_unlock(&mutex);
}
```

## 关键注意事项总结

### 1. **虚假唤醒（Spurious Wakeup）**

条件变量等待**必须**使用 while 循环检查条件：

```c
// 错误：if 判断
if (condition_is_false) {
    pthread_cond_wait(&cond, &mutex);
}

// 正确：while 循环
while (condition_is_false) {
    pthread_cond_wait(&cond, &mutex);
}
```

### 2. **资源管理**

- 动态初始化的 mutex/cond 必须销毁
- 使用 RAII（Resource Acquisition Is Initialization）模式

### 3. **错误处理**

所有 pthread 函数都有返回值，生产代码应该检查：

```c
int ret = pthread_create(&tid, NULL, func, NULL);
if (ret != 0) {
    // 错误处理
}
```

### 4. **线程安全设计原则**

1. **共享数据最小化**：减少需要锁保护的数据
2. **锁的持有时间尽量短**
3. **避免在持有锁时调用未知函数**（可能造成死锁）
4. **使用更高级的同步原语**（如信号量、读写锁）时需谨慎

## 实际工程建议

在实际 C++ 项目中，更推荐使用 C++11 的 `<thread>`、`<mutex>`、`<condition_variable>`，它们提供了更好的类型安全和 RAII 支持。POSIX thread 函数是底层基础，理解它们有助于深入理解多线程编程的本质。

这 11 个函数确实是多线程编程的基石，掌握它们就能解决大部分线程同步问题。muduo 网络库正是基于这些基本原语构建了高效的多线程架构。

## 核心 POSIX 线程函数总结

| 类别               | 函数                       | 功能描述               | 关键注意事项                                     |
| ------------------ | -------------------------- | ---------------------- | ------------------------------------------------ |
| **线程创建与销毁** | `pthread_create()`         | 创建新线程并开始执行   | 传递参数给线程函数；线程属性通常为 NULL          |
|                    | `pthread_join()`           | 等待线程结束并回收资源 | 避免僵尸线程；获取返回值；每个线程只能 join 一次 |
| **互斥锁操作**     | `pthread_mutex_init()`     | 初始化互斥锁           | 可使用 `PTHREAD_MUTEX_INITIALIZER` 静态初始化    |
|                    | `pthread_mutex_destroy()`  | 销毁互斥锁             | 确保无线程持有锁；不可重复销毁                   |
|                    | `pthread_mutex_lock()`     | 对互斥锁加锁           | 注意锁顺序以避免死锁                             |
|                    | `pthread_mutex_unlock()`   | 对互斥锁解锁           | 确保与加锁配对使用                               |
| **条件变量操作**   | `pthread_cond_init()`      | 初始化条件变量         | 可使用 `PTHREAD_COND_INITIALIZER` 静态初始化     |
|                    | `pthread_cond_destroy()`   | 销毁条件变量           | 确保无线程等待                                   |
|                    | `pthread_cond_wait()`      | 等待条件变量           | 必须与互斥锁配合使用；总是用 while 循环检查条件  |
|                    | `pthread_cond_signal()`    | 唤醒至少一个等待线程   | 通常在持有互斥锁时调用                           |
|                    | `pthread_cond_broadcast()` | 唤醒所有等待线程       | 唤醒多个等待者时使用                             |

## 示例

```cpp
#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <errno.h>

// 定义线程参数结构体
typedef struct {
    int fd;                // 文件描述符
    char* buffer;          // 缓冲区指针
    int size;              // 缓冲区大小
    volatile int running;  // 运行状态标志（volatile 确保可见性）
    pthread_mutex_t mutex; // 互斥锁保护共享数据
    pthread_cond_t cond;   // 条件变量用于线程同步
} thread_args_t;

// 线程函数：使用 while 循环检查条件，避免虚假唤醒
void* uart_thread_func(void* arg) {
    thread_args_t* args = (thread_args_t*)arg;

    printf("UART thread started (fd: %d)\n", args->fd);

    while (1) {
        pthread_mutex_lock(&args->mutex);

        // 检查停止条件（使用 while 循环防止虚假唤醒）
        while (args->running == 0) {
            printf("Thread exiting...\n");
            pthread_mutex_unlock(&args->mutex);
            pthread_exit(NULL);
        }
        pthread_mutex_unlock(&args->mutex);

        // 读取数据
        int ret = read(args->fd, args->buffer, args->size - 1);

        if (ret > 0) {
            // 成功读取数据
            args->buffer[ret] = '\0'; // 确保字符串结束

            pthread_mutex_lock(&args->mutex);
            printf("UART received (%d bytes): %s\n", ret, args->buffer);
            pthread_mutex_unlock(&args->mutex);

            // 通知主线程数据已就绪（如果有需要）
            pthread_cond_signal(&args->cond);
        } else if (ret == 0) {
            // EOF，设备可能断开
            printf("UART device closed or EOF reached\n");
            usleep(100000); // 100ms 延时
        } else {
            if (errno == EAGAIN || errno == EWOULDBLOCK) {
                // 非阻塞读取，没有数据可用
                usleep(50000); // 50ms 延时，避免忙等待
            } else {
                // 读取错误
                perror("UART read error");
                usleep(100000); // 100ms 延时后重试
            }
        }
    }

    return NULL;
}

// 初始化 UART 接收线程（使用 RAII 思想进行资源管理）
int uart_recv_thread_init(int fd, char* buffer, int size, thread_args_t** args_ptr) {
    if (fd < 0 || buffer == NULL || size <= 0) {
        fprintf(stderr, "Invalid parameters\n");
        return -1;
    }

    // 分配参数内存
    thread_args_t* args = (thread_args_t*)calloc(1, sizeof(thread_args_t));
    if (!args) {
        perror("malloc failed");
        return -1;
    }

    // 初始化参数
    args->fd = fd;
    args->buffer = buffer;
    args->size = size;
    args->running = 1;

    // 初始化互斥锁和条件变量
    int ret = pthread_mutex_init(&args->mutex, NULL);
    if (ret != 0) {
        fprintf(stderr, "pthread_mutex_init failed: %s\n", strerror(ret));
        free(args);
        return -1;
    }

    ret = pthread_cond_init(&args->cond, NULL);
    if (ret != 0) {
        fprintf(stderr, "pthread_cond_init failed: %s\n", strerror(ret));
        pthread_mutex_destroy(&args->mutex);
        free(args);
        return -1;
    }

    // 创建线程
    pthread_t thread;
    ret = pthread_create(&thread, NULL, uart_thread_func, (void*)args);
    if (ret != 0) {
        fprintf(stderr, "pthread_create failed: %s\n", strerror(ret));
        pthread_cond_destroy(&args->cond);
        pthread_mutex_destroy(&args->mutex);
        free(args);
        return -1;
    }

    // 设置线程为分离状态（自动回收资源）
    ret = pthread_detach(thread);
    if (ret != 0) {
        fprintf(stderr, "pthread_detach failed: %s\n", strerror(ret));
        // 继续执行，因为线程已创建成功
    }

    // 返回参数指针供外部使用
    if (args_ptr) { *args_ptr = args; }

    printf("UART receive thread created successfully\n");
    return 0;
}

// 线程清理函数（安全的资源释放）
void uart_recv_thread_cleanup(thread_args_t* args) {
    if (!args) { return; }

    printf("Cleaning up UART thread...\n");

    // 首先停止线程运行
    pthread_mutex_lock(&args->mutex);
    args->running = 0;
    pthread_mutex_unlock(&args->mutex);

    // 发送条件信号，唤醒可能正在等待的线程
    pthread_cond_signal(&args->cond);

    // 等待一小段时间让线程退出（实际应用中可能需要更精确的同步）
    usleep(100000); // 100ms

    // 销毁同步原语
    pthread_cond_destroy(&args->cond);
    pthread_mutex_destroy(&args->mutex);

    // 释放内存
    free(args);

    printf("UART thread cleanup completed\n");
}

// 等待数据就绪的辅助函数
int wait_for_data(thread_args_t* args, int timeout_ms) {
    if (!args) { return -1; }

    struct timespec ts;
    clock_gettime(CLOCK_REALTIME, &ts);
    ts.tv_sec += timeout_ms / 1000;
    ts.tv_nsec += (timeout_ms % 1000) * 1000000;

    pthread_mutex_lock(&args->mutex);
    int ret = pthread_cond_timedwait(&args->cond, &args->mutex, &ts);
    pthread_mutex_unlock(&args->mutex);

    return ret;
}

// 主函数示例
int main() {
    // 打开串口设备（示例）
    int fd = open("/dev/ttyUSB0", O_RDWR | O_NOCTTY | O_NONBLOCK);
    if (fd < 0) {
        // 尝试备用设备
        fd = open("/dev/ttyS0", O_RDWR | O_NOCTTY | O_NONBLOCK);
        if (fd < 0) {
            perror("Failed to open UART device");
            return -1;
        }
    }

    // 配置串口参数（实际应用中需要根据硬件配置）
    // struct termios options;
    // tcgetattr(fd, &options);
    // cfsetispeed(&options, B9600);
    // cfsetospeed(&options, B9600);
    // options.c_cflag &= ~PARENB;   // 无奇偶校验
    // options.c_cflag &= ~CSTOPB;   // 1位停止位
    // options.c_cflag &= ~CSIZE;
    // options.c_cflag |= CS8;       // 8位数据位
    // tcsetattr(fd, TCSANOW, &options);

    char buffer[1024] = {0};
    thread_args_t* thread_args = NULL;

    // 初始化接收线程
    if (uart_recv_thread_init(fd, buffer, sizeof(buffer), &thread_args) != 0) {
        close(fd);
        return -1;
    }

    printf("Main thread running. Press Enter to exit...\n");

    // 主线程工作循环
    for (int i = 0; i < 10; i++) {
        printf("Main thread working... (%d/10)\n", i + 1);
        sleep(1);

        // 可以在这里等待数据或进行其他处理
        // if (wait_for_data(thread_args, 500) == 0) {
        //     printf("Data received in main thread\n");
        // }
    }

    printf("Press Enter to clean up and exit...\n");
    getchar();

    // 清理资源
    uart_recv_thread_cleanup(thread_args);
    close(fd);

    printf("Program exited successfully\n");
    return 0;
}
```
