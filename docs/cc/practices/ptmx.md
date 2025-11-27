# 虚拟串口

以下是一个使用 /dev/ptmx 创建虚拟串口的示例程序。这个程序会创建一个主从伪终端对，允许在两个进程之间进行通信。

```cpp
#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <unistd.h>
#include <string.h>
#include <errno.h>
#include <poll.h>

int main() {
    int master_fd;
    char slave_name[256];
    char buffer[256];
    ssize_t bytes_read;

    // 创建虚拟串口
    master_fd = open("/dev/ptmx", O_RDWR | O_NOCTTY);
    if (master_fd == -1) {
        perror("Failed to open /dev/ptmx");
        exit(EXIT_FAILURE);
    }

    if (grantpt(master_fd) == -1 || unlockpt(master_fd) == -1) {
        perror("Failed to setup pseudo-terminal");
        close(master_fd);
        exit(EXIT_FAILURE);
    }

    if (ptsname_r(master_fd, slave_name, sizeof(slave_name)) != 0) {
        perror("Failed to get slave device name");
        close(master_fd);
        exit(EXIT_FAILURE);
    }

    printf("Virtual serial port ready:\n");
    printf("Slave device: %s\n", slave_name);
    printf("Waiting for incoming data...\n");

    // 持续读取数据
    while (1) {
        bytes_read = read(master_fd, buffer, sizeof(buffer) - 1);

        if (bytes_read == -1) {
            perror("Read error");
            break;
        } else if (bytes_read == 0) {
            // 连接关闭
            printf("Connection closed\n");
            break;
        } else {
            buffer[bytes_read] = '\0';
            printf("Received: %s", buffer);

            // 这里可以添加数据处理逻辑
            // 例如：解析数据、响应等
        }
    }

    close(master_fd);
    return 0;
}
```

另一个进程持续向虚拟串口写入数据：

```bash
#!/bin/bash

if [ $# -eq 0 ]; then
    echo "Usage: $0 <slave_device>"
    echo "Example: $0 /dev/pts/2"
    exit 1
fi

SLAVE_DEVICE=$1

echo "Writing to slave device: $SLAVE_DEVICE"
echo "Type your messages (Ctrl+D to exit):"

while read line; do
    echo "$line" > $SLAVE_DEVICE
    sleep 0.1
done
```

```bash
echo "Hello from terminal" > /dev/pts/2
```
