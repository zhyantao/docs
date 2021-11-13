==============
小样本学习调研
==============

新手入门
--------

科普视频
~~~~~~~~

- 元学习与小样本学习 `王树森 <https://space.bilibili.com/1369507485>`__
  on `哔哩哔哩 <https://www.bilibili.com/medialist/play/ml1245757985/BV1B44y1r75K>`__
  Slide `Introduction <https://kdocs.cn/l/cpTe5jubAGog>`_/\ 
  `Siamese Network <https://kdocs.cn/l/cvbUxZGl0zwe>`_/\ 
  `Pretraining & Fine Tuning <https://kdocs.cn/l/cbBZGuwm26Yr>`_
- 深度强化学习 `王树森 <https://www.youtube.com/c/ShusenWang>`__
  on `YouTube <https://www.youtube.com/watch?v=vmkRMvhCW5c&list=PLvOO0btloRnsiqM72G4Uid0UWljikENlU>`__
  Slide `Intro <https://kdocs.cn/l/cnurQ40MrFLJ>`_/\
  `Value-Based <https://kdocs.cn/l/couQ5BWFzS57>`_/\
  `Policy-Based <https://kdocs.cn/l/cguX6PpD6QSb>`_/\ 
  `Actor-Critic Methods <https://kdocs.cn/l/cbNH5Phx6tnZ>`_/\ 
  `Model-Based <https://kdocs.cn/l/ceckin3M9Eat>`_
- 王树森课程讲义 `深度强化学习.PDF <https://kdocs.cn/l/cmGWnLP1u5VF>`__

科普博文
~~~~~~~~

- `Model-Agnostic Meta-Learning（MAML）模型介绍及算法详解 <https://zhuanlan.zhihu.com/p/57864886>`_
- `MAML算法，model-agnostic metalearnings? <https://www.zhihu.com/question/266497742>`_
- `元学习的前世今生 <https://zhuanlan.zhihu.com/p/146877957>`_
- `从 CVPR 2019 一览小样本学习研究进展 <https://www.leiphone.com/category/academic/4wc0990rNQf43mss.html>`_ 每年 CVPR 都会有针对小样本学习的一个总结
- `Learning to learn - The Berkeley Artificial Intelligence Research <https://bair.berkeley.edu/blog/2017/07/18/learning-to-learn/>`_
- `Meta-Learning: Learning to Learn Fast <https://lilianweng.github.io/lil-log/2018/11/30/meta-learning.html>`_ 
  及 `译文 <https://wei-tianhao.github.io/blog/2019/09/17/meta-learning.html>`__
- `元学习（Meta Learning）与迁移学习（Transfer Learning）的区别联系是什么？ <https://www.zhihu.com/question/299020462/answer/1009811572>`_
- `How to train your MAML: A step by step approach <https://www.bayeswatch.com/2018/11/30/HTYM/>`_
- `An Introduction to Meta-Learning <https://medium.com/walmartglobaltech/an-introduction-to-meta-learning-ced7072b80e7>`_
- `From zero to research — An introduction to Meta-learning <https://medium.com/huggingface/from-zero-to-research-an-introduction-to-meta-learning-8e16e677f78a>`_
- `Meta Reinforcement Learning <https://lilianweng.github.io/lil-log/2019/06/23/meta-reinforcement-learning.html>`_
- `Meta-Learning: Learning to Learn Fast <https://lilianweng.github.io/lil-log/2018/11/30/meta-learning.html>`_

领域综述
~~~~~~~~

- Generalizing from a Few Examples: A Survey on Few-Shot Learning `笔记 <https://kdocs.cn/l/ce6RjgEp9WT9>`_ 
  及 `文章解读 <https://zhuanlan.zhihu.com/p/129786553>`_
- `Meta-Learning in Neural Networks: A Survey <https://arxiv.org/pdf/2004.05439.pdf>`_
- `A CLOSER LOOK AT FEW-SHOT CLASSIFICATION <https://arxiv.org/pdf/1904.04232.pdf>`_
- `A Baseline for Few-Shot Image Classification <https://arxiv.org/pdf/1909.02729.pdf>`_

教学视频
~~~~~~~~

- CS 330: Deep Multi-Task and Meta Learning `主页 <http://cs330.stanford.edu/>`__ 或 `哔哩哔哩 <https://www.bilibili.com/video/BV1He411s7K4>`__ 17.75 小时
- Chelsea Finn: Meta-Learning: from Few-Shot Learning to Rapid  Reinforcement Learning `主页 <https://sites.google.com/view/icml19metalearning>`__
  或 `哔哩哔哩 <https://www.bilibili.com/video/BV1o4411A7YE>`__
- Chelsea Finn: Building Unsupervised Versatile Agents with Meta-Learning `YouTube  <https://www.youtube.com/watch?v=i05Fk4ebMY0>`__ 1 小时
- 李宏毅：Meta Learning `YouTube <http://speech.ee.ntu.edu.tw/~tlkagk/courses_ML20.html>`__
  或 `哔哩哔哩 <https://www.bilibili.com/video/BV1pQ4y1K7cw?p=32>`__

特邀演讲
~~~~~~~~

- Generalizing from Few Examples with Meta-Learning by Hugo Larochelle `Video <https://www.bilibili.com/video/av61821192/>`__ 
  及 `Slides <https://kdocs.cn/l/cpswKp8xJuZj>`__
