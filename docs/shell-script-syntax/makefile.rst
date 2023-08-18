=========
Makefile
=========

基本语法
--------

.. code-block:: bash

    # VERSION 1
    # 最简单的方式就是把文件一个一个手打出来进行编译
    hello: main.cpp printhello.cpp  factorial.cpp
    	g++ -o hello main.cpp printhello.cpp  factorial.cpp
    
    # VERSION 2
    # 采用 Makefile 只会更新有变动的文件，在工程比较大的情况下可以节省很多时间
    CXX = g++
    TARGET = hello
    	OBJ = main.o printhello.o factorial.o
    
    $(TARGET): $(OBJ)
    	$(CXX) -o $(TARGET) $(OBJ)
    
    main.o: main.cpp
    	$(CXX) -c main.cpp
    
    printhello.o: printhello.cpp
    	$(CXX) -c printhello.cpp
    
    factorial.o: factorial.cpp
    	$(CXX) -c factorial.cpp
    
    
    # VERSION 3
    CXX = g++
    TARGET = hello
    	OBJ = main.o printhello.o factorial.o
    
    CXXFLAGS = -c -Wall
    
    $(TARGET): $(OBJ)
    	$(CXX) -o $@ $^
    
    %.o: %.cpp
    	$(CXX) $(CXXFLAGS) $< -o $@
    
    .PHONY: clean
    clean:
    	rm -f *.o $(TARGET)
    
    
    # VERSION 4
    # 这是目前 Makefile 的主流编写方式
    # := 表示临时赋值
    CXX := g++
    TARGET := hello
    SRC := $(wildcard *.cpp)
    OBJ := $(patsubst %.cpp, %.o, $(SRC))
    
    CXXFLAGS := -c -Wall

    # 基本格式：目标文件:依赖文件
    # $@ 代表目标文件，匹配目标二进制文件 hello
    # $^ 代表依赖文件，匹配目标二进制文件 hello 依赖的所有 .o 文件，即 $(OBJ)
    $(TARGET): $(OBJ)
    	$(CXX) -o $@ $^

    # 这句话用来将所有的 .cpp 文件编译成对应的 .o 文件（文件名不变，扩展名改变）
    # $@ 代表目标文件，匹配目标 .o 文件
    # $< 代表依赖文件，匹配目标 .o 文件依赖的第一个 .c 文件，即与 .o 文件文件名相同的 .cpp 文件
    # % 是通配符，它和字符串中任意个数的字符相匹配
    %.o: %.cpp
    	$(CXX) $(CXXFLAGS) $< -o $@

    # .PHONY 作用在于防止 clean 这个命令和系统中可能存在的 clean 命令冲突
    .PHONY: clean
    clean:
    	rm -f *.o $(TARGET)

.. rubric:: 参考资料

1. Shell 工具和脚本 https://missing-semester-cn.github.io/2020/shell-tools/
2. 韦东山. 嵌入式 Linux 应用开发完全手册 [M]. 人民邮电出版社, 2008.
3. 跟我一起写 Makefile. https://seisman.github.io/how-to-write-makefile/index.html
4. 在 Linux 下使用 CMake 构建应用程序. https://www.ibm.com/developerworks/cn/linux/l-cn-cmake/
5. CMake 入门实战. https://www.hahack.com/codes/cmake/
6. Makefile 由浅入深--教程、干货. https://zhuanlan.zhihu.com/p/47390641
7. Cmake 实战 https://kdocs.cn/l/ch0JlSoQjQdm
