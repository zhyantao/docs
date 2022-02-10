==================
连铸仿真的计算模型
==================

背景介绍
--------

连铸，即连续铸造。英文是 continuous casting 或 strand casting。
连铸本质上是一种传热过程，去除钢水中的过热、潜热和显热以产生预定截面尺寸的固态铸坯。

注意，strand 指的是处于固液混合状态的铸坯，slab 指的是固态的铸坯，这两个词在论文中经常出现。
因此，在引锭杆还未将铸坯完全拉出时，也就是带液芯的铸坯，通常用 strand 称呼，完全拉出后，用 slab 称呼。

对连铸过程建模，首先应该理解连铸到底是怎么一个过程。首先认识一下连铸机（侧视图）：

.. panels::
    :column: col-lg-12

    .. image:: ../../_static/images/600px-Lingotamento_Continuo-Continuous_Casting.png
    
    +++
    Continuous casting. [1]_

    1: Ladle (大包). 2: Stopper (塞棒). 3: Tundish (中间包). 4: Shroud/pipe (导管). 5: Mold/Crystallizer (模具/结晶器). 
    6: Roll support (支持辊). 7: Turning zone (弯曲段). 8: Shroud/pipe. 9: Bath level (液位). 10: Meniscus (弯月面). 11: Withdrawal unit (引锭杆). 12: Slab (铸坯).
    
    A: Liquid metal. B: Solidified metal. C: Slag. D: Water-cooled copper plates (水冷铜板). E: Refractory material (耐火材料).


对连铸过程建模是一项艰巨的任务，通常会有多种现象搅在一起，它们之间相互制约又相互影响，很难将其解耦。
这些复杂的物理现象包括：传热和凝固、多相湍流、堵塞、电磁效应、复杂的界面行为、夹杂物、热机械变形、应力、裂纹、偏析、显微组织等。

从时间角度上讲，有些现象时瞬间发生的，而有些现象的结果将会产生持续的影响。
从空间角度上讲，有些现象只会影响到比较小的局部，而另一些可能会产生比较大范围的影响。

Brain G. Thomas :footcite:p:`thomas2018review` 对很多现象应该如何建模和现阶段仍然存在的挑战进行了总结和归纳，重点介绍了应该如何利用这些数学模型来模拟缺陷的形成过程。
注意，这里的缺陷大多指的是表面裂纹和内部裂纹。

很多缺陷的形成来源于结晶器这一部分，引起表面裂纹的主要因素有： [2]_

- 钢的高温力学行为；
- 凝固过程中的冶金行为；
- 铸机设备的运行状态；
- 钢成分对裂纹的敏感性。

把结晶器作为重点的研究对象，宏观了解一下它内部流体的流动现象，如下图：

.. panels::
    :column: col-lg-12

    .. image:: ../../_static/images/fluid-flow-phenomena-in-the-mold-region.png

    +++

    Fluid-flow phenomena in the mold region of a steel slab caster. :footcite:p:`thomas2018review`

作者认为在建模时，应该遵循以下步骤：

- 选择模型目的(域)和控制方程（关键）；
- 解耦错综复杂的物理现象（如流体流动的有限差分法、应力分析的有限元法等）；
- 进行充分的数值验证（误差来源：过于粗放的计算域、求解非线性方程组时的不完全收敛）；
- 现场运行以矫正和确认模型的准确性。

本文系 2021 年 11 月 8 号的一次分享，由于当时没有完全理解控制领域的一些方程，后续更新将在 `PPT <https://kdocs.cn/l/ctd6tabkiJCa>`_ 上做修改。
若您发现了本文的错误，可以选择右上角 ``Github`` 菜单下的 ``Open Issue`` 或 ``Suggest Edit`` 和我一起修改本文，谢谢。


资料调研
--------

入门科普
~~~~~~~~~


入门科普
~~~~~~~~

- Continuous Casting - `Wikipedia <https://en.wikipedia.org/wiki/Continuous_casting>`__
- Continuous Casting, 1970's - Film 9080 `YouTube <https://www.youtube.com/watch?v=AZXWAd-KjHQ>`__
- Continuous Casting Process \| Elements \| Process \| Die Casting \| Types \| Applications \| Pros and Cons `YouTube <https://www.youtube.com/watch?v=JAqhwR7bJTU>`__
- Continuous Casting Refractory Process \| Vishva Vishal Engineering (Quality Refractory) `YouTube <https://www.youtube.com/watch?v=LlXhF8mRAmo>`__
- Fluid-flow and Stress Analysis of Steel Continuous Casting - Brian Thomas `YouTube <https://www.youtube.com/watch?v=XGMf7vrGGJk>`__
- 冶金学 - 东北大学 `哔哩哔哩 <https://www.bilibili.com/video/BV1ob411U7c5?p=66>`__
- 板坯连铸机(第一部分: 术语) `PDF <https://members.wto.org/crnattachments/2020/TBT/CHN/20_6840_00_x.pdf>`__


领域学者
~~~~~~~~

- `Brian G. Thomas <http://ccc.illinois.edu/publications.html>`_ 及 `课题组成员 <http://ccc.illinois.edu/people.html>`_
- `冯科 <https://kns.cnki.net/kcms/detail/knetsearch.aspx?dbcode=CDFD&code=000040780083&sfield=au&skey=%e5%86%af%e7%a7%91&uniplatform=NZKPT>`_ - 重庆大学
- `张伟 <https://charmve.github.io/>`_ - 扬州大学


论文和数据集
~~~~~~~~~~~~

- Review on modeling and simulation of continuous casting. :footcite:p:`thomas2018review`
- 基于深度学习的表面缺陷检测方法综述 `自动化学报 <http://www.aas.net.cn/cn/article/doi/10.16383/j.aas.c190811?viewType=HTML>`_
- Surface Defect Detection: Dataset & Papers `Github <https://github.com/Charmve/Surface-Defect-Detection>`__
- 工业缺陷检测 `飞桨 AI Stuido <https://aistudio.baidu.com/aistudio/datasetdetail/47124>`__
- 布匹缺陷 `飞桨 AI Stuido <https://aistudio.baidu.com/aistudio/datasetdetail/31076>`__
- 瓷砖缺陷 `飞桨 AI Stuido <https://aistudio.baidu.com/aistudio/datasetdetail/32615>`__
- 绝缘子自爆缺陷图像 4 `飞桨 AI Stuido <https://aistudio.baidu.com/aistudio/datasetdetail/33087>`__
- PCB 缺陷检测 `飞桨 AI Stuido <https://aistudio.baidu.com/aistudio/datasetdetail/49931>`__
- 手扶电梯梯级 `飞桨 AI Stuido <https://aistudio.baidu.com/aistudio/datasetdetail/44820>`__
- 汇总 \| 缺陷检测数据集 `微信公众号 <https://mp.weixin.qq.com/s/kw_jRWevs_TMhIqWCDC55A>`__
- 旋转机械故障诊断公开数据集整理 `CSDN <https://blog.csdn.net/hustcxl/article/details/89394428>`__


仿真软件
~~~~~~~~

- `Design Environment for FORMing <https://www.deform.com/>`_
- `华铸软件 <http://www.intecast.com/index.asp>`_
- `Any Casting <https://www.anycasting.com/en/>`_
- `ESI Group <https://www.esi-group.com/>`_


.. rubric:: 参考资料

.. [1] Continuous casting. https://en.wikipedia.org/wiki/Continuous_casting
.. [2] 蔡开科. 连铸坯表面裂纹的控制[J]. 鞍钢技术, 2004(3):8.
.. footbibliography::
