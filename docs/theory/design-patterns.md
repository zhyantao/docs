# 设计模式

学习设计模式一定要跟具体的场景联系起来，知道什么时候用什么设计模式才是最重要的。

| 模式名称     | 使用场景                        | 例子                                         |
| ------------ | ------------------------------- | -------------------------------------------- |
| 工厂模式     | 统一管理类的实例化              | 根据不同参数创建不同类型日志记录对象         |
| 抽象工厂模式 | 创建一组相关或依赖对象族        | 跨平台 UI 库，创建按钮、文本框等组件族       |
| 生成器模式   | 分步骤构建复杂对象              | 构建不同配置的计算机，如 CPU、内存、硬盘组合 |
| 原型模式     | 通过复制已有对象创建新对象      | 复制已有用户配置生成新用户默认设置           |
| 单例模式     | 确保一个类只有一个实例          | 数据库连接池，确保全局唯一访问               |
| 适配器模式   | 兼容不兼容接口                  | 将旧支付接口适配为支持新支付网关调用         |
| 组合模式     | 树形结构处理，如文件系统        | 文件系统管理，处理文件夹包含文件的结构       |
| 外观模式     | 简化子系统的调用入口            | 简化下单流程，统一调用库存、支付、物流接口   |
| 桥接模式     | 抽象与实现分离，独立变化        | 不同形状（圆形、方形）与颜色（红、蓝）组合   |
| 装饰模式     | 动态添加功能，比继承更灵活      | 给文本添加滚动条或边框等附加功能             |
| 享元模式     | 共享对象减少内存开销            | 文字编辑器中共享相同字体格式的对象           |
| 代理模式     | 代理控制对原对象的访问          | 远程调用服务代理，隐藏网络通信细节           |
| 策略模式     | 封装可互换的算法逻辑            | 支付方式选择，如支付宝、微信、银联策略切换   |
| 观察者模式   | 实现事件通知机制                | 天气预报系统，多个设备自动更新天气数据       |
| 状态模式     | 对象状态变化时行为随之变化      | 订单状态变更，如待付款、已发货、已完成       |
| 模板方法模式 | 定义算法骨架，子类实现具体步骤  | 单元测试框架定义测试执行流程，子类实现用例   |
| 备忘录模式   | 保存和恢复对象内部状态          | 游戏存档功能，保存和恢复角色当前状态         |
| 中介者模式   | 集中管理对象交互                | 聊天室服务器协调多个客户端之间的消息发送     |
| 迭代器模式   | 遍历聚合对象，不暴露其结构      | 遍历树形结构菜单项而不暴露其内部实现         |
| 命令模式     | 将请求封装为对象，支持撤销/重做 | 实现操作回退功能，如撤销上一步编辑操作       |
| 访问者模式   | 在不修改结构的前提下增加新操作  | 对文档元素（如段落、图片）进行不同格式导出   |

## 创建型模式

### 工厂模式

根据不同参数创建不同类型日志记录对象。

```cpp
#include <string>
#include <cstdio>
using namespace std;

class Log {
public:
    virtual ~Log() {}; // Fix compile warning
    virtual void print_log() = 0;
};

class DatabaseLog : public Log {
public:
    void print_log() override {
        printf("DatabaseLog");
    }
};

class FileLog : public Log {
public:
    void print_log() override {
        printf("FileLog");
    }
};

class LogFactory {
public:
    Log* createLog(string type) {
        if (type == "database") {
            return new DatabaseLog{};
        } else if (type == "file") {
            return new FileLog();
        }
        return NULL;
    }
};

int main() {
    LogFactory factory;
    Log* log = factory.createLog("database");
    if (log) {
        log->print_log();
        delete log;
    }
    return 0;
}
```

### 抽象工厂模式

 跨平台 UI 库，创建按钮、文本框等组件族。

```cpp
#include <cstdio>
#include <memory> // for std::unique_ptr and std::make_unique
using namespace std;

// =================== 抽象产品类 ===================
class Button {
public:
    virtual void render() = 0;
    virtual ~Button() = default;
};

class Text {
public:
    virtual void display() = 0;
    virtual ~Text() = default;
};

// =================== 具体产品类 - Windows 风格 ======
class WinButton : public Button {
public:
    void render() override {
        printf("Windows Button\n");
    }
};

class WinText : public Text {
public:
    void display() override {
        printf("Windows Text\n");
    }
};

// =================== 具体产品类 - Mac 风格 ==========
class MacButton : public Button {
public:
    void render() override {
        printf("Mac Button\n");
    }
};

class MacText : public Text {
public:
    void display() override {
        printf("Mac Text\n");
    }
};

// =================== 抽象工厂类 ===================
class UIFactory {
public:
    virtual unique_ptr<Button> createButton() = 0;
    virtual unique_ptr<Text> createText() = 0;
    virtual ~UIFactory() = default;
};

// =================== 具体工厂类 ===================
class WinUIFactory : public UIFactory {
public:
    unique_ptr<Button> createButton() override {
        return make_unique<WinButton>();
    }

    unique_ptr<Text> createText() override {
        return make_unique<WinText>();
    }
};

class MacUIFactory : public UIFactory {
public:
    unique_ptr<Button> createButton() override {
        return make_unique<MacButton>();
    }

    unique_ptr<Text> createText() override {
        return make_unique<MacText>();
    }
};

// =================== 客户端使用 ===================
void renderUI(UIFactory& factory) {
    auto button = factory.createButton();
    auto text = factory.createText();

    button->render();  // 根据平台调用不同的实现
    text->display();
}

int main() {
    WinUIFactory winFactory;
    MacUIFactory macFactory;

    printf("Rendering Windows UI:\n");
    renderUI(winFactory);

    printf("\nRendering Mac UI:\n");
    renderUI(macFactory);

    return 0;
}
```

### 生成器模式

```cpp
/**
 * It makes sense to use the Builder pattern only when your products are quite
 * complex and require extensive configuration.
 *
 * Unlike in other creational patterns, different concrete builders can produce
 * unrelated products. In other words, results of various builders may not
 * always follow the same interface.
 */

class Product1 {
public:
    std::vector<std::string> parts_;
    void ListParts() const {
        std::cout << "Product parts: ";
        for (size_t i = 0; i < parts_.size(); i++) {
            if (parts_[i] == parts_.back()) {
                std::cout << parts_[i];
            } else {
                std::cout << parts_[i] << ", ";
            }
        }
        std::cout << "\n\n";
    }
};

/**
 * The Builder interface specifies methods for creating the different parts of
 * the Product objects.
 */
class Builder {
public:
    virtual ~Builder() {}
    virtual void ProducePartA() const = 0;
    virtual void ProducePartB() const = 0;
    virtual void ProducePartC() const = 0;
};
/**
 * The Concrete Builder classes follow the Builder interface and provide
 * specific implementations of the building steps. Your program may have several
 * variations of Builders, implemented differently.
 */
class ConcreteBuilder1 : public Builder {
private:
    Product1* product;

    /**
     * A fresh builder instance should contain a blank product object, which is
     * used in further assembly.
     */
public:
    ConcreteBuilder1() {
        this->Reset();
    }

    ~ConcreteBuilder1() {
        delete product;
    }

    void Reset() {
        this->product = new Product1();
    }
    /**
     * All production steps work with the same product instance.
     */

    void ProducePartA() const override {
        this->product->parts_.push_back("PartA1");
    }

    void ProducePartB() const override {
        this->product->parts_.push_back("PartB1");
    }

    void ProducePartC() const override {
        this->product->parts_.push_back("PartC1");
    }

    /**
     * Concrete Builders are supposed to provide their own methods for
     * retrieving results. That's because various types of builders may create
     * entirely different products that don't follow the same interface.
     * Therefore, such methods cannot be declared in the base Builder interface
     * (at least in a statically typed programming language). Note that PHP is a
     * dynamically typed language and this method CAN be in the base interface.
     * However, we won't declare it there for the sake of clarity.
     *
     * Usually, after returning the end result to the client, a builder instance
     * is expected to be ready to start producing another product. That's why
     * it's a usual practice to call the reset method at the end of the
     * `getProduct` method body. However, this behavior is not mandatory, and
     * you can make your builders wait for an explicit reset call from the
     * client code before disposing of the previous result.
     */

    /**
     * Please be careful here with the memory ownership. Once you call
     * GetProduct the user of this function is responsable to release this
     * memory. Here could be a better option to use smart pointers to avoid
     * memory leaks
     */

    Product1* GetProduct() {
        Product1* result = this->product;
        this->Reset();
        return result;
    }
};

/**
 * The Director is only responsible for executing the building steps in a
 * particular sequence. It is helpful when producing products according to a
 * specific order or configuration. Strictly speaking, the Director class is
 * optional, since the client can control builders directly.
 */
class Director {
    /**
     * @var Builder
     */
private:
    Builder* builder;
    /**
     * The Director works with any builder instance that the client code passes
     * to it. This way, the client code may alter the final type of the newly
     * assembled product.
     */

public:
    void set_builder(Builder* builder) {
        this->builder = builder;
    }

    /**
     * The Director can construct several product variations using the same
     * building steps.
     */

    void BuildMinimalViableProduct() {
        this->builder->ProducePartA();
    }

    void BuildFullFeaturedProduct() {
        this->builder->ProducePartA();
        this->builder->ProducePartB();
        this->builder->ProducePartC();
    }
};
/**
 * The client code creates a builder object, passes it to the director and then
 * initiates the construction process. The end result is retrieved from the
 * builder object.
 */
/**
 * I used raw pointers for simplicity however you may prefer to use smart
 * pointers here
 */
void ClientCode(Director& director) {
    ConcreteBuilder1* builder = new ConcreteBuilder1();
    director.set_builder(builder);
    std::cout << "Standard basic product:\n";
    director.BuildMinimalViableProduct();

    Product1* p = builder->GetProduct();
    p->ListParts();
    delete p;

    std::cout << "Standard full featured product:\n";
    director.BuildFullFeaturedProduct();

    p = builder->GetProduct();
    p->ListParts();
    delete p;

    // Remember, the Builder pattern can be used without a Director class.
    std::cout << "Custom product:\n";
    builder->ProducePartA();
    builder->ProducePartC();
    p = builder->GetProduct();
    p->ListParts();
    delete p;

    delete builder;
}

int main() {
    Director* director = new Director();
    ClientCode(*director);
    delete director;
    return 0;
}
```