- Workshop on Meta-Learning (MetaLearn 2021) `Video <https://meta-learn.github.io/>`__
- Deep Learning: Bridging Theory and Practice `Video <https://ludwigschmidt.github.io/nips17-dl-workshop-website/>`__
- Challenges in Multi-Task Learning and Meta-Learning `Video <https://www.youtube.com/watch?v=Rq40Bze_hMA>`__ 
  及 `Slides <https://ai.stanford.edu/~cbfinn/_files/ias_slides.pdf>`__
- The Big Problem with Meta-Learning and How Bayesians Can Fix It 
  `Video <https://slideslive.com/38922670/invited-talk-the-big-problem-with-metalearning-and-how-bayesians-can-fix-it>`__ 
  及 `Slides <https://ai.stanford.edu/~cbfinn/_files/neurips19_memorization.pdf>`__

小样本学习方法
--------------

- **Data Augmentation / Hallucination Based / Sample Synthesis (learn to augment data)**

  - GAN: Covariance-Preserving Adversarial Augmentation Networks - 2018 NeurIPS
  - Low-Shot Learning from Imaginary Data - 2018 CVPR
  - :math:`\Delta`-encoder: Sample Synthesis - 2018 NeurIPS
  - Semantic Feature Augmentation - 2018 arXiv

- **Metric-Learning Based (learn to compare)**

  - Siamese Network - 2015 ICML
  - Matching Network - 2016 NIPS
  - Prototype Network - 2017 NIPS
  - Relation Network - 2018 CVPR
  - Covariance Metric Network - 2019 AAAI
  - Deep Nearest Neighbor Neural Network - 2019 CVPR
  - Large Margin Meta-Learning - 2018 arXiv
  - RepMet: Few-Shot Detection - 2019 CVPR

- **Meta-Learning Based (learn to learn)**

  - **Recurrent meta-learners**

    - Matching Network - 2016 NIPS
    - `MANN: Memory-Augmented Neural Network <https://kdocs.cn/l/crnNROG2VCMf>`_ - 2016 ICML

  - **Optimizers**

    - MAML: Model-Agnostic Meta-Learning - 2017 ICML
    - Meta-SGD - 2017 arXiv
    - LEO: Meta-Learning with Latent Embedding Optimization - 2019 ICLR
    - Reptile - 2018 arXiv
    - Meta-Learner LSTM - 2017 ICLR
    - Dynamic FSL - 2018 CVPR
    - MTL: Meta-Transfer Learning - 2019 CVPR
    - Meta Network - 2017 ICML

- **Finetune Based**

  - Baseline for Few-Shot Image Classification - 2019 arXiv

算法实现
--------

- `Papers With Code: Few-Shot Learning <https://paperswithcode.com/task/few-shot-learning>`_

数据集
~~~~~~

- `Omniglot data set for one-shot learning <https://github.com/brendenlake/omniglot>`_ 及 `Paper <https://kdocs.cn/l/cgtqdhdNglDz>`_
- `Tools for mini-ImageNet Dataset <https://github.com/yaoyao-liu/mini-imagenet-tools>`_
- `ImageNet Large Scale Visual Recognition Challenge (ILSVRC) <https://image-net.org/challenges/LSVRC/>`_
- `FGVC-Aircraft Benchmark <https://www.robots.ox.ac.uk/~vgg/data/fgvc-aircraft/>`_
- `Caltech-UCSD Birds-200-2011 <http://www.vision.caltech.edu/visipedia/CUB-200-2011.html>`_
- `google-research/meta-dataset <https://github.com/google-research/meta-dataset>`_
- `relevant-awesome-datasets-repo - Few shot <https://github.com/Duan-JM/awesome-papers-fewshot#relevant-awesome-datasets-repo>`_
- 评价强化学习模型效果的工具： `OpenAI Gym <http://gym.openai.com/>`_

领域学者
--------

- `Chelsea Finn <https://ai.stanford.edu/~cbfinn/>`_, UC Berkeley
- `Pieter Abbeel <https://people.eecs.berkeley.edu/~pabbeel/>`_, UC Berkeley
- `Erin Grant <https://people.eecs.berkeley.edu/~eringrant/>`_,UC Berkeley
- `Raia Hadsell <http://raiahadsell.com/index.html>`_, DeepMind
- `Misha Denil <http://mdenil.com/>`_, DeepMind
- `Adam Santoro <https://scholar.google.com/citations?hl=en&user=evIkDWoAAAAJ&view_op=list_works&sortby=pubdate>`_, DeepMind
- `Sachin Ravi <http://www.cs.princeton.edu/~sachinr/>`_, Princeton University
- `David Abel <https://david-abel.github.io/>`_, Brown University
- `Brenden Lake <https://cims.nyu.edu/~brenden/>`_, Facebook AI Research

参考文献
--------

1. `小样本学习与元学习资料调研：白小鱼 <https://youngfish42.yuque.com/docs/share/5cd14926-6954-4dca-bf39-d17c56fece53>`_
2. `Meta learning (computer science) <https://en.wikipedia.org/wiki/Meta_learning_(computer_science)>`_
3. `Awesome Meta Learning <https://github.com/sudharsan13296/Awesome-Meta-Learning>`_
4. `Meta-Learning-Papers <https://github.com/floodsung/Meta-Learning-Papers>`_
5. `FSL-Meta: A collection of resources for few-shot learning <https://github.com/tata1661/FSL-Mate>`_