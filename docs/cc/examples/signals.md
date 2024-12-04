# 如何使用信号

```cpp
#include <signal.h>
#include <stdbool.h>

static volatile bool quit = false;

static void sighandler_exit(int signum) {
    printf("Calling sighandler_exit()\n");
    quit = true;
}

int main(int argc, char* argv[]) {
    struct sigaction sigact;
    sigact.sa_handler = sighandler_exit;
    sigemptyset(&sigact.sa_mask); // 清空信号掩码集合
    sigact.sa_flags = 0;          // 不设置任何特殊标志

    // 捕获 Ctrl + C 信号，触发 sighandler_exit 调用
    sigaction(SIGINT, &sigact, NULL);

    // 捕获 kill 信号，触发 sighandler_exit 调用
    sigaction(SIGTERM, &sigact, NULL);

    // 捕获 Ctrl + \ 信号，触发 sighandler_exit 调用
    sigaction(SIGQUIT, &sigact, NULL);

    while (!quit) {
        sleep(1);
    }

    return 0;
}
```