### 原型模式

```cpp
using std::string;

// Prototype Design Pattern
//
// Intent: Lets you copy existing objects without making your code dependent on
// their classes.

enum Type {
    PROTOTYPE_1 = 0,
    PROTOTYPE_2
};

/**
 * The example class that has cloning ability. We'll see how the values of field
 * with different types will be cloned.
 */

class Prototype {
protected:
    string prototype_name_;
    float prototype_field_;

public:
    Prototype() {}
    Prototype(string prototype_name) : prototype_name_(prototype_name) {}
    virtual ~Prototype() {}
    virtual Prototype* Clone() const = 0;
    virtual void Method(float prototype_field) {
        this->prototype_field_ = prototype_field;
        std::cout << "Call Method from " << prototype_name_ << " with field : " << prototype_field
                  << std::endl;
    }
};

/**
 * ConcretePrototype1 is a Sub-Class of Prototype and implement the Clone Method
 * In this example all data members of Prototype Class are in the Stack. If you
 * have pointers in your properties for ex: String* name_ ,you will need to
 * implement the Copy-Constructor to make sure you have a deep copy from the
 * clone method
 */

class ConcretePrototype1 : public Prototype {
private:
    float concrete_prototype_field1_;

public:
    ConcretePrototype1(string prototype_name, float concrete_prototype_field)
        : Prototype(prototype_name), concrete_prototype_field1_(concrete_prototype_field) {}

    /**
     * Notice that Clone method return a Pointer to a new ConcretePrototype1
     * replica. so, the client (who call the clone method) has the responsability
     * to free that memory. If you have smart pointer knowledge you may prefer to
     * use unique_pointer here.
     */
    Prototype* Clone() const override {
        return new ConcretePrototype1(*this);
    }
};

class ConcretePrototype2 : public Prototype {
private:
    float concrete_prototype_field2_;

public:
    ConcretePrototype2(string prototype_name, float concrete_prototype_field)
        : Prototype(prototype_name), concrete_prototype_field2_(concrete_prototype_field) {}
    Prototype* Clone() const override {
        return new ConcretePrototype2(*this);
    }
};

/**
 * In PrototypeFactory you have two concrete prototypes, one for each concrete
 * prototype class, so each time you want to create a bullet , you can use the
 * existing ones and clone those.
 */

class PrototypeFactory {
private:
    std::unordered_map<Type, Prototype*, std::hash<int>> prototypes_;

public:
    PrototypeFactory() {
        prototypes_[Type::PROTOTYPE_1] = new ConcretePrototype1("PROTOTYPE_1 ", 50.f);
        prototypes_[Type::PROTOTYPE_2] = new ConcretePrototype2("PROTOTYPE_2 ", 60.f);
    }

    /**
     * Be carefull of free all memory allocated. Again, if you have smart pointers
     * knowelege will be better to use it here.
     */

    ~PrototypeFactory() {
        delete prototypes_[Type::PROTOTYPE_1];
        delete prototypes_[Type::PROTOTYPE_2];
    }

    /**
     * Notice here that you just need to specify the type of the prototype you
     * want and the method will create from the object with this type.
     */
    Prototype* CreatePrototype(Type type) {
        return prototypes_[type]->Clone();
    }
};

void Client(PrototypeFactory& prototype_factory) {
    std::cout << "Let's create a Prototype 1\n";

    Prototype* prototype = prototype_factory.CreatePrototype(Type::PROTOTYPE_1);
    prototype->Method(90);
    delete prototype;

    std::cout << "\n";

    std::cout << "Let's create a Prototype 2 \n";

    prototype = prototype_factory.CreatePrototype(Type::PROTOTYPE_2);
    prototype->Method(10);

    delete prototype;
}

int main() {
    PrototypeFactory* prototype_factory = new PrototypeFactory();
    Client(*prototype_factory);
    delete prototype_factory;

    return 0;
}
```

### 单例模式

#### 基础单例

```cpp
/**
 * The Singleton class defines the `GetInstance` method that serves as an
 * alternative to constructor and lets clients access the same instance of this
 * class over and over.
 */
class Singleton {

    /**
     * The Singleton's constructor should always be private to prevent direct
     * construction calls with the `new` operator.
     */

protected:
    Singleton(const std::string value) : value_(value) {}

    static Singleton* singleton_;

    std::string value_;

public:
    /**
     * Singletons should not be cloneable.
     */
    Singleton(Singleton& other) = delete;
    /**
     * Singletons should not be assignable.
     */
    void operator=(const Singleton&) = delete;
    /**
     * This is the static method that controls the access to the singleton
     * instance. On the first run, it creates a singleton object and places it
     * into the static field. On subsequent runs, it returns the client existing
     * object stored in the static field.
     */

    static Singleton* GetInstance(const std::string& value);
    /**
     * Finally, any singleton should define some business logic, which can be
     * executed on its instance.
     */
    void SomeBusinessLogic() {
        // ...
    }

    std::string value() const {
        return value_;
    }
};

Singleton* Singleton::singleton_ = nullptr;

/**
 * Static methods should be defined outside the class.
 */
Singleton* Singleton::GetInstance(const std::string& value) {
    /**
     * This is a safer way to create an instance. instance = new Singleton is
     * dangeruous in case two instance threads wants to access at the same time
     */
    if (singleton_ == nullptr) {
        singleton_ = new Singleton(value);
    }
    return singleton_;
}

void ThreadFoo() {
    // Following code emulates slow initialization.
    std::this_thread::sleep_for(std::chrono::milliseconds(1000));
    Singleton* singleton = Singleton::GetInstance("FOO");
    std::cout << singleton->value() << "\n";
}

void ThreadBar() {
    // Following code emulates slow initialization.
    std::this_thread::sleep_for(std::chrono::milliseconds(1000));
    Singleton* singleton = Singleton::GetInstance("BAR");
    std::cout << singleton->value() << "\n";
}

int main() {
    std::cout << "If you see the same value, then singleton was reused (yay!\n"
              << "If you see different values, then 2 singletons were created (booo!!)\n\n"
              << "RESULT:\n";
    std::thread t1(ThreadFoo);
    std::thread t2(ThreadBar);
    t1.join();
    t2.join();

    return 0;
}
```

#### 线程安全单例

```cpp
/**
 * The Singleton class defines the `GetInstance` method that serves as an
 * alternative to constructor and lets clients access the same instance of this
 * class over and over.
 */
class Singleton {

    /**
     * The Singleton's constructor/destructor should always be private to
     * prevent direct construction/desctruction calls with the `new`/`delete`
     * operator.
     */
private:
    static Singleton* pinstance_;
    static std::mutex mutex_;

protected:
    Singleton(const std::string value) : value_(value) {}
    ~Singleton() {}
    std::string value_;

public:
    /**
     * Singletons should not be cloneable.
     */
    Singleton(Singleton& other) = delete;
    /**
     * Singletons should not be assignable.
     */
    void operator=(const Singleton&) = delete;
    /**
     * This is the static method that controls the access to the singleton
     * instance. On the first run, it creates a singleton object and places it
     * into the static field. On subsequent runs, it returns the client existing
     * object stored in the static field.
     */

    static Singleton* GetInstance(const std::string& value);
    /**
     * Finally, any singleton should define some business logic, which can be
     * executed on its instance.
     */
    void SomeBusinessLogic() {
        // ...
    }

    std::string value() const {
        return value_;
    }
};

/**
 * Static methods should be defined outside the class.
 */

Singleton* Singleton::pinstance_{nullptr};
std::mutex Singleton::mutex_;

/**
 * The first time we call GetInstance we will lock the storage location
 *      and then we make sure again that the variable is null and then we
 *      set the value. RU:
 */
Singleton* Singleton::GetInstance(const std::string& value) {
    std::lock_guard<std::mutex> lock(mutex_);
    if (pinstance_ == nullptr) {
        pinstance_ = new Singleton(value);
    }
    return pinstance_;
}

void ThreadFoo() {
    // Following code emulates slow initialization.
    std::this_thread::sleep_for(std::chrono::milliseconds(1000));
    Singleton* singleton = Singleton::GetInstance("FOO");
    std::cout << singleton->value() << "\n";
}

void ThreadBar() {
    // Following code emulates slow initialization.
    std::this_thread::sleep_for(std::chrono::milliseconds(1000));
    Singleton* singleton = Singleton::GetInstance("BAR");
    std::cout << singleton->value() << "\n";
}

int main() {
    std::cout << "If you see the same value, then singleton was reused (yay!\n"
              << "If you see different values, then 2 singletons were created (booo!!)\n\n"
              << "RESULT:\n";
    std::thread t1(ThreadFoo);
    std::thread t2(ThreadBar);
    t1.join();
    t2.join();

    return 0;
}
```

