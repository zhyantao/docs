# 可视化 C++ 调用链

## 使用 Clang++ 可视化调用

1. 安装 MSYS2：<https://www.msys2.org/>
2. 安装 Clang++：`pacman -S mingw-w64-x86_64-clang`
3. 安装 Graphviz：<https://graphviz.org/>
4. 运行下面的命令：

```bash
clang++ -S -emit-llvm demo.cpp -o dump.txt
opt -passes=dot-callgraph dump.txt -o callgraph.dot
dot -Tpng dump.txt.callgraph.dot -o callgraph.png
```
