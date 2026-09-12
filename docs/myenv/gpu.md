(training-with-gpu)=

# GPU

## CPU 与 GPU 的区别

英特尔（Intel）、超微半导体（AMD）、英伟达（NVIDIA）都是既生产 CPU 也生产 GPU。
不过，这三家公司也有些区别，比如 Intel 和 AMD 主要做 CPU，而 NVIDIA 主要做 GPU。

当然，还有一个体量不是那么大的公司就是 ARM，这家公司也是主要做 CPU。
Intel 和 AMD 做的 CPU 主要是 x86 架构，ARM 做的 CPU 则是 ARM 架构。
x86 架构普遍用在了个人电脑，服务器等高端设备上，而 ARM 架构更多地部署在性能不那么高的单片机等硬件上。
为了满足通用性，x86 架构的处理器通常都采用 CISC 指令集；
为了满足更加丰富的定制性，ARM 架构通常采用 RISC 指令集。

```{note}
i386 是指 32 位版本，而 AMD64 (或 x86_64) 是指 Intel 和 AMD 处理器的 64 位版本 [^cpu-arch]。
```

GPU 和 CPU 本质上属于同类型的产品，只不过侧重点不一样，CPU 偏向控制，GPU 偏向计算。

注意，为笔记本电脑上显示器提供输出的 GPU 不算是本文提及的 GPU。

我们通常说的显卡不等于 GPU，它是一块集成板卡。显卡由 GPU、显存、电路板、BIOS 固件组成。
GPU 是显卡的核心，它是显卡上的一块芯片，因此我们很多时候提到显卡，关注的重点往往是 GPU。