## 结构型模式

### 适配器模式

#### 对象适配器

```cpp
/**
 * The Target defines the domain-specific interface used by the client code.
 */
class Target {
public:
    virtual ~Target() = default;

    virtual std::string Request() const {
        return "Target: The default target's behavior.";
    }
};

/**
 * The Adaptee contains some useful behavior, but its interface is incompatible
 * with the existing client code. The Adaptee needs some adaptation before the
 * client code can use it.
 */
class Adaptee {
public:
    std::string SpecificRequest() const {
        return ".eetpadA eht fo roivaheb laicepS";
    }
};

/**
 * The Adapter makes the Adaptee's interface compatible with the Target's
 * interface.
 */
class Adapter : public Target {
private:
    Adaptee* adaptee_;

public:
    Adapter(Adaptee* adaptee) : adaptee_(adaptee) {}
    std::string Request() const override {
        std::string to_reverse = this->adaptee_->SpecificRequest();
        std::reverse(to_reverse.begin(), to_reverse.end());
        return "Adapter: (TRANSLATED) " + to_reverse;
    }
};

/**
 * The client code supports all classes that follow the Target interface.
 */
void ClientCode(const Target* target) {
    std::cout << target->Request();
}

int main() {
    std::cout << "Client: I can work just fine with the Target objects:\n";
    Target* target = new Target;
    ClientCode(target);
    std::cout << "\n\n";
    Adaptee* adaptee = new Adaptee;
    std::cout << "Client: The Adaptee class has a weird interface. See, I don't understand it:\n";
    std::cout << "Adaptee: " << adaptee->SpecificRequest();
    std::cout << "\n\n";
    std::cout << "Client: But I can work with it via the Adapter:\n";
    Adapter* adapter = new Adapter(adaptee);
    ClientCode(adapter);
    std::cout << "\n";

    delete target;
    delete adaptee;
    delete adapter;

    return 0;
}
```

#### 类适配器

```cpp
/**
 * The Target defines the domain-specific interface used by the client code.
 */
class Target {
public:
    virtual ~Target() = default;

    virtual std::string Request() const {
        return "Target: The default target's behavior.";
    }
};

/**
 * The Adaptee contains some useful behavior, but its interface is incompatible
 * with the existing client code. The Adaptee needs some adaptation before the
 * client code can use it.
 */
class Adaptee {
public:
    std::string SpecificRequest() const {
        return ".eetpadA eht fo roivaheb laicepS";
    }
};

/**
 * The Adapter makes the Adaptee's interface compatible with the Target's
 * interface.
 */
class Adapter : public Target {
private:
    Adaptee* adaptee_;

public:
    Adapter(Adaptee* adaptee) : adaptee_(adaptee) {}
    std::string Request() const override {
        std::string to_reverse = this->adaptee_->SpecificRequest();
        std::reverse(to_reverse.begin(), to_reverse.end());
        return "Adapter: (TRANSLATED) " + to_reverse;
    }
};

/**
 * The client code supports all classes that follow the Target interface.
 */
void ClientCode(const Target* target) {
    std::cout << target->Request();
}

int main() {
    std::cout << "Client: I can work just fine with the Target objects:\n";
    Target* target = new Target;
    ClientCode(target);
    std::cout << "\n\n";
    Adaptee* adaptee = new Adaptee;
    std::cout << "Client: The Adaptee class has a weird interface. See, I don't understand it:\n";
    std::cout << "Adaptee: " << adaptee->SpecificRequest();
    std::cout << "\n\n";
    std::cout << "Client: But I can work with it via the Adapter:\n";
    Adapter* adapter = new Adapter(adaptee);
    ClientCode(adapter);
    std::cout << "\n";

    delete target;
    delete adaptee;
    delete adapter;

    return 0;
}
```

### 组合模式

```cpp
#include <algorithm>
#include <iostream>
#include <list>
#include <string>
/**
 * The base Component class declares common operations for both simple and
 * complex objects of a composition.
 */
class Component {
    /**
     * @var Component
     */
protected:
    Component* parent_;
    /**
     * Optionally, the base Component can declare an interface for setting and
     * accessing a parent of the component in a tree structure. It can also
     * provide some default implementation for these methods.
     */
public:
    virtual ~Component() {}
    void SetParent(Component* parent) {
        this->parent_ = parent;
    }
    Component* GetParent() const {
        return this->parent_;
    }
    /**
     * In some cases, it would be beneficial to define the child-management
     * operations right in the base Component class. This way, you won't need to
     * expose any concrete component classes to the client code, even during the
     * object tree assembly. The downside is that these methods will be empty for
     * the leaf-level components.
     */
    virtual void Add(Component* component) {}
    virtual void Remove(Component* component) {}
    /**
     * You can provide a method that lets the client code figure out whether a
     * component can bear children.
     */
    virtual bool IsComposite() const {
        return false;
    }
    /**
     * The base Component may implement some default behavior or leave it to
     * concrete classes (by declaring the method containing the behavior as
     * "abstract").
     */
    virtual std::string Operation() const = 0;
};
/**
 * The Leaf class represents the end objects of a composition. A leaf can't have
 * any children.
 *
 * Usually, it's the Leaf objects that do the actual work, whereas Composite
 * objects only delegate to their sub-components.
 */
class Leaf : public Component {
public:
    std::string Operation() const override {
        return "Leaf";
    }
};
/**
 * The Composite class represents the complex components that may have children.
 * Usually, the Composite objects delegate the actual work to their children and
 * then "sum-up" the result.
 */
class Composite : public Component {
    /**
     * @var \SplObjectStorage
     */
protected:
    std::list<Component*> children_;

public:
    /**
     * A composite object can add or remove other components (both simple or
     * complex) to or from its child list.
     */
    void Add(Component* component) override {
        this->children_.push_back(component);
        component->SetParent(this);
    }
    /**
     * Have in mind that this method removes the pointer to the list but doesn't
     * frees the
     *     memory, you should do it manually or better use smart pointers.
     */
    void Remove(Component* component) override {
        children_.remove(component);
        component->SetParent(nullptr);
    }
    bool IsComposite() const override {
        return true;
    }
    /**
     * The Composite executes its primary logic in a particular way. It traverses
     * recursively through all its children, collecting and summing their results.
     * Since the composite's children pass these calls to their children and so
     * forth, the whole object tree is traversed as a result.
     */
    std::string Operation() const override {
        std::string result;
        for (const Component* c : children_) {
            if (c == children_.back()) {
                result += c->Operation();
            } else {
                result += c->Operation() + "+";
            }
        }
        return "Branch(" + result + ")";
    }
};
/**
 * The client code works with all of the components via the base interface.
 */
void ClientCode(Component* component) {
    // ...
    std::cout << "RESULT: " << component->Operation();
    // ...
}

/**
 * Thanks to the fact that the child-management operations are declared in the
 * base Component class, the client code can work with any component, simple or
 * complex, without depending on their concrete classes.
 */
void ClientCode2(Component* component1, Component* component2) {
    // ...
    if (component1->IsComposite()) {
        component1->Add(component2);
    }
    std::cout << "RESULT: " << component1->Operation();
    // ...
}

/**
 * This way the client code can support the simple leaf components...
 */

int main() {
    Component* simple = new Leaf;
    std::cout << "Client: I've got a simple component:\n";
    ClientCode(simple);
    std::cout << "\n\n";
    /**
     * ...as well as the complex composites.
     */

    Component* tree = new Composite;
    Component* branch1 = new Composite;

    Component* leaf_1 = new Leaf;
    Component* leaf_2 = new Leaf;
    Component* leaf_3 = new Leaf;
    branch1->Add(leaf_1);
    branch1->Add(leaf_2);
    Component* branch2 = new Composite;
    branch2->Add(leaf_3);
    tree->Add(branch1);
    tree->Add(branch2);
    std::cout << "Client: Now I've got a composite tree:\n";
    ClientCode(tree);
    std::cout << "\n\n";

    std::cout
        << "Client: I don't need to check the components classes even when managing the tree:\n";
    ClientCode2(tree, simple);
    std::cout << "\n";

    delete simple;
    delete tree;
    delete branch1;
    delete branch2;
    delete leaf_1;
    delete leaf_2;
    delete leaf_3;

    return 0;
}
```

### 外观模式

外观模式是一种结构型设计模式， 能为程序库、 框架或其他复杂类提供一个简单的接口。

