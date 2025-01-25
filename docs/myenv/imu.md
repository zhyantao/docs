# 使用 IMU 校正定位偏移

现有一块开发板，新焊接了一个 IMU 器件（ASM330LHH），如何利用这个器件来校正 GNSS 的定位？

为了解决这个问题，有两个子问题需要优先解决：

1. GNSS 芯片如何与 IMU 器件进行数据交互？
2. GNSS 芯片如何利用从 IMU 器件获取到的值纠正定位？

对于第一个问题，已知背景信息，IMU 器件通过两路 I2C 线和 GNSS 芯片相连，因此，通信方式为 I2C。

由于这是一个新添加的器件，Linux 内核并不能识别到这个器件，因此对于新添加的设备，必须先在设备树文件上注册一个地址。这个地址指向了 IMU 器件，之后的数据通信通过 I2C 总线接口来读取 IMU 器件的值。

要确定 I2C 控制器所在的总线以及连接到该控制器的设备地址，可以通过以下步骤进行：

首先，我们需要查看设备树文件来获取 I2C 控制器的相关信息。

- 查看 `/sys/class/i2c-adapter` 目录下的信息。这个目录包含了系统中所有可用的 I2C 适配器的信息。
- 对于每个适配器，例如 `i2c-0`，你可以查看它的详细信息，包括它的类型和设备树路径。

  ```sh
  cat /sys/class/i2c-adapter/i2c-0/new_device
  ```

  这个文件会显示适配器的类型和设备树路径。例如：

  ```
  i2c-adapter i2c@e0023000 0 10
  ```

- 每个适配器目录下有一个 `i2c-dev` 子目录，里面包含了该适配器连接的所有设备。

  ```sh
  ls /sys/class/i2c-adapter/i2c-0/i2c-dev/
  ```

- 每个设备都有一个以 `i2c-` 开头的文件夹，后面跟着适配器编号和设备地址。例如：

  ```sh
  ls /sys/class/i2c-adapter/i2c-0/i2c-dev/i2c-0/
  ```

  在这个目录下，你可以看到类似 `i2c-0-0012` 和 `i2c-0-0018` 的文件夹，这些表示该适配器上的设备地址。

首先，检查在 Linux 系统中已有的设备树文件：

```bash
ls /proc/device-tree
```

查看某个 I2C 设备的属性，检查设备文件中的内容：

```bash
readlink -f /proc/device-tree/aliases/i2c0
cat /proc/device-tree/aliases/i2c0
# /soc/i2c@E0023000
```

在设备树中，路径 `/soc/i2c@e0023000` 表示一个 I2C 控制器节点，该控制器位于 SoC（System on Chip，系统级芯片）内部，并且其基地址为 `0xe0023000`。

让我们分解一下这个路径：

- `/soc/`：表示这是系统级芯片（SoC）的根节点。SoC 节点通常包含所有其他硬件组件，如 CPU、内存控制器、外设等。
- `i2c@e0023000`：表示这是一个 I2C 控制器节点，其物理基地址为 `0xe0023000`。

I2C 是一种用于连接低速器件的两线式串行通信协议，常用于连接传感器、EEPROM、A/D 和 D/A 转换器等。在设备树中，每个 I2C 控制器都有一个唯一的地址，该地址对应于控制器的物理内存映射地址。

这个节点通常包含了 I2C 控制器的具体配置信息，比如它的时钟频率、中断配置等。此外，该节点还可能包含其连接的设备列表，每个设备也会有自己的子节点。

例如，如果你想要查看这个 I2C 控制器所连接的设备，你可以检查 `/soc/i2c@e0023000` 下的子节点，它们通常以 `i2c@<address>` 的形式出现，其中 `<address>` 是 I2C 设备在其总线上的地址。

要查看这个节点的具体信息，需要找到 `.dts` 文件并查看。在 Linux 中，设备树的定义文件路径如下：

```bash
linux-5.4/arch/arm64/boot/dts/zte/zx298501/zx298501.dtsi
```

在 `.dts` 文件中，查找与 I2C 控制器相关的节点。例如，在 `/soc/i2c@e0023000` 节点下，你应该能看到类似这样的条目：

```dts
i2c@e0023000 {
    #address-cells = <1>;
    #size-cells = <0>;
    compatible = "some-vendor,some-i2c-controller";
    reg = <0xe0023000 0x1000>;
    interrupts = <IRQ_NUMBER>;
    interrupt-parent = <&intc>;
    ...
    i2c@12 { /* This is the I2C slave address of a connected device */ };
    i2c@18 { /* Another I2C slave address */ };
    ...
};
```

在这个例子中，`i2c@12` 和 `i2c@18` 分别表示连接到 I2C 控制器的两个设备的 I2C 地址。
