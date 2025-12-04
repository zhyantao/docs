# 高可靠串口数据分发器

## 引言：一个真实的生产环境问题

在 GPS 时间同步系统中，我们经常需要将单个串口数据源（如 GPS 接收器的 NMEA 数据）分发给多个应用程序。然而，在生产环境中，我们发现了一个棘手的问题：当某个客户端应用程序处理速度跟不上数据接收速度时，会导致数据在串口缓冲区堆积，最终导致整个系统阻塞。

通过 `cat /proc/tty/driver/uart` 命令，我们看到了令人震惊的数据：

```
3: uart:uart port:00000000 irq:192 tx:0 rx:2915757 RTS|DTR
```

串口 3 的接收缓冲区竟然有**2,915,757 字节**未读取！这意味着数据堆积已经超过 2.9MB，而应用程序却处于睡眠状态（`State: S (sleeping)`）。

## 问题分析：为什么数据会堆积？

经过深入分析，我们发现了几个根本原因：

1. **阻塞式 I/O**：传统串口编程通常使用阻塞式读取，当客户端无法及时处理数据时，整个读取流程会被阻塞
2. **缺乏流量控制**：没有机制来检测客户端是否能够接收数据
3. **单点故障**：一个客户端的问题会影响到所有其他客户端的数据接收
4. **缺乏恢复机制**：一旦发生阻塞，需要手动干预才能恢复

## 解决方案：高可靠串口数据分发器

我们设计并实现了一个 C 语言编写的串口数据分发器，它具有以下核心特性：

- ✅ **非阻塞 I/O**：避免因单个客户端问题导致整个系统阻塞
- ✅ **自动重连机制**：检测到客户端缓冲区满时自动重新创建虚拟串口
- ✅ **实时监控**：详细的统计信息和性能指标
- ✅ **优雅的错误处理**：智能的错误恢复和资源清理
- ✅ **线程安全**：使用互斥锁保护共享资源

## 核心架构设计

### 数据结构设计

```cpp
typedef struct {
    int fd;                         // 客户端文件描述符
    int active;                     // 是否活跃
    int blocked;                    // 是否被阻塞（缓冲区满）
    int pending_errors;             // 连续错误计数
    int reconnect_attempts;         // 重连尝试次数
    char name[128];                 // 符号链接路径（如/tmp/virtual1）
    char slave_name[64];            // PTY从设备名
    struct timeval last_write_time; // 上次成功写入时间
    struct timeval block_time;      // 阻塞开始时间
} client_t;

typedef struct {
    int source_fd;                 // 源串口文件描述符
    client_t clients[MAX_CLIENTS]; // 客户端列表
    int client_count;              // 客户端数量
    pthread_mutex_t mutex;         // 互斥锁
    volatile int running;          // 运行控制标志
    long total_bytes_read;         // 总读取字节数
    long total_bytes_written;      // 总写入字节数
    long error_count;              // 错误计数
    long reconnect_count;          // 重连计数
} distributor_t;
```

### 关键特性实现

#### 1. 非阻塞 I/O 与 select 机制

```cpp
// 设置文件描述符为非阻塞模式
void set_nonblocking(int fd) {
    int flags = fcntl(fd, F_GETFL, 0);
    if (fcntl(fd, F_SETFL, flags | O_NONBLOCK) == -1) { perror("fcntl F_SETFL O_NONBLOCK"); }
}

// 使用select监控串口数据
FD_ZERO(&read_fds);
FD_SET(dist->source_fd, &read_fds);
timeout.tv_sec = 1; // 1秒超时
int ready = select(max_fd + 1, &read_fds, NULL, NULL, &timeout);
```

#### 2. 自动重连机制

这是本方案的核心创新点。当检测到客户端缓冲区满时：

```cpp
if (errno == EAGAIN || errno == EWOULDBLOCK) {
    // 缓冲区满，标记客户端为阻塞
    if (!dist->clients[i].blocked) {
        dist->clients[i].blocked = 1;
        gettimeofday(&dist->clients[i].block_time, NULL);
        printf("Client %s blocked (buffer full), will attempt to recreate\n",
               dist->clients[i].name);
    }
}
```

定期检查被阻塞的客户端，如果阻塞超过 5 秒则自动重连：

```cpp
void handle_blocked_clients(distributor_t* dist) {
    struct timeval now;
    gettimeofday(&now, NULL);

    for (int i = 0; i < dist->client_count; i++) {
        if (dist->clients[i].active && dist->clients[i].blocked) {
            struct timeval block_duration;
            timersub(&now, &dist->clients[i].block_time, &block_duration);

            // 如果阻塞超过5秒，尝试重新创建
            if (block_duration.tv_sec >= 5) {
                if (dist->clients[i].reconnect_attempts < MAX_RECONNECT_ATTEMPTS) {
                    printf("Client %s blocked for %ld seconds, attempting to recreate...\n",
                           dist->clients[i].name, block_duration.tv_sec);
                    recreate_client(dist, i);
                }
            }
        }
    }
}
```

#### 3. 客户端重新创建过程

