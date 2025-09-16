# 多线程示例

```cpp
#include <pthread.h>
#include <stdio.h>
#include <fcntl.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>

// 定义参数结构体
typedef struct {
    int fd;
    char* buffer;
    int size;
    volatile int running; // 添加运行状态标志
} thread_args_t;

// 线程函数
void* thread_func(void* arg) {
    thread_args_t* args = (thread_args_t*)arg;

    while (args->running) {
        // 读取数据
        int ret = read(args->fd, args->buffer, args->size);
        if (ret == 0) {
            // 读取结束
            usleep(10000); // 避免忙等待
            continue;
        } else if (ret < 0) {
            // 读取错误，短暂延时后重试
            perror("read error");
            usleep(100000); // 100ms延时
            continue;
        } else {
            // 成功读取数据，可以在这里处理数据
            // 例如: printf("Received: %.*s\n", ret, args->buffer);
        }
    }

    return NULL;
}

int uart_recv_thread_init(int fd, char* buffer, int size) {
    pthread_t thread;

    // 动态分配参数内存，避免栈变量生命周期问题
    thread_args_t* args = (thread_args_t*)malloc(sizeof(thread_args_t));
    if (!args) {
        perror("malloc failed");
        return -1;
    }

    // 初始化参数
    args->fd = fd;
    args->buffer = buffer;
    args->size = size;
    args->running = 1; // 设置运行标志

    if (pthread_create(&thread, NULL, thread_func, (void*)args) != 0) {
        perror("pthread_create");
        free(args);
        return -1;
    }

    pthread_detach(thread);

    return 0;
}

// 添加清理函数
void uart_recv_thread_cleanup(thread_args_t* args) {
    if (args) {
        args->running = 0; // 停止线程循环
        // 注意：这里不能立即free，因为线程可能还在使用
        // 实际应用中需要更复杂的同步机制
    }
}

int main() {
    int fd = open("/dev/ttyUSB0", O_RDWR | O_NOCTTY);
    if (fd < 0) {
        perror("open failed");
        return -1;
    }

    char buffer[256] = {0};
    int size = sizeof(buffer);

    // 配置串口参数（实际应用中需要添加）
    // struct termios options;
    // tcgetattr(fd, &options);
    // cfsetispeed(&options, B9600);
    // cfsetospeed(&options, B9600);
    // tcsetattr(fd, TCSANOW, &options);

    if (uart_recv_thread_init(fd, buffer, size) != 0) {
        close(fd);
        return -1;
    }

    // 主线程可以做其他工作
    printf("UART receive thread started. Press Enter to exit...\n");
    getchar();

    // 清理工作
    close(fd);

    return 0;
}
```