```cpp
/**
 * The Subsystem can accept requests either from the facade or client directly.
 * In any case, to the Subsystem, the Facade is yet another client, and it's not
 * a part of the Subsystem.
 */
class Subsystem1 {
public:
    std::string Operation1() const {
        return "Subsystem1: Ready!\n";
    }
    // ...
    std::string OperationN() const {
        return "Subsystem1: Go!\n";
    }
};
/**
 * Some facades can work with multiple subsystems at the same time.
 */
class Subsystem2 {
public:
    std::string Operation1() const {
        return "Subsystem2: Get ready!\n";
    }
    // ...
    std::string OperationZ() const {
        return "Subsystem2: Fire!\n";
    }
};

/**
 * The Facade class provides a simple interface to the complex logic of one or
 * several subsystems. The Facade delegates the client requests to the
 * appropriate objects within the subsystem. The Facade is also responsible for
 * managing their lifecycle. All of this shields the client from the undesired
 * complexity of the subsystem.
 */
class Facade {
protected:
    Subsystem1* subsystem1_;
    Subsystem2* subsystem2_;
    /**
     * Depending on your application's needs, you can provide the Facade with
     * existing subsystem objects or force the Facade to create them on its own.
     */
public:
    /**
     * In this case we will delegate the memory ownership to Facade Class
     */
    Facade(
        Subsystem1* subsystem1 = nullptr,
        Subsystem2* subsystem2 = nullptr) {
        this->subsystem1_ = subsystem1 ?: new Subsystem1;
        this->subsystem2_ = subsystem2 ?: new Subsystem2;
    }
    ~Facade() {
        delete subsystem1_;
        delete subsystem2_;
    }
    /**
     * The Facade's methods are convenient shortcuts to the sophisticated
     * functionality of the subsystems. However, clients get only to a fraction of
     * a subsystem's capabilities.
     */
    std::string Operation() {
        std::string result = "Facade initializes subsystems:\n";
        result += this->subsystem1_->Operation1();
        result += this->subsystem2_->Operation1();
        result += "Facade orders subsystems to perform the action:\n";
        result += this->subsystem1_->OperationN();
        result += this->subsystem2_->OperationZ();
        return result;
    }
};

/**
 * The client code works with complex subsystems through a simple interface
 * provided by the Facade. When a facade manages the lifecycle of the subsystem,
 * the client might not even know about the existence of the subsystem. This
 * approach lets you keep the complexity under control.
 */
void ClientCode(Facade* facade) {
    // ...
    std::cout << facade->Operation();
    // ...
}
/**
 * The client code may have some of the subsystem's objects already created. In
 * this case, it might be worthwhile to initialize the Facade with these objects
 * instead of letting the Facade create new instances.
 */

int main() {
    Subsystem1* subsystem1 = new Subsystem1;
    Subsystem2* subsystem2 = new Subsystem2;
    Facade* facade = new Facade(subsystem1, subsystem2);
    ClientCode(facade);

    delete facade;

    return 0;
}
```

### 桥接模式

桥接模式是一种结构型设计模式， 可将一个大类或一系列紧密相关的类拆分为抽象和实现两个独立的层次结构， 从而能在开发时分别使用。

```cpp
/**
 * The Implementation defines the interface for all implementation classes. It
 * doesn't have to match the Abstraction's interface. In fact, the two
 * interfaces can be entirely different. Typically the Implementation interface
 * provides only primitive operations, while the Abstraction defines higher-
 * level operations based on those primitives.
 */

class Implementation {
public:
    virtual ~Implementation() {}
    virtual std::string OperationImplementation() const = 0;
};

/**
 * Each Concrete Implementation corresponds to a specific platform and
 * implements the Implementation interface using that platform's API.
 */
class ConcreteImplementationA : public Implementation {
public:
    std::string OperationImplementation() const override {
        return "ConcreteImplementationA: Here's the result on the platform A.\n";
    }
};
class ConcreteImplementationB : public Implementation {
public:
    std::string OperationImplementation() const override {
        return "ConcreteImplementationB: Here's the result on the platform B.\n";
    }
};

/**
 * The Abstraction defines the interface for the "control" part of the two class
 * hierarchies. It maintains a reference to an object of the Implementation
 * hierarchy and delegates all of the real work to this object.
 */

class Abstraction {
    /**
     * @var Implementation
     */
protected:
    Implementation* implementation_;

public:
    Abstraction(Implementation* implementation) : implementation_(implementation) {
    }

    virtual ~Abstraction() {
    }

    virtual std::string Operation() const {
        return "Abstraction: Base operation with:\n" +
               this->implementation_->OperationImplementation();
    }
};
/**
 * You can extend the Abstraction without changing the Implementation classes.
 */
class ExtendedAbstraction : public Abstraction {
public:
    ExtendedAbstraction(Implementation* implementation) : Abstraction(implementation) {
    }
    std::string Operation() const override {
        return "ExtendedAbstraction: Extended operation with:\n" +
               this->implementation_->OperationImplementation();
    }
};

/**
 * Except for the initialization phase, where an Abstraction object gets linked
 * with a specific Implementation object, the client code should only depend on
 * the Abstraction class. This way the client code can support any abstraction-
 * implementation combination.
 */
void ClientCode(const Abstraction& abstraction) {
    // ...
    std::cout << abstraction.Operation();
    // ...
}
/**
 * The client code should be able to work with any pre-configured abstraction-
 * implementation combination.
 */

int main() {
    Implementation* implementation = new ConcreteImplementationA;
    Abstraction* abstraction = new Abstraction(implementation);
    ClientCode(*abstraction);
    std::cout << std::endl;
    delete implementation;
    delete abstraction;

    implementation = new ConcreteImplementationB;
    abstraction = new ExtendedAbstraction(implementation);
    ClientCode(*abstraction);

    delete implementation;
    delete abstraction;

    return 0;
}
```

### 装饰模式

装饰模式是一种结构型设计模式， 允许你通过将对象放入包含行为的特殊封装对象中来为原对象绑定新的行为。

```cpp
/**
 * The base Component interface defines operations that can be altered by
 * decorators.
 */
class Component {
public:
    virtual ~Component() {}
    virtual std::string Operation() const = 0;
};
/**
 * Concrete Components provide default implementations of the operations. There
 * might be several variations of these classes.
 */
class ConcreteComponent : public Component {
public:
    std::string Operation() const override {
        return "ConcreteComponent";
    }
};
/**
 * The base Decorator class follows the same interface as the other components.
 * The primary purpose of this class is to define the wrapping interface for all
 * concrete decorators. The default implementation of the wrapping code might
 * include a field for storing a wrapped component and the means to initialize
 * it.
 */
class Decorator : public Component {
    /**
     * @var Component
     */
protected:
    Component* component_;

public:
    Decorator(Component* component) : component_(component) {
    }
    /**
     * The Decorator delegates all work to the wrapped component.
     */
    std::string Operation() const override {
        return this->component_->Operation();
    }
};
/**
 * Concrete Decorators call the wrapped object and alter its result in some way.
 */
class ConcreteDecoratorA : public Decorator {
    /**
     * Decorators may call parent implementation of the operation, instead of
     * calling the wrapped object directly. This approach simplifies extension of
     * decorator classes.
     */
public:
    ConcreteDecoratorA(Component* component) : Decorator(component) {
    }
    std::string Operation() const override {
        return "ConcreteDecoratorA(" + Decorator::Operation() + ")";
    }
};
/**
 * Decorators can execute their behavior either before or after the call to a
 * wrapped object.
 */
class ConcreteDecoratorB : public Decorator {
public:
    ConcreteDecoratorB(Component* component) : Decorator(component) {
    }

    std::string Operation() const override {
        return "ConcreteDecoratorB(" + Decorator::Operation() + ")";
    }
};
/**
 * The client code works with all objects using the Component interface. This
 * way it can stay independent of the concrete classes of components it works
 * with.
 */
void ClientCode(Component* component) {
    // ...
    std::cout << "RESULT: " << component->Operation();
    // ...
}

int main() {
    /**
     * This way the client code can support both simple components...
     */
    Component* simple = new ConcreteComponent;
    std::cout << "Client: I've got a simple component:\n";
    ClientCode(simple);
    std::cout << "\n\n";
    /**
     * ...as well as decorated ones.
     *
     * Note how decorators can wrap not only simple components but the other
     * decorators as well.
     */
    Component* decorator1 = new ConcreteDecoratorA(simple);
    Component* decorator2 = new ConcreteDecoratorB(decorator1);
    std::cout << "Client: Now I've got a decorated component:\n";
    ClientCode(decorator2);
    std::cout << "\n";

    delete simple;
    delete decorator1;
    delete decorator2;

    return 0;
}
```

### 享元模式

享元模式是一种结构型设计模式， 它摒弃了在每个对象中保存所有数据的方式， 通过共享多个对象所共有的相同状态， 让你能在有限的内存容量中载入更多对象。

