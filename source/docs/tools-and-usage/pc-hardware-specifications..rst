============
电脑硬件属性
============

你有什么问题
------------

- 有时候，只想知道自己的电脑有没有 GPU 有没有 CUDA
- 如果有 GPU ，我的 GPU 是什么型号的
- AMD、NVIDIA、Intel 这三家公司分别生产什么产品
- 我们通常说的 AMD 指的是处理器还是显卡
- x86、ARM、AMD 都是架构的名称吗
- 机器学习到底需要什么样的配置
- 如何比较电脑的参数，如何衡量价格划不划算

查看本机参数
------------

共有 5 中查看方式：

- 设置 ``>>`` 系统 ``>>`` 关于
- Win + R ``>>`` msinfo32
- Win + R ``>>`` dxdiag
- PowerShell ``>>`` Get-ComputerInfo
- cmd.exe ``>>`` systeminfo
- 使用工具软件 `CPU-Z <https://www.cpuid.com/>`_


.. csv-table::
    :header: "CPU vs GPU", "Name", "# of Cores", "# of Threads", "Clock Speed", "Memory", "Price"

    "CPU", "Intel Core i7-7700K", "4", "8", "4.4GHz", "Shared with system", "$339"
    "CPU", "Intel Core i7-6950X", "10", "20", "3.5GHz", "Shared with system", "$1723"
    "GPU", "NVIDIA Titan Xp", "3840", "", "1.6GHz", "12GB GDDR5X", "$1200"
    "GPU", "NVIDIA GTX 1070", "1920", "", "1.68GHz", "8GB GDDR5", "$339"
