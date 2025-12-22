# STM32MP157PRO 开发指南

## 将开发板连接到 PC

```{dropdown} 拨码开关（控制开发板的启动方式）
|      | EMMC     | SD           | USB      | M4       |
| ---- | -------- | ------------ | -------- | -------- |
| 1    | OFF      | **ON**       | OFF      | OFF      |
| 2    | **ON**   | OFF          | OFF      | OFF      |
| 3    | OFF      | **ON**       | OFF      | **ON**   |
| 备注 | 正常启动 | 从 SD 卡启动 | 烧写系统 | 调试模式 |
```

- 硬件版本：`100ASK_STM32MP157_V11`
- 开发板正面接线图：<https://pan.quark.cn/s/532f2b7cc07d>
- 开发板背面接线图：<https://pan.quark.cn/s/b78f6941857c>
- `J5 USB Serial`：串口（内核）日志，波特率 115200
- `J18 OTG`：烧录口（对应通用串行总线设备中的 DFU）
- `J10 NET1`：SSH 登录开发板（需要使用以太网转换器连接 PC）
- `J11 NET2`：使用网线直接连接到路由器上
- `J3 BOOT CFG`：拨码开关，正常使用选择 EMMC 模式

## 给开发板烧录版本

- 烧录工具：[STM32CubeProgrammer](https://pan.quark.cn/s/1a50bbd2fbac)（安装路径不能有中文）
- 下载固件：<https://pan.quark.cn/s/3619f69a933b>

更新整个系统的烧写方式：

- 关闭电源，将 `J18 OTG` 接到 PC 上，将拨码开关设置为从 USB 启动
- 打开电源
- 打开 STM32CubeProgrammer，选择 `USB` > 在 `USB configuration` 中点击刷新按钮，Port 选择 `USB1` > 选择 `connect`
- 解压下载好的固件：[Buildroot_2020.zip](https://pan.quark.cn/s/3619f69a933b)
- 选择分区配置文件：点击 `Open File`，选择 `Buildroot_2020/Flashlayout/Buildroot_Emmc_Systemall.tsv`
- `Binaries path` 选择 `uImage` 所在的目录，也就是 `Buildroot_2020/`
- 点击 `Dwonload` 开始烧写，烧写过程中不要中断电源
- 烧写成功，关闭电源，将启动方式设置为 EMMC，打开电源

单独更新 Trust Boot，步骤同上，在选择分区配置文件时，选择 `Buildroot_2020/Flashlayout/Buildroot_Emmc_TrustUbootBootloader.tsv`

## 配置网络

串口登录开发板：输入 root，没有密码。配置网络：

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

下载虚拟机：<https://pan.quark.cn/s/278d398939e4>（用户名：`root`，密码：`123456`）

双击 `ubuntu18.04_x64.vmx` 用 VMware Workstation Pro 打开虚拟机，配置虚拟机桥接网卡（用于和开发板互相通信）

```bash
虚拟机 - 设置 - 添加 - 网络适配器 - 桥接模式 - 复制物理网络连接状态
编辑 - 虚拟网络编辑器 - 更改设置 - 添加网络 - VMnet0 - 桥接模式选择 AXIC 网络适配器 - 应用 - 确定
```

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

配置电脑端 AXIC 网络适配器的 IPv4 和网关（用于和开发板和虚拟机通信）

```bash
更改 AXIC 网络适配器属性

IPv4    : 192.168.5.10
Netmask : 255.255.255.0
Gateway : 192.168.5.1

关闭 Windows 公用网络防火墙
```

```{admonition} 开发板上网
开发板接上网线后执行 `udhcpc -i eth1`。
```

## 下载代码编辑器

- 下载 [STM32CubeMX](https://pan.quark.cn/s/b1be5a3d9b68)（设置硬件引脚，生成 HAL 层代码）
- 下载 [STM32CubeIDE](https://pan.quark.cn/s/8b8cb53b823e)（编写业务代码）

## 下载源代码

```bash
export PROJECT_DIR=~/workshop/stm32mp-ya15xc
mkdir -p $PROJECT_DIR && cd $PROJECT_DIR
repo init -u git@gitee.com:zhyantao/manifest.git -b stm32mp-ya15xc -m STM32MP157_V11.xml
repo sync -j8
```

## 从源码生成交叉编译工具链

```bash
# 安装必要的编译工具链和依赖包
sudo apt install -y build-essential make unzip mtools

# 删除系统默认的 python 符号链接（通常是 python3）
sudo rm /usr/bin/python
sudo ln -s /usr/bin/python2 /usr/bin/python

# 加载特定开发板的配置文件
cd $PROJECT_DIR/Buildroot_2020.02.x
make 100ask_stm32mp157_pro_ddr512m_systemD_qt5_defconfig

# 开始完整编译，使用 4 个并行任务加速编译过程
make all -j4

# 生成 SDK 工具链，用于后续应用程序开发
# 该工具链将包含交叉编译器、库文件等
make sdk
```

````{dropdown} tree $PROJECT_DIR/output/images/
```
output/images/
├── rootfs.ext2                 # 根文件系统镜像（ext2 格式）
├── rootfs.ext4 -> rootfs.ext2  # ext4 格式的符号链接（实际仍为 ext2）
├── sdcard.img                  # 完整的 SD 卡镜像，可直接烧录
├── stm32mp157c-dk2.dtb         # 设备树二进制文件，描述硬件配置
├── tf-a-stm32mp157c-dk2.stm32  # TF-A 固件（ARM Trusted Firmware）
├── u-boot.stm32                # U-Boot 引导加载程序镜像
└── zImage                      # 压缩的内核镜像
```
````

````{dropdown} tree $PROJECT_DIR/output/host/bin/
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
export PATH=$PATH:$PROJECT_DIR/Buildroot_2020.02.x/output/host/usr/bin
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
cp stm32wrapper4dbg $PROJECT_DIR/Buildroot_2020.02.x/output/host/usr/bin/
cd $PROJECT_DIR/Tfa-v2.2
make -f Makefile.sdk all
mkdir -p $PROJECT_DIR/output/tfa
cp $PROJECT_DIR/build/serialboot/tf-a-stm32mp157c-100ask-512d-v1.stm32 $PROJECT_DIR/output/tfa/
```

````{dropdown} tree $PROJECT_DIR/output/
```
output/
├── boot/          # 内核镜像和设备树
├── rootfs/        # 内核模块
├── drivers/       # 驱动模块和测试程序
├── tfa/           # TF-A 镜像
└── uboot/         # U-Boot 镜像
```
````