```cpp
/**
 * Flyweight Design Pattern
 *
 * Intent: Lets you fit more objects into the available amount of RAM by sharing
 * common parts of state between multiple objects, instead of keeping all of the
 * data in each object.
 */

struct SharedState {
    std::string brand_;
    std::string model_;
    std::string color_;

    SharedState(const std::string& brand, const std::string& model, const std::string& color)
        : brand_(brand), model_(model), color_(color) {
    }

    friend std::ostream& operator<<(std::ostream& os, const SharedState& ss) {
        return os << "[ " << ss.brand_ << " , " << ss.model_ << " , " << ss.color_ << " ]";
    }
};

struct UniqueState {
    std::string owner_;
    std::string plates_;

    UniqueState(const std::string& owner, const std::string& plates)
        : owner_(owner), plates_(plates) {
    }

    friend std::ostream& operator<<(std::ostream& os, const UniqueState& us) {
        return os << "[ " << us.owner_ << " , " << us.plates_ << " ]";
    }
};

/**
 * The Flyweight stores a common portion of the state (also called intrinsic
 * state) that belongs to multiple real business entities. The Flyweight accepts
 * the rest of the state (extrinsic state, unique for each entity) via its
 * method parameters.
 */
class Flyweight {
private:
    SharedState* shared_state_;

public:
    Flyweight(const SharedState* shared_state) : shared_state_(new SharedState(*shared_state)) {
    }
    Flyweight(const Flyweight& other) : shared_state_(new SharedState(*other.shared_state_)) {
    }
    ~Flyweight() {
        delete shared_state_;
    }
    SharedState* shared_state() const {
        return shared_state_;
    }
    void Operation(const UniqueState& unique_state) const {
        std::cout << "Flyweight: Displaying shared (" << *shared_state_ << ") and unique (" << unique_state << ") state.\n";
    }
};
/**
 * The Flyweight Factory creates and manages the Flyweight objects. It ensures
 * that flyweights are shared correctly. When the client requests a flyweight,
 * the factory either returns an existing instance or creates a new one, if it
 * doesn't exist yet.
 */
class FlyweightFactory {
    /**
     * @var Flyweight[]
     */
private:
    std::unordered_map<std::string, Flyweight> flyweights_;
    /**
     * Returns a Flyweight's string hash for a given state.
     */
    std::string GetKey(const SharedState& ss) const {
        return ss.brand_ + "_" + ss.model_ + "_" + ss.color_;
    }

public:
    FlyweightFactory(std::initializer_list<SharedState> share_states) {
        for (const SharedState& ss : share_states) {
            this->flyweights_.insert(std::make_pair<std::string, Flyweight>(this->GetKey(ss), Flyweight(&ss)));
        }
    }

    /**
     * Returns an existing Flyweight with a given state or creates a new one.
     */
    Flyweight GetFlyweight(const SharedState& shared_state) {
        std::string key = this->GetKey(shared_state);
        if (this->flyweights_.find(key) == this->flyweights_.end()) {
            std::cout << "FlyweightFactory: Can't find a flyweight, creating new one.\n";
            this->flyweights_.insert(std::make_pair(key, Flyweight(&shared_state)));
        } else {
            std::cout << "FlyweightFactory: Reusing existing flyweight.\n";
        }
        return this->flyweights_.at(key);
    }
    void ListFlyweights() const {
        size_t count = this->flyweights_.size();
        std::cout << "\nFlyweightFactory: I have " << count << " flyweights:\n";
        for (std::pair<std::string, Flyweight> pair : this->flyweights_) {
            std::cout << pair.first << "\n";
        }
    }
};

// ...
void AddCarToPoliceDatabase(
    FlyweightFactory& ff, const std::string& plates, const std::string& owner,
    const std::string& brand, const std::string& model, const std::string& color) {
    std::cout << "\nClient: Adding a car to database.\n";
    const Flyweight& flyweight = ff.GetFlyweight({brand, model, color});
    // The client code either stores or calculates extrinsic state and passes it
    // to the flyweight's methods.
    flyweight.Operation({owner, plates});
}

/**
 * The client code usually creates a bunch of pre-populated flyweights in the
 * initialization stage of the application.
 */

int main() {
    FlyweightFactory* factory = new FlyweightFactory({{"Chevrolet", "Camaro2018", "pink"}, {"Mercedes Benz", "C300", "black"}, {"Mercedes Benz", "C500", "red"}, {"BMW", "M5", "red"}, {"BMW", "X6", "white"}});
    factory->ListFlyweights();

    AddCarToPoliceDatabase(*factory,
                           "CL234IR",
                           "James Doe",
                           "BMW",
                           "M5",
                           "red");

    AddCarToPoliceDatabase(*factory,
                           "CL234IR",
                           "James Doe",
                           "BMW",
                           "X1",
                           "red");
    factory->ListFlyweights();
    delete factory;

    return 0;
}
```

### 代理模式

代理模式是一种结构型设计模式， 让你能够提供对象的替代品或其占位符。 代理控制着对于原对象的访问， 并允许在将请求提交给对象前后进行一些处理。

```cpp
#include <iostream>
/**
 * The Subject interface declares common operations for both RealSubject and the
 * Proxy. As long as the client works with RealSubject using this interface,
 * you'll be able to pass it a proxy instead of a real subject.
 */
class Subject {
public:
    virtual void Request() const = 0;
};
/**
 * The RealSubject contains some core business logic. Usually, RealSubjects are
 * capable of doing some useful work which may also be very slow or sensitive -
 * e.g. correcting input data. A Proxy can solve these issues without any
 * changes to the RealSubject's code.
 */
class RealSubject : public Subject {
public:
    void Request() const override {
        std::cout << "RealSubject: Handling request.\n";
    }
};
/**
 * The Proxy has an interface identical to the RealSubject.
 */
class Proxy : public Subject {
    /**
     * @var RealSubject
     */
private:
    RealSubject* real_subject_;

    bool CheckAccess() const {
        // Some real checks should go here.
        std::cout << "Proxy: Checking access prior to firing a real request.\n";
        return true;
    }
    void LogAccess() const {
        std::cout << "Proxy: Logging the time of request.\n";
    }

    /**
     * The Proxy maintains a reference to an object of the RealSubject class. It
     * can be either lazy-loaded or passed to the Proxy by the client.
     */
public:
    Proxy(RealSubject* real_subject) : real_subject_(new RealSubject(*real_subject)) {
    }

    ~Proxy() {
        delete real_subject_;
    }
    /**
     * The most common applications of the Proxy pattern are lazy loading,
     * caching, controlling the access, logging, etc. A Proxy can perform one of
     * these things and then, depending on the result, pass the execution to the
     * same method in a linked RealSubject object.
     */
    void Request() const override {
        if (this->CheckAccess()) {
            this->real_subject_->Request();
            this->LogAccess();
        }
    }
};
/**
 * The client code is supposed to work with all objects (both subjects and
 * proxies) via the Subject interface in order to support both real subjects and
 * proxies. In real life, however, clients mostly work with their real subjects
 * directly. In this case, to implement the pattern more easily, you can extend
 * your proxy from the real subject's class.
 */
void ClientCode(const Subject& subject) {
    // ...
    subject.Request();
    // ...
}

int main() {
    std::cout << "Client: Executing the client code with a real subject:\n";
    RealSubject* real_subject = new RealSubject;
    ClientCode(*real_subject);
    std::cout << "\n";
    std::cout << "Client: Executing the same client code with a proxy:\n";
    Proxy* proxy = new Proxy(real_subject);
    ClientCode(*proxy);

    delete real_subject;
    delete proxy;
    return 0;
}
```

## 行为模式

### 策略模式

```cpp
/**
 * The Strategy interface declares operations common to all supported versions
 * of some algorithm.
 *
 * The Context uses this interface to call the algorithm defined by Concrete
 * Strategies.
 */
class Strategy {
public:
    virtual ~Strategy() = default;
    virtual std::string doAlgorithm(std::string_view data) const = 0;
};

/**
 * The Context defines the interface of interest to clients.
 */

class Context {
    /**
     * @var Strategy The Context maintains a reference to one of the Strategy
     * objects. The Context does not know the concrete class of a strategy. It
     * should work with all strategies via the Strategy interface.
     */
private:
    std::unique_ptr<Strategy> strategy_;
    /**
     * Usually, the Context accepts a strategy through the constructor, but also
     * provides a setter to change it at runtime.
     */
public:
    explicit Context(std::unique_ptr<Strategy>&& strategy = {}) : strategy_(std::move(strategy)) {}
    /**
     * Usually, the Context allows replacing a Strategy object at runtime.
     */
    void set_strategy(std::unique_ptr<Strategy>&& strategy) {
        strategy_ = std::move(strategy);
    }
    /**
     * The Context delegates some work to the Strategy object instead of
     * implementing +multiple versions of the algorithm on its own.
     */
    void doSomeBusinessLogic() const {
        if (strategy_) {
            std::cout << "Context: Sorting data using the strategy (not sure how it'll do it)\n";
            std::string result = strategy_->doAlgorithm("aecbd");
            std::cout << result << "\n";
        } else {
            std::cout << "Context: Strategy isn't set\n";
        }
    }
};

/**
 * Concrete Strategies implement the algorithm while following the base Strategy
 * interface. The interface makes them interchangeable in the Context.
 */
class ConcreteStrategyA : public Strategy {
public:
    std::string doAlgorithm(std::string_view data) const override {
        std::string result(data);
        std::sort(std::begin(result), std::end(result));

        return result;
    }
};
class ConcreteStrategyB : public Strategy {
    std::string doAlgorithm(std::string_view data) const override {
        std::string result(data);
        std::sort(std::begin(result), std::end(result), std::greater<>());

        return result;
    }
};
/**
 * The client code picks a concrete strategy and passes it to the context. The
 * client should be aware of the differences between strategies in order to make
 * the right choice.
 */

void clientCode() {
    Context context(std::make_unique<ConcreteStrategyA>());
    std::cout << "Client: Strategy is set to normal sorting.\n";
    context.doSomeBusinessLogic();
    std::cout << "\n";
    std::cout << "Client: Strategy is set to reverse sorting.\n";
    context.set_strategy(std::make_unique<ConcreteStrategyB>());
    context.doSomeBusinessLogic();
}

int main() {
    clientCode();
    return 0;
}
```

