# Spring Boot

## 使用 Spring 框架的好处是什么

Spring 提供 IoC 技术，容器会帮你管理依赖的对象，从而不需要自己创建和管理依赖对象了，更轻松的实现了程序的解耦。

Spring 提供了事务支持，使得事务操作变的更加方便。

Spring 提供了 AOP 面向切片编程，这样可以更方便的处理某一类的问题。

更方便的框架集成，Spring 可以很方便的集成其他框架，比如 MyBatis、Hibernates 等。

## 简述核心容器（Spring Context 应用上下文）模块

这是基本的 Spring 模块，提供 Spring 框架的基础功能，BeanFactory 是任何以 Spring 为基础的应用的核心。Spring 框架建立在此模块之上，它使 Spring 成为一个容器。

Bean 工厂是工厂模式的一个实现，提供了控制反转功能，用来把应用的配置和依赖从真正的应用代码中分离。最常用的就是`org.springframework.beans.factory.xml.XmlBeanFactory`，它根据 XML 文件中的定义加载 Beans。该容器从 XML 文件读取配置元数据并用它去创建一个完全配置的系统或应用。

## 什么是 IoC

Spring 的核心就是提供了一个 IoC 容器，它可以管理所有轻量级的 Bean 组件，提供的底层服务包括组件的生命周期管理、配置和组装服务、AOP 支持，以及建立在 AOP 基础上的声明式事务服务等。

Inversion of Control（控制反转）是 Spring 的核心。对于 Spring 框架来说，就是由 Spring 来负责控制对象的生命周期和对象间的关系。简单来说，控制指的是当前对象对内部成员的控制权。控制反转指的是，在 IoC 模式下，控制权发生了反转，即从应用程序转移到了 IoC 容器，所有组件不再由应用程序自己创建和配置，而是由 IoC 容器负责，这样，应用程序只需要直接使用已经创建好并且配置好的组件。

因此，IoC 也称为依赖注入。IoC 的一个实现就是 BeanFactory。

## 什么是 AOP

AOP 是面向切面编程，其实，我们不用关心 AOP 创造的 "术语"，只需要理解 AOP 本质上只是一种代理模式的实现方式，在 Spring 的容器中实现 AOP 特别方便。简单来说就是统一处理某一 "切面"（类）的问题的编程思想，比如统一处理日志、异常等。

## AOP 的代理有哪几种方式

AOP 思想的实现一般都是基于代理模式，在 Java 中一般采用 JDK 动态代理模式，但是我们都知道，JDK 动态代理模式只能代理接口而不能代理类。

因此，Spring AOP 会按照下面两种情况进行切换，因为 Spring AOP 同时支持 CGLIB、ASPECTJ、JDK 动态代理。

- 如果目标对象的实现类实现了接口，Spring AOP 将会采用 JDK 动态代理来生成 AOP 代理类；
- 如果目标对象的实现类没有实现接口，Spring AOP 将会采用 CGLIB 来生成 AOP 代理类。

不过这个选择过程对开发者完全透明、开发者也无需关心。

## 怎么实现 JDK 动态代理

实现 `java.lang.reflect.InvocationHandler` 中的 `invoke` 接口。

## AOP 的基本概念

- 切面（Aspect）：官方的抽象定义为 "一个关注点的模块化，这个关注点可能会横切多个对象"。
- 连接点（Joinpoint）：程序执行过程中的某一行为。
- 通知（Advice）："切面" 对于某个 "连接点" 所产生的动作。
- 切入点（Pointcut）：匹配连接点的断言，在 AOP 中通知和一个切入点表达式关联。
- 目标对象（Target Object）：被一个或者多个切面所通知的对象。
- AOP 代理（AOP Proxy）：在 Spring AOP 中有两种代理方式，JDK 动态代理和 CGLIB 代理。

## 通知类型（Advice）有哪些

