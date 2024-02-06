# GPSD 源码分析

首先，从每个模块所能提供的功能入手（参考官方文档）：

[GPSd — Put your GPS on the net!](https://gpsd.io/index.html#documentation)

## GPS 的工作原理

GPS 的应用前提：需要对卫星轨道进行精确建模。

由于地球时刻在自转，那么我们应该找到一个固定不变的坐标系，这样就可以计算当前物体在坐标系中的位置了。而这个固定不变的坐标系是由卫星组成的。卫星跟随地球自转，保持速度一致，那么就可以获得一个固定不变的坐标系了。

由于我们不能保证卫星和地球自转的速度完全一致，那么我们在进行定位时，就要对计算结果进行校正，这种技术叫做补偿，也可以叫做差分。

而且，当你正在运动时，GPS 的定位精度也会略有下降，这主要是因为 GPS 计算位置总是需要一些时间，当 GPS 计算出来了你在哪里时，实际上你已经不在原来的位置了。

对于计算结果，GPS 应该主要关注四个方面：**经度、纬度、海拔、时间**。

现在 GPS 能够提供的经纬度与实际差异大概在 10 米左右，如果使用 DGPS，可以将误差降低到 2 米左右。而海拔的计算精度会低很多，大概会有 50 米左右的误差。

一个位置可以由 7 个自由度的向量组成： $(T, X, Y, Z, vx, vy, vz)$ 以及误差估计值。这里 $T$ 表示时间， $X, Y, Z$ 表示三维坐标， $vx, vy, vz$ 表示在三维坐标中的速度。

## 数据传输格式：NMEA

**NMEA** stands for **N**ational **M**arine **E**lectronics **A**ssociation.（美国国家海洋电子协会）

[NMEA Revealed (gpsd.io)](https://gpsd.io/NMEA.html)

这个数据传输格式可以在用到的时候去查，但是如果直接读，可能会感觉很乏味。

推荐运行下面的例子，并观察输出 30s 左右，来尝试理解 GPSD 做了什么：

```bash
/usr/sbin/gpsd -N -n -D 2 /dev/ttyS3
```

几乎所有的 GPS 都通过 RS232 串口和计算机通信，但是将来的趋势是用 USB 代替串口通信。

除了 gpsd，另外也有一些可以用来解析 NMEA 的小工具：

- [kosma/minmea: a lightweight GPS NMEA 0183 parser library in pure C (github.com)](https://github.com/kosma/minmea)
- [mikalhart/TinyGPSPlus: A new, customizable Arduino NMEA parsing library (github.com)](https://github.com/mikalhart/TinyGPSPlus)

常见的 NMEA 语句及解释：
[An architect's guide to GPS and GPS data formats | Enable Architect (redhat.com)](https://www.redhat.com/architect/architects-guide-gps-and-gps-data-formats)

## 理解 GPSD 的工作原理

如果你想修改源代码，请务必阅读下面这些文章（虽然它有些过时了，但是仍然很有用）：

- [A Tour of the GPSD Internals](https://gpsd.io/internals.html)（解释 GPSD 核心功能函数的作用）
- [gpsd Client Example Code](https://gpsd.io/gpsd-client-example-code.html)（如何使用 GPSD 的接口函数）
- [aosabook.org](https://aosabook.org/en/gpsd.html)（由于公司网络原因，无法访问）

satellite constellation 应该翻译成卫星星群更准确一些，constellation 有星座的意思。
