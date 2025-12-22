# Buildroot

```{note}
Buildroot 学习资料请参考：<https://bootlin.com/doc/training/buildroot/buildroot-slides.pdf>
```

Buildroot 可用于：

- 配置和编译内核
- 配置和编译 uboot
- 创建根文件系统

## 使用方法

1、下载并解压源代码：

```bash
curl https://buildroot.org/downloads/buildroot-2020.02.9.tar.gz
tar xf buildroot-2020.02.9.tar.gz
```

2、编写配置文件，将其拷贝到 buildroot 根目录下：

```bash
cp -r custom/* buildroot-2020.02.9
```

3、升成编译所需的配置文件：

```bash
cd buildroot-2020.02.9 && make 100ask_stm32mp157_pro_ddr512m_systemD_qt5_defconfig
```

4、编译和生成 kernel、u-boot、fs 等：

```bash
make all -j4
```

## 常用命令

```bash
# buildroot 下进入 menuconfig 包选择配置配置界面
make menuconfig

# buildroot 下单独编译内核
make linux-rebuild

# buildroot 下进入内核 make menuconfig 配置选项界面
make linux-menuconfig

# buildroot 下单独编译 u-boot
make uboot-rebuild

# buildroot 下单独编译某个软件包
make <pkg>-rebuild

# buildroot 下进入 busybox 配置界面
make busybox-menuconfig

# buildroot 下生成系统 sdk，最后生成的目录在 output/images/ 目录下
make sdk
```
