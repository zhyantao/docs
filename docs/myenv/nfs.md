(nfs)=

# NFS 挂载操作详解

## 一、NFS 基本概念

### 什么是 NFS？

- **NFS（Network File System）**：网络文件系统
- **作用**：允许计算机之间通过网络共享目录和文件
- **架构**：Client-Server 模式
- **优势**：开发板可以直接运行 Ubuntu 上的程序，无需拷贝，便于调试

**重要提示**：在本教程中，我们使用 `/home/yantao/nfs_rootfs` 作为共享目录，如果你的 Ubuntu 用户名不同，请相应修改路径。

---

## 二、Ubuntu 端配置（NFS 服务器）

### 1. 安装 NFS 服务器

```bash
# Ubuntu 安装 NFS 服务
sudo apt-get update
sudo apt-get install nfs-kernel-server
```

### 2. 配置共享目录

```bash
# 创建共享目录
mkdir -p /home/yantao/nfs_rootfs

# 修改目录权限
sudo chmod 777 /home/yantao/nfs_rootfs

# 编辑 NFS 配置文件
sudo vim /etc/exports
```

### 3. 编辑 exports 文件内容

在 `/etc/exports` 文件中添加：

```bash
# 语法：共享目录 客户端IP(权限选项)
/home/yantao/nfs_rootfs *(rw,sync,no_root_squash,no_subtree_check)
```

**选项说明**：

- `rw`：读写权限
- `sync`：同步写入
- `no_root_squash`：root 用户保持权限
- `no_subtree_check`：不检查子目录权限

### 4. 重启 NFS 服务

```bash
# 使配置生效
sudo exportfs -ra

# 重启 NFS 服务
sudo service nfs-kernel-server restart
# 或
sudo systemctl restart nfs-kernel-server

# 查看 NFS 共享状态
sudo exportfs -v
```

### 5. 查看 Ubuntu IP 地址

```bash
# 查看网络接口和 IP
ifconfig

# 或使用 ip 命令
ip addr show

# 重点关注桥接网卡的 IP
# 假设网络配置如下：
# - 192.168.5.9：开发板 IP
# - 192.168.5.10：Windows IP
# - 192.168.5.11：Ubuntu IP
```

---

## 三、开发板端操作（NFS 客户端）

### 1. 确保网络连通

```bash
# 首先 ping 通 Ubuntu
ping 192.168.5.11

# 如果 ping 不通，检查：
# 1. 网线连接
# 2. IP 地址设置
# 3. 防火墙设置
```

### 2. 挂载 NFS 目录

```bash
# 基本挂载命令
mount -t nfs -o nolock,vers=3 192.168.5.11:/home/yantao/nfs_rootfs /mnt

# 参数详解：
# -t nfs：指定文件系统类型为 NFS
# -o nolock：禁用文件锁（避免挂载失败）
# -o vers=3：使用 NFS 版本 3（兼容性好）
# 192.168.5.11：Ubuntu 的 IP 地址
# :/home/yantao/nfs_rootfs：Ubuntu 的共享目录
# /mnt：开发板上的挂载点

# 挂载成功不会有提示，可用 df 命令验证
df -h
```

### 3. 验证挂载

```bash
# 查看挂载信息
mount | grep nfs

# 列出 /mnt 目录内容
ls /mnt

# 测试读写
echo "test" > /mnt/test.txt
cat /mnt/test.txt
rm /mnt/test.txt
```

### 4. 自动化挂载（可选）

```bash
# 编辑 /etc/fstab 文件实现开机自动挂载
vim /etc/fstab
# 添加以下行：
192.168.5.11:/home/yantao/nfs_rootfs /mnt nfs nolock,vers=3 0 0

# 测试 fstab 配置
mount -a
```

### 5. 卸载 NFS

```bash
# 卸载挂载点
umount /mnt

# 如果提示 "device is busy"，查找占用进程
fuser -m /mnt
# 或
lsof /mnt
```

---

## 四、Windows 端相关操作

### 1. Windows 作为 NFS 客户端

#### 启用 NFS 客户端（Windows 专业版/企业版）

```powershell
# 打开 "启用或关闭 Windows 功能"
# 勾选 "NFS 客户端"
# 或使用 PowerShell 命令：
Enable-WindowsOptionalFeature -FeatureName ServicesForNFS-ClientOnly, ClientForNFS-Infrastructure -Online -NoRestart
```

#### 挂载 NFS 共享

```bash
# 命令格式
mount \\Ubuntu_IP\共享目录 盘符:
# 示例：
mount \\192.168.5.11\home\yantao\nfs_rootfs Z:

# 注意：Windows 需要 Linux 路径转换
# /home/yantao/nfs_rootfs 在 Windows 中显示为 \home\yantao\nfs_rootfs

# 卸载
umount Z:
```

