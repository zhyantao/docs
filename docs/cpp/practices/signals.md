# 如何使用信号

```cpp
#include <signal.h>
#include <stdbool.h>
#include <stdio.h>
#include <unistd.h>
#include <string.h>

static volatile bool quit = false;

static void sighandler_exit(int signum) {
    printf("\nCalling sighandler_exit(): %s\n", strsignal(signum));
    quit = true;
}

int main(int argc, char* argv[]) {
    struct sigaction sigact;
    sigact.sa_handler = sighandler_exit;
    sigemptyset(&sigact.sa_mask); // 清空信号掩码集合
    sigact.sa_flags = 0;          // 不设置任何特殊标志

    // 将 Ctrl + C 信号与 sighandler_exit 函数关联
    sigaction(SIGINT, &sigact, NULL);

    // 将 kill 信号与 sighandler_exit 函数关联
    sigaction(SIGTERM, &sigact, NULL);

    // 将 Ctrl + \ 信号与 sighandler_exit 函数关联
    sigaction(SIGQUIT, &sigact, NULL);

    while (!quit) {
        sleep(1);
    }

    return 0;
}
```
