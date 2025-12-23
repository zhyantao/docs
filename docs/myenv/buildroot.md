# STM32MP157 开发指南：从烧录系统到构建编译环境

## 将开发板连接到 PC

- **硬件版本**：`100ASK_STM32MP157_V11`
- **开发板正面接线图**：<https://pan.quark.cn/s/532f2b7cc07d>
- **开发板背面接线图**：<https://pan.quark.cn/s/b78f6941857c>
- `J5 USB Serial`：串口（用于查看内核日志），波特率为 115200
- `J18 OTG`：烧录口（对应通用串行总线设备中的 DFU 模式）
- `J10 NET1`：用于 SSH 登录开发板（需使用以太网转换器连接至 PC）
- `J11 NET2`：可直接通过网线连接到路由器
- `J3 BOOT CFG`：拨码开关，正常使用时请选择 EMMC 模式

**拨码开关（控制开发板的启动方式）：**

|      | EMMC     | SD           | USB      | M4       |
| ---- | -------- | ------------ | -------- | -------- |
| 1    | OFF      | **ON**       | OFF      | OFF      |
| 2    | **ON**   | OFF          | OFF      | OFF      |
| 3    | OFF      | **ON**       | OFF      | **ON**   |
| 备注 | 正常启动 | 从 SD 卡启动 | 烧写系统 | 调试模式 |

## 烧录系统

