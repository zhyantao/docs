=========
Makefile
=========

基本语法
--------

.. code-block:: bash

    # := 表示临时赋值
    src := $(shell ls *.c)
    objs := $(patsubst %.c,%.o,$(src)

    # 基本格式：target:dependencies
    # $@ 代表 target
    # $^ 代表 dependencies
    test: $(objs)
    gcc -o $@ $^

    # 生成中目标文件的中间文件（dependencies）
    # 即 .o 文件的生成规则
    # $< 表示匹配到的第一个依赖文件名
    # % 是通配符，它和字符串中任意个数的字符相匹配
    %.o: %.c
    gcc -c -o $@ $<

    clean:
    rm -f test *.o
 
还有其他的语法比如 ``.PHONY`` 可以参考下面的参考文献中的 **跟我一起写Makefile**


.. rubric:: 参考资料

1. 韦东山. 嵌入式 Linux 应用开发完全手册 [M]. 人民邮电出版社, 2008.
2. 跟我一起写 Makefile. https://seisman.github.io/how-to-write-makefile/index.html
3. 在 Linux 下使用 CMake 构建应用程序. https://www.ibm.com/developerworks/cn/linux/l-cn-cmake/
4. CMake 入门实战. https://www.hahack.com/codes/cmake/
5. Makefile 由浅入深--教程、干货. https://zhuanlan.zhihu.com/p/47390641
6. Cmake 实战 https://kdocs.cn/l/ch0JlSoQjQdm
