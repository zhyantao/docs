# TSV 文件详解与应用指南

## 一、TSV 文件基础

### 1.1 文件性质

- **文件类型**：STM32CubeProgrammer 烧录脚本文件
- **扩展名**：`.tsv`
- **编写方式**：手动编写（通常基于模板修改）
- **分隔符**：必须使用**制表符（TAB）**，不能使用空格
- **注释**：以 `#` 开头的行被视为注释

### 1.2 文件位置

- 示例通常放在烧录工具包的 `flashlayout` 文件夹下
- 根据存储介质不同，通常包含 `sd` 卡和 `emmc` 两种版本

## 二、TSV 文件结构解析

### 2.1 基本格式（7 列）

```tsv
#Opt    Id      Name        Type        IP      Offset      Binary
-       0x01    fsbl1-boot  Binary      none    0x0         Ram/tf-a-stm32mp157c-100ask-512d-v1-serialboot.stm32
-       0x03    ssbl-boot   Binary      none    0x0         Ram/u-boot.stm32
P       0x04    fsbl1       Binary      mmc1    boot1       tf-a-stm32mp157c-100ask-512d-v1.stm32
P       0x05    fsbl2       Binary      mmc1    boot2       tf-a-stm32mp157c-100ask-512d-v1.stm32
PD      0x06    ssbl        Binary      mmc1    0x00080000  u-boot.stm32
P       0x21    rootfs1     System      mmc1    0x00280000  bootfs.ext4
P       0x22    rootfs2     FileSystem  mmc1    0x08280000  rootfs.ext4
```

### 2.2 各列含义

| 列名       | 含义     | 说明                                                                |
| ---------- | -------- | ------------------------------------------------------------------- |
| **Opt**    | 操作选项 | `-`：加载到 RAM；`P`：编程到 Flash；`PD`：编程后删除；`D`：删除分区 |
| **Id**     | 标识符   | 十六进制编号，决定烧录顺序和方式                                    |
| **Name**   | 分区名称 | 分区标识名                                                          |
| **Type**   | 数据类型 | Binary：二进制文件；System：系统分区；FileSystem：文件系统          |
| **IP**     | 存储设备 | none：RAM；mmc1：eMMC/SD 卡；nor：NOR Flash                         |
| **Offset** | 偏移地址 | 在存储设备中的起始位置（十六进制或特殊标识）                        |
| **Binary** | 文件名   | 要烧录的文件路径（支持相对/绝对路径）                               |

### 2.3 关键 ID 说明

| ID   | 用途       | 说明                               |
| ---- | ---------- | ---------------------------------- |
| 0x01 | fsbl1-boot | TF-A 串行启动加载器（加载到 RAM）  |
| 0x03 | ssbl-boot  | U-Boot 串行启动（加载到 RAM）      |
| 0x04 | fsbl1      | TF-A 主分区（烧写到 eMMC boot1）   |
| 0x05 | fsbl2      | TF-A 备份分区（烧写到 eMMC boot2） |
| 0x06 | ssbl       | U-Boot 持久化分区                  |
| 0x21 | rootfs1    | 引导文件系统分区                   |
| 0x22 | rootfs2    | 根文件系统分区                     |

## 三、文件编写方法

### 3.1 编写步骤

1. **复制模板**：从已有 TSV 文件复制
2. **修改路径**：调整 Binary 列的相对/绝对路径
3. **配置分区**：根据硬件选择 mmc1（eMMC/SD）或其他存储介质
4. **设置 Offset**：按分区规划设置偏移地址（支持 boot1/boot2 标识符）
5. **保存文件**：使用制表符分隔，UTF-8 编码

### 3.2 注意事项

- **必须使用制表符**：空格会导致 STM32CubeProgrammer 报错
- **第一行注释**：建议保留说明行，便于维护
- **文件顺序**：按烧录顺序排列，先烧 TF-A，再烧 U-Boot，最后烧文件系统
- **特殊 Offset**：`boot1` 和 `boot2` 是 eMMC 的特殊分区标识符

### 3.3 示例配置详解

```tsv
# 第一行：串行启动加载器到 RAM
-       0x01    fsbl1-boot  Binary      none    0x0         Ram/tf-a-serialboot.stm32

# 第二行：U-Boot 串行启动到 RAM
-       0x03    ssbl-boot   Binary      none    0x0         Ram/u-boot.stm32

# 第三行：TF-A 主分区烧写到 eMMC boot1
P       0x04    fsbl1       Binary      mmc1    boot1       tf-a.stm32

# 第四行：TF-A 备份分区烧写到 eMMC boot2
P       0x05    fsbl2       Binary      mmc1    boot2       tf-a.stm32

# 第五行：U-Boot 持久化分区（编程后删除缓存）
PD      0x06    ssbl        Binary      mmc1    0x00080000  u-boot.stm32

# 第六行：引导文件系统分区
P       0x21    rootfs1     System      mmc1    0x00280000  bootfs.ext4

# 第七行：根文件系统分区
P       0x22    rootfs2     FileSystem  mmc1    0x08280000  rootfs.ext4
```

