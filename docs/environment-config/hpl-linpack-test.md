# Linpack 之 HPL 测试

## 配置编译器

```{code-block} bash
sudo apt install gfortran gcc
```

## 配置 BLAS/CBLAS/ATLAS 库

- 创建目录并切换：`mkdir ~/prepare && cd ~/prepare`
- 下载：`wget http://www.netlib.org/blas/blas-3.8.0.tgz`
- 解压包：`tar -xzf blas-3.8.0.tgz`
- 切换目录：`cd BLAS-3.8.0`
- 编译生成 `blas_LINUX.a`：`make`
- 链接 `.o` 文件生成 `libblas.a`：`ar rv libblas.a *.o`
- 切换到 `prepare` 目录：`cd ~/prepare`
- 下载：`wget http://www.netlib.org/blas/blast-forum/cblas.tgz`
- 解压包：`tar -xzf cblas.tgz`
- 切换目录：`cd CBLAS`
- 将第 5 步产生的 `.a` 文件拷贝到当前目录：`cp ~/prepare/BLAS-3.8.0/blas_LINUX.a ./`
- 修改 `Makefile.in` 文件中的 `BLLIB`：`vim Makefile.in`：

    ```{code-block} bash
    BLLIB = ~/prepare/BLAS-3.8.0/blas_LINUX.a
    ```

- 编译：`make`
- 测试运行：`./testing/xzcblat1`

## 配置 MPICH 并行环境

- 切换目录：`cd ~/prepare`
- 下载：`wget http://www.mpich.org/static/downloads/3.2.1/mpich-3.2.1.tar.gz`
- 解压安装包：`tar xzf mpich-3.2.1.tar.gz`
- 切换到主目录：`cd mpich-3.2.1`
- 设置安装路径：`./configure [--disable-cxx]`
- 编译：`make`
- 安装：`sudo make install`
- 查看前面工作是否成功：`which mpicc && which mpiexec`
- 创建目录：`mkdir mytest`
- 测试运行：`mpiexec -f mytest -n 3 hostname && mpiexec -n 5 -f mytest ./examples/cpi`

## 配置 HPL 环境

- 切换目录：`cd ~/prepare`
- 复制文件：`sudo cp CBLAS/lib/* /usr/local/lib`
- 复制文件：`sudo cp BLAS-3.8.0/blas_LINUX.a /usr/local/lib`
- 下载：`wget http://www.netlib.org/benchmark/hpl/hpl-2.3.tar.gz`
- 解压包：`tar -xzf hpl-2.3.tar.gz`
- 切换目录：`cd hpl-2.3`
- 复制文件：`cp setup/Make.Linux_PII_CBLAS ./`
- 复制文件：`sudo cp include/* /usr/local/include`
- 打开 `Make.top` 文件：`vim Make.top`，做如下修改：

    ```{code-block} bash
    arch = Linux_PII_CBLAS
    ```

- 打开 `Makefile` 文件：`vim Makefile`，做如下修改：

    ```{code-block} bash
    arch = Linux_PII_CBLAS
    ```

- 打开 `Make.Linux_PII_CBLAS` 文件：`vim Make.Linux_PII_CBLAS`，做如下修改：

    ```{code-block} bash
    ARCH         = Linux_PII_CBLAS

    TOPdir       = ~/prepare/hpl-2.3

    MPdir        = /usr/local
    MPlib        = $(MPdir)/lib/libmpich.so

    LAdir        = /usr/local/lib
    LAlib        = $(LAdir)/cblas_LINUX.a $(LAdir)/blas_LINUX.a

    CC           = /usr/local/bin/mpicc

    LINKER       = /usr/local/bin/mpif77
    ```

- 编译：`make arch=Linux_PII_CBLAS`
- 运行测试：`cd bin/Linux_PII_CBLAS && mpirun -np 4 ./xhpl > HPL-Benchmark.txt`

## 配置 HPCG 环境

- 切换目录：`cd ~/prepare`
- 下载 HPCG 源代码：`git clone https://github.com/hpcg-benchmark/hpcg.git`
- `cd` 到 `setup`：`cd hpcg/setup`
- 修改 `Make.Linux_MPI`：`vim Make.Linux_MPI`：

    ```{code-block} bash
    MPdir        = /usr/local

    CXX          = /usr/local/bin/mpicxx
    ```

- 创建 `build` 文件夹：`mkdir build && cd build`
- 设置安装环境：`../../configure Linux_MPI`
- 开始安装：`make`
- 运行测试：`cd bin && mpirun -np 8 ./xhpcg`

---

下载结果文件 [HPL-Benchmark.txt](https://zhyantao.lanzouj.com/iAUIr0396s5c)