### 观察者模式

观察者模式是一种行为设计模式， 允许你定义一种订阅机制， 可在对象事件发生时通知多个 “观察” 该对象的其他对象。

```cpp
/**
 * Observer Design Pattern
 *
 * Intent: Lets you define a subscription mechanism to notify multiple objects
 * about any events that happen to the object they're observing.
 *
 * Note that there's a lot of different terms with similar meaning associated
 * with this pattern. Just remember that the Subject is also called the
 * Publisher and the Observer is often called the Subscriber and vice versa.
 * Also the verbs "observe", "listen" or "track" usually mean the same thing.
 */

#include <iostream>
#include <list>
#include <string>

class IObserver {
public:
    virtual ~IObserver() {};
    virtual void Update(const std::string& message_from_subject) = 0;
};

class ISubject {
public:
    virtual ~ISubject() {};
    virtual void Attach(IObserver* observer) = 0;
    virtual void Detach(IObserver* observer) = 0;
    virtual void Notify() = 0;
};

/**
 * The Subject owns some important state and notifies observers when the state
 * changes.
 */

class Subject : public ISubject {
public:
    virtual ~Subject() {
        std::cout << "Goodbye, I was the Subject.\n";
    }

    /**
     * The subscription management methods.
     */
    void Attach(IObserver* observer) override {
        list_observer_.push_back(observer);
    }
    void Detach(IObserver* observer) override {
        list_observer_.remove(observer);
    }
    void Notify() override {
        std::list<IObserver*>::iterator iterator = list_observer_.begin();
        HowManyObserver();
        while (iterator != list_observer_.end()) {
            (*iterator)->Update(message_);
            ++iterator;
        }
    }

    void CreateMessage(std::string message = "Empty") {
        this->message_ = message;
        Notify();
    }
    void HowManyObserver() {
        std::cout << "There are " << list_observer_.size() << " observers in the list.\n";
    }

    /**
     * Usually, the subscription logic is only a fraction of what a Subject can
     * really do. Subjects commonly hold some important business logic, that
     * triggers a notification method whenever something important is about to
     * happen (or after it).
     */
    void SomeBusinessLogic() {
        this->message_ = "change message message";
        Notify();
        std::cout << "I'm about to do some thing important\n";
    }

private:
    std::list<IObserver*> list_observer_;
    std::string message_;
};

class Observer : public IObserver {
public:
    Observer(Subject& subject) : subject_(subject) {
        this->subject_.Attach(this);
        std::cout << "Hi, I'm the Observer \"" << ++Observer::static_number_ << "\".\n";
        this->number_ = Observer::static_number_;
    }
    virtual ~Observer() {
        std::cout << "Goodbye, I was the Observer \"" << this->number_ << "\".\n";
    }

    void Update(const std::string& message_from_subject) override {
        message_from_subject_ = message_from_subject;
        PrintInfo();
    }
    void RemoveMeFromTheList() {
        subject_.Detach(this);
        std::cout << "Observer \"" << number_ << "\" removed from the list.\n";
    }
    void PrintInfo() {
        std::cout << "Observer \"" << this->number_ << "\": a new message is available --> " << this->message_from_subject_ << "\n";
    }

private:
    std::string message_from_subject_;
    Subject& subject_;
    static int static_number_;
    int number_;
};

int Observer::static_number_ = 0;

void ClientCode() {
    Subject* subject = new Subject;
    Observer* observer1 = new Observer(*subject);
    Observer* observer2 = new Observer(*subject);
    Observer* observer3 = new Observer(*subject);
    Observer* observer4;
    Observer* observer5;

    subject->CreateMessage("Hello World! :D");
    observer3->RemoveMeFromTheList();

    subject->CreateMessage("The weather is hot today! :p");
    observer4 = new Observer(*subject);

    observer2->RemoveMeFromTheList();
    observer5 = new Observer(*subject);

    subject->CreateMessage("My new car is great! ;)");
    observer5->RemoveMeFromTheList();

    observer4->RemoveMeFromTheList();
    observer1->RemoveMeFromTheList();

    delete observer5;
    delete observer4;
    delete observer3;
    delete observer2;
    delete observer1;
    delete subject;
}

int main() {
    ClientCode();
    return 0;
}
```

### 状态模式

状态模式是一种行为设计模式， 让你能在一个对象的内部状态变化时改变其行为， 使其看上去就像改变了自身所属的类一样。

```cpp
#include <iostream>
#include <typeinfo>
/**
 * The base State class declares methods that all Concrete State should
 * implement and also provides a backreference to the Context object, associated
 * with the State. This backreference can be used by States to transition the
 * Context to another State.
 */

class Context;

class State {
    /**
     * @var Context
     */
protected:
    Context* context_;

public:
    virtual ~State() {
    }

    void set_context(Context* context) {
        this->context_ = context;
    }

    virtual void Handle1() = 0;
    virtual void Handle2() = 0;
};

/**
 * The Context defines the interface of interest to clients. It also maintains a
 * reference to an instance of a State subclass, which represents the current
 * state of the Context.
 */
class Context {
    /**
     * @var State A reference to the current state of the Context.
     */
private:
    State* state_;

public:
    Context(State* state) : state_(nullptr) {
        this->TransitionTo(state);
    }
    ~Context() {
        delete state_;
    }
    /**
     * The Context allows changing the State object at runtime.
     */
    void TransitionTo(State* state) {
        std::cout << "Context: Transition to " << typeid(*state).name() << ".\n";
        if (this->state_ != nullptr)
            delete this->state_;
        this->state_ = state;
        this->state_->set_context(this);
    }
    /**
     * The Context delegates part of its behavior to the current State object.
     */
    void Request1() {
        this->state_->Handle1();
    }
    void Request2() {
        this->state_->Handle2();
    }
};

/**
 * Concrete States implement various behaviors, associated with a state of the
 * Context.
 */

class ConcreteStateA : public State {
public:
    void Handle1() override;

    void Handle2() override {
        std::cout << "ConcreteStateA handles request2.\n";
    }
};

class ConcreteStateB : public State {
public:
    void Handle1() override {
        std::cout << "ConcreteStateB handles request1.\n";
    }
    void Handle2() override {
        std::cout << "ConcreteStateB handles request2.\n";
        std::cout << "ConcreteStateB wants to change the state of the context.\n";
        this->context_->TransitionTo(new ConcreteStateA);
    }
};

void ConcreteStateA::Handle1() {
    {
        std::cout << "ConcreteStateA handles request1.\n";
        std::cout << "ConcreteStateA wants to change the state of the context.\n";

        this->context_->TransitionTo(new ConcreteStateB);
    }
}

/**
 * The client code.
 */
void ClientCode() {
    Context* context = new Context(new ConcreteStateA);
    context->Request1();
    context->Request2();
    delete context;
}

int main() {
    ClientCode();
    return 0;
}
```

### 模板方法模式

模板方法模式是一种行为设计模式， 它在超类中定义了一个算法的框架， 允许子类在不修改结构的情况下重写算法的特定步骤。

- 抽象步骤必须由各个子类来实现
- 可选步骤已有一些默认实现， 但仍可在需要时进行重写

还有另一种名为钩子的步骤。 钩子是内容为空的可选步骤。 即使不重写钩子， 模板方法也能工作。 钩子通常放置在算法重要步骤的前后， 为子类提供额外的算法扩展点。

```cpp
/**
 * The Abstract Class defines a template method that contains a skeleton of some
 * algorithm, composed of calls to (usually) abstract primitive operations.
 *
 * Concrete subclasses should implement these operations, but leave the template
 * method itself intact.
 */
class AbstractClass {
    /**
     * The template method defines the skeleton of an algorithm.
     */
public:
    void TemplateMethod() const {
        this->BaseOperation1();
        this->RequiredOperations1();
        this->BaseOperation2();
        this->Hook1();
        this->RequiredOperation2();
        this->BaseOperation3();
        this->Hook2();
    }
    /**
     * These operations already have implementations.
     */
protected:
    void BaseOperation1() const {
        std::cout << "AbstractClass says: I am doing the bulk of the work\n";
    }
    void BaseOperation2() const {
        std::cout << "AbstractClass says: But I let subclasses override some operations\n";
    }
    void BaseOperation3() const {
        std::cout << "AbstractClass says: But I am doing the bulk of the work anyway\n";
    }
    /**
     * These operations have to be implemented in subclasses.
     */
    virtual void RequiredOperations1() const = 0;
    virtual void RequiredOperation2() const = 0;
    /**
     * These are "hooks." Subclasses may override them, but it's not mandatory
     * since the hooks already have default (but empty) implementation. Hooks
     * provide additional extension points in some crucial places of the
     * algorithm.
     */
    virtual void Hook1() const {}
    virtual void Hook2() const {}
};
/**
 * Concrete classes have to implement all abstract operations of the base class.
 * They can also override some operations with a default implementation.
 */
class ConcreteClass1 : public AbstractClass {
protected:
    void RequiredOperations1() const override {
        std::cout << "ConcreteClass1 says: Implemented Operation1\n";
    }
    void RequiredOperation2() const override {
        std::cout << "ConcreteClass1 says: Implemented Operation2\n";
    }
};
/**
 * Usually, concrete classes override only a fraction of base class' operations.
 */
class ConcreteClass2 : public AbstractClass {
protected:
    void RequiredOperations1() const override {
        std::cout << "ConcreteClass2 says: Implemented Operation1\n";
    }
    void RequiredOperation2() const override {
        std::cout << "ConcreteClass2 says: Implemented Operation2\n";
    }
    void Hook1() const override {
        std::cout << "ConcreteClass2 says: Overridden Hook1\n";
    }
};
/**
 * The client code calls the template method to execute the algorithm. Client
 * code does not have to know the concrete class of an object it works with, as
 * long as it works with objects through the interface of their base class.
 */
void ClientCode(AbstractClass* class_) {
    // ...
    class_->TemplateMethod();
    // ...
}

int main() {
    std::cout << "Same client code can work with different subclasses:\n";
    ConcreteClass1* concreteClass1 = new ConcreteClass1;
    ClientCode(concreteClass1);
    std::cout << "\n";
    std::cout << "Same client code can work with different subclasses:\n";
    ConcreteClass2* concreteClass2 = new ConcreteClass2;
    ClientCode(concreteClass2);
    delete concreteClass1;
    delete concreteClass2;
    return 0;
}
```

