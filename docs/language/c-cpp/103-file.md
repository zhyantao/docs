# 普通文件读写

在 Linux 中，一切皆文件。学会操作文件，对于学习 Linux 来讲，是一项必备技能。在操作系统的底层，对文件操作的 API 封装已经很好了，使用起来也比较方便，下面是三个文件操作的例子。

第一个例子是使用 `open` 和 `write` 函数复制文件：

```c
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <stdio.h>

int main(int argc, char *argv[])
{
    int fd_old, fd_new;
    char buf[1024];
    int len;

    if (argc != 3)
    {
        printf("Usage: %s <old_file> <new_file>\n", argv[0]);
        return -1;
    }

    fd_old = open(argv[1], O_RDONLY);
    if (fd_old == -1)
    {
        printf("Open file error: %s\n", argv[1]);
        return -1;
    }

    fd_new = open(argv[2], O_WRONLY | O_CREAT | O_TRUNC,
                  S_IRUSR | S_IWUSR | S_IRGRP | S_IWGRP | S_IROTH | S_IWOTH);
    if (fd_new == -1)
    {
        printf("Open file error: %s\n", argv[2]);
        return -1;
    }

    while ((len = read(fd_old, buf, 1024)) > 0)
    {
        if (write(fd_new, buf, len) != len)
        {
            printf("Can not write to file: %s\n", argv[2]);
            return -1;
        }
    }

    close(fd_old);
    close(fd_new);

    return 0;
}
```

第二个例子是使用 `putc` 写文件，使用 `getc` 读文件：

```c
#include <stdio.h>

int main()
{
    char c;
    FILE *fp = NULL;

    // 写文件
    fp = fopen("INPUT", "w");
    while((c = getchar()) != '\n')
    {
        putc(c, fp);
    }
    fclose(fp);

    // 读文件
    fp = fopen("INPUT", "r");
    while((c = getc(fp)) != EOF)
    {
        printf("%c", c);
    }
    fclose(fp);
    printf("\n");

    return 0;
}
```

第三个例子相较于前两个更加高级，它使用 `mmap` 将文件内容映射到内存，实现了对内存操作即可修改文件内容的功能：

```c
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <stdio.h>
#include <sys/mman.h> // 此功能并非所有机器都支持，共享内存性能更高

int main(int argc, char *argc[])
{
    int fd_old, fd_new;
    struct stat stat;
    char *buf;

    if (argc != 3)
    {
        printf("Usage: %s <old_file> <new_file>\n", argv[0]);
        return -1;
    }

    fd_old = open(argv[1], O_RDONLY);
    if (fd_old == -1)
    {
        printf("Open file error: %s\n", argv[1]);
        return -1;
    }

    // 确定老文件的大小
    if (fstat(fd_old, &stat) == -1)
    {
        printf("Can not get stat of file: %s\n", argv[1]);
        return -1;
    }

    // 映射老文件
    buf = mmap(NULL, stat.st_size, PORT_READ, MAP_SHARED, fd_old, 0);
    if (buf == MAP_FAILED)
    {
        printf("Can not mmap file: %s\n", argv[1]);
        return -1;
    }

    fd_new = open(argv[2], O_WRONLY | O_CREAT | O_TRUNC,
                  S_IRUSR | S_IWUSR | S_IRGRP | S_IWGRP | S_IROTH | S_IWOTH);
    if (fd_new == -1)
    {
        printf("Open file error: %s\n", argv[2]);
        return -1;
    }

    if (write(fd_new, buf, stat.st_size) != stat.st_size)
    {
        printf("Can not write to file: %s\n", argv[2]);
        return -1;
    }

    close(fd_old);
    close(fd_new);

    return 0;
}
```

## fstream 无法使用相对路径

尝试修改 Visual Stuido 中项目的 >> `属性` >> `调试` >> `工作目录`。
