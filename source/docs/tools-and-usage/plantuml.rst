==============
PlantUML 入门
==============

.. tip:: 
    
    本文并未提供更多细节，比如 `画类图在这里找不见合适的图形怎么办 <https://www.uml-diagrams.org/class-reference.html>`_ 、
    `我们使用 UML 处理业务需求时有哪些模型可以参考 <https://www.uml-diagrams.org/index-examples.html>`_
    以及 `PlantUML 给我们提供了哪些更多的绘制方法 <https://plantuml.com/zh/>`_ 等都需要我们进一步参考官方的说明。

类图
-----

元素声明
~~~~~~~~

.. code-block:: text

    .. uml::

        @startuml

        class           ClassDemo           /'普通类'/
        abstract        AbstractClassDemo   /'抽象类'/
        interface       InterfaceDemo       /'接口'/
        annotation      AnnotationDemo      /'注释'/
        enum            EnumClassDemo       /'枚举'/
        circle          CircleDemo          /'圆'/
        diamond         DiamondDemo         /'菱形'/
        entity          EntityDemo          /'条目'/
        
        
        class Foo<? extends Element> {      /'泛型'/
            int size()
        }

        package foo3 <<Folder>> {           /'包'/
            class Class3
        }

        skinparam classAttributeIconSize 0 /'更改访问权限的表示方式'/

        abstract AbstractClassDemo {
            +{static} public_field          /'静态字段'/
            ~package_private_field
            #protected_field
            -private_field
            +{abstract} publicMethod()      /'抽象方法'/
            ~packagePrivateMethod()
            #protectedMethod()
            -privateMethod()
        }

        
        interface InterfaceDemo {
            +{static} public_field
            ~package_private_field
            #protected_field
            -private_field
            +{abstract} publicMethod() 
            ~packagePrivateMethod()
            #protectedMethod()
            -privateMethod()
        }

        @enduml

.. uml::

    @startuml

    class           ClassDemo           /'普通类'/
    abstract        AbstractClassDemo   /'抽象类'/
    interface       InterfaceDemo       /'接口'/
    annotation      AnnotationDemo      /'注释'/
    enum            EnumClassDemo       /'枚举'/
    circle          CircleDemo          /'圆'/
    diamond         DiamondDemo         /'菱形'/
    entity          EntityDemo          /'条目'/
    
    
    class Foo<? extends Element> {      /'泛型'/
        int size()
    }

    package foo3 <<Folder>> {           /'包'/
        class Class3
    }

    skinparam classAttributeIconSize 0 /'更改访问权限的表示方式'/

    abstract AbstractClassDemo {
        +{static} public_field          /'静态字段'/
        ~package_private_field
        #protected_field
        -private_field
        +{abstract} publicMethod()      /'抽象方法'/
        ~packagePrivateMethod()
        #protectedMethod()
        -privateMethod()
    }

    
    interface InterfaceDemo {
        +{static} public_field
        ~package_private_field
        #protected_field
        -private_field
        +{abstract} publicMethod() 
        ~packagePrivateMethod()
        #protectedMethod()
        -privateMethod()
    }

    @enduml

类之间的关系
~~~~~~~~~~~~

.. code-block:: text

    .. uml::

        @startuml

        AbsClass ^-- ImplClass                  /'抽象类的实现'/
        Interface <|.. ImplClass                /'接口的实现'/
        ImplClass <|-- ChildClass               /'继承'/
        ImplClass #-- UsePort                   /'使用接口'/
        ChildClass -- AssocClass                /'关联'/
        (ChildClass, AssocClass) .. AnnotClass  /'产生关联的类或注释'/
        GooseGroup o-- Goose : belong to <      /'聚合（末端箭头可加可不加）'/
        Goose "1" *-- "2" Wings                 /'组合（末端箭头可加可不加）'/
        Wings *--> Feather : have >             /'组合（末端箭头可加可不加）'/
        OuterClass +-- InnerClass               /'内部类或嵌套关系'/
        Source --> Target1  /'Source 可以导航到 Target，但是不知道 Target 能否导航到 Source'/
        Target2 x-- Source  /'不能从 Target2 导航到 Source，但是不知道能否从 Source 导航到 Target2'/
        Client ..> Supplier                     /'依赖'/

        class ImplClass {
            +port()
        }

        abstract AbsClass
        interface Interface
    
        @enduml

.. uml::

    @startuml

    AbsClass ^-- ImplClass                  /'抽象类的实现'/
    Interface <|.. ImplClass                /'接口的实现'/
    ImplClass <|-- ChildClass               /'继承'/
    ImplClass #-- UsePort                   /'使用接口'/
    ChildClass -- AssocClass                /'关联'/
    (ChildClass, AssocClass) .. AnnotClass  /'产生关联的类或注释'/
    GooseGroup o-- Goose : belong to <      /'聚合（末端箭头可加可不加）'/
    Goose "1" *-- "2" Wings                 /'组合（末端箭头可加可不加）'/
    Wings *--> Feather : have >             /'组合（末端箭头可加可不加）'/
    OuterClass +-- InnerClass               /'内部类或嵌套关系'/
    Source --> Target1  /'Source 可以导航到 Target，但是不知道 Target 能否导航到 Source'/
    Target2 x-- Source  /'不能从 Target2 导航到 Source，但是不知道能否从 Source 导航到 Target2'/
    Client ..> Supplier                     /'依赖'/

    class ImplClass {
        +port()
    }

    abstract AbsClass
    interface Interface

    @enduml

