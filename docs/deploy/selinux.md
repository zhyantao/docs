# 配置 SELinux 安全策略

SELinux 是一种安全访问控制的软件实现。SELinux 主要回答了类似这样的问题：网站管理员是否有权限访问用户目录？

所有的进程和文件都被做了标记，SELinux 定义了进程和文件之间的交互规则，以及进程和进程之间的交互规则。我们在本文主要学习如何手动设计这些访问规则。

## 查看违规记录

```bash
cat /var/log/audit/audit.log | grep avc
```

## 查看 SELinux 状态

```bash
# cat /etc/selinux/config
getenforce
sestatus
```

## 设置 SELinux 状态

```bash
setenforce [Enforcing|Permissive|1|0]
```

## 查看 SELinux 上下文

进程和文件都被标记为 SELinux 上下文（也包括额外的信息：`user:role:type:level`）。SELinux 根据上下文对访问权限进行控制。

```bash
# 查看文件的 SELinux 上下文
ls -Z /etc/adjtime
stat -c "%C" /etc/adjtime

# 查看进程的 SELinux 上下文
ps -eZ | grep passwd

# 查看文件的目标上下文，参考 /etc/selinux/targeted/contexts/files/
restorecon -R -v /var/lib/isulad/storage/overlay2
```

## 修改 SELinux 上下文

```bash
chcon -R -t container_ro_file_t /var/lib/isulad/storage/overlay2
```

## SELinux boolearn

SELinux 布尔值可以在程序运行期间修改，查看和修改方法如下：

```bash
getsebool -a
getsebool allow_cvs_read_shadow
setsebool allow_cvs_read_shadow [on/off]
```

## 添加规则

简单来讲，需要手动创建或修改三个文件：`.te`、`.fc`、`.if`。

参考文献：

[1] <https://github.com/SELinuxProject/refpolicy/wiki/GettingStarted>

[2] <https://l.github.io/debian-handbook/html/zh-CN/sect.selinux.html>

[3] <https://wiki.gentoo.org/wiki/SELinux/Tutorials/The_security_context_of_a_process>