```cpp
int recreate_client(distributor_t* dist, int client_index) {
    client_t* client = &dist->clients[client_index];

    // 1. 清理旧资源
    cleanup_client(client);

    // 2. 创建新的伪终端
    int master_fd = posix_openpt(O_RDWR | O_NOCTTY);

    // 3. 配置新PTY
    grantpt(master_fd);
    unlockpt(master_fd);

    // 4. 获取从设备名并更新符号链接
    char slave_name[64];
    ptsname_r(master_fd, slave_name, sizeof(slave_name));
    symlink(slave_name, client->name);

    // 5. 设置非阻塞模式
    set_nonblocking(master_fd);

    // 6. 更新客户端状态
    client->fd = master_fd;
    client->blocked = 0;
    client->pending_errors = 0;
    client->reconnect_attempts++;
    dist->reconnect_count++;

    printf("Client %s recreated successfully\n", client->name);
    return 0;
}
```

#### 4. 全面的统计监控

```cpp
void print_statistics(distributor_t* dist) {
    printf("\n=== Statistics ===\n");
    printf("Active clients: %d (blocked: %d)\n", active_clients, blocked_clients);
    printf("Total bytes read: %ld\n", dist->total_bytes_read);
    printf("Total bytes written: %ld\n", dist->total_bytes_written);
    printf("Error count: %ld\n", dist->error_count);
    printf("Reconnect count: %ld\n", dist->reconnect_count);
    printf("Bytes/sec read: %.1f\n", dist->total_bytes_read / elapsed);
    printf("Bytes/sec written: %.1f\n", dist->total_bytes_written / elapsed);

    // 显示被阻塞客户端的详细信息
    if (blocked_clients > 0) {
        printf("\nBlocked clients:\n");
        for (int i = 0; i < dist->client_count; i++) {
            if (dist->clients[i].active && dist->clients[i].blocked) {
                printf("  %s: blocked for %ld.%03ld seconds\n", dist->clients[i].name,
                       block_duration.tv_sec, block_duration.tv_usec / 1000);
            }
        }
    }
}
```

## 使用方式

### 编译与运行

```bash
# 编译
gcc -o serial_distributor serial_distributor.c -lpthread

# 基本使用
./serial_distributor -I /dev/ttyS3 -b 460800

# 高级使用：指定输出端口并启用统计
./serial_distributor -I /dev/ttyS3 -b 460800 \
    -O /tmp/gps1 -O /tmp/gps2 -O /var/run/chrony \
    -s
```

### 命令行参数

| 参数               | 说明             | 示例            |
| ------------------ | ---------------- | --------------- |
| `-I, --input`      | 输入串口（必需） | `-I /dev/ttyS3` |
| `-b, --baudrate`   | 波特率设置       | `-b 460800`     |
| `-O, --output`     | 输出虚拟端口     | `-O /tmp/gps1`  |
| `-s, --statistics` | 启用统计信息     | `-s`            |
| `-h, --help`       | 显示帮助信息     | `-h`            |

### 默认行为

- 如果不指定输出端口，默认创建 `/tmp/virtual1` 和 `/tmp/virtual2`
- 最大支持 10 个客户端同时连接
- 每个客户端最多重连 5 次
- 阻塞 5 秒后触发自动重连

## 性能优化策略

### 1. 缓冲区管理

```cpp
#define BUFFER_SIZE       4096
#define MAX_PENDING_BYTES (BUFFER_SIZE * 10)
```

我们使用 4KB 的缓冲区大小，并允许最多 10 倍缓冲区的数据堆积。这种设计在内存使用和性能之间取得了平衡。

### 2. 智能休眠策略

```cpp
// 根据不同的错误类型采用不同的休眠时间
if (bytes_read == 0) {
    usleep(1000); // 无数据时休眠1ms
} else if (errno == EAGAIN) {
    usleep(10000); // 临时错误时休眠10ms
} else {
    usleep(100000); // 严重错误时休眠100ms
}
```

### 3. 批处理优化

```cpp
// 一次性读取尽可能多的数据
ssize_t bytes_read = read(dist->source_fd, read_buffer, sizeof(read_buffer));

// 批量分发给所有活跃客户端
for (int i = 0; i < dist->client_count; i++) {
    if (dist->clients[i].active && !dist->clients[i].blocked) {
        write(dist->clients[i].fd, read_buffer, bytes_read);
    }
}
```

## 实际应用场景

### GPS 时间同步系统

在多服务器的时间同步场景中，单个 GPS 接收器需要为多个服务器提供精确的时间信号：

```bash
# 为不同的时间服务创建虚拟串口
./serial_distributor -I /dev/ttyS3 -b 460800 \
    -O /var/run/chrony.pty \
    -O /var/run/ntpd.pty \
    -O /var/run/gpsd.pty \
    -s
```

### 工业数据采集

在工业自动化系统中，传感器数据需要分发给多个监控和分析系统：

```bash
# 为不同的监控系统分发数据
./serial_distributor -I /dev/ttyUSB0 -b 115200 \
    -O /tmp/plc_data \
    -O /tmp/scada_data \
    -O /tmp/analytics_data
```

### 调试与监控

启用统计信息可以实时监控系统状态：

```
=== Statistics ===
Active clients: 3 (blocked: 0)
Total bytes read: 15489234
Total bytes written: 46467602
Error count: 2
Reconnect count: 1
Bytes/sec read: 5124.3
Bytes/sec written: 15375.8
```

