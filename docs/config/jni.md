# 在 Java 中调用 C++ 函数

如果我们用 C++ 开发了一个算法，想要给别人使用。

但如果另一个人用的不是 C++，而是 Java 那么如何实现这个通信过程呢？

本文参考了一些网络资料，然后整理了一个小示例，如下所示：

项目源代码：<https://gitee.com/zhyantao/hello-jni>

## 开发环境

| IDE | 备注 | 模式|
| --- | --- | --- |
| Intellij IDEA 2022 专业版 | JDK 1.8.0_331 | 32 位 |
| Visual Studio 社区版 | Debug x86 模式 | 32 位 |

## 运行结果

[下载源代码](https://gitee.com/zhyantao/hello-jni)，然后用 IDEA 打开
`java` 文件夹下的项目，运行 `main()` 函数即可，下面是输出结果：

```bash
Hello World! by Java
Hello World! by C++
进程已结束,退出代码0
```

第一行是 Java 打印出来的语句，第二行是 C++ 打印的语句。

## JNI 的使用步骤

- 用 IDEA 打开 java 项目，在项目中创建一个类 `HelloJNI`（类名可以随意，类内的方法名也随意）；
- 在 `src/main/java/` 文件夹下打开 cmd（而不是 PowerShell），使用
  `javah -jni -encoding UTF-8 org.example.HelloJNI` 编译生成 `.h` 文件（命令 `javah` 适用于 JDK 1.8 版本）；
- 用 Visual Studio 打开 cpp 项目（我们的目标是拿到解决方案为我们生成的 `.dll` 文件）；
- VS 选择 `Debug` - `x86` 模式，在项目上右击，选择 `属性` > `配置属性` > `VC++ 目录` > 编辑
  `包含目录` > 添加 `$(JAVA_HOME)\include` 和 `$(JAVA_HOME)\include\win32` 以及第 2 步生成的
  `org_example_HelloJNI.h` 所在的文件夹；
- 将生成的 `org_example_HelloJNI.h` 复制到到 VS 项目中（目标位置随意），在 VS 项目中，右击
  `头文件` > `添加` > `现有项` > 选择 `org_example_HelloJNI.h`；
- 在 `pch.h` 中添加一句宏定义，后面会用到 `#define API_DLL __declspec(dllexport)`；
- 在 VS 项目的 `HelloJNI.cpp` 中实现 `org_example_HelloJNI.h` 中声明的函数（可以在该实现中调用 C++ 中的代码）；
- 将 C++ 项目中需要调用的函数前添加关键字 `API_DLL`；
- 将 VS 项目的 `属性` > `配置属性` > `常规` > `配置类型` 更改为 `动态库(.dll)`；
- 在 VS 项目上右击，选择 `重新生成`；
- 将生成的 `HelloJNI.dll` 复制到 IDEA 项目（根目录）下；
- 在 Java 项目中使用 `System.loadLibrary("HelloJNI");` 引入动态库；
- 运行 Java 项目的 `main()` 函数，查看结果。
