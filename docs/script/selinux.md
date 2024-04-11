# SELinux

SELinux 是一种安全访问控制的软件实现，它主要回答类似这样的问题：网站管理员是否有权限访问用户目录？

SELinux 对所有的进程和文件都做了标记（Context），然后根据这些标记（Context）规定进程和文件之间的访问规则，以及进程和进程之间的访问规则。

我们在本文主要学习如何手动调整这些访问规则。

## SELinux Status

```bash
# 查看 SELinux 配置
cat /etc/selinux/config

# 检查 SELinux 是否开启
getenforce
sestatus

# 打开/关闭 SELinux
setenforce [Enforcing|Permissive|1|0]
```

## SELinux Context

进程和文件都被标记为 SELinux 上下文（也包括额外的信息：`user:role:type:level`）。

```bash
# 查看文件的 SELinux 上下文
ls -Z /etc/adjtime
stat -c "%C" /etc/adjtime

# 查看进程的 SELinux 上下文
ps -eZ | grep passwd

# 信息来源 /etc/selinux/targeted/contexts/files/
# 查看文件的目标上下文
restorecon -R -v /var/lib/isulad/storage/overlay2

# 修改 SELinux 上下文
chcon -R -t container_ro_file_t /var/lib/isulad/storage/overlay2
```

## SELinux Boolearn

```bash
# 查看 SELinux 布尔值
getsebool -a
getsebool allow_cvs_read_shadow

# 修改 SELinux 布尔值
# SELinux 布尔值可以在程序运行期间修改
setsebool allow_cvs_read_shadow [on/off]
```

## 查看违规记录

```bash
cat /var/log/audit/audit.log | grep avc
```

## 添加规则

简单来讲，需要手动创建或修改三个文件：`.te`、`.fc`、`.if`。

参考文献：

[1] <https://github.com/SELinuxProject/refpolicy/wiki/GettingStarted>

[2] <https://l.github.io/debian-handbook/html/zh-CN/sect.selinux.html>

[3] <https://wiki.gentoo.org/wiki/SELinux/Tutorials>
