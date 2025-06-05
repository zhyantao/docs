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

// 将日志级别转为字符串
static inline const char* log_level_to_str(LogLevel level) {
    switch (level) {
    case LOG_LEVEL_DEBUG: return "DEBUG";
    case LOG_LEVEL_INFO: return "INFO ";
    case LOG_LEVEL_WARN: return "WARN ";
    case LOG_LEVEL_ERROR: return "ERROR";
    case LOG_LEVEL_FATAL: return "FATAL";
    default: return "UNKWN";
    }
}

// 获取时间戳
static inline void get_timestamp(char* buffer, size_t size) {
    time_t t = time(NULL);
    struct tm tm;
    localtime_r(&t, &tm); // 线程安全版本
    strftime(buffer, size, "%Y-%m-%d %H:%M:%S", &tm);
}

// 带日志级别的日志宏（使用字符串表示级别）
#define LOG_WITH_LVL(level, fmt, ...)                                                         \
    do {                                                                                      \
        if (level >= LOG_LEVEL) {                                                             \
            char timestamp[64];                                                               \
            get_timestamp(timestamp, sizeof(timestamp));                                      \
            printf("[%s] %-5s %s:%d " fmt "\n", timestamp, log_level_to_str(level), __FILE__, \
                   __LINE__, ##__VA_ARGS__);                                                  \
        }                                                                                     \
    } while (0)

// 默认日志宏
#define LOG(fmt, ...) LOG_WITH_LVL(LOG_LEVEL_DEBUG, fmt, ##__VA_ARGS__)

// https://gitlab.com/gpsd/gpsd/-/blob/release-3.25/include/gpsd.h?ref_type=tags#L1128
// 重写 GPSD_LOG(lvl, eo, ...), 将日志打印到控制台
#ifdef GPSD_LOG
#undef GPSD_LOG
#define GPSD_LOG(lvl, eo, fmt, ...) LOG_WITH_LVL(lvl, fmt, ##__VA_ARGS__)
#endif

// https://github.com/nwtime/linuxptp/blob/master/print.h#L70
// 重写 pr_debug(x...)，将日志打印到控制台
#ifdef pr_debug
#undef pr_debug
// #define pr_debug(x...) LOG_WITH_LVL(LOG_LEVEL_DEBUG, x)                   /* GCC 扩展语法 (非标准) */
// #define pr_debug(...) LOG_WITH_LVL(LOG_LEVEL_DEBUG, __VA_ARGS__)          /* C99 语法 (标准) */
#define pr_debug(fmt, ...) LOG_WITH_LVL(LOG_LEVEL_DEBUG, fmt, ##__VA_ARGS__) /* 比 pr_debug(...) 更安全 */
#endif

#endif // DEBUG_H
```
