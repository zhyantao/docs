# syslog

在改动开源模块时，每个开源项目都有自己的日志系统，我们可能会花很长时间去分析它们的日志系统的流程是怎么样的。但是有一个更加简单地方法，就是我们覆盖掉原来的日志模块，重新定义符合自己习惯的日志系统。等待调试完成后，再把自己定义的日志去掉，恢复开源代码原来的样子。

示例请参考：<https://gitee.com/zhyantao/misc/blob/master/leetcode/cpp/include/debug.h>

```cpp
/////////////////////////////////////  ONLY FOR DEBUG USE  /////////////////////////////////////
#ifndef DEBUG_H
#define DEBUG_H

#include <stdio.h>
#include <time.h>
#include <string.h>

// 日志级别
typedef enum {
    LOG_LEVEL_DEBUG = 0,
    LOG_LEVEL_INFO,
    LOG_LEVEL_WARN,
    LOG_LEVEL_ERROR,
    LOG_LEVEL_FATAL
} LogLevel;

// 默认日志级别
#ifndef LOG_LEVEL
#define LOG_LEVEL LOG_LEVEL_DEBUG
#endif

// 获取时间戳
static inline void get_timestamp(char* buffer, size_t size) {
    time_t t = time(NULL);
    struct tm tm;
    localtime_r(&t, &tm); // 线程安全版本
    strftime(buffer, size, "%Y-%m-%d %H:%M:%S", &tm);
}

// 带日志级别的日志宏
#define LOG_WITH_LVL(level, fmt, ...)                                                        \
    do {                                                                                     \
        if (level >= LOG_LEVEL) {                                                            \
            char timestamp[64];                                                              \
            get_timestamp(timestamp, sizeof(timestamp));                                     \
            printf("[%s] LEVEL=%d %s:%d:%s " fmt "\n", timestamp, level, __FILE__, __LINE__, \
                   __func__, ##__VA_ARGS__);                                                 \
        }                                                                                    \
    } while (0)

// 默认日志宏
#define LOG(fmt, ...) LOG_WITH_LVL(LOG_LEVEL_DEBUG, fmt, ##__VA_ARGS__)

// 重写 GPSD_LOG(lvl, eo, ...), 将日志打印到控制台
#ifdef GPSD_LOG
#undef GPSD_LOG
#define GPSD_LOG(lvl, eo, fmt, ...) LOG_WITH_LVL(lvl, fmt, ##__VA_ARGS__)
#endif

#endif // DEBUG_H
```
