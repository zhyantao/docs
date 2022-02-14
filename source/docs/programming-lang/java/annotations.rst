====
注解
====

什么是注解（Annotation）
------------------------

注解是放在Java源码的类、方法、字段、参数前的一种特殊 "注释"：

.. code-block:: java

    // this is a component:
    @Resource("hello")
    public class Hello {
        @Inject
        int n;

        @PostConstruct
        public void hello(@Param String name) {
            System.out.println(name);
        }

        @Override
        public String toString() {
            return "Hello";
        }
    }

注释会被编译器直接忽略，注解则可以被编译器打包进入 ``.class`` 文件，因此，注解是一种用作标注的 "元数据"。

元注解
------

元注解就是定义其他注解的注解。
比如 ``@Override`` 这个注解就不是一个元注解，而是通过元注解定义出来的。

.. code-block:: java

    @Target(ElementType.METHOD)
    @Retention(RetentionPolicy.SOURCE)
    public @interface Override {}

这里用到的 ``@Target`` 和 ``@Retention`` 就是元注解。

元注解只有四个：

- ``@Documented`` ：被修饰的注解类将被 javadoc 工具提取成文档
- ``@Inherited`` ：被修饰的注解类将具有继承性
- ``@Retention`` ：用于指定被修饰的注解可以存在于哪里（源代码、 ``.class`` 文件、运行时）
- ``@Target`` ：用于指定被修饰的注解修饰哪些程序单元（类、方法、字段）

自定义注解
----------

除了元注解，都是自定义注解。比如我们常用的 ``@Override`` 、 ``@Autowire``。

Java 语言使用 ``@interface`` 语法来定义自己的注解，格式如下：

.. code-block:: java

    @Retention(RetentionPolicy.RUNTIME)
    @Target(ElementType.METHOD)
    public @interface Report {
        int type() default 0;
        String level() default "info";
        String value() default "";
    }

注解的参数类似无参数方法，可以用 ``default`` 设定一个默认值（强烈推荐）。
最常用的参数应当命名为 ``value``。

一些常用的注解
--------------

**以下是 Java 中常用的注解：**

``@Override`` 表示当前方法覆盖了父类的方法。

``@Deprecation`` 表示方法已经过时，方法上有横线，使用时会警告。

``@SuppressWarnings`` 表示关闭一些警告信息。

``@SafeVarages`` 表示专门抑制 "堆污染" 警告提供的。

``@FunctionalInterface`` 用来指定某个接口必须是函数式接口，否则编译出错。

**以下是 Spring 中常用的注解：**

``@Configuration`` 把一个类作为 IoC 容器，它的某个方法上如果注册了 ``@Bean`` 就会作为该 Spring 容器中的 Bean。 

``@Scope`` 注解作用域。 

``@Lazy(true)`` 表示延迟初始化。 

``@Service`` 用于标注业务层组件。 

``@Controller`` 用于标注控制层组件。

``@Repository`` 用于标注数据访问组件，即 DAO 组件。

``@Component`` 泛指组件，当组件不好归类的时候，我们可以使用这个注解进行标注。 

``@Scope`` 用于指定 Scope 作用域（用在类上）。 

``@PostConstruct`` 用于指定初始化方法（用在方法上）。 

``@PreDestory`` 用于指定销毁方法（用在方法上）。 

``@DependsOn`` 定义 Bean 初始化及销毁时的顺序。 

``@Primary`` 自动装配时当出现多个 Bean 候选者时，被注解为 ``@Primary`` 的 Bean 将作为首选者，否则将抛出异常。 

``@Autowired`` 默认按类型装配，如果我们想使用按名称装配，可以结合 ``@Qualifier`` 注解一起使用。

``@Resource`` 默认按名称装配，当找不到与名称匹配的 Bean 才会按类型装配。 

``@PreDestroy`` 摧毁注解，默认，单例，启动就加载。

注解的存活时间
--------------

