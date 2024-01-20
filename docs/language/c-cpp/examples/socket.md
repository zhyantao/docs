# Socket 网络编程

[“一切皆 socket，些许有些夸张，但是事实也是如此，现在的网络编程几乎都是用的 socket。” ](https://www.cnblogs.com/skynet/archive/2010/12/12/1903949.html)

进程间通信，可以分为本地和远程。

本地进程间通信可以使用的方法比较多：

- 消息传递（管道、FIFO、消息队列）
- 同步（互斥量、条件变量、读写锁、文件和写记录锁、信号量）
- 共享内存（匿名的和具名的）
- 远程过程调用（Solaris 和 Sun RPC）

远程进程间通信也是网络进程通信，就目前而言，几乎所有的应用程序都是采用 socket。

在网络通信中，通信的双方只要知道  `(IP 地址, 协议, 端口号)` 三元组就可以标识对方了。IP 地址可以唯一标识网络中的主机，协议和端口号可以唯一标识主机中的应用程序。

什么是 socket？文件。在 Linux 中，所有的文件操作都是“打开、读写、关闭”这个流程。Socket 就是实现了这种模式的特殊文件。

打开普通文件会返回一个文件描述符，打开 socket 文件会返回一个 socket 描述符。不管是普通文件还是 socket 文件，后续的操作都是用描述符来读写文件的。下面是 TCP 调用的基本流程：

```{figure} ../../../_static/images/socket-api-tcp-implement.png
:name: socket-api-tcp-implement

网络应用的 socket API (TCP) 调用基本流程
```

学习 socket 网络编程，主要是学习图片中出现的几个函数的使用方法，下面将做详细介绍。

## socket() 函数

```cpp
int socket(int domain, int type, int protocol);
```

打开 socket 文件时，需要指定的参数有三个：

**domain：协议族（family）决定了 socket 的地址类型**

- `AF_INET`（必须用 32 位的 IPv4 地址和 16 位的端口号）
- `AF_INET6`（必须使用 IPv6 协议）
- `AF_UNIX` 或 `AF_LOCAL`（本地通信，必须用绝对路径作为地址）
- `AF_ROUTE`

**type：指定了 socket 的类型**

- `SOCK_STREAM`（流格式套接字，使用面向连接的 TCP 协议，可靠性高）
- `SOCK_DGRAM`（数据报格式套接字，使用无连接的 UDP 协议，速度快）
- `SOCK_RAW`
- `SOCK_PACKET`
- `SOCK_SEQPACKET`

**protocol：指定了传输协议**

- `IPPROTO_TCP`
- `IPPROTO_UDP`
- `IPPROTO_SCTP`
- `IPPROTO_TIPC`

注意，type 和 protocol 并不是随意组合的。比如 `SOCK_STREAM` 不可以跟 `IPPROTO_UDP` 组合，当 protocol 为 0 时，会自动选择 type 类型对应的默认协议。

当我们调用 `socket()` 创建 socket 时，返回的 socket 描述符存在于协议族空间中，但是并没有一个具体的地址，如果我们想给它赋值一个地址，必须使用 `bind()` 函数，否则就在调用 `connect()` 和 `listen()` 时系统自动随机分配一个端口。

## bind() 函数

```cpp
int bind(int sockfd, const struct sockaddr *addr, socklen_t addrlen);
```

`bind()` 函数用于把地址族中的一个特定地址赋值给 socket。例如 `AF_INET` 和 `AF_INET6` 就是把一个 IPv4 或 IPv6 地址和端口号组合赋给 socket。

**sockfd：socket 描述符，唯一标识一个 socket，bind() 函数将为它绑定 IP 地址和端口号。**

**addr：指定要绑定给 sockfd 的协议地址，地址结构根据创建 socket 时协议族的不同而不同。**

IPv4 对应的地址结构如下：

```cpp
struct sockaddr_in {
    sa_family_t    sin_family; /* address family: AF_INET */
    in_port_t      sin_port;   /* port in network byte order */
    struct in_addr sin_addr;   /* internet address */
};

/* Internet address. */
struct in_addr {
    uint32_t       s_addr;     /* address in network byte order */
};
```

IPv6 对应的地址结构如下：

```cpp
struct sockaddr_in6 { 
    sa_family_t     sin6_family;   /* AF_INET6 */ 
    in_port_t       sin6_port;     /* port number */ 
    uint32_t        sin6_flowinfo; /* IPv6 flow information */ 
    struct in6_addr sin6_addr;     /* IPv6 address */ 
    uint32_t        sin6_scope_id; /* Scope ID (new in 2.4) */ 
};

struct in6_addr { 
    unsigned char   s6_addr[16];   /* IPv6 address */ 
};
```

UNIX 协议的地址结构如下：

```cpp
#define UNIX_PATH_MAX    108

struct sockaddr_un { 
    sa_family_t sun_family;               /* AF_UNIX */ 
    char        sun_path[UNIX_PATH_MAX];  /* pathname */ 
};
```

**addrlen：地址的长度。**

通常服务器在启动的时候都会绑定一个众所周知的地址（如 IP 地址 + 端口号），用于提供服务，客户就可以通过它来接连服务器；而客户端就不用指定，由系统自动分配一个端口号和自身的 IP 地址组合。这就是为什么通常服务器端在 `listen()` 之前会调用 `bind()`，而客户端就不会调用，而是在 `connect()` 时由系统随机生成一个。

**网络字节序与主机字节序**

**主机字节序**就是我们平常说的大端和小端模式：不同的 CPU 有不同的字节序类型，这些字节序是指整数在内存中保存的顺序，这个叫做主机序。引用标准的 Big-Endian 和 Little-Endian 的定义如下：

- Little-Endian 就是低位字节排放在内存的低地址端，高位字节排放在内存的高地址端。
- Big-Endian 就是高位字节排放在内存的低地址端，低位字节排放在内存的高地址端。

**网络字节序**：4 个字节的 32 bit 值以下面的次序传输：首先是 0～7bit，其次 8～15bit，然后 16～23bit，最后是 24 ~ 31bit。这种传输次序称作大端字节序。**由于 TCP/IP 首部中所有的二进制整数在网络中传输时都要求以这种次序，因此它又称作网络字节序。字节序，顾名思义即字节的顺序，就是大于一个字节类型的数据在内存中的存放顺序，一个字节的数据没有顺序的问题了。**

所以：在将一个地址绑定到 socket 的时候，请先将主机字节序转换成为网络字节序，而不要假定主机字节序跟网络字节序一样使用的是 Big-Endian。由于这个问题曾引发过血案！公司项目代码中由于存在这个问题，导致了很多莫名其妙的问题，所以请谨记对主机字节序不要做任何假定，务必将其转化为网络字节序再赋给 socket。

## listen() 和 connect() 函数

```cpp
int listen(int sockfd, int backlog);
int connect(int sockfd, const struct sockaddr *addr, socklen_t addrlen);
```

在服务器端，调用 `socket()` 和 `bind()` 函数后就应该调用 `listen()` 来监听这个 socket，这时在客户端调用 `connect()` 发出连接请求，服务器端就会收到这个请求。

`listen()` 函数的第一个参数是要监听的 socket 描述符，第二个参数是可以排队连接到该 socket 的最大连接个数。`socket()` 函数创建的 socket 默认是一个主动类型的，`listen()` 函数将 socket 变为被动类型的，等待客户的连接请求。

`connect()` 函数的第一个参数是客户端的 socket 描述符，第二参数是服务器的 socket 地址，第三个参数为 socket 地址的长度。客户端通过调用 `connect()` 函数与服务器建立 TCP 连接。

## accept() 函数

TCP 服务器端依次调用 `socket()`、`bind()`、`listen()` 之后，就会监听指定的 socket 地址了。TCP 客户端依次调用 `socket()`、`connect()` 之后就向 TCP 服务器发送了一个连接请求。TCP 服务器监听到这个请求之后，就会调用 `accept()` 函数取接收请求，这样连接就建立好了。之后就可以开始网络 I/O 操作了，类似于普通文件的读写操作。

```cpp
int accept(int sockfd, struct sockaddr *addr, socklen_t *addrlen);
```

`accept()` 函数的第一个参数是服务器的 socket 描述符，第二个参数是指向客户端的协议地址的指针，第三个参数是客户端协议地址的长度。如果 `accpet()` 成功，那么其返回值是由系统自动生成的一个**全新的描述符**，代表 TCP 连接。

注意：`accept()` 函数的第一个参数是服务器调用 `socket()` 函数生成的描述符，称为监听 socket 描述符；而 `accept()` 函数返回的是已连接的 socket 描述符。**一个服务器通常通常仅仅只创建一个监听 socket 描述符**，它在该服务器的生命周期内一直存在。同时，系统为每个被服务器接受的客户连接请求创建一个已连接 socket 描述符，当服务器完成某个客户请求，相应的已连接 socket 描述符就被关闭。

## send() 和 recv() 函数

万事具备只欠东风，至此服务器与客户已经建立好连接了。可以调用网络 I/O 进行读写操作了，常用的网络 I/O 操作接口有下面 5 组：

**read() / write()**

```cpp
#include <unistd.h>

ssize_t read(int fd, void *buf, size_t count);
ssize_t write(int fd, const void *buf, size_t count);
```

`read()` 函数从 `fd` 中读取内容。读成功时，返回读取的字节数。如果返回值是 0，表示已经读到文件末尾，小于 0 表示出现了错误。如果错误为 `EINTR` 表示读操作被中断了，如果是 `ECONNREST` 表示网络连接出了问题。

`write()` 函数将 `buf` 中 `count` 字节的内容写入 `fd`。写成功时，返回写入的字节数，写失败时，返回 -1，并设置 `errno` 变量。如果错误为 `EINTR` 表示写操作被中断，如果是 `EPIPE` 表示对方关闭了连接。

**send() / recv()**

```cpp
#include <sys/types.h>
#include <sys/socket.h>

ssize_t send(int sockfd, const void *buf, size_t len, int flags);
ssize_t recv(int sockfd, void *buf, size_t len, int flags);
```

**readv() / writev()**

```cpp
#include <sys/types.h>
#include <sys/socket.h>

ssize_t sendto(int sockfd, const void *buf, size_t len, int flags,
               const struct sockaddr *dest_addr, socklen_t addrlen);
ssize_t recvfrom(int sockfd, void *buf, size_t len, int flags,
                 struct sockaddr *src_addr, socklen_t *addrlen);
```

**sendmsg() / recvmsg()**

```cpp
#include <sys/types.h>
#include <sys/socket.h>

ssize_t sendmsg(int sockfd, const struct msghdr *msg, int flags);
ssize_t recvmsg(int sockfd, struct msghdr *msg, int flags);
```

**sendto() / recvfrom()**

```cpp
#include <sys/types.h>
#include <sys/socket.h>

ssize_t sendto(int sockfd, const void *buf, size_t len, int flags,
               const struct sockaddr *dest_addr, socklen_t addrlen);
ssize_t recvfrom(int sockfd, void *buf, size_t len, int flags,
                 struct sockaddr *src_addr, socklen_t *addrlen);
```

推荐使用 `sendmsg()` 和 `recvmsg()` 函数，这两个是最通用的 I/O 函数，实际上可以把其他函数都替换成这两个。

## close() 函数

```cpp
#include <unistd.h>

int close(int fd);
```

关闭 TCP socket 的缺省行为是把该 socket 标记为关闭，然后立即返回调用进程，该描述字不能再被调用进程使用，也就是说不能再作为 `read()` 或 `write()` 的第一个参数。

注意：`close()` 操作只是使相应 socket 描述字的引用计数减 1，只有当引用计数为 0 的时候，才会触发客户端向服务器发送终止连接请求。

## 一个例子

```cpp
// server.c

#include <errno.h>
#include <netinet/in.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <unistd.h>

#define MAXLINE 4096

int main(int argc, char **argv)
{
    int listenfd, connfd;
    struct sockaddr_in serveraddr;
    char buf[4096];
    int n;

    // (1) 创建 socket
    if ((listenfd = socket(AF_INET, SOCK_STREAM, 0)) == -1)
    {
        printf("create socket failed: %s(errno: %d)\n", strerror(errno), errno);
        exit(-1);
    }

    memset(&serveraddr, 0, sizeof(serveraddr));
    serveraddr.sin_family = AF_INET;                // 使用 IPv4 协议
    serveraddr.sin_addr.s_addr = htonl(INADDR_ANY); // 将主机字节序转换为网络字节序
    serveraddr.sin_port = htons(6666);              // 将无符号整数转换为网络字节序

    // (2) 为 socket 分配 IP 和端口号
    if (bind(listenfd, (struct sockaddr *)&serveraddr, sizeof(serveraddr)) == -1)
    {
        printf("bind socket failed: %s(errno: %d)\n", strerror(errno), errno);
        exit(-2);
    }

    // (3) 监听 socket
    if (listen(listenfd, 10) == -1)
    {
        printf("listen socket failed: %s(errno: %d)\n", strerror(errno), errno);
        exit(-3);
    }
    printf("...... waiting for client's request\n");

    while (1)
    {
        // (4) 建立连接，三次握手
        if ((connfd = accept(listenfd, (struct sockaddr *)NULL, NULL)) == -1)
        {
            printf("accept socket failed: %s(errno: %d)\n", strerror(errno), errno);
            continue;
        }

        // (5) 网络 I/O 操作
        memset(buf, 0, sizeof(buf));
        n = recv(connfd, buf, MAXLINE, 0);

        // (6) TODO: 处理客户端发来的数据
        printf("[server] recv msg from client: %s\n", buf);

        // (7) TODO: 将处理结果返回给客户端
        printf("[server] send msg to client: %s\n", buf);
        send(connfd, buf, strlen(buf), 0);

        // (8) 关闭连接，四次挥手
        close(connfd);
    }

    // (9) 关闭 socket
    close(listenfd);

    return 0;
}
```

```cpp
// client.c

#include <arpa/inet.h>
#include <errno.h>
#include <netinet/in.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <unistd.h>

#define MAXLINE 4096

int main(int argc, char **argv)
{
    int sockfd;
    char recvline[4096], sendline[4096];
    struct sockaddr_in serveraddr;

    if (argc != 2)
    {
        printf("usage: ./client <ipaddress>\n");
        exit(-1);
    }

    // (1) 创建 socket
    if ((sockfd = socket(AF_INET, SOCK_STREAM, 0)) < 0)
    {
        printf("create socket error: %s(errno: %d)\n", strerror(errno), errno);
        exit(-2);
    }

    memset(&serveraddr, 0, sizeof(serveraddr));
    serveraddr.sin_family = AF_INET;   // 使用 IPv4 协议
    serveraddr.sin_port = htons(6666); // 将无符号整数转换为网络字节序
    // 将标准文本表示形式的 IPv4 或 IPv6 地址转换为数字二进制形式
    if (inet_pton(AF_INET, argv[1], &serveraddr.sin_addr) <= 0)
    {
        printf("inet_pton error for %s\n", argv[1]);
        exit(-3);
    }

    // (2) 发送连接请求
    if (connect(sockfd, (struct sockaddr *)&serveraddr, sizeof(serveraddr)) < 0)
    {
        printf("connect error: %s(errno: %d)\n", strerror(errno), errno);
        exit(-4);
    }

    // (3) TODO: 撰写需要向服务器发送的数据
    printf("[client] send msg to server: ");
    fgets(sendline, 4096, stdin);

    // (4) 向服务器发送数据
    if (send(sockfd, sendline, strlen(sendline), 0) < 0)
    {
        printf("send msg error: %s(errno: %d)\n", strerror(errno), errno);
        exit(-5);
    }

    // (5) 接收服务器的回复
    if (recv(sockfd, recvline, MAXLINE, 0) < 0)
    {
        printf("recv msg error: %s(errno: %d)\n", strerror(errno), errno);
        exit(-6);
    }

    printf("[client] received reply from server: %s\n", recvline);

    // (6) 关闭 socket
    close(sockfd);

    return 0;
}
```

当然，上面的代码很简单，也有很多缺点，比如每次建立连接后只能接收一条消息，就断开连接了，这仅仅简单地演示 socket 的基本使用。其实不管有多复杂的网络程序，都使用的这些基本函数。上面的服务器使用的是迭代模式的，即只有处理完一个客户端请求才会去处理下一个客户端的请求，这样的服务器处理能力是很弱的，现实中的服务器都需要有并发处理能力！因此，强烈建议参考 [Muduo 的思想](https://www.cnblogs.com/S1mpleBug/p/16712003.html) 来真正落实网络编程。
