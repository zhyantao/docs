(nfs)=

# NFS 挂载操作详解

## 什么是 NFS？

- **NFS（Network File System）**：网络文件系统，允许计算机之间通过网络共享目录和文件
- **架构**：Client-Server 模式
- **优势**：开发板可直接运行 Ubuntu 上的程序，无需拷贝，便于调试

## 快速开始

```text
开发板 (192.168.5.9)  ←→  交换机/路由器  ←→  Windows (192.168.5.10)
                              ↑
                              ↓
                         Ubuntu (192.168.5.11)
```

> 本教程使用 `/home/yantao/nfs_rootfs` 作为共享目录，请根据你的 Ubuntu 用户名相应调整。

```bash
# ========== Ubuntu 端 (192.168.5.11) ==========
# 1. 安装配置 NFS
sudo apt-get install nfs-kernel-server
sudo mkdir -p /home/yantao/nfs_rootfs
sudo chmod 777 /home/yantao/nfs_rootfs

# 2. 配置 exports
sudo vim /etc/exports
# 添加：/home/yantao/nfs_rootfs 192.168.5.9(rw,sync,no_root_squash) 192.168.5.10(ro,sync)

# 3. 重启服务
sudo exportfs -ra
sudo service nfs-kernel-server restart

# 4. 放入测试文件
cd /home/yantao/nfs_rootfs
echo "Hello from Ubuntu at 192.168.5.11 from /home/yantao/nfs_rootfs" > ubuntu_test.txt

# ========== 开发板端 (192.168.5.9) ==========
# 1. 挂载 NFS
mount -t nfs -o nolock,vers=3 192.168.5.11:/home/yantao/nfs_rootfs /mnt

# 2. 验证读取
cat /mnt/ubuntu_test.txt

# 3. 测试写入
echo "Hello from Board at 192.168.5.9" > /mnt/board_test.txt

# ========== Windows 端 (192.168.5.10) ==========
# 1. 打开命令提示符
# 2. 挂载 NFS
mount \\192.168.5.11\home\yantao\nfs_rootfs Z:

# 3. 查看文件
dir Z:\
# 应该看到 ubuntu_test.txt 和 board_test.txt

# 4. 测试读取（只读权限）
type Z:\ubuntu_test.txt
```

## Ubuntu 端配置（NFS 服务器）

### 1. 安装 NFS 服务器

```bash
sudo apt-get update
sudo apt-get install nfs-kernel-server
```

### 2. 配置共享目录

```bash
mkdir -p /home/yantao/nfs_rootfs
sudo chmod 777 /home/yantao/nfs_rootfs
sudo echo "/home/yantao/nfs_rootfs *(rw,sync,no_root_squash,no_subtree_check)" >> /etc/exports
```

**选项说明**：

| 选项               | 含义              |
| ------------------ | ----------------- |
| `rw`               | 读写权限          |
| `sync`             | 同步写入          |
| `no_root_squash`   | root 用户保持权限 |
| `no_subtree_check` | 不检查子目录权限  |

### 3. 重启 NFS 服务

```bash
sudo exportfs -ra                        # 使配置生效
sudo service nfs-kernel-server restart   # 或 systemctl restart nfs-kernel-server
sudo exportfs -v                         # 查看共享状态
```

## 开发板端操作（NFS 客户端）

### 1. 确保网络连通

```bash
ping 192.168.5.11
nc -zv 192.168.5.11 2049    # 检查 NFS 端口
```

### 2. 挂载 NFS 目录

```bash
mount -t nfs -o nolock,vers=3 192.168.5.11:/home/yantao/nfs_rootfs /mnt

# 参数说明：
# -t nfs       : 文件系统类型
# -o nolock    : 禁用文件锁（避免挂载失败）
# -o vers=3    : 使用 NFS 版本 3（兼容性好）
```

挂载成功后可用 `df -h` 验证。

### 3. 验证挂载

```bash
mount | grep nfs      # 查看挂载信息
ls /mnt               # 列出目录内容

# 测试读写
echo "test" > /mnt/test.txt
cat /mnt/test.txt
rm /mnt/test.txt
```

### 4. 自动化挂载（可选）

```bash
vim /etc/fstab
# 添加：192.168.5.11:/home/yantao/nfs_rootfs /mnt nfs nolock,vers=3 0 0

mount -a    # 测试配置
```

### 5. 卸载 NFS

```bash
umount /mnt

# 如提示 "device is busy"，查找占用进程：
fuser -m /mnt   # 或 lsof /mnt
```

## Windows 端操作

### 作为 NFS 客户端

#### 启用 NFS 客户端（Windows 专业版/企业版）

```powershell
# 方式一：控制面板 → 启用或关闭 Windows 功能 → 勾选 "NFS 客户端"
# 方式二：PowerShell 命令
Enable-WindowsOptionalFeature -FeatureName ServicesForNFS-ClientOnly, ClientForNFS-Infrastructure -Online -NoRestart
```

#### 挂载与卸载

```bash
# 挂载（注意路径转换：/home/... 变为 \home\...）
mount \\192.168.5.11\home\yantao\nfs_rootfs Z:

# 卸载
umount Z:
```

### 通过 Samba 共享给开发板

#### 启用 SMB 支持

控制面板 → 程序和功能 → 启用 Windows 功能 → 勾选 "SMB 1.0/CIFS 文件共享支持"

#### 共享文件夹

1. 右键文件夹 → 属性 → 共享
2. 添加共享用户和权限
3. 记录共享路径：`\\Windows_IP\共享名`

#### 开发板挂载 Samba

```bash
apt-get install cifs-utils

# 有密码挂载
mount -t cifs -o username=Windows用户名,password=密码 //192.168.5.10/share /mnt/windows

# 无密码挂载（需 Windows 设置为无密码共享）
mount -t cifs -o guest //192.168.5.10/share /mnt/windows
```

## 实际开发工作流

### 场景 1：应用程序开发调试

```bash
# Ubuntu 编译（192.168.5.11）
cd /home/yantao/nfs_rootfs
arm-buildroot-linux-gnueabihf-gcc -o hello hello.c

# 开发板运行（192.168.5.9）
cd /mnt && ./hello
```

### 场景 2：内核模块开发

```bash
# Ubuntu 编译
cd /home/yantao/nfs_rootfs
make ARCH=arm CROSS_COMPILE=arm-buildroot-linux-gnueabihf-

# 开发板加载测试
cd /mnt
insmod mymodule.ko && lsmod
```

### 场景 3：多机协作开发

1. Windows 编辑代码
2. 上传到 Ubuntu 的 `/home/yantao/nfs_rootfs/`
3. Ubuntu 交叉编译
4. 开发板通过 NFS 直接运行测试

## 扩展配置

### 多客户端访问控制

```bash
# /etc/exports 配置示例：

# 特定 IP 不同权限
/home/yantao/nfs_rootfs 192.168.5.9(rw,sync,no_root_squash) 192.168.5.10(ro,sync)

# 整个网段
/home/yantao/nfs_rootfs 192.168.5.0/24(rw,sync,no_root_squash)
```

### 性能优化挂载选项

```bash
mount -t nfs -o nolock,vers=3,rsize=32768,wsize=32768,timeo=15 192.168.5.11:/home/yantao/nfs_rootfs /mnt

# rsize/wsize：读写缓冲区大小（默认 4096，可增大）
# timeo：超时时间（默认 7 个 0.1 秒）
```
