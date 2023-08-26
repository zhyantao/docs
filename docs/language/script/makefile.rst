=========
Makefile
=========

本文仅提供编写手动编写 Makefile 的简单示例，理解了本文就能够应付大部分的 Makefile 了，更加复杂的 Makefile 都是在这种简单规则上叠加的。但是只阅读本文是远远不够的，为了能够对 Makefile 有更加清晰的认识，我这里推荐另外一个文档：https://seisman.github.io/how-to-write-makefile。

.. note::

    在实际工程中，虽然也有只用 Makefile 的项目，但是更为方便的方式是使用 CMakeList 来生成 Makefile。cmake 管理工程的最大优势在于跨平台，自己不用书写太复杂的脚本了，自己写一写配置文件，后面的工作就都是自动化的了。


基本语法
--------

.. code-block:: bash

    # ====================== VERSION 1 ======================
    # 最简单的方式就是把文件一个一个手打出来进行编译
    hello: main.cpp printhello.cpp  factorial.cpp
    	g++ -o hello main.cpp printhello.cpp  factorial.cpp
    
    # ====================== VERSION 2 ======================
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
    
    
    # ====================== VERSION 3 ======================
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
    
    
    # ====================== VERSION 4 ======================
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
