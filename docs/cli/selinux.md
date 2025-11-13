# SELinux 概述

SELinux（Security-Enhanced Linux）是一种基于安全策略的强制访问控制（MAC）系统，作为 Linux 内核安全模块实现。它能够明确界定进程与文件之间的访问权限，例如：是否允许 Web 服务器进程访问用户主目录中的文件。

SELinux 为所有进程与文件分配安全上下文标签，并依据预定义的安全策略，管理进程对文件的访问以及进程间的交互行为。

本文主要介绍如何查看与调整 SELinux 安全策略及上下文设置。

## SELinux 状态管理

```bash
# 查看 SELinux 配置
cat /etc/selinux/config

# 检查 SELinux 运行状态
getenforce
sestatus

# 临时切换 SELinux 运行模式
setenforce [Enforcing|Permissive|1|0]
```

## SELinux 安全上下文

每个进程与文件都被赋予一个 SELinux 安全上下文，格式通常为：`user:role:type:level`。

```bash
# 查看文件的安全上下文
ls -Z /etc/adjtime
stat -c "%C" /etc/adjtime

# 查看进程的安全上下文
ps -eZ | grep passwd

# 查看文件系统的默认上下文设置
# 策略文件位置：/etc/selinux/targeted/contexts/files/
restorecon -R -v /var/lib/isulad/storage/overlay2

# 修改文件或目录的安全上下文
chcon -R -t container_ro_file_t /var/lib/isulad/storage/overlay2
```

## SELinux 布尔值

SELinux 布尔值是一组可动态调整的策略开关，用于灵活控制特定功能或服务的访问权限。

```bash
# 查看所有布尔值及其状态
getsebool -a
getsebool allow_cvs_read_shadow

# 启用或禁用布尔值（运行时生效）
setsebool allow_cvs_read_shadow [on|off]
```

## 查看 SELinux 违规日志

```bash
# 筛选访问向量缓存（AVC）拒绝记录
cat /var/log/audit/audit.log | grep avc
```

## 自定义 SELinux 策略模块

用户可通过编写策略模块扩展 SELinux 策略，通常涉及以下文件类型：

- `.te`：类型强制规则文件
- `.fc`：文件上下文定义文件
- `.if`：策略接口文件

## 参考文献

[1] SELinux Project. *Getting Started with the Reference Policy*. https://github.com/SELinuxProject/refpolicy/wiki/GettingStarted

[2] *Debian Handbook: SELinux*. https://l.github.io/debian-handbook/html/zh-CN/sect.selinux.html

[3] Gentoo Wiki. *SELinux Tutorials*. https://wiki.gentoo.org/wiki/SELinux/Tutorials
