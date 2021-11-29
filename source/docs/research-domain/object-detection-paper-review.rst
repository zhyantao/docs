============
目标检测调研
============

目标检测技术分类
----------------

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
    

目标检测工具集
--------------

- `MMDetection <https://mmdetection.readthedocs.io/en/latest/>`_

参考文献
--------

.. [1] https://zhuanlan.zhihu.com/p/166275032
.. [2] https://zhuanlan.zhihu.com/p/160991530
.. [3] https://zhuanlan.zhihu.com/p/136048045
