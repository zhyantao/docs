# SELinux

## 什么是 SELinux？

想象一下，你的 Linux 系统是一个大型公司，SELinux 就是公司的安全部门。它给每个员工（进程）和每份文件都发了特定的工作证（安全标签），然后严格规定：谁可以进入哪个办公室，谁能查看哪些文件。

**技术定义**：SELinux（安全增强型 Linux）是 Linux 内核中的强制访问控制系统，通过精细的安全策略来控制进程对文件和资源的访问权限。

## 核心概念：安全上下文

每个文件和进程都有一个安全标签，格式为：`用户:角色:类型:级别`

例如：
- `system_u:system_r:httpd_t:s0` - Web 服务器进程
- `system_u:object_r:httpd_content_t:s0` - 网站文件

## 日常管理操作

### 1. 检查 SELinux 状态

```bash
# 查看当前状态
getenforce
# 输出：Enforcing（强制模式）| Permissive（宽容模式）| Disabled（禁用）

# 查看详细状态信息
sestatus

# 查看配置文件
cat /etc/selinux/config
```

### 2. 临时切换模式

```bash
# 切换到宽容模式（仅记录违规，不阻止）
setenforce 0

# 切换到强制模式（阻止所有违规操作）
setenforce 1

# 或者使用可读模式
setenforce Permissive
setenforce Enforcing
```

### 3. 查看安全标签

```bash
# 查看文件的安全标签
ls -Z /etc/passwd
# 输出：system_u:object_r:passwd_file_t:s0 /etc/passwd

# 查看进程的安全标签
ps -eZ | grep nginx

# 查看文件的默认安全标签
restorecon -v /var/www/html/index.html
```

### 4. 修改安全标签

```bash
# 临时修改文件标签
chcon -t httpd_sys_content_t /var/www/mycustom.html

# 永久修改文件标签（重启后生效）
semanage fcontext -a -t httpd_sys_content_t "/var/www/mycustom.html"
restorecon -v /var/www/mycustom.html
```

### 5. 使用布尔值开关

布尔值就像是 SELinux 的快捷开关，可以快速启用或禁用特定功能。

```bash
# 查看所有布尔值
getsebool -a

# 查看特定布尔值
getsebool httpd_enable_homedirs

# 临时启用布尔值
setsebool httpd_enable_homedirs on

# 永久启用布尔值
setsebool -P httpd_enable_homedirs on
```

### 6. 查看安全日志

当应用被 SELinux 阻止时，查看日志：

```bash
# 查看最近的 SELinux 拒绝记录
ausearch -m avc

# 或者直接查看审计日志
grep "avc:.*denied" /var/log/audit/audit.log
```

## 实战案例：解决 gpsd 服务问题

### 问题现象

在日志中发现 gpsd 服务被 SELinux 阻止创建 socket 文件：

```bash
grep "gpsd" /var/log/audit/audit.log | grep denied
```

**错误信息示例**：
```
avc: denied { create } for pid=5323 comm="gpsd" 
name="gpsd.unix.sock" 
scontext=system_u:system_r:gpsd_t:s0 
tcontext=system_u:object_r:tmpfs_t:s0 
tclass=sock_file
```

**解读**：
- `gpsd_t` 进程想要在 `tmpfs_t` 目录中创建 socket 文件
- SELinux 拒绝了这次创建操作

### 解决方案

#### 方法一：快速修复（推荐新手）

```bash
# 1. 自动分析日志并生成解决方案
grep gpsd /var/log/audit/audit.log | audit2why

# 2. 自动生成并安装策略模块
grep gpsd /var/log/audit/audit.log | audit2allow -M gpsdfix
semodule -i gpsdfix.pp

# 3. 重启服务测试
systemctl restart gpsd
```

#### 方法二：手动创建精细策略（推荐高级用户）

**步骤 1：创建策略文件**

创建 `gpsd_fix.te`：
```selinux
policy_module(gpsd_fix, 1.0)

# 允许 gpsd 创建和管理 socket 文件
allow gpsd_t tmpfs_t:sock_file { create write unlink };
allow gpsd_t tmpfs_t:dir { search write add_name remove_name };
```

**步骤 2：编译安装**
```bash
# 编译策略
checkmodule -M -m -o gpsd_fix.mod gpsd_fix.te
semodule_package -o gpsd_fix.pp -m gpsd_fix.mod

# 安装策略
semodule -i gpsd_fix.pp
```

**步骤 3：验证修复**
```bash
# 检查策略是否加载
semodule -l | grep gpsd_fix

# 重启服务测试
systemctl restart gpsd

# 检查是否还有错误
ausearch -m avc -c gpsd
```

#### 方法三：检查现有解决方案

```bash
# 首先检查是否有现成的布尔值可以解决
getsebool -a | grep gpsd

# 搜索是否有现有的策略包
yum search selinux-gpsd
# 或
dnf search selinux-gpsd
```

## 最佳实践建议

1. **保持 Enforcing 模式**：不要轻易禁用 SELinux
2. **先看日志**：遇到问题先查 `/var/log/audit/audit.log`
3. **使用布尔值**：优先使用布尔值而非自定义策略
4. **最小权限**：只授予必要的权限
5. **测试验证**：修改后充分测试应用功能

## 常用故障排查命令

```bash
# 查看 SELinux 对特定服务的策略
seinfo -t | grep httpd

# 查看文件默认上下文
semanage fcontext -l | grep /var/www

# 分析 SELinux 日志工具
sealert -a /var/log/audit/audit.log

# 临时放行所有操作（排障用）
setenforce 0
# 排障后记得恢复
setenforce 1
```

## 学习资源

- [SELinux 官方文档](https://github.com/SELinuxProject/refpolicy/wiki/GettingStarted)
- [Debian SELinux 手册](https://l.github.io/debian-handbook/html/zh-CN/sect.selinux.html)
- [Gentoo SELinux 教程](https://wiki.gentoo.org/wiki/SELinux/Tutorials)
