# Boost

[Boost](https://www.boost.io/doc/user-guide/intro.html) 是经过同行评审的高质量 C++ 库，这些库函数已经经过了严苛的测试，相比于自己写的轮子，Boost 提供的轮子可能更加稳定。

## 安装 Boost

在 Ubuntu 上安装 Boost 只需要运行下面的命令：

```bash
# Update your package list
sudo apt update
# Install the Boost development libraries
sudo apt install libboost-all-dev
```

安装完成后，使用下面的命令检查 Boost 版本号：

```bash
cat /usr/include/boost/version.hpp | grep "BOOST_LIB_VERSION"
```

## 使用 Boost

```cpp
// example.cpp
#include <algorithm>
#include <boost/lambda/lambda.hpp>
#include <iostream>
#include <iterator>

int main() {
    using namespace boost::lambda;
    typedef std::istream_iterator<int> in;

    std::for_each(in(std::cin), in(), std::cout << (_1 * 3) << " ");
}
```

```cmake
cmake_minimum_required(VERSION 3.0)
project(MyProject)

find_package(Boost REQUIRED)
add_executable(MyProject example.cpp)
target_link_libraries(MyProject Boost::headers)
```

```bash
mkdir build 
cd build 
cmake ..
cmake --build . 
```

```bash
echo 1 2 3 | ./MyProject
```
