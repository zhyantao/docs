# stderr

```c
#include <stdio.h>

void div(int n)
{
    if (n % 2 != 0)
    {
        fprintf(stderr, "Error: The input must be an even number. Here it's %d\n", n);
    }
    else
    {
        int result = n / 2;
        fprintf(stdout, "Info: The result is %d\n", result);
    }
    return;
}

int main()
{
    for (int n = -5; n <= 5; n++)
        div(n);
    return 0;
}
```

```bash
./a.out | less

# 将正常日志打印到 output.log 中，将错误日志打印到屏幕上
./a.out > output.log
./a.out 1> output.log
./a.out >> output.log

# 将正常日志打印到黑洞文件，将错误日志打印到屏幕上
./a.out > /dev/null

# 将错误日志打印到 error.log 中，将正常日志打印到屏幕上
./a.out 2> error.log

# 将正常日志打印到 output.log 中，将错误日志打印到 error.log
./a.out > output.log 2> error.log

# 后台运行，将所有日志（包括错误日志）打印到 all.log 中
./a.out &> all.log

# 前台运行，将所有日志（包括错误日志）打印到 all.log 中
./a.out > all.log 2>&1
```
