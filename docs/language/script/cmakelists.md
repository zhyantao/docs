# CMakeLists

使用 CMake 最大的优势在于跨平台，它会为我们生成一份 Makefile，然后就和 Makefile 的使用方法就一样了。

1、编写 CMakeLists

```cmake
# CMakeLists.txt

cmake_minimum_required(VERSION 3.12)

project(persondemo)

ADD_EXECUTABLE(persondemo main.cpp student.cpp)
```

2、开始编译

```bash
mkdir build
cd build && cmake ..
make
sudo make install
```

1. 在 Linux 下使用 CMake 构建应用程序. <https://www.ibm.com/developerworks/cn/linux/l-cn-cmake/>
2. CMake 入门实战. <https://www.hahack.com/codes/cmake/>
3. CMake 实战 <https://kdocs.cn/l/ch0JlSoQjQdm>