通常说到处理器，指的一般是 Intel 和 AMD 生产的 CPU（中央处理器），CPU 是主板上的一块芯片。
但是，容易被大家忽略的是 GPU 也是处理器，它是图形处理器。
关于 CPU 和 GPU 的区别，可以阅读
[这篇文章](https://www.intel.cn/content/www/cn/zh/products/docs/processors/cpu-vs-gpu.html)。
总结一句话，仅有 GPU 无法完成工作，需要 CPU 的支持，而 CPU 更适合串行任务，GPU 则更适合并行任务。

打开任务管理器后，我们或许会看到这样一张图：

```{figure} ../_static/images/gpu_info.png
```

图中的共享 GPU 内存，是集成显卡的一部分。集成或共享显卡内置在 CPU 所处的同一个芯片上。
与依赖于专用或独立显卡的 CPU 相比，某些 CPU 可以配备内置式 GPU。
集成显卡有时也被称为集成显卡处理器（IGP），与 CPU 共享内存。
集显专用内存是 BIOS 从系统内存（RAM）划分出来的，因此，共享显存容量可以通过 BIOS 来设置。
如果将 RAM 的一些存储容量分配给某张显卡时，其他显卡和电脑零件（比如 BIOS 固件）就不能使用了。

独显专用内存是独显自带的内存。

共享 GPU 内存的速度会远低于专用 GPU 内存的速度。
深度学习算法通常需要用到更大更广泛的加速效果，因此，GPU 是一个更好的选择。
NVIDIA 的 Titan 系列、Intel 的 Xeon 系列，都可以通过官方软件包为算法落地提供便利。

对于深度学习来讲，到底需要一台什么配置的电脑呢？
根据我的目前的实验来看，深度学习不建议用个人电脑，服务器往往能提供更大的平台，让算法得以实现。

比如，我在笔记本电脑上首先安装了 PaddlePaddle，如下图所示。

```{figure} ../_static/images/gpu_paddle_install.png
```

然后用 PaddlePaddle 跑了 YOLO 模型，发现 batch_size 设置的稍微大一点就会发生程序内存溢出，不得改小这个值。
因此，如果非要在个人电脑上运行深度学习程序，那么不免在算法准确性和程序运行时间上做出一些妥协，因为根本跑不动。

## 安装 CUDA 环境

用 GPU 训练网络肯定会用到 CUDA，但是，安装 CUDA 环境经常会出现一些问题，我们最好先用 `nvidia-smi`
看一下电脑上的 Driver API Version，然后去官网下载一个**相同版本**的
[CUDA Toolkit](https://developer.nvidia.com/cuda-toolkit-archive) 以及与 CUDA 版本相对应的
[cuDNN](https://developer.nvidia.com/rdp/cudnn-archive)。

如果你已经安装了 Anaconda 或 Miniconda，那么使用 `conda install cudatoolkit` 和
`conda install cudnn` 可以更加方便快捷地完成环境部署。当然，你也可以先从官网下载安装器，然后按照下面
UI 界面的提示进行安装。这个软件比较大，你可以不用完整安装，勾选如下选项即可：

```{figure} ../_static/images/gpu_cuda_installation.png
```

安装完可以通过 `nvcc --version`
命令查看 CUDA 是否安装成功。在 Python 中添加这样一行代码 `os.environ['CUDA_VISIBLE_DEVICES'] = '0'`
就可以为你的程序加速了（前提是有 NVIDIA 的 GPU，这通过任务管理器可以查看，见本页第一张图）。
**但是，令人疑惑的是，我安装了 PaddlePaddle 的 GPU 版本，这句话不管设不设置，效果都一样，都用到了 GPU。**
英特尔 GPU 应该用什么加速，我没用过，暂时不知道。

根据你安装的 CUDA 版本，再去下载安装对应版本的
[PaddlePaddle](https://www.paddlepaddle.org.cn/install/quick)
应该就可以了，因为我的版本都是 11.1 所以，我用 pip 安装了 PaddlePaddle 的 11.1 版本。下图是成功后的训练过程：

```{figure} ../_static/images/gpu_training_success.png
```

另外，如果想查看本机的其他参数，可以使用下面几种方式中的一种：

- 设置 `>>` 系统 `>>` 关于
- Win + R `>>` msinfo32
- Win + R `>>` dxdiag
- PowerShell `>>` Get-ComputerInfo
- cmd.exe `>>` systeminfo
- 使用工具软件 [CPU-Z](https://www.cpuid.com/)

## CUDA 12 + OpenCV

### 软件环境

本教程在 WSL2 Ubuntu 20.04 上测试通过。

安装完成 CUDA 12 后，`nvcc --version` 的输出类似：

```bash
$ nvcc --version
nvcc: NVIDIA (R) Cuda compiler driver
Copyright (c) 2005-2024 NVIDIA Corporation
Built on ...
Cuda compilation tools, release 12.x, V12.x...
```

### CUDA 路径

```bash
$ whereis cuda
cuda: /usr/lib/cuda /usr/include/cuda.h /usr/local/cuda
```

### 安装步骤

#### 1. 安装 CUDA 密钥环和更新

```bash
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-keyring_1.1-1_all.deb
sudo dpkg -i cuda-keyring_1.1-1_all.deb
sudo apt-get update
```

#### 2. 安装 cuDNN

```bash
sudo apt-get -y install cudnn
sudo apt-get -y install cudnn-cuda-12
```

也可以手动下载对应 CUDA 版本的 cuDNN 归档文件安装（二选一即可）：

```bash
# 下载并解压 cuDNN 归档文件
wget https://developer.download.nvidia.com/compute/cudnn/redist/cudnn/linux-x86_64/cudnn-linux-x86_64-9.2.0.82_cuda12-archive.tar.xz
tar -xvf cudnn-linux-x86_64-9.2.0.82_cuda12-archive.tar.xz

# 复制头文件和库文件
sudo cp cudnn-*-archive/include/cudnn*.h /usr/local/cuda/include
sudo cp -P cudnn-*-archive/lib/libcudnn* /usr/local/cuda/lib64
sudo chmod a+r /usr/local/cuda/include/cudnn*.h /usr/local/cuda/lib64/libcudnn*
```

#### 3. 准备 OpenCV 源码

```bash
mkdir -p opencv
cd opencv
git clone https://github.com/opencv/opencv.git
git clone https://github.com/opencv/opencv_contrib.git
```

#### 4. 配置和编译 OpenCV

```bash
cd opencv
mkdir build && cd build

cmake -D CMAKE_BUILD_TYPE=RELEASE \
    -D CMAKE_INSTALL_PREFIX=/usr/local \
    -D OPENCV_EXTRA_MODULES_PATH=../../opencv_contrib/modules \
    -D WITH_CUDA=ON \
    -D OPENCV_DNN_CUDA=ON \
    -D CUDA_ARCH_BIN=8.6 \
    -D CUDA_ARCH_PTX="" \
    -D CUDA_TOOLKIT_ROOT_DIR=/usr/local/cuda \
    -D CUDNN_LIBRARY=/usr/local/cuda/lib64/libcudnn.so \
    -D CUDNN_INCLUDE_DIR=/usr/local/cuda/include \
    -D WITH_CUBLAS=ON \
    -D WITH_NVCUVID=ON \
    -D BUILD_opencv_python3=ON \
    -D WITH_FFMPEG=ON \
    -D WITH_GSTREAMER=ON \
    -D WITH_V4L=ON \
    -D BUILD_opencv_videoio=ON \
    -D BUILD_EXAMPLES=OFF ..

make -j$(nproc)
sudo make install
```

#### 5. 清理潜在的冲突

```bash
pip uninstall opencv-python
pip uninstall opencv-python-headless
```

### 注意事项

1. **CUDA 架构配置**：`CUDA_ARCH_BIN=8.6` 对应 Ampere 架构（如 RTX 30 系列），请根据您的 GPU 架构调整（例如 Turing 为 7.5、Ada Lovelace 为 8.9）。

2. **环境变量**：编译完成后，建议更新库路径：

   ```bash
   sudo ldconfig
   ```

3. **验证安装**：可以通过以下命令验证 OpenCV 是否成功编译并支持 CUDA：

   ```python
   import cv2
   print(cv2.__version__)
   print(cv2.cuda.getCudaEnabledDeviceCount())
   ```

4. **依赖安装**：如果编译过程中缺少依赖，可以使用以下命令安装常见依赖：

   ```bash
   sudo apt-get install build-essential cmake git pkg-config \
        libgtk-3-dev libavcodec-dev libavformat-dev libswscale-dev \
        libv4l-dev libxvidcore-dev libx264-dev libjpeg-dev \
        libpng-dev libtiff-dev gfortran openexr libatlas-base-dev \
        python3-dev python3-numpy libtbb2 libtbb-dev libdc1394-22-dev
   ```

## 用 NPU 训练神经网络

### 检查是否支持 NPU

```bash
pip install openvino
python -c "from openvino import Core; print(Core().available_devices)"
```

```{dropdown}
['CPU', 'GPU', 'NPU']
```

### 下载和运行示例代码

```bash
git clone https://github.com/openvinotoolkit/openvino_notebooks
```

在 Windows 上安装环境：<https://github.com/openvinotoolkit/openvino_notebooks/wiki/Windows>

将示例代码中运行实例的载体改为 NPU：

```python
device = widgets.Dropdown(
    options=core.available_devices + ["AUTO"],
    value='NPU',  # 改为 NPU 既可使用 NPU 资源
    description='Device:',
    disabled=False,
)
```

### 观察实验结果

```{figure} ../_static/images/npu_intel.png

```


[^cpu-arch]: https://ubuntuqa.com/article/371.html
