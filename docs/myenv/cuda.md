# 从源码安装 CV2 以支持 CUDA

## 软件环境

本教程在 WSL2 Ubuntu 20.04 上测试通过。

```bash
$ nvcc --version
nvcc: NVIDIA (R) Cuda compiler driver
Copyright (c) 2005-2019 NVIDIA Corporation
Built on Sun_Jul_28_19:07:16_PDT_2019
Cuda compilation tools, release 10.1, V10.1.243

$ whereis cuda
cuda: /usr/lib/cuda /usr/include/cuda.h /usr/local/cuda

$ dpkg -l | grep cudnn
ii  cudnn                                        9.8.0-1                               amd64        NVIDIA CUDA Deep Neural Network library (cuDNN)
ii  cudnn9                                       9.8.0-1                               amd64        NVIDIA CUDA Deep Neural Network library (cuDNN)
ii  cudnn9-cuda-12                               9.8.0.87-1                            amd64        NVIDIA cuDNN for CUDA 12
ii  cudnn9-cuda-12-8                             9.8.0.87-1                            amd64        NVIDIA cuDNN for CUDA 12.8
ii  libcudnn9-cuda-12                            9.8.0.87-1                            amd64        cuDNN runtime libraries for CUDA 12.8
ii  libcudnn9-dev-cuda-12                        9.8.0.87-1                            amd64        cuDNN development headers and symlinks for CUDA 12.8
ii  libcudnn9-samples                            9.8.0.87-1                            all          cuDNN samples
ii  libcudnn9-static-cuda-12                     9.8.0.87-1                            amd64        cuDNN static libraries for CUDA 12.8

$ dpkg -l | grep cuda
ii  cuda                                         12.8.1-1                              amd64        CUDA meta-package
ii  cuda-12-8                                    12.8.1-1                              amd64        CUDA 12.8 meta-package
ii  cuda-cccl-12-8                               12.8.90-1                             amd64        CUDA CCCL
ii  cuda-command-line-tools-12-8                 12.8.1-1                              amd64        CUDA command-line tools
ii  cuda-compiler-12-8                           12.8.1-1                              amd64        CUDA compiler
ii  cuda-crt-12-8                                12.8.93-1                             amd64        CUDA crt
ii  cuda-cudart-12-8                             12.8.90-1                             amd64        CUDA Runtime native Libraries
ii  cuda-cudart-dev-12-8                         12.8.90-1                             amd64        CUDA Runtime native dev links, headers
ii  cuda-cuobjdump-12-8                          12.8.90-1                             amd64        CUDA cuobjdump
ii  cuda-cupti-12-8                              12.8.90-1                             amd64        CUDA profiling tools runtime libs.
ii  cuda-cupti-dev-12-8                          12.8.90-1                             amd64        CUDA profiling tools interface.
ii  cuda-cuxxfilt-12-8                           12.8.90-1                             amd64        CUDA cuxxfilt
ii  cuda-demo-suite-12-8                         12.8.90-1                             amd64        Demo suite for CUDA
ii  cuda-documentation-12-8                      12.8.90-1                             amd64        CUDA documentation
ii  cuda-driver-dev-12-8                         12.8.90-1                             amd64        CUDA Driver native dev stub library
ii  cuda-drivers-570                             570.124.06-0ubuntu1                   amd64        CUDA Driver meta-package, branch-specific
ii  cuda-gdb-12-8                                12.8.90-1                             amd64        CUDA-GDB
ii  cuda-keyring                                 1.1-1                                 all          GPG keyring for the CUDA repository
ii  cuda-libraries-12-8                          12.8.1-1                              amd64        CUDA Libraries 12.8 meta-package
ii  cuda-libraries-dev-12-8                      12.8.1-1                              amd64        CUDA Libraries 12.8 development meta-package
ii  cuda-nsight-12-8                             12.8.90-1                             amd64        CUDA nsight
ii  cuda-nsight-compute-12-8                     12.8.1-1                              amd64        NVIDIA Nsight Compute
ii  cuda-nsight-systems-12-8                     12.8.1-1                              amd64        NVIDIA Nsight Systems
ii  cuda-nvcc-12-8                               12.8.93-1                             amd64        CUDA nvcc
ii  cuda-nvdisasm-12-8                           12.8.90-1                             amd64        CUDA disassembler
ii  cuda-nvml-dev-12-8                           12.8.90-1                             amd64        NVML native dev links, headers
ii  cuda-nvprof-12-8                             12.8.90-1                             amd64        CUDA Profiler tools
ii  cuda-nvprune-12-8                            12.8.90-1                             amd64        CUDA nvprune
ii  cuda-nvrtc-12-8                              12.8.93-1                             amd64        NVRTC native runtime libraries
ii  cuda-nvrtc-dev-12-8                          12.8.93-1                             amd64        NVRTC native dev links, headers
ii  cuda-nvtx-12-8                               12.8.90-1                             amd64        NVIDIA Tools Extension
ii  cuda-nvvm-12-8                               12.8.93-1                             amd64        CUDA nvvm
ii  cuda-nvvp-12-8                               12.8.93-1                             amd64        CUDA Profiler tools
ii  cuda-opencl-12-8                             12.8.90-1                             amd64        CUDA OpenCL native Libraries
ii  cuda-opencl-dev-12-8                         12.8.90-1                             amd64        CUDA OpenCL native dev links, headers
ii  cuda-profiler-api-12-8                       12.8.90-1                             amd64        CUDA Profiler API
ii  cuda-runtime-12-8                            12.8.1-1                              amd64        CUDA Runtime 12.8 meta-package
ii  cuda-sanitizer-12-8                          12.8.93-1                             amd64        CUDA Sanitizer
ii  cuda-toolkit-12-8                            12.8.1-1                              amd64        CUDA Toolkit 12.8 meta-package
ii  cuda-toolkit-12-8-config-common              12.8.90-1                             all          Common config package for CUDA Toolkit 12.8.
ii  cuda-toolkit-12-config-common                12.8.90-1                             all          Common config package for CUDA Toolkit 12.
ii  cuda-toolkit-config-common                   12.8.90-1                             all          Common config package for CUDA Toolkit.
ii  cuda-tools-12-8                              12.8.1-1                              amd64        CUDA Tools meta-package
ii  cuda-visual-tools-12-8                       12.8.1-1                              amd64        CUDA visual tools
ii  cudnn9-cuda-12                               9.8.0.87-1                            amd64        NVIDIA cuDNN for CUDA 12
ii  cudnn9-cuda-12-8                             9.8.0.87-1                            amd64        NVIDIA cuDNN for CUDA 12.8
ii  libcudart10.1:amd64                          10.1.243-3                            amd64        NVIDIA CUDA Runtime Library
ii  libcudnn9-cuda-12                            9.8.0.87-1                            amd64        cuDNN runtime libraries for CUDA 12.8
ii  libcudnn9-dev-cuda-12                        9.8.0.87-1                            amd64        cuDNN development headers and symlinks for CUDA 12.8
ii  libcudnn9-static-cuda-12                     9.8.0.87-1                            amd64        cuDNN static libraries for CUDA 12.8
ii  nvidia-cuda-dev                              10.1.243-3                            amd64        NVIDIA CUDA development files
ii  nvidia-cuda-doc                              10.1.243-3                            all          NVIDIA CUDA and OpenCL documentation
ii  nvidia-cuda-gdb                              10.1.243-3                            amd64        NVIDIA CUDA Debugger (GDB)
ii  nvidia-cuda-toolkit                          10.1.243-3                            amd64        NVIDIA CUDA development toolkit
```

## 安装教程

```bash
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-keyring_1.1-1_all.deb
sudo dpkg -i cuda-keyring_1.1-1_all.deb
sudo apt-get update
sudo apt-get -y install cudnn
sudo apt-get -y install cudnn-cuda-12
wget https://developer.download.nvidia.com/compute/cudnn/redist/cudnn/linux-x86_64/cudnn-linux-x86_64-9.2.0.82_cuda12-archive.tar.xz
tar -xvf cudnn-linux-x86_64-9.2.0.82_cuda12-archive.tar.xz
sudo cp cudnn-*-archive/include/cudnn*.h /usr/local/cuda/include
sudo cp -P cudnn-*-archive/lib/libcudnn* /usr/local/cuda/lib64
sudo chmod a+r /usr/local/cuda/include/cudnn*.h /usr/local/cuda/lib64/libcudnn*

mkdir -p opencv
git clone https://github.com/opencv/opencv.git
git clone https://github.com/opencv/opencv_contrib.git
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

````{note}
`compute_50,code=sm_50` 通过 `nvcc --help | grep compute` 来检查是否存在。

删除 pip 安装的 opencv，以防止冲突：

```bash
pip uninstall opencv-python
pip uninstall opencv-python-headless
```
````
