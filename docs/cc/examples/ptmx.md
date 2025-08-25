# 虚拟串口

以下是一个使用 /dev/ptmx 创建虚拟串口的示例程序。这个程序会创建一个主从伪终端对，允许在两个进程之间进行通信。

```cpp
#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <unistd.h>
#include <string.h>
#include <errno.h>
#include <sys/ioctl.h>
#include <termios.h>

int main() {
    int master_fd, slave_fd;
    char slave_name[256];
    char buffer[256];
    ssize_t bytes_read;

    // 打开主设备（伪终端主设备）
    master_fd = open("/dev/ptmx", O_RDWR | O_NOCTTY);
    if (master_fd == -1) {
        perror("Failed to open /dev/ptmx");
        exit(EXIT_FAILURE);
    }

    // 设置伪终端从设备的权限
    if (grantpt(master_fd) == -1) {
        perror("grantpt failed");
        close(master_fd);
        exit(EXIT_FAILURE);
    }

    // 解锁伪终端从设备
    if (unlockpt(master_fd) == -1) {
        perror("unlockpt failed");
        close(master_fd);
        exit(EXIT_FAILURE);
    }

    // 获取从设备名称
    if (ptsname_r(master_fd, slave_name, sizeof(slave_name)) != 0) {
        perror("Failed to get slave device name");
        close(master_fd);
        exit(EXIT_FAILURE);
    }

    printf("Virtual serial port created successfully:\n");
    printf("Master device: /dev/ptmx (fd=%d)\n", master_fd);
    printf("Slave device: %s\n", slave_name);

    // 打开从设备（在实际应用中，这通常在另一个进程中进行）
    slave_fd = open(slave_name, O_RDWR | O_NOCTTY);
    if (slave_fd == -1) {
        perror("Failed to open slave device");
        close(master_fd);
        exit(EXIT_FAILURE);
    }

    printf("Slave device opened (fd=%d)\n", slave_fd);

    // 简单演示：向主设备写入数据，从从设备读取
    const char *test_message = "Hello, Virtual Serial Port!\n";
    printf("Sending test message: %s", test_message);
    
    if (write(master_fd, test_message, strlen(test_message)) == -1) {
        perror("Failed to write to master device");
        close(master_fd);
        close(slave_fd);
        exit(EXIT_FAILURE);
    }

    // 从从设备读取数据
    bytes_read = read(slave_fd, buffer, sizeof(buffer) - 1);
    if (bytes_read == -1) {
        perror("Failed to read from slave device");
        close(master_fd);
        close(slave_fd);
        exit(EXIT_FAILURE);
    }

    buffer[bytes_read] = '\0';
    printf("Received from slave device: %s", buffer);

    // 关闭文件描述符
    close(master_fd);
    close(slave_fd);

    printf("Program finished.\n");
    return 0;
}
```
