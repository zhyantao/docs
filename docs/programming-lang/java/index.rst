=============
Java 基础知识
=============

《Java 编程思想 :footcite:p:`BruceEckel2007Java`\ 》是一本优秀的 Java
学习教材，内容覆盖比较全面，但是也有一定的难度。
因此，我将自己觉得重要的部分整理了一下，在本文中做相关记录。

学习 Java 并不能仅限于学习 Java 这门语言本身，还有其他很多附属工具需要补充进知识体系。
这些附属工具出现的目的仅是简化开发流程，让业务人员不用太过关注与业务无关的代码逻辑。
但是，因为这些附属工具有很强的前后关联性，因此学习它们的先后顺序显得尤为重要，故制定以下学习路线供参考。

.. panels::
    :container: timeline
    :column: col-6 p-0
    :card:

    ---
    :column: +entry left

    Java / Servlet / Maven / Tomcat [`video <https://www.bilibili.com/video/BV12J411M7Sj?p=3>`__]
    ^^^

    ---
    :column: +right
    ---
    :column: +left
    ---
    :column: +entry right

    JavaScript [`webpage <https://wangdoc.com/javascript/>`__] [`webpage <https://zh.javascript.info/>`__] / Vue [:ref:`webpage <vue.js-basic>`]
    ^^^

    ---
    :column: +entry left

    MySQL / JDBC [`video <https://www.bilibili.com/video/BV1NJ411J79W>`__]
    ^^^

    ---
    :column: +right
    ---
    :column: +left
    ---
    :column: +entry right

    MyBatis-3 入门 [`webpage <https://mybatis.org/mybatis-3/zh/index.html>`__]
    ^^^

    ---
    :column: +entry left

    Spring、SpringMVC
    ^^^

    ---
    :column: +right
    ---
    :column: +left
    ---
    :column: +entry right

    Spring Boot / Spring Cloud
    ^^^

    ---
    :column: +entry left

    中间件 Redis / Kafka / Dubbo
    ^^^

    ---
    :column: +right
    ---
    :column: +left
    ---
    :column: +entry right

    JVM 原理 / Java 高并发
    ^^^

    ---
    :column: +entry left

    阅读《凤凰架构》项目代码
    ^^^


.. toctree::
    :titlesonly:
    :glob:
    :hidden:

    objects.rst
    metadata.rst
    initialization.rst
    access.rst
    reusing.rst
    polymorphism.rst
    interfaces.rst
    innerclasses.rst
    containers.rst
    exceptions.rst
    string.rst
    typeinfo.rst
    generics.rst
    arrays.rst
    io.rst
    enumerated.rst
    annotations.rst
    concurrency.rst

.. rubric:: 参考资料

.. footbibliography:: 
