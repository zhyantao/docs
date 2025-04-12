# 从源码安装 CV2 以支持 CUDA

```bash
mkdir -p opencv
git clone https://github.com/opencv/opencv.git
git clone https://github.com/opencv/opencv_contrib.git
cd opencv
mkdir build && cd build
cmake -D CMAKE_BUILD_TYPE=RELEASE \
    -D CMAKE_INSTALL_PREFIX=/usr/local \
    -D OPENCV_EXTRA_MODULES_PATH=../../opencv_contrib/modules \
    -D WITH_CUDA=ON \
    -D CUDA_ARCH_BIN=8.6 \
    -D CUDA_ARCH_PTX="" \
    -D CUDA_NVCC_FLAGS="-gencode arch=compute_50,code=sm_50" \ # 使用 nvcc --help | grep compute 检查 compute_50 和 sm_50 是否存在
    -D CUDA_TOOLKIT_ROOT_DIR=/usr/local/cuda-12.8 \ # 确保已安装 CUDA 12.8, 检查此路径存在
    -D WITH_CUBLAS=ON \
    -D WITH_NVCUVID=ON \
    -D BUILD_opencv_python3=ON \
    -D BUILD_EXAMPLES=OFF ..
make -j$(nproc)
sudo make install
```