### 2. Windows 通过 Samba 共享给开发板

#### 安装 Samba 服务

1. 控制面板 → 程序和功能 → 启用 "Windows 功能"
2. 勾选 "SMB 1.0/CIFS 文件共享支持"

#### 共享文件夹

1. 右键文件夹 → 属性 → 共享
2. 添加共享用户和权限
3. 记录共享路径：`\\Windows_IP\共享名`

#### 开发板挂载 Samba（使用 Windows IP：192.168.5.10）

```bash
# 安装 cifs 工具（如果未安装）
apt-get install cifs-utils

# 挂载命令
mount -t cifs -o username=Windows用户名,password=密码 //192.168.5.10/share /mnt/windows

# 无密码挂载（需要 Windows 设置共享为无密码）
mount -t cifs -o guest //192.168.5.10/share /mnt/windows
```

---

## 五、三机网络配置参考

### 推荐网络配置

```text
开发板 (192.168.5.9)  ←→  交换机/路由器  ←→  Windows (192.168.5.10)
                              ↑
                              ↓
                         Ubuntu (192.168.5.11)
```

### 各设备作用

1. **开发板 (192.168.5.9)**：
   - NFS 客户端
   - 运行测试程序
   - 通过串口连接调试

2. **Windows (192.168.5.10)**：
   - 开发主机
   - 代码编辑
   - 文件管理（通过 FileZilla）
   - 串口终端（MobaXterm）

3. **Ubuntu (192.168.5.11)**：
   - NFS 服务器
   - TFTP 服务器
   - 交叉编译环境
   - 版本控制（Git）
   - 共享目录：`/home/yantao/nfs_rootfs`

### 测试网络连通性

```bash
# 在开发板上测试
ping 192.168.5.10  # 测试到 Windows 的连通性
ping 192.168.5.11  # 测试到 Ubuntu 的连通性

# 在 Ubuntu 上测试
ping 192.168.5.9   # 测试到开发板的连通性
ping 192.168.5.10  # 测试到 Windows 的连通性

# 在 Windows 上测试（命令提示符）
ping 192.168.5.9
ping 192.168.5.11
```

---

## 六、实际开发工作流

### 场景 1：应用程序开发调试

```bash
# Ubuntu 上编译程序（192.168.5.11）
cd /home/yantao/nfs_rootfs
arm-buildroot-linux-gnueabihf-gcc -o hello hello.c

# 开发板上直接运行（192.168.5.9）
cd /mnt
./hello
# 无需拷贝，立即测试
```

### 场景 2：内核模块开发

```bash
# Ubuntu 编译内核模块（192.168.5.11）
cd /home/yantao/nfs_rootfs
make ARCH=arm CROSS_COMPILE=arm-buildroot-linux-gnueabihf-

# 开发板加载测试（192.168.5.9）
cd /mnt
insmod mymodule.ko
lsmod
```

### 场景 3：多机协作开发

```bash
# 开发流程：
# 1. 在 Windows (192.168.5.10) 上编辑代码
# 2. 通过 FileZilla 上传到 Ubuntu (192.168.5.11) 的 /home/yantao/nfs_rootfs/
# 3. 在 Ubuntu 上交叉编译
# 4. 在开发板 (192.168.5.9) 上通过 NFS 直接运行测试
# 5. 调试修改，循环 1-4 步骤
```

---

## 七、常见问题与解决方法

### 问题 1：挂载失败 "Connection refused"

```bash
# 检查 Ubuntu 端（192.168.5.11）：
# 1. NFS 服务是否运行
sudo service nfs-kernel-server status

# 2. 防火墙是否阻止
sudo ufw status
sudo ufw allow 2049  # NFS 端口

# 3. exports 配置是否正确
sudo cat /etc/exports
```

### 问题 2：权限问题 "Permission denied"

```bash
# 解决方案：
# 1. 确保 exports 文件有 no_root_squash 选项
# 2. 检查目录权限
sudo chmod 777 /home/yantao/nfs_rootfs
# 3. 确认开发板（192.168.5.9）以 root 用户操作
```

### 问题 3：路径不存在

```bash
# 检查目录是否存在
ls -la /home/yantao/nfs_rootfs

# 如果目录不存在，创建它
sudo mkdir -p /home/yantao/nfs_rootfs
sudo chmod 777 /home/yantao/nfs_rootfs
```

### 问题 4：Windows 无法访问 NFS

```powershell
# 检查 Windows（192.168.5.10）：
# 1. NFS 客户端功能是否启用
# 2. 防火墙是否允许 NFS
# 3. 尝试使用完整 UNC 路径
mount \\192.168.5.11\home\yantao\nfs_rootfs Z:
```

### 问题 5：IP 地址冲突

