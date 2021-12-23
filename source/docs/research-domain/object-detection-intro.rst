============
目标检测介绍
============

基本概念
--------

目标检测，从字面意思上来看，它是说从一幅图像中识别出目标。

目标检测主要分为三类 [6]_ ：

.. image:: ../../_static/images/obj-det-types.png

- 图像分类，预测图像中是否包含某个目标，代表算法如 CNN；
- 预测图像中是否包含某个目标，并对它进行定位，代表算法如 YOLO，R-CNN；
- 预测图像中包含的多个目标，并对他们进行定位，代表算法如 YOLO，R-CNN。

研究这三类问题主要有两种方法：

.. image:: ../../_static/images/obj-det-methods.png

- 边界框检测（注，bbox = Bounding Box）
- 特征点检测（landmark detection）

需要注意的是，边界框和锚框的区别：锚框是一组预定义的大小确定的边界框。
目标检测算法通常会在输入图像中采样大量的区域，然后判断这些区域中是否包含我们感兴趣的目标，
并调整区域边缘从而更准确低预测目标的真实边界框（ground-truth bounding box） [4]_ 。
需要注意的是，以像素为中心分别生成多个大小不等的锚框，指的是通常意义上的滑动窗口。
滑动窗口的运算量极大，包含大量的重复计算，因此出现了像 YOLO 这样的改进算法。

.. image:: ../../_static/images/obj-det-yolo-init.png

不同的算法会采用不用的采样方法。以 YOLO 为例（上图所示 [5]_ ），它首先将图像划分为网格结构，每个网格都是一个锚框。
所有锚框以平铺的方式占满图像，对每个网格应用 CNN 预测 :math:`y` ，进而调整区域边缘。
YOLO 的锚框可以看成是 :math:`stride = b_w` 的滑动窗口。

如果一幅图像中包含多个目标，可以同时设定多个大小不等的锚框，分别平铺整个图像。而预测步骤与前述无异。

需要注意的是，目标检测通常也是监督学习方法，我们需要设定标签，通常情况下有两种设置方式：

1. 左上角坐标 :math:`(x_1, y_1)` ，右下角坐标 :math:`(x_2, y_2)` ，合起来 :math:`(x_1, y_1, x_2, y_2)` 。
2. 中心点坐标 :math:`(b_x, b_y)` ，锚框高度 :math:`b_h` ，锚框宽度 :math:`b_w` ，合起来 :math:`(b_x, b_y, b_h, b_w)` 。

两种方式任选一种，然后整个网络的标签可以用如法方式表示：

.. image:: ../../_static/images/obj-det-label-demo.png

模型训练完成后，通常用交并比（Intersection over Union，IoU）来评价模型效果：

.. image:: ../../_static/images/obj-det-assessment.png

常用的基本思路是：1）生成多个候选框，2）计算每个候选框的概率，3）使用非最大抑制方法移除部分候选框。

.. image:: ../../_static/images/obj-det-main-idea.png


非极大值抑制（Non-Maximum Suppression，NMS）算法流程：

假设现在有 6 个候选框（A、B、C、D、E、F）对小熊进行预测，

1. 首先计算每个候选框的概率，保留概率最大的候选框，比如 F；
2. 将 F 和其余 5 个候选框计算 IoU，去除结果大于阈值的候选框，比如 A、C、E；
3. 在剩下的 B、D 中，保留概率较大者，重复步骤 2、3，对比 B 和 D。

就这样一直重复，找到所有被保留下来的矩形框 [7]_ [8]_。多分类对每个类别分别应用 NMS [8]_。

以上是我于 2021 年 11 月 22 日 `PPT <https://kdocs.cn/l/cd1NvZhHxEyh>`_ 中的部分摘录。

技术分类
--------

- Anchor based

  - One-stage（速度更快）：SSD、DSSD、\ **RetinaNet**\ 、RefineDet、YOLOV3
  - Two-stage（精度更高）：Faster-RCNN、R-FCN、FPN、Cascade R-CNN、SNIP

- Anchor-free

  - Keypoint：CornerNet、CenterNet、CornerNet-Lite
  - Segmentation：FSAF、\ **FCOS**\ 、FoveaBox

Anchor-based
    与锚点框相关超参 (scale、aspect ratio、IoU Threshold) 会较明显的影响最终预测效果；
    预置的锚点大小、比例在检测差异较大物体时不够灵活；
    大量的锚点会导致运算复杂度增大，产生的参数较多；
    容易导致训练时 negative 与 positive 的比例失衡。

Anchor-free
    使用类似分割的思想来解决目标检测问题；
    不需要调优与 anchor 相关的超参数；
    避免大量计算 GT boxes 和 anchor boxes 之间的 IoU，使得训练过程占用内存更低。

Label Assignment in Object Detection
    label assignment 就是要对目标检测中的 anchor box 或者 anchor point 打上 label，
    是positive、negative 还是 ignore。这里面有两个挑战，一个挑战是 negative 非常多，容易导致样本不均衡问题；
    另一个挑战是判定标准只能经验性地设置，然后通过实验结果来验证，基本是一个 trial and error 的过程 [1]_ 。
    另外，参考 [2]_ [3]_
    

相关工具
--------

- `MMDetection <https://mmdetection.readthedocs.io/en/latest/>`_

参考文献
--------

.. [1] https://zhuanlan.zhihu.com/p/166275032
.. [2] https://zhuanlan.zhihu.com/p/160991530
.. [3] https://zhuanlan.zhihu.com/p/136048045
.. [4] `边界框（bounding box） — PaddleEdu documentation <https://paddlepedia.readthedocs.io/en/latest/tutorials/computer_vision/object_detection/Bounding_Box_Anchor.html>`_
.. [5] `Anchor Boxes for Object Detection - MATLAB & Simulink - MathWorks 中国 <https://ww2.mathworks.cn/help/vision/ug/anchor-boxes-for-object-detection.html>`_
.. [6] `[金山文档] super-cheatsheet-deep-learning.pdf <https://kdocs.cn/l/caIiLHnpo5UV>`_
.. [7] `[金山文档] 动手学深度学习（第 2 版）PyTorch 实现 13.4.锚框 <https://kdocs.cn/l/crOymfQ4SKRt>`_
.. [8] https://www.cnblogs.com/makefile/p/nms.html