- 前置通知（Before advice）：在某连接点（JoinPoint）之前执行的通知，但这个通知不能阻止连接点前的执行。ApplicationContext 中在 < aop:aspect > 里面使用 < aop:before > 元素进行声明；
- 后置通知（After advice）：当某连接点退出的时候执行的通知（不论是正常返回还是异常退出）。ApplicationContext 中在 < aop:aspect > 里面使用 < aop:after > 元素进行声明。
- 返回后通知（After return advice ：在某连接点正常完成后执行的通知，不包括抛出异常的情况。ApplicationContext 中在 < aop:aspect > 里面使用 < after-returning > 元素进行声明。
- 环绕通知（Around advice）：包围一个连接点的通知，类似 Web 中 Servlet规范中的 Filter 的 doFilter 方法。可以在方法的调用前后完成自定义的行为，也可以选择不执行。ApplicationContext 中在 < aop:aspect > 里面使用 < aop:around > 元素进行声明。
- 抛出异常后通知（After throwing advice）：在方法抛出异常退出时执行的通知。ApplicationContext 中在 < aop:aspect > 里面使用 < aop:after-throwing > 元素进行声明。

## Bean 的生命周期

在传统的 Java 应用中，Bean 的生命周期很简单，使用 Java 关键字 new 进行 Bean 的实例化，然后该 Bean 就能够使用了。一旦 Bean 不再被使用，则由 Java 自动进行垃圾回收。

相比之下，Spring 管理 Bean 的生命周期就复杂多了，正确理解 Bean 的生命周期非常重要，因为 Spring 对 Bean 的管理可扩展性非常强，下面展示了一个 Bean 的构造过程：

- Spring 启动，查找并加载需要被 Spring 管理的 Bean，进行 Bean 的实例化；
- Bean 实例化后，对 Bean 的引入和值注入到 Bean 的属性中；
- 如果 Bean 实现了 BeanNameAware 接口的话，Spring 将 Bean 的 Id 传递给 setBeanName() 方法；
- 如果 Bean 实现了 BeanFactoryAware 接口的话，Spring 将调用 setBeanFactory() 方法，将 BeanFactory 容器实例传入；
- 如果 Bean 实现了 ApplicationContextAware 接口的话，Spring 将调用 Bean 的 setApplicationContext() 方法，将 Bean 所在应用上下文引用传入进来；
- 如果 Bean 实现了 BeanPostProcessor 接口，Spring 就将调用它们的 postProcessBeforeInitialization() 方法；
- 如果 Bean 实现了 InitializingBean 接口，Spring 将调用它们的 afterPropertiesSet() 方法。类似地，如果 Bean 使用 init-method 声明了初始化方法，该方法也会被调用；
- 如果 Bean 实现了 BeanPostProcessor 接口，Spring 就将调用它们的 postProcessAfterInitialization() 方法；
- 此时，Bean 已经准备就绪，可以被应用程序使用了。它们将一直驻留在应用上下文中，直到应用上下文被销毁；
- 如果 Bean 实现了 DisposableBean 接口，Spring 将调用它的 destory() 接口方法，同样，如果 Bean 使用了 destory-method 声明销毁方法，该方法也会被调用。

## Bean 的作用域

- singleton : 唯一 bean 实例，Spring 中的 bean 默认都是单例的；
- prototype : 每次请求都会创建一个新的 bean 实例；
- request：每一次 HTTP 请求都会产生一个新的 bean，该 bean 仅在当前 HTTP request 内有效；
- session : 每一次 HTTP 请求都会产生一个新的 bean，该 bean 仅在当前 HTTP session 内有效；
- global-session：全局 session 作用域，仅仅在基于 portlet 的 web 应用中才有意义，Spring5 已经没有了。Portlet 是能够生成语义代码（例如：HTML）片段的小型 Java Web 插件。它们基于 portlet 容器，可以像 servlet 一样处理 HTTP 请求。但是，与 servlet 不同，每个 portlet 都有不同的会话。

## 单例 Bean 的线程安全问题

Spring 中的 Bean 默认是单例模式，Spring 框架并没有对单例 Bean 进行多线程的封装处理。