```bash
# 如果 IP 冲突，修改配置：
# Ubuntu（192.168.5.11）：修改 /etc/netplan/ 配置
# Windows（192.168.5.10）：网络设置中修改
# 开发板（192.168.5.9）：U-Boot 或系统中修改

# 查看当前网络中的设备
arp -a
```

---

## 八、高级配置技巧

### 1. 使用静态 IP 确保稳定性

```bash
# Ubuntu（192.168.5.11）设置静态 IP
sudo vim /etc/netplan/01-netcfg.yaml
# 添加：
network:
  version: 2
  ethernets:
    ens33:
      addresses: [192.168.5.11/24]
      gateway4: 192.168.5.1
      nameservers:
        addresses: [8.8.8.8]
```

### 2. 配置多客户端访问

```bash
# /etc/exports 配置允许特定 IP 访问：
/home/yantao/nfs_rootfs 192.168.5.9(rw,sync,no_root_squash) 192.168.5.10(ro,sync)

# 或允许整个网段
/home/yantao/nfs_rootfs 192.168.5.0/24(rw,sync,no_root_squash)
```

### 3. 性能优化挂载选项

```bash
# 开发板（192.168.5.9）上优化挂载
mount -t nfs -o nolock,vers=3,rsize=32768,wsize=32768,timeo=15 192.168.5.11:/home/yantao/nfs_rootfs /mnt

# 参数说明：
# rsize/wsize：读写缓冲区大小（默认 4096，可增大）
# timeo：超时时间（默认 7，可适当增大）
```

### 4. 创建快捷脚本

```bash
# 在 Ubuntu 创建快捷脚本
cat > /usr/local/bin/nfs_status.sh << EOF
#!/bin/bash
echo "NFS 共享目录: /home/yantao/nfs_rootfs"
echo "当前共享状态:"
sudo exportfs -v | grep yantao
echo "目录权限:"
ls -ld /home/yantao/nfs_rootfs
EOF
sudo chmod +x /usr/local/bin/nfs_status.sh

# 在开发板创建挂载脚本
cat > /root/mount_nfs.sh << EOF
#!/bin/bash
MOUNT_POINT="/mnt"
NFS_SERVER="192.168.5.11"
NFS_PATH="/home/yantao/nfs_rootfs"

if mount | grep -q "\${MOUNT_POINT}"; then
    echo "NFS already mounted at \${MOUNT_POINT}"
else
    mount -t nfs -o nolock,vers=3 \${NFS_SERVER}:\${NFS_PATH} \${MOUNT_POINT}
    if [ \$? -eq 0 ]; then
        echo "NFS mounted successfully"
        ls \${MOUNT_POINT}
    else
        echo "NFS mount failed"
    fi
fi
EOF
chmod +x /root/mount_nfs.sh
```

---

## 九、实际操作示例

### 完整三机联动演示

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

# 4. 测试读取（只能读，不能写）
type Z:\ubuntu_test.txt
```

---

## 十、重要注意事项

### 1. 路径一致性

- 确保所有地方使用相同的路径：`/home/yantao/nfs_rootfs`
- 如果 Ubuntu 用户名不是 yantao，请相应修改所有路径

### 2. IP 地址规划

- **192.168.5.9**：开发板 IP（建议固定）
- **192.168.5.10**：Windows IP（可 DHCP 或固定）
- **192.168.5.11**：Ubuntu IP（建议固定）
- 确保三者在同一网段（192.168.5.0/24）

### 3. 权限和安全

- 开发环境：可使用 `no_root_squash` 方便调试
- 生产环境：建议更严格的权限控制
- 考虑使用防火墙限制访问来源

### 4. 开发效率技巧

1. 在 Windows（192.168.5.10）上编辑代码
2. 使用同步工具自动同步到 Ubuntu 的 `/home/yantao/nfs_rootfs`
3. 在 Ubuntu（192.168.5.11）上交叉编译
4. 开发板（192.168.5.9）通过 NFS 直接测试
5. 使用版本控制（Git）管理代码

### 5. 故障排查顺序

1. 检查物理连接（网线、交换机）
2. 验证 IP 地址配置（三机互 ping）
3. 检查 NFS 服务状态（Ubuntu 端）
4. 查看防火墙设置（Ubuntu 和 Windows）
5. 检查目录权限和 exports 配置
6. 确认路径 `/home/yantao/nfs_rootfs` 存在且有正确权限

### 6. 快速检查命令

```bash
# Ubuntu 端检查
ls -ld /home/yantao/nfs_rootfs
sudo exportfs -v | grep yantao
sudo service nfs-kernel-server status

# 开发板端检查
ping 192.168.5.11
mount | grep nfs
ls /mnt

# Windows 端检查
ping 192.168.5.11
```

通过合理配置 NFS 挂载，可以实现 Windows、Ubuntu、开发板三机协同工作，充分利用各设备的优势，极大提高嵌入式开发效率。
