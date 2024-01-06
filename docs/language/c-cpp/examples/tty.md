# 读写串口设备

```{note}
波特率、数据位、停止位、奇偶校验位设置不正确，会导致输出乱码。
```

## 读串口数据

```cpp
#include <stdio.h>
#include <fcntl.h>   /* File Control Definitions           */
#include <termios.h> /* POSIX Terminal Control Definitions */
#include <unistd.h>  /* UNIX Standard Definitions      */
#include <errno.h>   /* ERROR Number Definitions           */

int main()
{
    int fd = -1; // file descriptor for the serial port

    fd = open("/dev/ttyUSB0", O_RDWR | O_NOCTTY);
    if (fd == -1)
    {
        perror("open_port: Unable to open /dev/ttyUSB0 - ");
    }

    struct termios options;
    tcgetattr(fd, &options);

    /* Set Baud Rate */
    cfsetispeed(&options, B9600);
    cfsetospeed(&options, B9600);

    /* Enable the receiver and set local mode... */
    options.c_cflag |= (CLOCAL | CREAD);

    /* Set data bits, stop bits, parity */
    options.c_cflag &= ~CSIZE;  /* Mask the character size bits */
    options.c_cflag |= CS8;     /* Select 8 data bits */
    options.c_cflag &= ~PARENB; /* No parity */
    options.c_cflag &= ~CSTOPB; /* 1 stop bit */

    /* Set the new options for the port... */
    tcsetattr(fd, TCSANOW, &options);

    char buf[255] = {0};

    while (1)
    {
        int n = read(fd, buf, sizeof(buf)); /* read up to 255 characters if ready to read */

        if (n < 0)
        {
            perror("Read failed - ");
            return -1;
        }
        else if (n == 0)
        {
            printf("No data on port\n");
        }
        else
        {
            buf[n] = 0;
            printf("%i bytes read : %s\n", n, buf);
        }
    }

    close(fd);
    return 0;
}
```