实际上大部分时候 Spring Bean 无状态的（比如 DAO 类），所有某种程度上来说 Bean 也是安全的，但如果 Bean 有状态的话（比如 view model 对象），那就要开发者自己去保证线程安全了，最简单的就是改变 Bean 的作用域，把 "singleton" 变更为 "prototype"，这样请求 Bean 相当于 new Bean() 了，所以就可以保证线程安全了。

## Spring 事务的实现方式

声明式事务：声明式事务也有两种实现方式：

- 基于 xml 配置文件的方式

- 注解方式（在类上添加 @Transaction 注解）

编码方式：提供编码的形式管理和维护事务。

## Spring 事务的隔离级别

Spring 默认隔离级别是 ISOLATION_DEFAULT（使用数据库的设置），其他四个隔离级别和数据库的隔离级别一致。

## Spring 事务的传播行为

事务传播行为是为了解决业务层方法之间互相调用的事务问题。当事务方法被另一个事务方法调用时，必须指定事务应该如何传播。例如：方法可能继续在现有事务中运行，也可能开启一个新事务，并在自己的事务中运行。在 TransactionDefinition 定义中包括了如下几个表示传播行为的常量：

**支持当前事务的情况：**

- TransactionDefinition.PROPAGATION_REQUIRED：如果当前存在事务，则加入该事务；如果当前没有事务，则创建一个新的事务；
- TransactionDefinition.PROPAGATION_SUPPORTS：如果当前存在事务，则加入该事务；如果当前没有事务，则以非事务的方式继续运行；
- TransactionDefinition.PROPAGATION_MANDATORY：如果当前存在事务，则加入该事务；如果当前没有事务，则抛出异常。

**不支持当前事务的情况：**

- TransactionDefinition.PROPAGATION_REQUIRES_NEW：创建一个新的事务，如果当前存在事务，则把当前事务挂起；
- TransactionDefinition.PROPAGATION_NOT_SUPPORTED：以非事务方式运行，如果当前存在事务，则把当前事务挂起。
- TransactionDefinition.PROPAGATION_NEVER：以非事务方式运行，如果当前存在事务，则抛出异常。

**其他情况：**

- TransactionDefinition.PROPAGATION_NESTED：如果当前存在事务，则创建一个事务作为当前事务的嵌套事务来运行；如果当前没有事务，则该取值等价于 TransactionDefinition.PROPAGATION_REQUIRED。

## Spring 常用的注入方式

- 构造器依赖注入：构造器依赖注入通过容器触发一个类的构造器来实现的，该类有一系列参数，每个参数代表一个对其他类的依赖。
- Setter 方法注入：Setter 方法注入是容器通过调用无参构造器或无参 static 工厂方法实例化 bean 之后，调用该 bean 的 Setter 方法，即实现了基于 Setter 的依赖注入。
- 基于注解的注入：最好的解决方案是用构造器参数实现强制依赖，Setter 方法实现可选依赖。

## Spring 用到了哪些设计模式

- 工厂模式：BeanFactory 就是简单工厂模式的体现，用来创建对象的实例；
- 单例模式：Bean 默认为单例模式。
- 代理模式：Spring 的 AOP 功能用到了 JDK 的动态代理和 CGLIB 字节码生成技术；
- 模板方法：用来解决代码重复的问题。比如 RestTemplate，JmsTemplate，JpaTemplate。
- 观察者模式：定义对象键一种一对多的依赖关系，当一个对象的状态发生改变时，所有依赖于它的对象都会得到通知被制动更新，如Spring 中 listener 的实现 ApplicationListener。

## ApplicationContext 通常的实现有哪些

- FileSystemXmlApplicationContext：此容器从一个 XML 文件中加载 beans 的定义，XML Bean 配置文件的全路径名必须提供给它的构造函数。
- ClassPathXmlApplicationContext：此容器也从一个 XML 文件中加载 beans 的定义，这里，你需要正确设置 classpath 因为这个容器将在 classpath 里找 bean 配置。
- WebXmlApplicationContext：此容器加载一个 XML 文件，此文件定义了一个 Web 应用的所有 bean。

