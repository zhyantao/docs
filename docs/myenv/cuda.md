# 从源码安装支持 CUDA 的 OpenCV

## 软件环境

本教程在 WSL2 Ubuntu 20.04 上测试通过。

### CUDA 版本

```bash
$ nvcc --version
nvcc: NVIDIA (R) Cuda compiler driver
Copyright (c) 2005-2019 NVIDIA Corporation
Built on Sun_Jul_28_19:07:16_PDT_2019
Cuda compilation tools, release 10.1, V10.1.243
```

### CUDA 路径

```bash
$ whereis cuda
cuda: /usr/lib/cuda /usr/include/cuda.h /usr/local/cuda
```

## 安装步骤

### 1. 安装 CUDA 密钥环和更新

```bash
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-keyring_1.1-1_all.deb
sudo dpkg -i cuda-keyring_1.1-1_all.deb
sudo apt-get update
```

### 2. 安装 cuDNN

```bash
sudo apt-get -y install cudnn
sudo apt-get -y install cudnn-cuda-12

# 下载并解压 cuDNN 归档文件
wget https://developer.download.nvidia.com/compute/cudnn/redist/cudnn/linux-x86_64/cudnn-linux-x86_64-9.2.0.82_cuda12-archive.tar.xz
tar -xvf cudnn-linux-x86_64-9.2.0.82_cuda12-archive.tar.xz

# 复制头文件和库文件
sudo cp cudnn-*-archive/include/cudnn*.h /usr/local/cuda/include
sudo cp -P cudnn-*-archive/lib/libcudnn* /usr/local/cuda/lib64
sudo chmod a+r /usr/local/cuda/include/cudnn*.h /usr/local/cuda/lib64/libcudnn*
```

### 3. 准备 OpenCV 源码

```bash
mkdir -p opencv
cd opencv
git clone https://github.com/opencv/opencv.git
git clone https://github.com/opencv/opencv_contrib.git
```

### 4. 配置和编译 OpenCV

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
    -D CUDA_NVCC_FLAGS="-gencode arch=compute_50,code=sm_50" \
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

### 5. 清理潜在的冲突

```bash
pip uninstall opencv-python
pip uninstall opencv-python-headless
```

## 注意事项

1. **CUDA 架构配置**：`compute_50,code=sm_50` 可以通过 `nvcc --help | grep compute` 来检查是否存在，请根据您的 GPU 架构进行调整。

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
