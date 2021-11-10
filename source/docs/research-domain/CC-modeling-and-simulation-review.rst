==================
连铸建模和仿真调研
==================

.. note:: 

    本文提及到的建模涉及到两个不同的含义：1）构建计算模型，2）构建三维可视化模型。


构建计算模型
------------

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


构建三维可视化模型
------------------


三维可视化建模这个任务拆分来看，包括以下几个部分：

- 建模：用曲线或曲面造型技术和实体造型技术建立真实场景的几何表示，研究面的表示和处理的方法；
- `渲染`_：计算在假想的光源、纹理、材质属性下的光照明效果，研究模拟光线传递和散射效果的算法；
- 动画：使用运动捕捉、骨骼动画、动力学模拟等方法研究移动的表示和操作方法。

.. note:: 

    我们希望用计算机来表现或处理图像数据，初衷是 **让人们更加容易地认识和理解多维数据** ，产生令人赏心悦目的真实感。

矢量图形和光栅图形
    矢量图形格式与光栅图形是互补的，光栅图形由大量像素构成，通常的代表是摄影图像。
    矢量图形使用形状和颜色的编码数据构成图像，在渲染方面可以更灵活。

三维计算机图形软件
------------------

.. hint:: 
    
    上面提到的动画、建模、渲染、材质功能，现在很多
    `三维计算机图形软件 <https://en.wikipedia.org/wiki/3D_computer_graphics>`_
    都能满足。因此，我们可以借助这些工具加速完成我们的创意。

    但是，不可忽视的是，我们要清楚自己要建立的是什么模型？
    每一类的精度都有自己的要求，建模方式也不尽相同。
    因此，我们在工具选型时要注意区分。

机械模型
~~~~~~~~

- SolidWorks：构造实体模型，广泛用于机械模型，强调物理尺度保真度；

建筑模型
~~~~~~~~

- Autodesk Revit：适合建筑师、景观设计师，结构工程师，给排水工程师、承包商；

电子/元件
~~~~~~~~~

- Altium Designer
- SolidWorks Electrical
- Proteus
- NI Multisim

影视/游戏
~~~~~~~~~

- [开源] Blender：可提供动画、建模、渲染、材质功能，可与中高端收费套件竞争；
- [开源] Wings 3D：比 Blender 更简单，但功能更少，适合初学者；
- Autodesk Maya：许多电影特效均有这个软件制作；
- Autodesk 3ds Max：电子游戏行业占主导地位的动画程序；
- Cinema 4D：对艺术家友善的界面，以及低廉的价格；

仿真模型
~~~~~~~~

- [生物] Protein Structure Prediction
- [生物] Nucleic Acid Simulations
- [化学] Quantum Chemistry
- [化学] Molecular Modeling
- [化学] Monte Carlo Molecular Modeling
- [化学] Molecular Design
- [物理] Finite Element
- [物理] Cosmological Simulation

虚拟现实
~~~~~~~~

- [开源] Unreal Engine
- Unity3D
- `List of game engines <https://en.wikipedia.org/wiki/List_of_game_engines>`_

三维图形应用程序接口（API）
---------------------------

除了使用集成软件（IDE）辅助设计，我们也可以使用应用程序接口（API）处理三维模型。
这些API对于计算机图形硬件厂商也是极为重要的，因为他们提供给程序员一种使用硬件的抽象方式，而依然能够利用那个显卡的特定硬件的长处。

这些三维计算机图形的API颇为流行：

- OpenGL和OpenGL着色语言
- OpenGL ES嵌入式设备的三维API
- Direct3D（DirectX的子集）
- RenderMan
- RenderWare

也有一些高层的三维场景图API，他们提供在底层绘制API之上的附加功能。处于活跃的发展中的这类程序库包括：

- QSDK
- Quesa
- Java 3D
- JSR 184（M3G）
- NVidia Scene Graph
- OpenSceneGraph
- OpenSG
- OGRE
- Irrlicht

.. _渲染: https://en.wikipedia.org/wiki/Visualization_(graphics)



参考文献
--------

.. footbibliography::