## 谈谈你对 MVC 模式的理解

MVC 是 Model —— View —— Controler 的简称，它是一种架构模式，它分离了表现与交互。

它被分为三个核心部件：模型、视图、控制器。

- Model（模型）：是程序的主体部分，主要包含业务数据和业务逻辑。在模型层，还会涉及到用户发布的服务，在服务中会根据不同的业务需求，更新业务模型中的数据。
- View（视图）：是程序呈现给用户的部分，是用户和程序交互的接口，用户会根据具体的业务需求，在 View 视图层输入自己特定的业务数据，并通过界面的事件交互，将对应的输入参数提交给后台控制器进行处理。
- Controller（控制器）：Controller 是用来处理用户输入数据，以及更新业务模型的部分。控制器中接收了用户与界面交互时传递过来的数据，并根据数据业务逻辑来执行服务的调用和更新业务模型的数据和状态。

## SpringMVC 的工作原理/执行流程

- SpringMVC 先将请求发送给 DispatcherServlet。
- DispatcherServlet 查询一个或多个 HandlerMapping，找到处理请求的 Controller。
- DispatcherServlet 再把请求提交到对应的 Controller。
- Controller 进行业务逻辑处理后，会返回一个 ModelAndView。
- Dispathcher 查询一个或多个 ViewResolver 视图解析器，找到 ModelAndView 对象指定的视图对象。
- 视图对象负责渲染返回给客户端。

## SpringMVC 的核心组件有哪些

- 前置控制器 DispatcherServlet。
- 映射控制器 HandlerMapping。
- 处理器 Controller。
- 模型和视图 ModelAndView。
- 视图解析器 ViewResolver。

## SpringMVC 常用的注解有哪些

- @RequestMapping：用于处理请求 URL 映射的注解，可用于类或方法上。用于类上，则表示类中的所有响应请求的方法都是以该地址作为父路径；
- @RequestBody：实现接收 HTTP 请求的 JSON 数据，将 JSON 转换为 Java 对象；
- @ResponseBody：注解实现将 Controller 方法返回对象转化为 JSON 对象响应给客户。

## @RequestMapping 的作用是什么

将 http 请求映射到相应的类/方法上。

## @Autowired 的作用是什么

@Autowired 它可以对类成员变量、方法及构造函数进行标注，完成自动装配的工作，通过 @Autowired 的使用来消除 set/get 方法。

## SpringMVC 的控制器是不是单例模式

是单例模式，所以在多线程访问的时候有线程安全问题。但是不要使用同步，会影响性能，解决方案是在控制器里面不能写字段。

## SpringMVC 怎么样设定重定向和转发的

- 转发：在返回值前面加 "forward:"，譬如： `"forward:user.do?name=method2"`
- 重定向：在返回值前面加 "redirect:"

## SpringMVC 里面拦截器是怎么写的

- 方法一：实现 HandlerInterceptor 接口；
- 方法二：继承适配器类，接着在接口方法当中，实现处理逻辑，然后在 SpringMVC 的配置文件中配置拦截器即可。

## 什么是 Spring Boot

Spring Boot 是为 Spring 服务的，是用来简化新 Spring 应用的初始搭建以及开发过程的。

## 为什么要用 Spring Boot

- 配置简单
- 独立运行自动装配
- 无代码生成和 xml 配置
- 提供应用监控
- 易上手
- 提升开发效率

## Spring Boot 核心配置文件是什么

bootstrap.properties 或 application.properties

## JPA 和 Hibernate 有什么区别

JPA 全称 Java Persistence API，是 Java 持久化接口规范，Hibernate 属于 JPA 的具体实现。

## 什么是 Spring Cloud

Spring Cloud 是一系列框架的有序集合。