## 四、烧录文件详解

### 4.1 必须烧录的文件

| 文件                      | 作用            | 烧录位置                    |
| ------------------------- | --------------- | --------------------------- |
| **tf-a-serialboot.stm32** | 串行启动 TF-A   | 加载到 RAM（临时）          |
| **u-boot.stm32**          | 串行启动 U-Boot | 加载到 RAM（临时）          |
| **tf-a.stm32**            | 安全启动固件    | eMMC boot1/boot2 分区       |
| **u-boot.stm32**          | 引导加载程序    | eMMC user area (0x00080000) |
| **bootfs.ext4**           | 引导文件系统    | eMMC (0x00280000)           |
| **rootfs.ext4**           | 根文件系统      | eMMC (0x08280000)           |

### 4.2 串行启动与持久化启动的区别

| 版本                           | 用途            | 说明                                   |
| ------------------------------ | --------------- | -------------------------------------- |
| **tf-a-serialboot.stm32**      | 串行启动 TF-A   | 通过 USB/UART 加载到 RAM，用于初始烧录 |
| **u-boot.stm32（ID 0x03）**    | 串行启动 U-Boot | 加载到 RAM，协助烧录过程               |
| **tf-a.stm32（ID 0x04/0x05）** | 持久化 TF-A     | 烧写到 eMMC boot 分区，用于正常启动    |
| **u-boot.stm32（ID 0x06）**    | 持久化 U-Boot   | 烧写到 eMMC user area，用于正常启动    |

### 4.3 Offset 设置规则

| 分区          | Offset 值  | 说明                             |
| ------------- | ---------- | -------------------------------- |
| TF-A（boot1） | boot1      | eMMC boot area 主分区            |
| TF-A（boot2） | boot2      | eMMC boot area 备份分区          |
| U-Boot        | 0x00080000 | user area 标准位置（512KB 偏移） |
| bootfs        | 0x00280000 | 引导文件系统（2.5MB 偏移）       |
| rootfs        | 0x08280000 | 根文件系统（130.5MB 偏移）       |

## 五、操作选项详解

### 5.1 Opt 字段类型

| 选项   | 含义         | 使用场景                     |
| ------ | ------------ | ---------------------------- |
| **-**  | 加载到 RAM   | 临时运行程序，不写入持久存储 |
| **P**  | 编程到 Flash | 将文件写入持久存储设备       |
| **PD** | 编程后删除   | 写入后删除缓存文件，节省空间 |
| **D**  | 删除分区     | 清空指定分区内容             |

### 5.2 Type 字段类型

| 类型           | 含义       | 适用文件                   |
| -------------- | ---------- | -------------------------- |
| **Binary**     | 二进制文件 | .stm32、.bin 等可执行文件  |
| **System**     | 系统分区   | 包含引导相关文件的文件系统 |
| **FileSystem** | 文件系统   | 完整的 Linux 根文件系统    |

## 六、开发板适配

### 6.1 典型开发板配置

- **基础方案**：基于 ST 官方 OpenSTLinux BSP 修改
- **存储方案**：支持 eMMC boot 分区双备份
- **文件系统**：分离的 bootfs 和 rootfs 设计
- **可靠性**：支持 A/B 系统切换，防变砖

### 6.2 烧录准备

1. 准备串行启动文件（放置在 Ram/ 目录下）
2. 准备持久化固件文件（主烧录文件）
3. 准备文件系统镜像（.ext4 格式）
4. 连接 USB 线到开发板
5. 提供外部供电（12V DC 或 USB）
6. 启动 STM32CubeProgrammer 软件
7. 选择 TSV 文件开始烧录

## 七、总结

| 问题                     | 回答                                         |
| ------------------------ | -------------------------------------------- |
| **TSV 文件生成方式**     | 半自动/手写，基于模板修改                    |
| **制表符 vs 空格**       | 必须使用制表符，空格会报错                   |
| **串行启动的作用**       | 通过 USB/UART 临时加载引导程序，用于初始烧录 |
| **boot1/boot2 意义**     | eMMC 的特殊 boot 分区，用于存放 TF-A         |
| **PD 选项的作用**        | 编程后删除缓存文件，适用于大文件烧录         |
| **Offset 0x00080000**    | U-Boot 在 eMMC user area 的标准存放位置      |
| **分离的 bootfs/rootfs** | bootfs 包含内核和设备树，rootfs 包含系统应用 |

**编写建议**：

1. 始终从可靠模板开始，逐步修改配置
2. 使用文本编辑器显示制表符功能确保格式正确
3. 注意文件路径的正确性，特别是相对路径的使用
4. 按照烧录顺序排列：串行启动 → TF-A → U-Boot → 文件系统
5. 合理规划分区大小和偏移地址，避免重叠