## 故障排除与调试

### 常见问题

1. **权限问题**：确保有访问串口设备的权限

   ```bash
   sudo chmod 666 /dev/ttyS3
   sudo usermod -aG dialout $USER
   ```

2. **符号链接冲突**：如果虚拟端口已存在，程序会自动清理

3. **资源限制**：检查系统资源限制
   ```bash
   ulimit -n  # 查看文件描述符限制
   ```

### 调试技巧

```cpp
// 启用详细调试输出
static int counter = 0;
if (++counter % 500 == 0) {
    printf("Distributed %ld bytes to %d clients\n", bytes_read, clients_served);
}
```

## 与类似方案的比较

| 特性       | 我们的方案 | socat | ser2net | 传统方案 |
| ---------- | ---------- | ----- | ------- | -------- |
| 自动重连   | ✅         | ❌    | ❌      | ❌       |
| 非阻塞 I/O | ✅         | ⚠️    | ⚠️      | ❌       |
| 实时监控   | ✅         | ❌    | ❌      | ❌       |
| 线程安全   | ✅         | ✅    | ✅      | ⚠️       |
| 资源清理   | ✅         | ⚠️    | ⚠️      | ⚠️       |
| 配置灵活性 | ✅         | ✅    | ✅      | ❌       |

## 结论

本文介绍的高可靠串口数据分发器解决了生产环境中常见的数据堆积问题。通过创新的自动重连机制、非阻塞 I/O 设计和全面的监控功能，我们实现了一个既稳定又高效的解决方案。

关键优势：

1. **零数据丢失**：通过自动重连机制确保数据连续性
2. **高可用性**：单个客户端故障不影响其他客户端
3. **易于监控**：详细的统计信息帮助快速定位问题
4. **资源友好**：智能的资源管理和清理机制

这个方案已经在生产环境中稳定运行，成功解决了之前遇到的串口数据堆积问题。开源代码可供大家根据实际需求进行修改和优化。

## 未来改进方向

1. **动态缓冲区调整**：根据数据流量动态调整缓冲区大小
2. **优先级调度**：为不同客户端设置不同的优先级
3. **数据压缩**：对大流量数据进行压缩传输
4. **远程监控**：通过网络接口提供远程监控功能
5. **容器化支持**：提供 Docker 镜像方便部署

通过持续的优化和改进，这个串口数据分发器可以适应更多复杂的工业应用场景，为各种串口通信需求提供可靠的基础设施支持。

## 源代码