**由编译器使用的注解**

比如 ``@Override`` 、 ``@SuppressWarnings``，编译后，这些注解不会进入 ``.class`` 文件，编译后就被扔掉了。

**由工具处理 ``.class`` 文件使用的注解**

比如在加载 ``.class`` 文件到内存的时候，对 ``.class`` 文件做动态修改，以实现一些特殊功能。

**在运行时能够读取的注解**

他们加载后一直存在于 JVM 中，比如 ``@PostConstruct`` 的方法会在调用构造方法后自动被调用。

注解和反射的结合
----------------

注解和反射经常结合在一起，在很多框架中都能看到他们的影子。

可以通过反射来判断类、方法、字段上是否有某个注解，以及获取注解中的值。

当开发者使用注解修饰了类、方法、字段后，这些注解不会自己生效，必须由开发者提供相应的代码来提取并处理注解信息。
这些处理提取和处理注解的代码统称为 APT（Annotation Processing Tool）。

作为示例，我们首先提出一个需求：
项目经理想跟踪一个项目中现在一共实现了多少个的用例。如果某个用例已经实现了，那么就添加一个 ``@UseCase`` 标记。
这样，我们就可以很方便地掌控项目的进展。而且，当用户需求发生变更时，也更容易定位代码，修改需求实现。

然后，我们开始写代码，首先定义 ``@UseCase`` 注解：

.. code-block:: java

    //: annotations/UseCase.java
    import java.lang.annotation.*;

    @Target(ElementType.METHOD)
    @Retention(RetentionPolicy.RUNTIME)
    public @interface UseCase {
        public int id();
        public String description() default "no description";
    } ///:~

然后，尝试使用这个注解。把这个注解用于 ``PasswordUtils`` 类的某个方法上：

.. code-block:: java

    //: annotations/PasswordUtils.java
    import java.util.*;

    public class PasswordUtils {
        @UseCase(id = 47, description = "Passwords must contain at least one numeric")
        public boolean validatePassword(String password) {
            return (password.matches("\\w*\\d\\w*"));
        }
        @UseCase(id = 48) // 注解并不会对方法的代码产生什么影响（也就是没有侵入性）
        public String encryptPassword(String password) {
        return new StringBuilder(password).reverse().toString();
        }
        @UseCase(id = 49, description = "New passwords can't equal previously used ones")
        public boolean checkForNewPassword(List<String> prevPasswords, String password) {
            return !prevPasswords.contains(password);
        }
    } ///:~

最后，我们需要解析注解。因为注解存活于运行时，我们使用反射机制，查找 ``@UseCase`` 标记，并获取它的值。

.. code-block:: java

    //: annotations/UseCaseTracker.java
    import java.lang.reflect.*;
    import java.util.*;

    public class UseCaseTracker {
        public static void trackUseCases(List<Integer> useCases, Class<?> cl) {
            for(Method m : cl.getDeclaredMethods()) {
                UseCase uc = m.getAnnotation(UseCase.class); // 对某个方法检查是否有对应的注解对象
                if(uc != null) { // 找到了，就拿出注解中的值
                    System.out.println("Found Use Case:" + uc.id() + " " + uc.description());
                    useCases.remove(new Integer(uc.id())); // 实现一个用例移除一个用例
                }
            }
            for(int i : useCases) { // 看看还有哪些用例没有实现
                System.out.println("Warning: Missing use case-" + i);
            }
        }
        public static void main(String[] args) {
            List<Integer> useCases = new ArrayList<Integer>();
            Collections.addAll(useCases, 47, 48, 49, 50); // 共有 47 48 49 50 四个用例需要实现
            trackUseCases(useCases, PasswordUtils.class);
        }
    } /* Output:
    Found Use Case:47 Passwords must contain at least one numeric
    Found Use Case:48 no description
    Found Use Case:49 New passwords can't equal previously used ones
    Warning: Missing use case-50
    *///:~