### 备忘录模式

备忘录模式是一种行为设计模式， 允许在不暴露对象实现细节的情况下保存和恢复对象之前的状态。

```cpp
/**
 * The Memento interface provides a way to retrieve the memento's metadata, such
 * as creation date or name. However, it doesn't expose the Originator's state.
 */
class Memento {
public:
    virtual ~Memento() {}
    virtual std::string GetName() const = 0;
    virtual std::string date() const = 0;
    virtual std::string state() const = 0;
};

/**
 * The Concrete Memento contains the infrastructure for storing the Originator's
 * state.
 */
class ConcreteMemento : public Memento {
private:
    std::string state_;
    std::string date_;

public:
    ConcreteMemento(std::string state) : state_(state) {
        this->state_ = state;
        std::time_t now = std::time(0);
        this->date_ = std::ctime(&now);
    }
    /**
     * The Originator uses this method when restoring its state.
     */
    std::string state() const override {
        return this->state_;
    }
    /**
     * The rest of the methods are used by the Caretaker to display metadata.
     */
    std::string GetName() const override {
        return this->date_ + " / (" + this->state_.substr(0, 9) + "...)";
    }
    std::string date() const override {
        return this->date_;
    }
};

/**
 * The Originator holds some important state that may change over time. It also
 * defines a method for saving the state inside a memento and another method for
 * restoring the state from it.
 */
class Originator {
    /**
     * @var string For the sake of simplicity, the originator's state is stored
     * inside a single variable.
     */
private:
    std::string state_;

    std::string GenerateRandomString(int length = 10) {
        const char alphanum[] =
            "0123456789"
            "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            "abcdefghijklmnopqrstuvwxyz";
        int stringLength = sizeof(alphanum) - 1;

        std::string random_string;
        for (int i = 0; i < length; i++) {
            random_string += alphanum[std::rand() % stringLength];
        }
        return random_string;
    }

public:
    Originator(std::string state) : state_(state) {
        std::cout << "Originator: My initial state is: " << this->state_ << "\n";
    }
    /**
     * The Originator's business logic may affect its internal state. Therefore,
     * the client should backup the state before launching methods of the business
     * logic via the save() method.
     */
    void DoSomething() {
        std::cout << "Originator: I'm doing something important.\n";
        this->state_ = this->GenerateRandomString(30);
        std::cout << "Originator: and my state has changed to: " << this->state_ << "\n";
    }

    /**
     * Saves the current state inside a memento.
     */
    Memento* Save() {
        return new ConcreteMemento(this->state_);
    }
    /**
     * Restores the Originator's state from a memento object.
     */
    void Restore(Memento* memento) {
        this->state_ = memento->state();
        std::cout << "Originator: My state has changed to: " << this->state_ << "\n";
    }
};

/**
 * The Caretaker doesn't depend on the Concrete Memento class. Therefore, it
 * doesn't have access to the originator's state, stored inside the memento. It
 * works with all mementos via the base Memento interface.
 */
class Caretaker {
    /**
     * @var Memento[]
     */
private:
    std::vector<Memento*> mementos_;

    /**
     * @var Originator
     */
    Originator* originator_;

public:
    Caretaker(Originator* originator) : originator_(originator) {
    }

    ~Caretaker() {
        for (auto m : mementos_) delete m;
    }

    void Backup() {
        std::cout << "\nCaretaker: Saving Originator's state...\n";
        this->mementos_.push_back(this->originator_->Save());
    }
    void Undo() {
        if (!this->mementos_.size()) {
            return;
        }
        Memento* memento = this->mementos_.back();
        this->mementos_.pop_back();
        std::cout << "Caretaker: Restoring state to: " << memento->GetName() << "\n";
        try {
            this->originator_->Restore(memento);
        } catch (...) {
            this->Undo();
        }
    }
    void ShowHistory() const {
        std::cout << "Caretaker: Here's the list of mementos:\n";
        for (Memento* memento : this->mementos_) {
            std::cout << memento->GetName() << "\n";
        }
    }
};
/**
 * Client code.
 */

void ClientCode() {
    Originator* originator = new Originator("Super-duper-super-puper-super.");
    Caretaker* caretaker = new Caretaker(originator);
    caretaker->Backup();
    originator->DoSomething();
    caretaker->Backup();
    originator->DoSomething();
    caretaker->Backup();
    originator->DoSomething();
    std::cout << "\n";
    caretaker->ShowHistory();
    std::cout << "\nClient: Now, let's rollback!\n\n";
    caretaker->Undo();
    std::cout << "\nClient: Once more!\n\n";
    caretaker->Undo();

    delete originator;
    delete caretaker;
}

int main() {
    std::srand(static_cast<unsigned int>(std::time(NULL)));
    ClientCode();
    return 0;
}
```

### 中介者模式

中介者模式是一种行为设计模式， 能让你减少对象之间混乱无序的依赖关系。 该模式会限制对象之间的直接交互， 迫使它们通过一个中介者对象进行合作。

```cpp
#include <iostream>
#include <string>
/**
 * The Mediator interface declares a method used by components to notify the
 * mediator about various events. The Mediator may react to these events and
 * pass the execution to other components.
 */
class BaseComponent;
class Mediator {
public:
    virtual void Notify(BaseComponent* sender, std::string event) const = 0;
};

/**
 * The Base Component provides the basic functionality of storing a mediator's
 * instance inside component objects.
 */
class BaseComponent {
protected:
    Mediator* mediator_;

public:
    BaseComponent(Mediator* mediator = nullptr) : mediator_(mediator) {
    }
    void set_mediator(Mediator* mediator) {
        this->mediator_ = mediator;
    }
};

/**
 * Concrete Components implement various functionality. They don't depend on
 * other components. They also don't depend on any concrete mediator classes.
 */
class Component1 : public BaseComponent {
public:
    void DoA() {
        std::cout << "Component 1 does A.\n";
        this->mediator_->Notify(this, "A");
    }
    void DoB() {
        std::cout << "Component 1 does B.\n";
        this->mediator_->Notify(this, "B");
    }
};

class Component2 : public BaseComponent {
public:
    void DoC() {
        std::cout << "Component 2 does C.\n";
        this->mediator_->Notify(this, "C");
    }
    void DoD() {
        std::cout << "Component 2 does D.\n";
        this->mediator_->Notify(this, "D");
    }
};

/**
 * Concrete Mediators implement cooperative behavior by coordinating several
 * components.
 */
class ConcreteMediator : public Mediator {
private:
    Component1* component1_;
    Component2* component2_;

public:
    ConcreteMediator(Component1* c1, Component2* c2) : component1_(c1), component2_(c2) {
        this->component1_->set_mediator(this);
        this->component2_->set_mediator(this);
    }
    void Notify(BaseComponent* sender, std::string event) const override {
        if (event == "A") {
            std::cout << "Mediator reacts on A and triggers following operations:\n";
            this->component2_->DoC();
        }
        if (event == "D") {
            std::cout << "Mediator reacts on D and triggers following operations:\n";
            this->component1_->DoB();
            this->component2_->DoC();
        }
    }
};

/**
 * The client code.
 */

void ClientCode() {
    Component1* c1 = new Component1;
    Component2* c2 = new Component2;
    ConcreteMediator* mediator = new ConcreteMediator(c1, c2);
    std::cout << "Client triggers operation A.\n";
    c1->DoA();
    std::cout << "\n";
    std::cout << "Client triggers operation D.\n";
    c2->DoD();

    delete c1;
    delete c2;
    delete mediator;
}

int main() {
    ClientCode();
    return 0;
}
```

### 迭代器模式

迭代器模式是一种行为设计模式， 让你能在不暴露集合底层表现形式 （列表、 栈和树等） 的情况下遍历集合中所有的元素。

