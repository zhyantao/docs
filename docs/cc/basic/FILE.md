# FILE

在 Linux 中，一切皆文件。学会操作文件，对于学习 Linux 来讲，是一项必备技能。在操作系统的底层，对文件操作的 API 封装已经很好了，使用起来也比较方便，下面是三个文件操作的例子。

## 例 1：open / write

```cpp
#include <fcntl.h>
#include <stdio.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>

int main(int argc, char* argv[]) {
    int fd_old, fd_new;
    char buf[1024];
    int len;

    if (argc != 3) {
        printf("Usage: %s <old_file> <new_file>\n", argv[0]);
        return -1;
    }

    fd_old = open(argv[1], O_RDONLY);
    if (fd_old == -1) {
        printf("Open file error: %s\n", argv[1]);
        return -1;
    }

    fd_new = open(argv[2], O_WRONLY | O_CREAT | O_TRUNC,
                  S_IRUSR | S_IWUSR | S_IRGRP | S_IWGRP | S_IROTH | S_IWOTH);
    if (fd_new == -1) {
        printf("Open file error: %s\n", argv[2]);
        return -1;
    }

    while ((len = read(fd_old, buf, 1024)) > 0) {
        if (write(fd_new, buf, len) != len) {
            printf("Can not write to file: %s\n", argv[2]);
            return -1;
        }
    }

    close(fd_old);
    close(fd_new);

    return 0;
}
```

## 例 2：fread / fwrite

```cpp
#include <fcntl.h>
#include <stdio.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>

int main() {
    FILE *fd_old, *fd_new;
    char buf[1024];
    int bytesread;
    char file_old[256] = {0};
    sprintf(file_old, "%s", "serial1.log");
    char file_new[256] = {0};
    sprintf(file_new, "%s", "serial2.log");

    fd_old = fopen(file_old, "rb");
    if (fd_old == NULL) {
        perror("Open file error");
        return -1;
    }

    fd_new = fopen(file_new, "wb");
    if (fd_new == NULL) {
        perror("Open file error");
        return -1;
    }

    while ((bytesread = fread(buf, 1, sizeof(buf), fd_old)) > 0) {
        fwrite(buf, 1, bytesread, fd_new);
    }

    fclose(fd_old);
    fclose(fd_new);
    return 0;
}
```

## 例 3：mmap 共享内存

```cpp
#include <fcntl.h>
#include <stdio.h>
#include <sys/mman.h> // 共享内存性能更高，但是此功能并非所有机器都支持
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>

int main(int argc, char* argv[]) {
    int fd_old, fd_new;
    struct stat stat;
    char* buf;

    if (argc != 3) {
        printf("Usage: %s <old_file> <new_file>\n", argv[0]);
        return -1;
    }

    fd_old = open(argv[1], O_RDONLY);
    if (fd_old == -1) {
        printf("Open file error: %s\n", argv[1]);
        return -1;
    }

    // 确定老文件的大小
    if (fstat(fd_old, &stat) == -1) {
        printf("Can not get stat of file: %s\n", argv[1]);
        return -1;
    }

    // 映射老文件
    buf = mmap(NULL, stat.st_size, PROT_READ, MAP_SHARED, fd_old, 0);
    if (buf == MAP_FAILED) {
        printf("Can not mmap file: %s\n", argv[1]);
        return -1;
    }

    fd_new = open(argv[2], O_WRONLY | O_CREAT | O_TRUNC,
                  S_IRUSR | S_IWUSR | S_IRGRP | S_IWGRP | S_IROTH | S_IWOTH);
    if (fd_new == -1) {
        printf("Open file error: %s\n", argv[2]);
        return -1;
    }

    if (write(fd_new, buf, stat.st_size) != stat.st_size) {
        printf("Can not write to file: %s\n", argv[2]);
        return -1;
    }

    close(fd_old);
    close(fd_new);

    return 0;
}
```

## 从指定位置读写文件

```{code-block} c
#include <stdio.h>

int main()
{
    char c;
    FILE *fp = NULL;

    // 读文件
    fp = fopen("INPUT", "r");

    int ret = fseek(fp, 28, 0); // 把文件指针放到指定位置
    printf("Return value of fseek(): %d\nPosition of pointer* fp: %d\n\n", ret, ftell(fp));

    while ((c = getc(fp)) != EOF)
    {
        printf("%c", c);
    }
    fclose(fp);
    printf("\n");

    return 0;
}
```

## Q & A

**fstream 无法使用相对路径**

尝试修改 Visual Stuido 中项目的 >> `属性` >> `调试` >> `工作目录`。
