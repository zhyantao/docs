# 微内核操作系统

## 环境安装

编译仿真器 QEMU 的时间较长。而且跟着步骤走，可能编译源代码的时候会出现点问题。

```{code-block} text
undefined reference to `major'
undefined reference to `minor'
```

在相应文件中添加头文件 `#include <sys/sysmacros.h>` 就可以了。
[参考链接](https://pdos.csail.mit.edu/6.828/2018/tools.html)

```{code-block} text
error: static declaration of ‘gettid’ follows non-static declaration
```

参考
[Patch](https://patchwork.kernel.org/project/qemu-devel/patch/20190320161842.13908-3-berrange@redhat.com/)
修改一下源文件。

```{code-block} text
qemu/linux-user/syscall.c:5912: undefined reference to `stime'
```

将 `linux-user/syscall.c` 中 `get_errno(stime(&host_time));` 改为 `get_errno(clock_settime(CLOCK_REALTIME, &host_time));`