```cpp
/**
 * Iterator Design Pattern
 *
 * Intent: Lets you traverse elements of a collection without exposing its
 * underlying representation (list, stack, tree, etc.).
 */

#include <iostream>
#include <string>
#include <vector>

/**
 * C++ has its own implementation of iterator that works with a different
 * generics containers defined by the standard library.
 */

template <typename T, typename U>
class Iterator {
public:
    typedef typename std::vector<T>::iterator iter_type;
    Iterator(U* p_data, bool reverse = false) : m_p_data_(p_data) {
        m_it_ = m_p_data_->m_data_.begin();
    }

    void First() {
        m_it_ = m_p_data_->m_data_.begin();
    }

    void Next() {
        m_it_++;
    }

    bool IsDone() {
        return (m_it_ == m_p_data_->m_data_.end());
    }

    iter_type Current() {
        return m_it_;
    }

private:
    U* m_p_data_;
    iter_type m_it_;
};

/**
 * Generic Collections/Containers provides one or several methods for retrieving
 * fresh iterator instances, compatible with the collection class.
 */

template <class T>
class Container {
    friend class Iterator<T, Container>;

public:
    void Add(T a) {
        m_data_.push_back(a);
    }

    Iterator<T, Container>* CreateIterator() {
        return new Iterator<T, Container>(this);
    }

private:
    std::vector<T> m_data_;
};

class Data {
public:
    Data(int a = 0) : m_data_(a) {}

    void set_data(int a) {
        m_data_ = a;
    }

    int data() {
        return m_data_;
    }

private:
    int m_data_;
};

/**
 * The client code may or may not know about the Concrete Iterator or Collection
 * classes, for this implementation the container is generic so you can used
 * with an int or with a custom class.
 */
void ClientCode() {
    std::cout << "________________Iterator with int______________________________________" << std::endl;
    Container<int> cont;

    for (int i = 0; i < 10; i++) {
        cont.Add(i);
    }

    Iterator<int, Container<int>>* it = cont.CreateIterator();
    for (it->First(); !it->IsDone(); it->Next()) {
        std::cout << *it->Current() << std::endl;
    }

    Container<Data> cont2;
    Data a(100), b(1000), c(10000);
    cont2.Add(a);
    cont2.Add(b);
    cont2.Add(c);

    std::cout << "________________Iterator with custom Class______________________________" << std::endl;
    Iterator<Data, Container<Data>>* it2 = cont2.CreateIterator();
    for (it2->First(); !it2->IsDone(); it2->Next()) {
        std::cout << it2->Current()->data() << std::endl;
    }
    delete it;
    delete it2;
}

int main() {
    ClientCode();
    return 0;
}
```

### 命令模式

命令模式是一种行为设计模式， 它可将请求转换为一个包含与请求相关的所有信息的独立对象。 该转换让你能根据不同的请求将方法参数化、 延迟请求执行或将其放入队列中， 且能实现可撤销操作。

```cpp
/**
 * The Command interface declares a method for executing a command.
 */
class Command {
public:
    virtual ~Command() {
    }
    virtual void Execute() const = 0;
};
/**
 * Some commands can implement simple operations on their own.
 */
class SimpleCommand : public Command {
private:
    std::string pay_load_;

public:
    explicit SimpleCommand(std::string pay_load) : pay_load_(pay_load) {
    }
    void Execute() const override {
        std::cout << "SimpleCommand: See, I can do simple things like printing (" << this->pay_load_ << ")\n";
    }
};

/**
 * The Receiver classes contain some important business logic. They know how to
 * perform all kinds of operations, associated with carrying out a request. In
 * fact, any class may serve as a Receiver.
 */
class Receiver {
public:
    void DoSomething(const std::string& a) {
        std::cout << "Receiver: Working on (" << a << ".)\n";
    }
    void DoSomethingElse(const std::string& b) {
        std::cout << "Receiver: Also working on (" << b << ".)\n";
    }
};

/**
 * However, some commands can delegate more complex operations to other objects,
 * called "receivers."
 */
class ComplexCommand : public Command {
    /**
     * @var Receiver
     */
private:
    Receiver* receiver_;
    /**
     * Context data, required for launching the receiver's methods.
     */
    std::string a_;
    std::string b_;
    /**
     * Complex commands can accept one or several receiver objects along with any
     * context data via the constructor.
     */
public:
    ComplexCommand(Receiver* receiver, std::string a, std::string b) : receiver_(receiver), a_(a), b_(b) {
    }
    /**
     * Commands can delegate to any methods of a receiver.
     */
    void Execute() const override {
        std::cout << "ComplexCommand: Complex stuff should be done by a receiver object.\n";
        this->receiver_->DoSomething(this->a_);
        this->receiver_->DoSomethingElse(this->b_);
    }
};

/**
 * The Invoker is associated with one or several commands. It sends a request to
 * the command.
 */
class Invoker {
    /**
     * @var Command
     */
private:
    Command* on_start_;
    /**
     * @var Command
     */
    Command* on_finish_;
    /**
     * Initialize commands.
     */
public:
    ~Invoker() {
        delete on_start_;
        delete on_finish_;
    }

    void SetOnStart(Command* command) {
        this->on_start_ = command;
    }
    void SetOnFinish(Command* command) {
        this->on_finish_ = command;
    }
    /**
     * The Invoker does not depend on concrete command or receiver classes. The
     * Invoker passes a request to a receiver indirectly, by executing a command.
     */
    void DoSomethingImportant() {
        std::cout << "Invoker: Does anybody want something done before I begin?\n";
        if (this->on_start_) {
            this->on_start_->Execute();
        }
        std::cout << "Invoker: ...doing something really important...\n";
        std::cout << "Invoker: Does anybody want something done after I finish?\n";
        if (this->on_finish_) {
            this->on_finish_->Execute();
        }
    }
};
/**
 * The client code can parameterize an invoker with any commands.
 */

int main() {
    Invoker* invoker = new Invoker;
    invoker->SetOnStart(new SimpleCommand("Say Hi!"));
    Receiver* receiver = new Receiver;
    invoker->SetOnFinish(new ComplexCommand(receiver, "Send email", "Save report"));
    invoker->DoSomethingImportant();

    delete invoker;
    delete receiver;

    return 0;
}
```

### 访问者模式

责任链模式是一种行为设计模式， 允许你将请求沿着处理者链进行发送。 收到请求后， 每个处理者均可对请求进行处理， 或将其传递给链上的下个处理者。

```cpp
/**
 * The Handler interface declares a method for building the chain of handlers.
 * It also declares a method for executing a request.
 */
class Handler {
public:
    virtual Handler* SetNext(Handler* handler) = 0;
    virtual std::string Handle(std::string request) = 0;
};
/**
 * The default chaining behavior can be implemented inside a base handler class.
 */
class AbstractHandler : public Handler {
    /**
     * @var Handler
     */
private:
    Handler* next_handler_;

public:
    AbstractHandler() : next_handler_(nullptr) {
    }
    Handler* SetNext(Handler* handler) override {
        this->next_handler_ = handler;
        // Returning a handler from here will let us link handlers in a convenient
        // way like this:
        // $monkey->setNext($squirrel)->setNext($dog);
        return handler;
    }
    std::string Handle(std::string request) override {
        if (this->next_handler_) {
            return this->next_handler_->Handle(request);
        }

        return {};
    }
};
/**
 * All Concrete Handlers either handle a request or pass it to the next handler
 * in the chain.
 */
class MonkeyHandler : public AbstractHandler {
public:
    std::string Handle(std::string request) override {
        if (request == "Banana") {
            return "Monkey: I'll eat the " + request + ".\n";
        } else {
            return AbstractHandler::Handle(request);
        }
    }
};
class SquirrelHandler : public AbstractHandler {
public:
    std::string Handle(std::string request) override {
        if (request == "Nut") {
            return "Squirrel: I'll eat the " + request + ".\n";
        } else {
            return AbstractHandler::Handle(request);
        }
    }
};
class DogHandler : public AbstractHandler {
public:
    std::string Handle(std::string request) override {
        if (request == "MeatBall") {
            return "Dog: I'll eat the " + request + ".\n";
        } else {
            return AbstractHandler::Handle(request);
        }
    }
};
/**
 * The client code is usually suited to work with a single handler. In most
 * cases, it is not even aware that the handler is part of a chain.
 */
void ClientCode(Handler& handler) {
    std::vector<std::string> food = {"Nut", "Banana", "Cup of coffee"};
    for (const std::string& f : food) {
        std::cout << "Client: Who wants a " << f << "?\n";
        const std::string result = handler.Handle(f);
        if (!result.empty()) {
            std::cout << "  " << result;
        } else {
            std::cout << "  " << f << " was left untouched.\n";
        }
    }
}
/**
 * The other part of the client code constructs the actual chain.
 */
int main() {
    MonkeyHandler* monkey = new MonkeyHandler;
    SquirrelHandler* squirrel = new SquirrelHandler;
    DogHandler* dog = new DogHandler;
    monkey->SetNext(squirrel)->SetNext(dog);

    /**
     * The client should be able to send a request to any handler, not just the
     * first one in the chain.
     */
    std::cout << "Chain: Monkey > Squirrel > Dog\n\n";
    ClientCode(*monkey);
    std::cout << "\n";
    std::cout << "Subchain: Squirrel > Dog\n\n";
    ClientCode(*squirrel);

    delete monkey;
    delete squirrel;
    delete dog;

    return 0;
}
```

```{toctree}
:titlesonly:
:glob:
:hidden:

design-patterns/*
```