- **烧录工具**：[STM32CubeProgrammer](https://pan.quark.cn/s/1a50bbd2fbac)（安装路径请勿包含中文）
- **系统固件**：[Buildroot_2020.zip](https://pan.quark.cn/s/3619f69a933b)

**更新整个系统的烧录步骤：**

1. 关闭电源，将 `J18 OTG` 连接到 PC，并将拨码开关设置为 USB 启动模式。
2. 打开电源。
3. 启动 STM32CubeProgrammer，选择 `USB` → 在 `USB configuration` 中点击刷新按钮，选择 `USB1` 端口 → 点击 `connect`。
4. 解压下载的固件：Buildroot_2020.zip。
5. 选择分区配置文件：点击 `Open File`，选择 `Buildroot_2020/Flashlayout/Buildroot_Emmc_Systemall.tsv`。
6. 在 `Binaries path` 中选择 `uImage` 所在的目录，即 `Buildroot_2020/`。
7. 点击 `Download` 开始烧写，烧写过程中请勿断开电源。
8. 烧写完成后，关闭电源，将启动方式重新设置为 EMMC，然后打开电源。

**单独更新 Trust Boot 的步骤与上述相同，仅在步骤 5 中选择分区配置文件时，改为选择 `Buildroot_2020/Flashlayout/Buildroot_Emmc_TrustUbootBootloader.tsv`。**

## 配置网络

通过串口登录开发板：用户名为 `root`，无密码。登录后配置网络：

```bash
cat <<EOF | tee /etc/systemd/network/50-static.network
[Match]
Name=eth0
[Network]
Address=192.168.5.9/24
Gateway=192.168.5.1
EOF

systemctl enable systemd-networkd
```

**虚拟机下载与配置：**

- 下载链接：<https://pan.quark.cn/s/278d398939e4>（用户名：`root`，密码：`123456`）。
- 使用 VMware Workstation Pro 打开 `ubuntu18.04_x64.vmx` 文件。

**配置虚拟机桥接网卡（用于与开发板通信）：**

```bash
虚拟机 - 设置 - 添加 - 网络适配器 - 桥接模式 - 复制物理网络连接状态
编辑 - 虚拟网络编辑器 - 更改设置 - 添加网络 - VMnet0 - 桥接模式选择 AXIC 网络适配器 - 应用 - 确定
```

**在虚拟机内配置网络：**

```bash
cat <<EOF | sudo tee /etc/netplan/99_config.yaml
network:
  version: 2
  renderer: networkd
  ethernets:
    ens33:
      dhcp4: true
      optional: true
    ens36:
      addresses:
        - 192.168.5.11/24
      routes:
        - to: 192.168.0.0/24
          via: 192.168.5.1
          metric: 100
EOF

sudo netplan apply
```

**配置 PC 端 AXIC 网络适配器（用于与开发板和虚拟机通信）：**

```bash
更改 AXIC 网络适配器属性

IPv4     : 192.168.5.10
子网掩码 : 255.255.255.0
网关     : 192.168.5.1

关闭 Windows 公用网络防火墙
```

```{admonition} 开发板上网
开发板接上网线后，可执行 `udhcpc -i eth1` 命令自动获取网络配置。
```

## 下载代码开发工具

- **STM32CubeMX**：[下载链接](https://pan.quark.cn/s/b1be5a3d9b68)（用于配置硬件引脚并生成 HAL 层代码）。
- **STM32CubeIDE**：[下载链接](https://pan.quark.cn/s/8b8cb53b823e)（用于编写业务层代码）。

## 下载源代码

```bash
export PROJECT_DIR=~/workshop/stm32mp-ya15xc
mkdir -p $PROJECT_DIR && cd $PROJECT_DIR
repo init -u git@gitee.com:zhyantao/manifest.git -b stm32mp-ya15xc -m STM32MP157_V11.xml
repo sync -j8
```

````{note}
如果网络连接速度较慢，可以下载已预先打包好的 Buildroot dl 目录源代码文件：<https://pan.quark.cn/s/7a874af81acb>

下载完成后，请使用以下命令解压至指定目录：

```bash
tar zxf Buildroot_2020.02.x_dl.tar.gz --directory=$PROJECT_DIR/Buildroot_2020.02.x
```
````

## 从源码生成交叉编译工具链

```bash
# 安装必要的编译工具和依赖包
sudo apt install -y build-essential make unzip mtools

# 删除系统默认的 python 符号链接（通常是 python3）
sudo rm /usr/bin/python
sudo ln -s /usr/bin/python2 /usr/bin/python

# 加载特定开发板的配置文件
cd $PROJECT_DIR/Buildroot_2020.02.x
make 100ask_stm32mp157_pro_ddr512m_systemD_qt5_defconfig

# 开始完整编译，使用 4 个并行任务加速编译过程
make all -j4

# 生成 SDK 工具链，用于后续的应用程序开发
# 该工具链包含交叉编译器、库文件等
make sdk

# 将构建后的 SDK 交叉编译工具链及所有的镜像文件复制到 output 目录
mkdir -p $PROJECT_DIR/output
cp -r output/host $PROJECT_DIR/output/
cp -r output/images $PROJECT_DIR/output/
```

````{admonition} tree $PROJECT_DIR/output/images/
```
output/images/
├── rootfs.ext2                 # 根文件系统镜像（ext2 格式）
├── rootfs.ext4 -> rootfs.ext2  # ext4 格式的符号链接（实际仍为 ext2）
├── sdcard.img                  # 完整的 SD 卡镜像，可直接烧录
├── stm32mp157c-dk2.dtb         # 设备树二进制文件，描述硬件配置
├── tf-a-stm32mp157c-dk2.stm32  # TF-A 固件（ARM Trusted Firmware）
├── u-boot.stm32                # U-Boot 引导加载程序镜像
└── uImage                      # 压缩的内核镜像
```
````

````{admonition} tree $PROJECT_DIR/output/host/bin/
```
output/host/bin/
# 该目录存放生成的交叉编译工具链（如 arm-linux-gcc 等）
# 在执行 `make sdk` 后，此目录会被打包到 SDK 中
# 可用于开发针对该嵌入式平台的应用程序
```
````

## 配置交叉编译环境

```bash
export ARCH=arm
export CROSS_COMPILE=arm-buildroot-linux-gnueabihf-
export PATH=$PATH:$PROJECT_DIR/output/host/usr/bin
${CROSS_COMPILE}gcc --version
```

## 系统组件编译方法

```bash
# 编译 U-Boot，配置为 STM32MP15 平台，生成 u-boot.stm32 镜像
cd $PROJECT_DIR/Uboot-2020.02
make stm32mp15_trusted_defconfig
make DEVICE_TREE=stm32mp157c-100ask-512d-v1 all -j4
mkdir -p $PROJECT_DIR/output/uboot
cp u-boot.stm32 $PROJECT_DIR/output/uboot/

# 编译 Linux 内核、设备树，生成 uImage 内核镜像和 dtb 设备树文件
cd $PROJECT_DIR/Linux-5.4/
make 100ask_stm32mp157_pro_defconfig
make uImage LOADADDR=0xC2000040
make dtbs
mkdir -p $PROJECT_DIR/output/boot
cp arch/arm/boot/uImage $PROJECT_DIR/output/boot/
cp arch/arm/boot/dts/stm32mp157c*.dtb $PROJECT_DIR/output/boot/

# 编译内核模块并安装到根文件系统目录，用于构建根文件系统
mkdir -p $PROJECT_DIR/output/rootfs
make modules -j8
make INSTALL_MOD_PATH=$PROJECT_DIR/output/rootfs INSTALL_MOD_STRIP=1 modules_install

# 编译 Trusted Firmware-A 安全启动固件
cd $PROJECT_DIR/stm32wrapper4dbg && make
cp stm32wrapper4dbg $PROJECT_DIR/output/host/usr/bin/
cd $PROJECT_DIR/Tfa-v2.2
make -f Makefile.sdk all
mkdir -p $PROJECT_DIR/output/tfa
cp output/serialboot/tf-a-stm32mp157c-100ask-512d-v1-serialboot.stm32 $PROJECT_DIR/output/tfa/
```

````{admonition} tree $PROJECT_DIR/output/
```
output/
├── host/          # 交叉编译工具链
├── images/        # 所有构建镜像文件
├── boot/          # 内核镜像和设备树
├── rootfs/        # 内核模块
├── tfa/           # RAM TF-A 镜像
└── uboot/         # RAM U-Boot 镜像
```
````

## 发布版本

```bash
# 设置发布目录路径
RELEASE_DIR=$PROJECT_DIR/output/release
SERIALBOOT_DIR=$PROJECT_DIR/output/release/Ram      # 串口下载工具目录
LAYOUT_DIR=$PROJECT_DIR/output/release/Flashlayout  # Flash 布局文件目录

# 清理并创建发布目录结构
rm -rf $RELEASE_DIR
mkdir -p $RELEASE_DIR
mkdir -p $SERIALBOOT_DIR
mkdir -p $LAYOUT_DIR

# 1. 串口启动文件（用于调试/烧录）
cp $PROJECT_DIR/output/tfa/tf-a-stm32mp157c-100ask-512d-v1-serialboot.stm32 $SERIALBOOT_DIR
cp $PROJECT_DIR/output/uboot/u-boot.stm32 $SERIALBOOT_DIR

# 2. TF-A 固件（FSBL - First Stage Boot Loader）
cp $PROJECT_DIR/output/images/tf-a-stm32mp157c-100ask-512d-v1.stm32 $RELEASE_DIR/

# 3. U-Boot 引导程序
cp $PROJECT_DIR/output/images/u-boot.stm32 $RELEASE_DIR/

# 4. Linux 内核与设备树
cp $PROJECT_DIR/output/images/uImage $RELEASE_DIR/
cp $PROJECT_DIR/output/boot/stm32mp157c-100ask-512d-v1.dtb $RELEASE_DIR/
cp $PROJECT_DIR/output/boot/stm32mp157c-100ask-512d-hdmi-v1.dtb $RELEASE_DIR/
cp $PROJECT_DIR/output/boot/stm32mp157c-100ask-512d-lcd-v1.dtb $RELEASE_DIR/

# 5. 文件系统镜像
cp $PROJECT_DIR/output/images/bootfs.ext4 $RELEASE_DIR/      # 引导分区文件系统
cp $PROJECT_DIR/output/images/rootfs.ext4 $RELEASE_DIR/      # 根文件系统

# 6. Flash布局配置文件
cp $PROJECT_DIR/Flashlayout/*.tsv $LAYOUT_DIR/
```