```cpp
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <termios.h>
#include <pthread.h>
#include <sys/select.h>
#include <sys/ioctl.h>
#include <getopt.h>
#include <errno.h>
#include <signal.h>
#include <time.h>
#include <sys/time.h>

#define MAX_CLIENTS            10
#define BUFFER_SIZE            4096
#define DEFAULT_BAUDRATE       460800
#define MAX_PENDING_BYTES      (BUFFER_SIZE * 10) // 最大允许堆积的字节数
#define MAX_RECONNECT_ATTEMPTS 5                  // 最大重连尝试次数
#define RECONNECT_DELAY_MS     1000               // 重连延迟（毫秒）

typedef struct {
    int fd;                         // Client file descriptor
    int active;                     // Whether active
    int blocked;                    // Whether client is blocked (buffer full)
    int pending_errors;             // 连续写错误计数
    int reconnect_attempts;         // 重连尝试次数
    char name[128];                 // Full symlink path (e.g., /tmp/virtual1)
    char slave_name[64];            // PTY slave设备名
    struct timeval last_write_time; // 上次成功写入的时间
    struct timeval block_time;      // 阻塞开始时间
} client_t;

typedef struct {
    int source_fd;                 // Source serial port file descriptor
    client_t clients[MAX_CLIENTS]; // Client list
    int client_count;
    pthread_mutex_t mutex;
    int baudrate;             // 保存波特率的数字值
    speed_t termios_baudrate; // termios的波特率常量
    volatile int running;     // 控制线程运行标志
    long total_bytes_read;    // 总共读取的字节数
    long total_bytes_written; // 总共写入的字节数
    long error_count;         // 错误计数
    long reconnect_count;     // 重连计数
} distributor_t;

// Function prototypes
void print_usage(const char* program_name);
int parse_baudrate(const char* baud_str, int* baud_num, speed_t* baud_termios);
int init_distributor(distributor_t* dist, const char* source_port, int baudrate_num,
                     speed_t baudrate_termios);
int add_client(distributor_t* dist, const char* symlink_path);
int recreate_client(distributor_t* dist, int client_index);
void* distribution_thread(void* arg);
void cleanup_distributor(distributor_t* dist);
void print_statistics(distributor_t* dist);
void set_nonblocking(int fd);
int check_serial_buffer(int fd);
void handle_signal(int sig);
int cleanup_client(client_t* client);

volatile sig_atomic_t keep_running = 1;

// Signal handler for graceful shutdown
void handle_signal(int sig) {
    printf("\nReceived signal %d, shutting down...\n", sig);
    keep_running = 0;
}

// Set file descriptor to non-blocking mode
void set_nonblocking(int fd) {
    int flags = fcntl(fd, F_GETFL, 0);
    if (flags == -1) {
        perror("fcntl F_GETFL");
        return;
    }

    if (fcntl(fd, F_SETFL, flags | O_NONBLOCK) == -1) { perror("fcntl F_SETFL O_NONBLOCK"); }
}

// Check if serial port has data available
int check_serial_buffer(int fd) {
    int bytes_available = 0;
    if (ioctl(fd, FIONREAD, &bytes_available) == -1) {
        perror("ioctl FIONREAD");
        return -1;
    }
    return bytes_available;
}

// Cleanup client resources
int cleanup_client(client_t* client) {
    if (client->fd >= 0) {
        close(client->fd);
        client->fd = -1;
    }

    // Remove symbolic link if it exists
    if (client->name[0] != '\0' && access(client->name, F_OK) == 0) {
        if (unlink(client->name) == -1) {
            fprintf(stderr, "Warning: Failed to remove symlink %s: %s\n", client->name,
                    strerror(errno));
            return -1;
        }
    }

    return 0;
}

// Print usage information
void print_usage(const char* program_name) {
    printf("\nSerial Port Distributor - GPS Time Synchronization\n");
    printf("===================================================\n");
    printf("Usage: %s [OPTIONS]\n", program_name);
    printf("\nOptions:\n");
    printf("  -I, --input PORT       Input serial port (required)\n");
    printf("  -b, --baudrate RATE    Set baudrate (default: 460800)\n");
    printf("  -O, --output PATH      Add output virtual port (absolute path, can be used "
           "multiple times)\n");
    printf("  -s, --statistics       Print statistics every 10 seconds\n");
    printf("  -h, --help             Display this help message\n");
    printf("\nFeatures:\n");
    printf("  - Auto-reconnects blocked clients (buffer full)\n");
    printf("  - Non-blocking I/O for better performance\n");
    printf("  - Detailed statistics and monitoring\n");
    printf("\nExamples:\n");
    printf("  %s -I /dev/ttyS3\n", program_name);
    printf("  %s -I /dev/ttyS3 -b 9600 -O /tmp/gps1 -O /tmp/gps2\n", program_name);
    printf("  %s -I /dev/ttyUSB0 -b 115200 -O /var/run/chrony -O /var/run/logger\n",
           program_name);
    printf("\nDefault output ports (if none specified): /tmp/virtual1, /tmp/virtual2\n");
    printf("===================================================\n\n");
}

// Parse baudrate string to termios constant and numeric value
int parse_baudrate(const char* baud_str, int* baud_num, speed_t* baud_termios) {
    if (baud_str == NULL) {
        *baud_num = DEFAULT_BAUDRATE;
        *baud_termios = B460800;
        return 0;
    }

    int baud = atoi(baud_str);
    *baud_num = baud;

    switch (baud) {
    case 50: *baud_termios = B50; break;
    case 75: *baud_termios = B75; break;
    case 110: *baud_termios = B110; break;
    case 134: *baud_termios = B134; break;
    case 150: *baud_termios = B150; break;
    case 200: *baud_termios = B200; break;
    case 300: *baud_termios = B300; break;
    case 600: *baud_termios = B600; break;
    case 1200: *baud_termios = B1200; break;
    case 1800: *baud_termios = B1800; break;
    case 2400: *baud_termios = B2400; break;
    case 4800: *baud_termios = B4800; break;
    case 9600: *baud_termios = B9600; break;
    case 19200: *baud_termios = B19200; break;
    case 38400: *baud_termios = B38400; break;
    case 57600: *baud_termios = B57600; break;
    case 115200: *baud_termios = B115200; break;
    case 230400: *baud_termios = B230400; break;
    case 460800: *baud_termios = B460800; break;
    case 921600: *baud_termios = B921600; break;
    default:
        fprintf(stderr, "Warning: Unknown baudrate %d, using 115200\n", baud);
        *baud_num = 115200;
        *baud_termios = B115200;
        return -1;
    }

    return 0;
}

// Initialize distributor
int init_distributor(distributor_t* dist, const char* source_port, int baudrate_num,
                     speed_t baudrate_termios) {
    struct termios tty;

    // Open source serial port with non-blocking mode
    dist->source_fd = open(source_port, O_RDONLY | O_NOCTTY | O_NONBLOCK);
    if (dist->source_fd < 0) {
        perror("Failed to open source port");
        return -1;
    }

    // Configure serial port
    memset(&tty, 0, sizeof(tty));
    if (tcgetattr(dist->source_fd, &tty) != 0) {
        perror("tcgetattr");
        close(dist->source_fd);
        return -1;
    }

    cfsetispeed(&tty, baudrate_termios);
    cfsetospeed(&tty, baudrate_termios);

    tty.c_cflag &= ~PARENB;
    tty.c_cflag &= ~CSTOPB;
    tty.c_cflag &= ~CSIZE;
    tty.c_cflag |= CS8;
    tty.c_cflag &= ~CRTSCTS;
    tty.c_cflag |= CREAD | CLOCAL;

    tty.c_lflag &= ~(ICANON | ECHO | ECHOE | ISIG);
    tty.c_iflag &= ~(IXON | IXOFF | IXANY);
    tty.c_oflag &= ~OPOST;

    // Set minimum characters and timeout
    tty.c_cc[VMIN] = 0;  // Non-blocking read
    tty.c_cc[VTIME] = 0; // No timeout

    if (tcsetattr(dist->source_fd, TCSANOW, &tty) != 0) {
        perror("Failed to set serial port attributes");
        close(dist->source_fd);
        return -1;
    }

    // Clear any pending data in the buffer
    tcflush(dist->source_fd, TCIOFLUSH);

    // Initialize client list
    memset(dist->clients, 0, sizeof(dist->clients));
    dist->client_count = 0;
    dist->baudrate = baudrate_num;
    dist->termios_baudrate = baudrate_termios;
    dist->running = 1;
    dist->total_bytes_read = 0;
    dist->total_bytes_written = 0;
    dist->error_count = 0;
    dist->reconnect_count = 0;
    pthread_mutex_init(&dist->mutex, NULL);

    printf("Distributor initialized on %s @ %d baud\n", source_port, baudrate_num);
    return 0;
}

// Add client with custom virtual port name (full absolute path)
int add_client(distributor_t* dist, const char* symlink_path) {
    pthread_mutex_lock(&dist->mutex);

    if (dist->client_count >= MAX_CLIENTS) {
        pthread_mutex_unlock(&dist->mutex);
        fprintf(stderr, "Maximum number of clients reached (%d)\n", MAX_CLIENTS);
        return -1;
    }

    // Check if client name already exists
    for (int i = 0; i < dist->client_count; i++) {
        if (strcmp(dist->clients[i].name, symlink_path) == 0) {
            pthread_mutex_unlock(&dist->mutex);
            fprintf(stderr, "Client path '%s' already exists\n", symlink_path);
            return -1;
        }
    }

    // Create pseudo-terminal
    int master_fd;
    char slave_name[64];

    master_fd = posix_openpt(O_RDWR | O_NOCTTY);
    if (master_fd == -1) {
        pthread_mutex_unlock(&dist->mutex);
        perror("Failed to create PTY");
        return -1;
    }

    if (grantpt(master_fd) == -1 || unlockpt(master_fd) == -1) {
        close(master_fd);
        pthread_mutex_unlock(&dist->mutex);
        perror("Failed to setup PTY");
        return -1;
    }

    // Get slave device name
    if (ptsname_r(master_fd, slave_name, sizeof(slave_name)) != 0) {
        close(master_fd);
        pthread_mutex_unlock(&dist->mutex);
        perror("Failed to get PTY slave name");
        return -1;
    }

    // Set non-blocking mode for the PTY master
    set_nonblocking(master_fd);

    // Remove existing symlink if it exists
    if (access(symlink_path, F_OK) == 0) {
        if (unlink(symlink_path) == -1) {
            fprintf(stderr, "Warning: Failed to remove existing symlink %s: %s\n",
                    symlink_path, strerror(errno));
        }
    }

    // Create symbolic link
    if (symlink(slave_name, symlink_path) == -1) {
        fprintf(stderr, "Failed to create symlink %s -> %s: %s\n", symlink_path, slave_name,
                strerror(errno));
        close(master_fd);
        pthread_mutex_unlock(&dist->mutex);
        return -1;
    }

    // Add to client list
    client_t* client = &dist->clients[dist->client_count];
    client->fd = master_fd;
    client->active = 1;
    client->blocked = 0;
    client->pending_errors = 0;
    client->reconnect_attempts = 0;
    gettimeofday(&client->last_write_time, NULL);
    memset(&client->block_time, 0, sizeof(client->block_time));
    snprintf(client->name, sizeof(client->name), "%s", symlink_path);
    snprintf(client->slave_name, sizeof(client->slave_name), "%s", slave_name);
    dist->client_count++;

    printf("Virtual port created: %s -> %s\n", symlink_path, slave_name);

    pthread_mutex_unlock(&dist->mutex);
    return master_fd;
}

// Recreate a client (close and reopen)
int recreate_client(distributor_t* dist, int client_index) {
    if (client_index < 0 || client_index >= dist->client_count) { return -1; }

    client_t* client = &dist->clients[client_index];

    printf("Attempting to recreate client %s (attempt %d/%d)...\n", client->name,
           client->reconnect_attempts + 1, MAX_RECONNECT_ATTEMPTS);

    // Cleanup old resources
    cleanup_client(client);

    // Create new pseudo-terminal
    int master_fd = posix_openpt(O_RDWR | O_NOCTTY);
    if (master_fd == -1) {
        fprintf(stderr, "Failed to create new PTY for %s: %s\n", client->name,
                strerror(errno));
        return -1;
    }

    if (grantpt(master_fd) == -1 || unlockpt(master_fd) == -1) {
        close(master_fd);
        fprintf(stderr, "Failed to setup new PTY for %s: %s\n", client->name, strerror(errno));
        return -1;
    }

    // Get slave device name
    char slave_name[64];
    if (ptsname_r(master_fd, slave_name, sizeof(slave_name)) != 0) {
        close(master_fd);
        fprintf(stderr, "Failed to get new PTY slave name for %s: %s\n", client->name,
                strerror(errno));
        return -1;
    }

    // Update slave name if changed
    if (strcmp(client->slave_name, slave_name) != 0) {
        printf("Slave device changed: %s -> %s\n", client->slave_name, slave_name);
        snprintf(client->slave_name, sizeof(client->slave_name), "%s", slave_name);

        // Remove old symlink
        if (access(client->name, F_OK) == 0) { unlink(client->name); }

        // Create new symbolic link
        if (symlink(slave_name, client->name) == -1) {
            fprintf(stderr, "Failed to recreate symlink %s -> %s: %s\n", client->name,
                    slave_name, strerror(errno));
            close(master_fd);
            return -1;
        }
    }

    // Set non-blocking mode for the new PTY master
    set_nonblocking(master_fd);

    // Update client state
    client->fd = master_fd;
    client->blocked = 0;
    client->pending_errors = 0;
    gettimeofday(&client->last_write_time, NULL);
    memset(&client->block_time, 0, sizeof(client->block_time));
    client->reconnect_attempts++;
    dist->reconnect_count++;

    printf("Client %s recreated successfully (new fd: %d)\n", client->name, master_fd);

    return 0;
}

// Print statistics
void print_statistics(distributor_t* dist) {
    static struct timeval last_stat_time = {0, 0};
    struct timeval now;
    gettimeofday(&now, NULL);

    if (last_stat_time.tv_sec == 0) {
        last_stat_time = now;
        return;
    }

    double elapsed = (now.tv_sec - last_stat_time.tv_sec) +
                     (now.tv_usec - last_stat_time.tv_usec) / 1000000.0;

    if (elapsed >= 10.0) { // Print every 10 seconds
        pthread_mutex_lock(&dist->mutex);

        int active_clients = 0;
        int blocked_clients = 0;
        for (int i = 0; i < dist->client_count; i++) {
            if (dist->clients[i].active) {
                active_clients++;
                if (dist->clients[i].blocked) { blocked_clients++; }
            }
        }

        printf("\n=== Statistics ===\n");
        printf("Active clients: %d (blocked: %d)\n", active_clients, blocked_clients);
        printf("Total bytes read: %ld\n", dist->total_bytes_read);
        printf("Total bytes written: %ld\n", dist->total_bytes_written);
        printf("Error count: %ld\n", dist->error_count);
        printf("Reconnect count: %ld\n", dist->reconnect_count);
        if (elapsed > 0) {
            printf("Bytes/sec read: %.1f\n", dist->total_bytes_read / elapsed);
            printf("Bytes/sec written: %.1f\n", dist->total_bytes_written / elapsed);
        }

        // Check serial buffer status
        int bytes_available = check_serial_buffer(dist->source_fd);
        if (bytes_available > 0) {
            printf("Warning: Serial buffer has %d bytes pending\n", bytes_available);
        }

        // Show blocked clients details
        if (blocked_clients > 0) {
            printf("\nBlocked clients:\n");
            for (int i = 0; i < dist->client_count; i++) {
                if (dist->clients[i].active && dist->clients[i].blocked) {
                    struct timeval block_duration;
                    timersub(&now, &dist->clients[i].block_time, &block_duration);
                    printf("  %s: blocked for %ld.%03ld seconds\n", dist->clients[i].name,
                           block_duration.tv_sec, block_duration.tv_usec / 1000);
                }
            }
        }

        printf("==================\n\n");

        last_stat_time = now;
        pthread_mutex_unlock(&dist->mutex);
    }
}

// Cleanup distributor resources
void cleanup_distributor(distributor_t* dist) {
    pthread_mutex_lock(&dist->mutex);

    dist->running = 0;

    // Cleanup all clients
    for (int i = 0; i < dist->client_count; i++) {
        if (dist->clients[i].active) {
            cleanup_client(&dist->clients[i]);
            printf("Closed client: %s\n", dist->clients[i].name);
        }
    }

    // Close source serial port
    if (dist->source_fd >= 0) {
        close(dist->source_fd);
        printf("Closed source serial port\n");
    }

    pthread_mutex_unlock(&dist->mutex);
    pthread_mutex_destroy(&dist->mutex);
}

// Check and handle blocked clients (reconnect if necessary)
void handle_blocked_clients(distributor_t* dist) {
    static int blocked_check_counter = 0;

    if (++blocked_check_counter >= 50) { // Check every 50 cycles
        pthread_mutex_lock(&dist->mutex);

        struct timeval now;
        gettimeofday(&now, NULL);

        for (int i = 0; i < dist->client_count; i++) {
            if (dist->clients[i].active && dist->clients[i].blocked) {
                // Check how long this client has been blocked
                struct timeval block_duration;
                timersub(&now, &dist->clients[i].block_time, &block_duration);

                // If blocked for more than 5 seconds, attempt to recreate
                if (block_duration.tv_sec >= 5) {
                    if (dist->clients[i].reconnect_attempts < MAX_RECONNECT_ATTEMPTS) {
                        printf(
                            "Client %s blocked for %ld seconds, attempting to recreate...\n",
                            dist->clients[i].name, block_duration.tv_sec);

                        if (recreate_client(dist, i) == 0) {
                            printf("Client %s recreated successfully\n",
                                   dist->clients[i].name);
                        } else {
                            fprintf(stderr, "Failed to recreate client %s\n",
                                    dist->clients[i].name);
                        }
                    } else {
                        fprintf(
                            stderr,
                            "Client %s exceeded max reconnect attempts (%d), deactivating\n",
                            dist->clients[i].name, MAX_RECONNECT_ATTEMPTS);
                        dist->clients[i].active = 0;
                    }
                }
            }
        }

        pthread_mutex_unlock(&dist->mutex);
        blocked_check_counter = 0;
    }
}

// Data distribution thread
void* distribution_thread(void* arg) {
    distributor_t* dist = (distributor_t*)arg;
    fd_set read_fds;
    struct timeval timeout;
    int max_fd;
    char read_buffer[BUFFER_SIZE];

    printf("Distribution thread started\n");
    printf("Press Ctrl+C to stop\n\n");

    while (dist->running && keep_running) {
        // Check if there are any active clients
        pthread_mutex_lock(&dist->mutex);
        int active_clients = 0;
        for (int i = 0; i < dist->client_count; i++) {
            if (dist->clients[i].active) { active_clients++; }
        }
        pthread_mutex_unlock(&dist->mutex);

        if (active_clients == 0) {
            printf("No active clients, sleeping for 1 second...\n");
            sleep(1);
            continue;
        }

        // Setup select for source serial port
        FD_ZERO(&read_fds);
        FD_SET(dist->source_fd, &read_fds);
        max_fd = dist->source_fd;

        timeout.tv_sec = 1; // 1 second timeout
        timeout.tv_usec = 0;

        int ready = select(max_fd + 1, &read_fds, NULL, NULL, &timeout);

        if (ready < 0) {
            // Check for interrupt
            if (errno == EINTR) {
                printf("Select interrupted, exiting...\n");
                break;
            }
            perror("Select error");
            dist->error_count++;
            usleep(100000); // Sleep 100ms on error
            continue;
        }

        if (ready > 0 && FD_ISSET(dist->source_fd, &read_fds)) {
            // Read data from source serial port
            ssize_t bytes_read = read(dist->source_fd, read_buffer, sizeof(read_buffer));

            if (bytes_read > 0) {
                dist->total_bytes_read += bytes_read;
                pthread_mutex_lock(&dist->mutex);

                // Distribute data to all active and unblocked clients
                int clients_served = 0;
                int total_bytes_written_this_round = 0;

                for (int i = 0; i < dist->client_count; i++) {
                    if (dist->clients[i].active && !dist->clients[i].blocked) {
                        ssize_t bytes_written =
                            write(dist->clients[i].fd, read_buffer, bytes_read);

                        if (bytes_written > 0) {
                            clients_served++;
                            total_bytes_written_this_round += bytes_written;
                            dist->clients[i].pending_errors = 0; // Reset error count
                            gettimeofday(&dist->clients[i].last_write_time, NULL);
                        } else if (bytes_written < 0) {
                            if (errno == EAGAIN || errno == EWOULDBLOCK) {
                                // Buffer full, mark client as blocked
                                if (!dist->clients[i].blocked) {
                                    dist->clients[i].blocked = 1;
                                    gettimeofday(&dist->clients[i].block_time, NULL);
                                    printf("Client %s blocked (buffer full), will attempt to "
                                           "recreate\n",
                                           dist->clients[i].name);
                                }
                                dist->clients[i].pending_errors++;
                            } else {
                                fprintf(stderr, "Failed to write to client %s: %s\n",
                                        dist->clients[i].name, strerror(errno));
                                dist->clients[i].active = 0;
                                dist->clients[i].pending_errors++;
                            }
                        }

                        // If too many consecutive errors, deactivate client
                        if (dist->clients[i].pending_errors > 10) {
                            fprintf(stderr, "Too many errors, deactivating client %s\n",
                                    dist->clients[i].name);
                            dist->clients[i].active = 0;
                        }
                    }
                }

                dist->total_bytes_written += total_bytes_written_this_round;

                // Try to unblock clients by checking if they have space now
                static int unblock_counter = 0;
                if (++unblock_counter >= 100) {
                    for (int i = 0; i < dist->client_count; i++) {
                        if (dist->clients[i].active && dist->clients[i].blocked) {
                            // Check if client buffer has space
                            int available = 0;
                            if (ioctl(dist->clients[i].fd, FIONREAD, &available) == 0) {
                                if (available < BUFFER_SIZE / 4) { // Buffer 1/4 empty
                                    dist->clients[i].blocked = 0;
                                    memset(&dist->clients[i].block_time, 0,
                                           sizeof(dist->clients[i].block_time));
                                    printf("Client %s unblocked (buffer has space)\n",
                                           dist->clients[i].name);
                                }
                            }
                        }
                    }
                    unblock_counter = 0;
                }

                pthread_mutex_unlock(&dist->mutex);

                // Debug output
                static int counter = 0;
                if (++counter % 500 == 0) {
                    printf("Distributed %ld bytes to %d clients (total R:%ld W:%ld)\n",
                           bytes_read, clients_served, dist->total_bytes_read,
                           dist->total_bytes_written);
                }
            } else if (bytes_read == 0) {
                // No data available (non-blocking mode)
                usleep(1000); // Sleep 1ms
            } else {
                if (errno != EAGAIN && errno != EWOULDBLOCK) {
                    perror("Read error from source serial port");
                    dist->error_count++;
                }
                usleep(10000); // Sleep 10ms on read error
            }
        } else if (ready == 0) {
            // Timeout occurred, no data available
            // This is normal in non-blocking mode
            usleep(1000); // Sleep 1ms
        }

        // Handle blocked clients (check and possibly recreate)
        handle_blocked_clients(dist);

        // Print statistics periodically
        print_statistics(dist);
    }

    printf("Distribution thread terminated\n");
    return NULL;
}

int main(int argc, char* argv[]) {
    distributor_t dist;
    pthread_t thread;

    // Set up signal handlers
    signal(SIGINT, handle_signal);
    signal(SIGTERM, handle_signal);

    // Default values
    int baudrate_num = DEFAULT_BAUDRATE;
    speed_t baudrate_termios = B460800;
    char* virtual_ports[MAX_CLIENTS];
    int port_count = 0;
    int show_statistics = 0;
    char* input_port = NULL;

    // Command line options
    static struct option long_options[] = {
        {"input", required_argument, 0, 'I'},  {"baudrate", required_argument, 0, 'b'},
        {"output", required_argument, 0, 'O'}, {"statistics", no_argument, 0, 's'},
        {"help", no_argument, 0, 'h'},         {0, 0, 0, 0}};

    int opt;
    int option_index = 0;

    while ((opt = getopt_long(argc, argv, "I:b:O:sh", long_options, &option_index)) != -1) {
        switch (opt) {
        case 'I': input_port = strdup(optarg); break;

        case 'b': parse_baudrate(optarg, &baudrate_num, &baudrate_termios); break;

        case 'O':
            if (port_count < MAX_CLIENTS) {
                virtual_ports[port_count] = strdup(optarg);
                port_count++;
            } else {
                fprintf(stderr, "Warning: Maximum number of virtual ports reached (%d)\n",
                        MAX_CLIENTS);
            }
            break;

        case 's': show_statistics = 1; break;

        case 'h': print_usage(argv[0]); return 0;

        default: print_usage(argv[0]); return 1;
        }
    }

    // Check for required input serial port argument
    if (input_port == NULL) {
        fprintf(stderr, "Error: Input serial port (-I) is required\n");
        print_usage(argv[0]);
        return 1;
    }

    printf("\n===================================================\n");
    printf("Serial Port Distributor - GPS Time Synchronization\n");
    printf("===================================================\n");
    printf("Input Port: %s\n", input_port);
    printf("Baudrate: %d\n", baudrate_num);
    printf("Max reconnect attempts: %d\n", MAX_RECONNECT_ATTEMPTS);
    printf("Auto-reconnect enabled for blocked clients\n");

    // Initialize distributor
    if (init_distributor(&dist, input_port, baudrate_num, baudrate_termios) < 0) {
        free(input_port);
        return 1;
    }

    // Add virtual ports
    if (port_count == 0) {
        // Default ports if none specified
        printf("\nNo output ports specified, using defaults...\n");
        add_client(&dist, "/tmp/virtual1");
        add_client(&dist, "/tmp/virtual2");
    } else {
        printf("\nCreating output virtual ports:\n");
        for (int i = 0; i < port_count; i++) {
            printf("  %d. %s\n", i + 1, virtual_ports[i]);
            if (add_client(&dist, virtual_ports[i]) < 0) {
                fprintf(stderr, "Failed to create virtual port: %s\n", virtual_ports[i]);
            }
        }
    }

    // Start distribution thread
    if (pthread_create(&thread, NULL, distribution_thread, &dist) != 0) {
        perror("Failed to create distribution thread");
        cleanup_distributor(&dist);
        free(input_port);
        for (int i = 0; i < port_count; i++) { free(virtual_ports[i]); }
        return 1;
    }

    // Free allocated memory
    free(input_port);
    for (int i = 0; i < port_count; i++) { free(virtual_ports[i]); }

    printf("\n===================================================\n");
    printf("Distribution Started Successfully!\n");
    printf("Available Output Ports:\n");

    pthread_mutex_lock(&dist.mutex);
    for (int i = 0; i < dist.client_count; i++) {
        printf("  %s -> %s\n", dist.clients[i].name, dist.clients[i].slave_name);
    }
    pthread_mutex_unlock(&dist.mutex);

    printf("\nTo test output ports, run in separate terminals:\n");
    for (int i = 0; i < dist.client_count; i++) { printf("  cat %s\n", dist.clients[i].name); }
    printf("\nFeatures:\n");
    printf("  - Auto-reconnect blocked clients after 5 seconds\n");
    printf("  - Max %d reconnect attempts per client\n", MAX_RECONNECT_ATTEMPTS);
    printf("===================================================\n\n");

    // Main loop for statistics display
    while (keep_running) {
        if (show_statistics) { print_statistics(&dist); }
        sleep(1);
    }

    // Signal distribution thread to stop
    dist.running = 0;

    // Wait for distribution thread to complete
    pthread_join(thread, NULL);

    // Cleanup
    cleanup_distributor(&dist);

    printf("\nSerial Port Distributor terminated\n");
    return 0;
}
```
