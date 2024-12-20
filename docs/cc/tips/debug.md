# 重定向日志

在改动开源模块时，每个开源项目都有自己的日志系统，我们可能会花很长时间去分析它们的日志系统的流程是怎么样的。但是有一个更加简单地方法，就是我们覆盖掉原来的日志模块，重新定义符合自己习惯的日志系统。等待调试完成后，再把自己定义的日志去掉，恢复开源代码原来的样子。

以下是示例：<https://gitee.com/zhyantao/misc/raw/master/tests/debug.h>

```cpp
////////////////////////  ONLY FOR DEBUG USE  ////////////////////////
#ifndef DEBUG_H
#define DEBUG_H

// Case 1: 带额外参数的日志宏
#ifdef LOG_WITH_EXTRA_ARGS
#undef LOG_WITH_EXTRA_ARGS
#endif
#define LOG_WITH_EXTRA_ARGS(level, fmt, ...)                          \
    printf("LOG_WITH_EXTRA_ARGS:%d %s:%d " fmt "\n", level, __FILE__, \
           __LINE__, ##__VA_ARGS__)

// Case 2: 不带额外参数的日志宏
#ifdef LOG_WITHOUT_EXTRA_ARGS
#undef LOG_WITHOUT_EXTRA_ARGS
#endif
#define LOG_WITHOUT_EXTRA_ARGS(fmt, ...) \
    printf("LOG_WITHOUT_EXTRA_ARGS:%s:%d " fmt "\n", ##__VA_ARGS__)

#endif // DEBUG_H
```