它利用 Spring Boot 的开发便利性巧妙地简化了分布式系统基础设施的开发，如服务发现注册、配置中心、消息总线、负载均衡、断路器、数据监控等，都可以用 Spring Boot 的开发风格做到一键启动和部署。

## Spring Cloud 的核心组件有哪些

- Eureka：服务注册于发现。
- Feign：基于动态代理机制，根据注解和选择的机器，拼接请求 URL 地址，发起请求。
- Ribbon：实现负载均衡，从一个服务的多台机器中选择一台。
- Hystrix：提供线程池，不同的服务走不同的线程池，实现了不同服务调用的隔离，避免了服务雪崩的问题。
- Zuul：网关管理，由 Zuul 网关转发请求给对应的服务。

## Spring Cloud 断路器的作用是什么

在分布式架构中，断路器模式的作用也是类似的，当某个服务单元发生故障（类似用电器发生短路）之后，通过断路器的故障监控（类似熔断保险丝），向调用方返回一个错误响应，而不是长时间的等待。这样就不会使得线程因调用故障服务被长时间占用不释放，避免了故障在分布式系统中的蔓延。

## 为什么要使用 hibernate

- hibernate 是对 jdbc 的封装，大大简化了数据访问层的繁琐的重复性代码。
- hibernate 是一个优秀的 ORM 实现，很多程度上简化了 DAO 层的编码功能。
- 可以很方便的进行数据库的移植工作。
- 提供了缓存机制，是程序执行更改的高效。

## 什么是 ORM 框架

ORM（Object Relation Mapping）对象关系映射，是把数据库中的关系数据映射成为程序中的对象。

使用 ORM 的优点：提高了开发效率降低了开发成本、开发更简单更对象化、可移植更强。

## hibernate 实体类可以被定义为 final 吗

实体类可以定义为 final 类，但这样的话就不能使用 hibernate 代理模式下的延迟关联提供性能了，所以不建议定义实体类为 final。

## 在 hibernate 中使用 Integer 和 int 做映射有什么区别

Integer 类型为对象，它的值允许为 null，而 int 属于基础数据类型，值不能为 null。

## hibernate 是如何工作的

- 读取并解析配置文件。
- 读取并解析映射文件，创建 SessionFactory。
- 打开 Session。
- 创建事务。
- 进行持久化操作。
- 提交事务。
- 关闭 Session。
- 关闭 SessionFactory。

## 说一下 hibernate 的缓存机制

hibernate 常用的缓存有一级缓存和二级缓存：

- 一级缓存：也叫 Session 缓存，只在 Session 作用范围内有效，不需要用户干涉，由 hibernate 自身维护，可以通过：evict(object)清除 object 的缓存；clear()清除一级缓存中的所有缓存；flush()刷出缓存；

- 二级缓存：应用级别的缓存，在所有 Session 中都有效，支持配置第三方的缓存，如：EhCache。

## hibernate 对象有哪些状态

- 临时/瞬时状态：直接 new 出来的对象，该对象还没被持久化（没保存在数据库中），不受 Session 管理。

- 持久化状态：当调用 Session 的 save/saveOrupdate/get/load/list 等方法的时候，对象就是持久化状态。

- 游离状态：Session 关闭之后对象就是游离状态。

## get() 和 load() 的区别

- 数据查询时，没有 OID 指定的对象，get() 返回 null；load() 返回一个代理对象。
- load() 支持延迟加载；get() 不支持延迟加载。

## 在 hibernate 中 getCurrentSession 和 openSession 的区别是什么

getCurrentSession 会绑定当前线程，而 openSession 则不会。

getCurrentSession 事务是 Spring 控制的，并且不需要手动关闭，而 openSession 需要我们自己手动开启和提交事务。

## hibernate 实体类必须要有无参构造函数吗？为什么？

hibernate 中每个实体类必须提供一个无参构造函数，因为 hibernate 框架要使用 reflection api，通过调用 ClassnewInstance() 来创建实体类的实例，如果没有无参的构造函数就会抛出异常。