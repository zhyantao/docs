# 普通文件读写

```{code-block} c
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

```{code-block} c
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

    fd_new = open(argv[2], O_WRONLY | O_CREAT | O_TRUNC, S_IRUSR | S_IWUSR | S_IRGRP | S_IWGRP | S_IROTH | S_IWOTH);
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

## fstream 无法使用相对路径

尝试修改 Visual Stuido 中项目的 >> `属性` >> `调试` >> `工作目录`。
