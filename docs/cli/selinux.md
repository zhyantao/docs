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

#### 优化后的 SELinux 策略创建流程

##### 准备工作

```bash
# 安装 SELinux 开发工具（如未安装）
sudo dnf install selinux-policy-devel    # RHEL/CentOS/Fedora
sudo apt-get install selinux-policy-dev  # Debian/Ubuntu

# 确认 audit.log 中有 gpsd 相关的拒绝记录
sudo grep "gpsd.*denied" /var/log/audit/audit.log
```

##### 步骤 1：创建策略源文件

创建 `gpsd.te`：

```selinux
policy_module(gpsd, 1.0)

###########################################
# 依赖类型声明
###########################################
gen_require(`
    type gpsd_t;
    type tmpfs_t;
    class sock_file { create write setattr unlink link rename getattr };
    class dir { search write add_name remove_name };
')

###########################################
# 新类型定义
###########################################
type gpsd_socket_t;
files_type(gpsd_socket_t)

###########################################
# 核心权限规则
###########################################

# 允许在 tmpfs 目录中操作
allow gpsd_t tmpfs_t:dir { search write add_name remove_name };

# 允许在 tmpfs 中创建和管理 socket 文件
allow gpsd_t tmpfs_t:sock_file { create write setattr unlink link rename };

# 允许管理专用类型的 socket 文件
allow gpsd_t gpsd_socket_t:sock_file { create write setattr unlink link rename getattr };

###########################################
# 可选：增强安全性的规则
###########################################
# 禁止 gpsd 访问其他敏感文件
dontaudit gpsd_t tmpfs_t:file ~{ create write unlink };
# 注意：dontaudit 在现代策略中已被 tunable_policy 替代
```

##### 步骤 2：创建文件上下文文件

创建 `gpsd.fc`：

```bash
# ==========================================
# gpsd Socket 文件安全上下文定义
# ==========================================

# 精确匹配特定 socket 文件
/var/run/gpsd/gpsd\.unix\.sock    --  gen_context(system_u:object_r:gpsd_socket_t,s0)
/var/run/gpsd/gpsd\.rawdata\.sock --  gen_context(system_u:object_r:gpsd_socket_t,s0)

# 通配符匹配所有 gpsd socket 文件
/var/run/gpsd/.*\.sock            --  gen_context(system_u:object_r:gpsd_socket_t,s0)

# 可选：确保 gpsd 运行时目录的上下文
/var/run/gpsd(/.*)?               gen_context(system_u:object_r:gpsd_var_run_t,s0)
```

##### 步骤 3：创建接口文件（可选）

创建 `gpsd.if`：

```selinux
###########################################
# gpsd 策略模块接口定义
###########################################

#### <summary>gpsd socket 文件管理策略</summary>
#### <desc>
#### 此策略为 gpsd 服务提供创建和管理 socket 文件所需的权限
#### </desc>

###########################################
# gpsd_socket_file 接口
###########################################
interface(`gpsd_socket_file',`
    gen_require(`
        type gpsd_socket_t;
    ')

    # 允许域类型管理 gpsd socket 文件
    allow $1 gpsd_socket_t:sock_file { create write setattr unlink link rename getattr };

    # 允许域类型在 gpsd 目录中操作
    allow $1 gpsd_var_run_t:dir { search write add_name remove_name };
')
```

##### 步骤 4：编译策略模块

**方法一：使用 Makefile（推荐）**

```bash
# 确保在包含 .te、.fc、.if 文件的目录中执行
sudo make -f /usr/share/selinux/devel/Makefile gpsd.pp

# 或者使用绝对路径
sudo make -f /usr/share/selinux/devel/Makefile
```

**方法二：手动编译**

```bash
# 1. 编译模块
checkmodule -M -m -o gpsd.mod gpsd.te

# 2. 打包策略模块（包含文件上下文）
semodule_package -o gpsd.pp -m gpsd.mod -f gpsd.fc

# 验证生成的 .pp 文件
sesearch -A -s gpsd_t -c sock_file -p create -C gpsd.pp
```

##### 步骤 5：安装并激活策略

```bash
# 安装策略模块
sudo semodule -i gpsd.pp

# 验证模块加载
sudo semodule -l | grep gpsd

# 应用文件上下文
sudo restorecon -R -v /var/run/gpsd/

# 如果目录不存在，先创建并设置永久上下文
sudo mkdir -p /var/run/gpsd
sudo semanage fcontext -a -t gpsd_var_run_t "/var/run/gpsd(/.*)?"
sudo restorecon -R -v /var/run/gpsd
```

##### 步骤 6：全面验证

```bash
# 1. 检查策略模块状态
echo "=== 检查策略模块 ==="
sudo semodule -l | grep gpsd

# 2. 检查文件上下文
echo "=== 检查文件上下文 ==="
ls -Z /var/run/gpsd/ 2>/dev/null || echo "目录尚未创建"

# 3. 重启服务测试
echo "=== 重启 gpsd 服务 ==="
sudo systemctl restart gpsd

# 4. 检查服务状态
echo "=== 检查服务状态 ==="
sudo systemctl status gpsd --no-pager -l

# 5. 检查 SELinux 拒绝记录
echo "=== 检查 SELinux 日志 ==="
sudo ausearch -m avc -c gpsd --start recent

# 6. 检查 socket 文件创建
echo "=== 检查 socket 文件 ==="
ls -la /var/run/gpsd/*.sock 2>/dev/null && ls -Z /var/run/gpsd/*.sock

# 7. 验证权限规则
echo "=== 验证策略规则 ==="
sudo sesearch -A -s gpsd_t -c sock_file -p create
```

##### 步骤 7：故障排查

如果问题仍然存在：

```bash
# 1. 临时切换到宽容模式进行测试
sudo setenforce 0
sudo systemctl restart gpsd
sudo setenforce 1

# 2. 详细分析审计日志
sudo grep "gpsd" /var/log/audit/audit.log | audit2allow -a

# 3. 检查是否有其他权限问题
sudo sealert -a /var/log/audit/audit.log

# 4. 查看完整的策略规则
sudo sesearch -A -s gpsd_t
```

##### 步骤 8：维护和管理

```bash
# 查看模块详情
semodule -l | grep gpsd

# 更新策略（先删除后安装）
semodule -r gpsd
semodule -i gpsd.pp

# 完全移除策略
semodule -r gpsd

# 导出策略源码（如果需要备份）
semodule -E gpsd
```

##### 完整的工作目录结构

```
gpsd/
├── gpsd.te          # 主策略文件
├── gpsd.fc          # 文件上下文
├── gpsd.if          # 接口文件（可选）
└── gpsd.pp          # 编译后的策略模块
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
