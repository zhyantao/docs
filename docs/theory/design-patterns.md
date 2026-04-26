# 设计模式

```{dropdown} 逆序析构过程（多态析构）

当基类的析构函数被声明为 `virtual` 时，通过基类指针或引用删除派生类对象时，C++ 会根据实际对象类型调用对应的析构函数，确保析构顺序为：

1. **首先执行派生类的析构函数**
2. 然后**自动调用其直接基类的析构函数**
3. 继续向上回溯，直到最顶层的基类

这个机制称为**多态析构（Polymorphic Destruction）**。它保证了对象生命周期结束时资源能正确释放，避免内存泄漏和未定义行为。

---

手动析构 vs 自动析构 对比表

| 手动析构                               | 自动析构（多态析构）                              |
| -------------------------------------- | ------------------------------------------------- |
| 显式调用 `delete` 或析构函数           | 通过基类指针调用 `delete`，且基类析构为 `virtual` |
| 只析构指针类型对应的对象（可能不完整） | 按照继承层次从派生类到基类依次析构                |
| 不安全（若用于多态类型）               | 安全（推荐用于多态基类）                          |
| `delete obj;`（obj 是具体类型）        | `Base* ptr = new Derived(); delete ptr;`          |

---

在面向对象设计中，尤其是使用继承和接口时，务必在基类中将析构函数设为 `virtual`。
```

学习设计模式一定要跟具体的场景联系起来，知道什么时候用什么设计模式才是最重要的。

一个运行代码的网址：<https://coliru.stacked-crooked.com/>

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

| 模式名称 | 使用场景           | 例子                                 |
| -------- | ------------------ | ------------------------------------ |
| 工厂模式 | 统一管理类的实例化 | 根据不同参数创建不同类型日志记录对象 |

::::{tab-set}
:::{tab-item} 基础版本

```cpp
#include <string>
#include <cstdio>
using namespace std;

class ILog {
public:
    virtual ~ILog() {}; // Fix compile warning
    virtual void print_log() = 0;
};

class DatabaseLog : public ILog {
public:
    void print_log() override { printf("DatabaseLog"); }
};

class FileLog : public ILog {
public:
    void print_log() override { printf("FileLog"); }
};

class LogFactory {
public:
    ILog* createLog(string type) {
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
    ILog* log = factory.createLog("database");
    if (log) {
        log->print_log();
        delete log;
    }
    return 0;
}
```

:::

:::{tab-item} 语法优化

```cpp
#include <string>
#include <cstdio>
#include <memory> // 智能指针防止内存泄漏
using namespace std;

class ILog {
public:
    virtual void print_log() = 0;
    virtual ~ILog() {}; // Fix compile warning
};

class DatabaseLog : public ILog {
public:
    void print_log() override { printf("DatabaseLog"); }
};

class FileLog : public ILog {
public:
    void print_log() override { printf("FileLog"); }
};

class LogFactory {
public:
    unique_ptr<ILog> createLog(const string& type) {
        if (type == "database") {
            return make_unique<DatabaseLog>();
        } else if (type == "file") {
            return make_unique<FileLog>();
        }
        return NULL;
    }
};

int main() {
    LogFactory factory;
    auto log = factory.createLog("database");
    if (log) {
        log->print_log();
    }
    return 0;
}
```

:::
::::

执行结果：

```text
DatabaseLog
```

### 抽象工厂模式

| 模式名称     | 使用场景                 | 例子                                   |
| ------------ | ------------------------ | -------------------------------------- |
| 抽象工厂模式 | 创建一组相关或依赖对象族 | 跨平台 UI 库，创建按钮、文本框等组件族 |

```cpp
#include <cstdio>
#include <memory> // for std::unique_ptr and std::make_unique
using namespace std;

// =================== 抽象产品类 ===================
class IButton {
public:
    virtual void render() = 0;
    virtual ~IButton()    = default;
};

class IText {
public:
    virtual void display() = 0;
    virtual ~IText()       = default;
};

// =================== 具体产品类 - Windows 风格 ======
class WinButton : public IButton {
public:
    void render() override { printf("Windows Button\n"); }
};

class WinText : public IText {
public:
    void display() override { printf("Windows Text\n"); }
};

// =================== 具体产品类 - Mac 风格 ==========
class MacButton : public IButton {
public:
    void render() override { printf("Mac Button\n"); }
};

class MacText : public IText {
public:
    void display() override { printf("Mac Text\n"); }
};

// =================== 抽象工厂类 ===================
class IUIFactory {
public:
    virtual unique_ptr<IButton> createButton() = 0;
    virtual unique_ptr<IText> createText()     = 0;
    virtual ~IUIFactory()                      = default;
};

// =================== 具体工厂类 ===================
class WinUIFactory : public IUIFactory {
public:
    unique_ptr<IButton> createButton() override { return make_unique<WinButton>(); }

    unique_ptr<IText> createText() override { return make_unique<WinText>(); }
};

class MacUIFactory : public IUIFactory {
public:
    unique_ptr<IButton> createButton() override { return make_unique<MacButton>(); }

    unique_ptr<IText> createText() override { return make_unique<MacText>(); }
};

// =================== 客户端使用 ===================
void renderUI(IUIFactory& factory) {
    auto button = factory.createButton();
    auto text   = factory.createText();

    button->render(); // 根据平台调用不同的实现
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

执行结果：

```text
Rendering Windows UI:
Windows Button
Windows Text

Rendering Mac UI:
Mac Button
Mac Text
```

### 生成器模式

| 模式名称   | 使用场景           | 例子                                         |
| ---------- | ------------------ | -------------------------------------------- |
| 生成器模式 | 分步骤构建复杂对象 | 构建不同配置的计算机，如 CPU、内存、硬盘组合 |

```cpp
#include <iostream>
#include <string>
using namespace std;

// ================== 产品类：计算机 ==================
class Computer {
private:
    string cpu;
    string ram;
    string storage;

public:
    void setCPU(const string& cpuType) { cpu = cpuType; }

    void setRAM(const string& ramSize) { ram = ramSize; }

    void setStorage(const string& storageSize) { storage = storageSize; }

    void showSpecs() const {
        cout << "电脑配置：" << endl;
        cout << "CPU: " << cpu << endl;
        cout << "内存: " << ram << endl;
        cout << "硬盘: " << storage << endl;
    }
};

// ================== 构建器接口 ==================
class IComputerBuilder {
public:
    virtual void buildCPU()         = 0;
    virtual void buildRAM()         = 0;
    virtual void buildStorage()     = 0;
    virtual Computer* getComputer() = 0;
    virtual ~IComputerBuilder()     = default;
};

// ================== 具体构建器：游戏电脑 ==================
class GamingComputerBuilder : public IComputerBuilder {
private:
    Computer* computer;

public:
    GamingComputerBuilder() { computer = new Computer(); }

    void buildCPU() override { computer->setCPU("Intel i9-13900K"); }

    void buildRAM() override { computer->setRAM("64GB DDR5"); }

    void buildStorage() override { computer->setStorage("2TB NVMe SSD"); }

    Computer* getComputer() override { return computer; }
};

// ================== 具体构建器：办公电脑 ==================
class OfficeComputerBuilder : public IComputerBuilder {
private:
    Computer* computer;

public:
    OfficeComputerBuilder() { computer = new Computer(); }

    void buildCPU() override { computer->setCPU("Intel i5-13400"); }

    void buildRAM() override { computer->setRAM("16GB DDR4"); }

    void buildStorage() override { computer->setStorage("512GB SSD"); }

    Computer* getComputer() override { return computer; }
};

// ================== 指挥者类 ==================
class Director {
private:
    IComputerBuilder* builder;

public:
    void setBuilder(IComputerBuilder* newBuilder) { builder = newBuilder; }

    void constructComputer() {
        builder->buildCPU();
        builder->buildRAM();
        builder->buildStorage();
    }
};

// ================== 主函数示例 ==================
int main() {
    Director director;

    // 构建游戏电脑
    GamingComputerBuilder gamingBuilder;
    director.setBuilder(&gamingBuilder);
    director.constructComputer();
    Computer* gamingPC = gamingBuilder.getComputer();
    gamingPC->showSpecs();

    cout << "-------------------------" << endl;

    // 构建办公电脑
    OfficeComputerBuilder officeBuilder;
    director.setBuilder(&officeBuilder);
    director.constructComputer();
    Computer* officePC = officeBuilder.getComputer();
    officePC->showSpecs();

    // 手动释放内存（可考虑使用智能指针）
    delete gamingPC;
    delete officePC;

    return 0;
}
```

执行结果：

```text
电脑配置：
CPU: Intel i9-13900K
内存: 64GB DDR5
硬盘: 2TB NVMe SSD
-------------------------
电脑配置：
CPU: Intel i5-13400
内存: 16GB DDR4
硬盘: 512GB SSD
```

### 原型模式

| 模式名称 | 使用场景                   | 例子                               |
| -------- | -------------------------- | ---------------------------------- |
| 原型模式 | 通过复制已有对象创建新对象 | 复制已有用户配置生成新用户默认设置 |

```cpp
#include <iostream>
#include <string>
using namespace std;

// ================== 原型接口 ==================
class UserConfigPrototype {
public:
    virtual UserConfigPrototype* clone() const = 0; // 克隆接口
    virtual void print() const                 = 0;
    virtual ~UserConfigPrototype()             = default;
};

// ================== 具体原型类 ==================
class UserConfig : public UserConfigPrototype {
private:
    string ipAddress;

public:
    explicit UserConfig(const string& ip) : ipAddress(ip) {}

    // 深拷贝实现（因为 string 和 vector 本身已实现深拷贝）
    UserConfigPrototype* clone() const override {
        return new UserConfig(*this); // 调用拷贝构造函数
    }

    void print() const override { cout << "当前 IP 配置: " << ipAddress << endl; }
};

// ================== 主函数示例 ==================
int main() {
    // 创建原型对象
    UserConfig original("26.10.128.0/20");
    original.print();

    // 克隆新对象
    UserConfigPrototype* copy = original.clone();
    copy->print();

    delete copy; // 手动释放内存（如未使用智能指针）

    return 0;
}
```

执行结果：

```text
当前 IP 配置: 26.10.128.0/20
当前 IP 配置: 26.10.128.0/20
```

### 单例模式

| 模式名称 | 使用场景               | 例子                           |
| -------- | ---------------------- | ------------------------------ |
| 单例模式 | 确保一个类只有一个实例 | 数据库连接池，确保全局唯一访问 |

```cpp
#include <iostream>
#include <cstdio>
using namespace std;

// ================== 单例类：数据库连接池 ==================
class DatabaseConnectionPool {
private:
    // 私有构造函数，防止外部创建实例
    DatabaseConnectionPool() { printf("数据库连接池已初始化\n"); }

    // 删除拷贝构造函数和赋值操作符，防止复制
    DatabaseConnectionPool(const DatabaseConnectionPool&)            = delete;
    DatabaseConnectionPool& operator=(const DatabaseConnectionPool&) = delete;

public:
    // 静态方法，提供全局访问点（C++11 起保证线程安全）
    static DatabaseConnectionPool& getInstance() {
        static DatabaseConnectionPool instance; // 局部静态变量，延迟加载
        return instance;
    }

    // 示例方法：显示连接池状态
    void connect() { printf("连接到数据库...\n"); }
};

// ================== 主函数示例 ==================
int main() {
    // 获取单例实例并调用方法
    DatabaseConnectionPool& pool = DatabaseConnectionPool::getInstance();
    pool.connect();

    // 再次获取实例，验证是否为同一个对象
    DatabaseConnectionPool& pool2 = DatabaseConnectionPool::getInstance();
    if (&pool == &pool2) {
        printf("pool 和 pool2 是同一个实例。\n");
    }

    return 0;
}
```

执行结果：

```text
数据库连接池已初始化
连接到数据库...
pool 和 pool2 是同一个实例。
```

## 结构型模式

### 适配器模式

| 模式名称   | 使用场景       | 例子                                 |
| ---------- | -------------- | ------------------------------------ |
| 适配器模式 | 兼容不兼容接口 | 将旧支付接口适配为支持新支付网关调用 |

```cpp
#include <cstdio>
using namespace std;

// ================== 老支付接口（旧系统）==================
class LegacyPayment {
public:
    void makeOldPayment(double amount) { printf("旧系统支付 %.2f 元\n", amount); }
};

// ================== 新支付网关接口（新系统期望的格式）==================
class INewPaymentGateway {
public:
    virtual void pay(double amount) = 0;
    virtual ~INewPaymentGateway()   = default;
};

// ===== 适配器类：将 LegacyPayment 包装成 INewPaymentGateway 格式 =====
class PaymentAdapter : public INewPaymentGateway {
private:
    LegacyPayment* legacyPayment; // 适配的对象

public:
    PaymentAdapter(LegacyPayment* payment) : legacyPayment(payment) {}

    // 实现新接口中的支付方法
    void pay(double amount) override {
        printf("通过适配器调用新接口，准备使用旧系统支付...\n");
        legacyPayment->makeOldPayment(amount); // 调用旧接口
    }
};

// ================== 主函数示例 ==================
int main() {
    // 创建旧系统的支付对象
    LegacyPayment oldPaymentSystem;

    // 创建适配器，将旧系统包装成新接口格式
    PaymentAdapter adapter(&oldPaymentSystem);

    // 使用统一的新接口进行支付
    adapter.pay(199.5);

    return 0;
}
```

执行结果：

```text
通过适配器调用新接口，准备使用旧系统支付...
旧系统支付 199.50 元
```

### 组合模式

| 模式名称 | 使用场景                 | 例子                                   |
| -------- | ------------------------ | -------------------------------------- |
| 组合模式 | 树形结构处理，如文件系统 | 文件系统管理，处理文件夹包含文件的结构 |

```cpp
#include <cstdio>
#include <string>
#include <vector>
using namespace std;

// ================== 抽象组件：文件系统组件 ==================
class IFileSystemComponent {
public:
    virtual void showDetail(int depth = 0) const = 0;
    virtual ~IFileSystemComponent()              = default;
};

// ================== 叶子组件：文件 ==================
class File : public IFileSystemComponent {
private:
    string name;

public:
    explicit File(const string& fileName) : name(fileName) {}

    void showDetail(int depth = 0) const override {
        for (int i = 0; i < depth; ++i)
            printf("  ");
        printf("📄 文件: %s\n", name.c_str());
    }
};

// ================== 复合组件：文件夹 ==================
class Directory : public IFileSystemComponent {
private:
    string name;
    vector<IFileSystemComponent*> components;

public:
    explicit Directory(const string& dirName) : name(dirName) {}

    void add(IFileSystemComponent* component) { components.push_back(component); }

    void showDetail(int depth = 0) const override {
        for (int i = 0; i < depth; ++i)
            printf("  ");
        printf("📁 文件夹: %s\n", name.c_str());

        for (const auto& comp : components) {
            comp->showDetail(depth + 1);
        }
    }

    ~Directory() override {
        for (auto comp : components) {
            delete comp;
        }
    }
};

// ================== 主函数示例 ==================
int main() {
    // 所有组件都用 new 分配在堆上
    Directory* root      = new Directory("根目录");
    Directory* documents = new Directory("文档");
    Directory* pictures  = new Directory("图片");

    File* file1          = new File("report.docx");
    File* file2          = new File("photo.jpg");
    File* file3          = new File("notes.txt");

    // 添加组件
    documents->add(file1);
    pictures->add(file2);

    root->add(documents);
    root->add(pictures);
    root->add(file3);

    // 显示结构
    root->showDetail();

    // 最后统一释放根节点即可（递归释放所有子节点）
    delete root;

    return 0;
}
```

执行结果：

```text
📁 文件夹: 根目录
  📁 文件夹: 文档
    📄 文件: report.docx
  📁 文件夹: 图片
    📄 文件: photo.jpg
  📄 文件: notes.txt
```

### 外观模式

| 模式名称 | 使用场景             | 例子                                       |
| -------- | -------------------- | ------------------------------------------ |
| 外观模式 | 简化子系统的调用入口 | 简化下单流程，统一调用库存、支付、物流接口 |

```cpp
#include <cstdio>
#include <string>
using namespace std;

// 子系统类：库存服务
class InventoryService {
public:
    bool checkStock(int productId) {
        printf("检查商品 %d 的库存...\n", productId);
        // 模拟库存充足
        return true;
    }

    void reduceStock(int productId) { printf("减少商品 %d 的库存\n", productId); }
};

// 子系统类：支付服务
class PaymentService {
public:
    bool processPayment(double amount) {
        printf("处理支付金额 %.2f 元...\n", amount);
        // 模拟支付成功
        return true;
    }
};

// 子系统类：物流服务
class ShippingService {
public:
    void shipOrder(const string& address) {
        printf("订单已发货，地址：%s\n", address.c_str());
    }
};

// 外观类：统一下单接口
class OrderFacade {
private:
    InventoryService inventory;
    PaymentService payment;
    ShippingService shipping;

public:
    bool placeOrder(int productId, double amount, const string& address) {
        printf("开始下单流程...\n");

        if (!inventory.checkStock(productId)) {
            printf("库存不足，无法下单。\n");
            return false;
        }

        if (!payment.processPayment(amount)) {
            printf("支付失败。\n");
            return false;
        }

        inventory.reduceStock(productId);
        shipping.shipOrder(address);

        printf("下单成功！\n");
        return true;
    }
};

// 客户端代码
int main() {
    OrderFacade orderSystem;

    int productId  = 101;
    double amount  = 99.9;
    string address = "北京市朝阳区某某街道";

    bool success   = orderSystem.placeOrder(productId, amount, address);

    if (success) {
        printf("订单已完成。\n");
    } else {
        printf("订单失败。\n");
    }

    return 0;
}
```

执行结果：

```text
开始下单流程...
检查商品 101 的库存...
处理支付金额 99.90 元...
减少商品 101 的库存
订单已发货，地址：北京市朝阳区某某街道
下单成功！
订单已完成。
```

### 桥接模式

| 模式名称 | 使用场景                 | 例子                                       |
| -------- | ------------------------ | ------------------------------------------ |
| 桥接模式 | 抽象与实现分离，独立变化 | 不同形状（圆形、方形）与颜色（红、蓝）组合 |

```cpp
#include <cstdio>
#include <string>
using namespace std;

// 实现接口：颜色
class IColor {
public:
    virtual string applyColor() const = 0;
};

// 具体实现类：红色
class RedColor : public IColor {
public:
    string applyColor() const override { return "红色"; }
};

// 具体实现类：蓝色
class BlueColor : public IColor {
public:
    string applyColor() const override { return "蓝色"; }
};

// 抽象类：形状
class IShape {
protected:
    IColor& color; // 桥接到颜色

public:
    IShape(IColor& c) : color(c) {}
    virtual string draw() const = 0;
};

// 扩展抽象类：圆形
class Circle : public IShape {
public:
    Circle(IColor& c) : IShape(c) {}

    string draw() const override { return "圆形，填充为" + color.applyColor(); }
};

// 扩展抽象类：方形
class Square : public IShape {
public:
    Square(IColor& c) : IShape(c) {}

    string draw() const override { return "方形，填充为" + color.applyColor(); }
};

// 客户端代码
int main() {
    RedColor red;
    BlueColor blue;

    // 组合1：红色圆形
    Circle redCircle(red);
    printf("%s\n", redCircle.draw().c_str());

    // 组合2：蓝色圆形
    Circle blueCircle(blue);
    printf("%s\n", blueCircle.draw().c_str());

    // 组合3：红色方形
    Square redSquare(red);
    printf("%s\n", redSquare.draw().c_str());

    // 组合4：蓝色方形
    Square blueSquare(blue);
    printf("%s\n", blueSquare.draw().c_str());

    return 0;
}
```

执行结果：

```text
圆形，填充为红色
圆形，填充为蓝色
方形，填充为红色
方形，填充为蓝色
```

### 装饰模式

| 模式名称 | 使用场景                   | 例子                             |
| -------- | -------------------------- | -------------------------------- |
| 装饰模式 | 动态添加功能，比继承更灵活 | 给文本添加滚动条或边框等附加功能 |

```cpp
#include <cstdio>
#include <string>
using namespace std;

// 组件接口：所有具体组件和装饰器都实现这个接口
class ITextDisplay {
public:
    virtual string getContent() const = 0;
    virtual void show() const { printf("%s\n", getContent().c_str()); };
    virtual ~ITextDisplay() = default;
};

// 具体组件：基础文本显示
class PlainTextDisplay : public ITextDisplay {
private:
    string text;

public:
    PlainTextDisplay(const string& t) : text(t) {}

    string getContent() const override { return text; }
};

// 装饰器基类：保持对组件的引用
class TextDisplayDecorator : public ITextDisplay {
protected:
    ITextDisplay* decoratedText;

public:
    TextDisplayDecorator(ITextDisplay* decorated) : decoratedText(decorated) {}

    string getContent() const override { return decoratedText->getContent(); }

    void show() const override { printf("%s\n", getContent().c_str()); }
};

// 具体装饰器1：添加滚动条
class ScrollBarDecorator : public TextDisplayDecorator {
public:
    ScrollBarDecorator(ITextDisplay* decorated) : TextDisplayDecorator(decorated) {}

    string getContent() const override {
        return "[滚动条开始]" + decoratedText->getContent() + "[滚动条结束]";
    }
};

// 具体装饰器2：添加边框
class BorderDecorator : public TextDisplayDecorator {
public:
    BorderDecorator(ITextDisplay* decorated) : TextDisplayDecorator(decorated) {}

    string getContent() const override {
        return "[边框开始]" + decoratedText->getContent() + "[边框结束]";
    }
};

// 客户端代码
int main() {
    // 基础文本
    ITextDisplay* basicText = new PlainTextDisplay("这是一个普通文本内容");
    basicText->show();

    // 加边框的文本
    ITextDisplay* borderedText = new BorderDecorator(basicText);
    borderedText->show();

    // 加滚动条的文本
    ITextDisplay* scrollText = new ScrollBarDecorator(basicText);
    scrollText->show();

    // 加滚动条和边框的文本（嵌套装饰）
    ITextDisplay* fullFeaturedText = new BorderDecorator(new ScrollBarDecorator(basicText));
    fullFeaturedText->show();

    // 清理资源
    delete basicText;
    delete borderedText;
    delete scrollText;
    delete fullFeaturedText;

    return 0;
}
```

执行结果：

```text
这是一个普通文本内容
[边框开始]这是一个普通文本内容[边框结束]
[滚动条开始]这是一个普通文本内容[滚动条结束]
[边框开始][滚动条开始]这是一个普通文本内容[滚动条结束][边框结束]
```

### 享元模式

| 模式名称 | 使用场景             | 例子                               |
| -------- | -------------------- | ---------------------------------- |
| 享元模式 | 共享对象减少内存开销 | 文字编辑器中共享相同字体格式的对象 |

```cpp
#include <iostream>
#include <string>
#include <unordered_map>
#include <memory>

using namespace std;

// =============================
// 1. 享元类（共享的字体格式）
// =============================
class FontFormat {
public:
    string fontName;
    int fontSize;
    string color;

    FontFormat(const string& name, int size, const string& color)
        : fontName(name), fontSize(size), color(color) {}

    void applyFormat() const {
        printf("应用格式: 字体=%s, 大小=%d, 颜色=%s\n", fontName.c_str(), fontSize,
               color.c_str());
    }
};

// =============================
// 2. 享元工厂类
// =============================
class FontFormatFactory {
private:
    unordered_map<string, shared_ptr<FontFormat>> pool;

    // 构造 key 的辅助函数
    string getKey(const string& fontName, int fontSize, const string& color) {
        return fontName + "-" + to_string(fontSize) + "-" + color;
    }

public:
    shared_ptr<FontFormat> getFontFormat(const string& fontName, int fontSize,
                                         const string& color) {
        string key = getKey(fontName, fontSize, color);
        if (pool.find(key) == pool.end()) {
            // 如果没有就创建一个新的
            pool[key] = make_shared<FontFormat>(fontName, fontSize, color);
            cout << "新建格式: " << key << endl;
        } else {
            cout << "复用已有格式: " << key << endl;
        }
        return pool[key];
    }
};

// =============================
// 3. 字符类（使用享元）
// =============================
class Character {
private:
    char value;                        // 内容（内部状态）
    shared_ptr<FontFormat> fontFormat; // 格式（外部状态，由享元提供）

public:
    Character(char c, shared_ptr<FontFormat> format) : value(c), fontFormat(format) {}

    void render(int position) const {
        cout << "字符 '" << value << "' 在位置 " << position << " 渲染，";
        fontFormat->applyFormat();
    }
};

// =============================
// 4. 客户端代码
// =============================
int main() {
    FontFormatFactory factory;

    // 创建一些字符，部分格式重复
    auto format1 = factory.getFontFormat("宋体", 12, "黑色");
    auto format2 = factory.getFontFormat("微软雅黑", 14, "红色");
    auto format3 = factory.getFontFormat("宋体", 12, "黑色"); // 应该复用 format1

    Character c1('H', format1);
    Character c2('e', format1);
    Character c3('l', format2);
    Character c4('l', format2);
    Character c5('o', format3);

    c1.render(0);
    c2.render(1);
    c3.render(2);
    c4.render(3);
    c5.render(4);

    return 0;
}
```

执行结果：

```text
新建格式: 宋体-12-黑色
新建格式: 微软雅黑-14-红色
复用已有格式: 宋体-12-黑色
字符 'H' 在位置 0 渲染，应用格式: 字体=宋体, 大小=12, 颜色=黑色
字符 'e' 在位置 1 渲染，应用格式: 字体=宋体, 大小=12, 颜色=黑色
字符 'l' 在位置 2 渲染，应用格式: 字体=微软雅黑, 大小=14, 颜色=红色
字符 'l' 在位置 3 渲染，应用格式: 字体=微软雅黑, 大小=14, 颜色=红色
字符 'o' 在位置 4 渲染，应用格式: 字体=宋体, 大小=12, 颜色=黑色
```

### 代理模式

| 模式名称 | 使用场景               | 例子                               |
| -------- | ---------------------- | ---------------------------------- |
| 代理模式 | 代理控制对原对象的访问 | 远程调用服务代理，隐藏网络通信细节 |

```cpp
#include <iostream>
#include <cstdio>
using namespace std;

class IService {
public:
    virtual void doCall() = 0;
    virtual ~IService()   = default;
};

class RealService : public IService {
public:
    void doCall() override { printf("Calling Real Service\n"); }
    ~RealService() override { printf("Destroying Real Service\n"); }
};

class ServiceProxy : public IService {
private:
    RealService* realService; // 持有真实服务对象的引用
    bool hasBeenCalled;       // 示例；用于演示代理控制逻辑

public:
    ServiceProxy() : realService(nullptr), hasBeenCalled(false) {}

    void doCall(void) override {
        if (!hasBeenCalled) {
            printf("Creating Real Service\n");
            realService   = new RealService(); // 延迟加载
            hasBeenCalled = true;
        }
        realService->doCall();
    }

    ~ServiceProxy() override {
        printf("Calling ~ServcieProxy\n");
        delete realService;
    }
};

int main() {
    IService* proxy = new ServiceProxy();

    proxy->doCall(); // 第一次调用，触发初始化
    proxy->doCall(); // 第多次调用，无需重复初始化

    delete proxy;

    return 0;
}
```

执行结果：

```text
Creating Real Service
Calling Real Service
Calling Real Service
Calling ~ServcieProxy
Destroying Real Service
```

## 行为模式

### 策略模式

| 模式名称 | 使用场景             | 例子                                       |
| -------- | -------------------- | ------------------------------------------ |
| 策略模式 | 封装可互换的算法逻辑 | 支付方式选择，如支付宝、微信、银联策略切换 |

```cpp
#include <iostream>
#include <cstdio>
using namespace std;

// ================== 策略接口 ==================
class IPaymentStrategy {
public:
    virtual void payAmount(int amount) = 0; // 支付指定金额
    virtual ~IPaymentStrategy()        = default;
};

// ================== 具体策略类 ==================
class AlipayStrategy : public IPaymentStrategy {
public:
    void payAmount(int amount) override { printf("通过支付宝支付: %d 元\n", amount); }
};

class WechatPayStrategy : public IPaymentStrategy {
public:
    void payAmount(int amount) override { printf("通过微信支付: %d 元\n", amount); }
};

class UnionPayStrategy : public IPaymentStrategy {
public:
    void payAmount(int amount) override { printf("通过银联支付: %d 元\n", amount); }
};

// ================== 上下文 Context ==================
class PaymentContext {
private:
    IPaymentStrategy* currentStrategy;

public:
    PaymentContext(IPaymentStrategy* strategy) : currentStrategy(strategy) {}

    void setStrategy(IPaymentStrategy* strategy) { currentStrategy = strategy; }

    void executePayment(int amount) {
        if (currentStrategy) {
            currentStrategy->payAmount(amount);
        } else {
            fprintf(stderr, "未设置支付策略！\n");
        }
    }
};

// ================== 主函数示例 ==================
int main() {
    // 创建具体策略
    AlipayStrategy alipay;
    WechatPayStrategy wechatpay;
    UnionPayStrategy unionpay;

    // 创建上下文并切换策略
    PaymentContext context(&alipay);
    context.executePayment(100);

    context.setStrategy(&wechatpay);
    context.executePayment(200);

    context.setStrategy(&unionpay);
    context.executePayment(300);

    return 0;
}
```

执行结果：

```text
通过支付宝支付: 100 元
通过微信支付: 200 元
通过银联支付: 300 元
```

### 观察者模式

| 模式名称   | 使用场景         | 例子                                   |
| ---------- | ---------------- | -------------------------------------- |
| 观察者模式 | 实现事件通知机制 | 天气预报系统，多个设备自动更新天气数据 |

```cpp
#include <vector>
#include <algorithm>
#include <cstdio>
using namespace std;

class ISubscriber {
public:
    virtual void update()  = 0;
    virtual ~ISubscriber() = default;
};

class IPublisher {
public:
    virtual void registerObserver(ISubscriber* subscriber) = 0;
    virtual void removeObserver(ISubscriber* subscriber)   = 0;
    virtual void notifyObservers()                         = 0;
    virtual ~IPublisher()                                  = default;
};

class Subscriber : public ISubscriber {
public:
    void update() override { printf("Device updated\n"); }
};

class Publisher : public IPublisher {
private:
    std::vector<ISubscriber*> subscribers; // 维护订阅者列表
public:
    void registerObserver(ISubscriber* subscriber) override {
        subscribers.push_back(subscriber);
        printf("Device registered\n");
    }

    void removeObserver(ISubscriber* subscriber) override {
        auto it = remove(subscribers.begin(), subscribers.end(), subscriber);
        if (it != subscribers.end()) {
            subscribers.erase(it, subscribers.end());
        }
        printf("Device removed\n");
    }

    void notifyObservers() override {
        printf("Notifying all devices:\n");
        for (auto* subscriber : subscribers) {
            subscriber->update();
        }
    }

    ~Publisher() override { subscribers.clear(); }
};

int main() {
    // 创建具体的订阅者（设备）
    ISubscriber* airConditioner = new Subscriber(); // 空调
    ISubscriber* waterHeater    = new Subscriber(); // 热水器

    // 创建发布者（天气站）
    IPublisher* weatherStation  = new Publisher();

    // 注册设备到天气站
    weatherStation->registerObserver(airConditioner);
    weatherStation->registerObserver(waterHeater);

    // 模拟通知更新
    weatherStation->notifyObservers();

    // 清理资源
    delete weatherStation;
    delete airConditioner;
    delete waterHeater;

    return 0;
}
```

执行结果：

```text
Device registered
Device registered
Notifying all devices:
Device updated
Device updated
```

### 状态模式

| 模式名称 | 使用场景                   | 例子                                   |
| -------- | -------------------------- | -------------------------------------- |
| 状态模式 | 对象状态变化时行为随之变化 | 订单状态变更，如待付款、已发货、已完成 |

```cpp
#include <iostream>
#include <cstdio>
using namespace std;

// 前向声明 Order 类，供状态接口使用
class Order;

// =============== 状态接口 ===============
class OrderState {
public:
    virtual void process(Order& order) = 0; // 处理订单状态
    virtual ~OrderState()              = default;
};

// =============== 具体状态类 ===============
class InitializedState : public OrderState {
public:
    void process(Order& order) override;
};

class PaidState : public OrderState {
public:
    void process(Order& order) override;
};

class ShippedState : public OrderState {
public:
    void process(Order& order) override;
};

class CompletedState : public OrderState {
public:
    void process(Order& order) override;
};

// =============== 订单类 ===============
class Order {
private:
    OrderState* currentState;

public:
    Order(OrderState* initialState) : currentState(initialState) {}

    void setState(OrderState* newState) { currentState = newState; }

    void process() {
        if (currentState) {
            currentState->process(*this);
        }
    }

    friend class InitializedState;
    friend class PaidState;
    friend class ShippedState;
    friend class CompletedState;
};

// =============== 具体状态实现 ===============
void InitializedState::process(Order& order) {
    printf("订单已付款...\n");
    order.setState(new PaidState());
}

void PaidState::process(Order& order) {
    printf("订单已发货...\n");
    order.setState(new ShippedState());
}

void ShippedState::process(Order& order) {
    printf("订单已完成...\n");
    order.setState(new CompletedState());
}

void CompletedState::process(Order& order) {
    printf("订单已是完成状态，无法继续处理。\n");
}

// =============== 主函数示例 ===============
int main() {
    Order order(new InitializedState());

    order.process(); // 初始化 -> 已付款
    order.process(); // 已付款 -> 已发货
    order.process(); // 已发货 -> 已完成
    order.process(); // 已完成 -> 不可再操作

    return 0;
}
```

执行结果：

```text
订单已付款...
订单已发货...
订单已完成...
订单已是完成状态，无法继续处理。
```

### 模板方法模式

| 模式名称     | 使用场景                       | 例子                                       |
| ------------ | ------------------------------ | ------------------------------------------ |
| 模板方法模式 | 定义算法骨架，子类实现具体步骤 | 单元测试框架定义测试执行流程，子类实现用例 |

```cpp
#include <iostream>
#include <cstdio>
using namespace std;

// 基类定义算法框架（模板方法）
class IUTest {
public:
    // 模板方法：定义算法骨架
    void runTestCase() {
        setup();
        executeTest();
        teardown();
    }

    virtual void setup() { printf("IUTest: Setup resources.\n"); }

    virtual void executeTest() = 0; // 子类必须实现

    virtual void teardown() { printf("IUTest: Teardown resources.\n"); }

    virtual ~IUTest() = default;
};

// 子类实现具体步骤
class AppTest : public IUTest {
public:
    void executeTest() override { printf("Running test in AppTest.\n"); }

    void setup() override { printf("AppTest: Custom setup.\n"); }

    void teardown() override { printf("AppTest: Custom teardown.\n"); }
};

int main() {
    AppTest test;
    test.runTestCase(); // 调用模板方法，执行完整流程

    return 0;
}
```

执行结果：

```text
AppTest: Custom setup.
Running test in AppTest.
AppTest: Custom teardown.
```

### 备忘录模式

| 模式名称   | 使用场景               | 例子                                 |
| ---------- | ---------------------- | ------------------------------------ |
| 备忘录模式 | 保存和恢复对象内部状态 | 游戏存档功能，保存和恢复角色当前状态 |

```cpp
#include <cstdio>
#include <vector>
#include <memory>

using namespace std;

// 角色类
class GameRole {
public:
    int hp;
    int mp;
    int level;

    GameRole() : hp(100), mp(50), level(1) {}

    void showStatus() const {
        printf("当前角色状态：\n");
        printf("HP: %d, MP: %d, Level: %d\n", hp, mp, level);
    }

    unique_ptr<class RoleMemento> save() const;
    void restore(const class RoleMemento& memento);
};

// 备忘录类
class RoleMemento {
private:
    int hp;
    int mp;
    int level;

public:
    RoleMemento(int h, int m, int l) : hp(h), mp(m), level(l) {}

    friend class GameRole;

    void showMemento() const {
        printf("存档状态：HP: %d, MP: %d, Level: %d\n", hp, mp, level);
    }
};

unique_ptr<RoleMemento> GameRole::save() const {
    return make_unique<RoleMemento>(hp, mp, level);
}

void GameRole::restore(const RoleMemento& m) {
    hp    = m.hp;
    mp    = m.mp;
    level = m.level;
}

// 存档管理类
class ArchiveManager {
private:
    vector<unique_ptr<RoleMemento>> archives;

public:
    void addArchive(unique_ptr<RoleMemento> memento) { archives.push_back(move(memento)); }

    RoleMemento* getArchive(size_t index) const {
        return (index < archives.size()) ? archives[index].get() : nullptr;
    }

    void showArchives() const {
        for (size_t i = 0; i < archives.size(); ++i) {
            printf("存档 %zu: ", i);
            archives[i]->showMemento();
        }
    }
};

int main() {
    GameRole role;
    ArchiveManager manager;

    printf("--- 初始状态 ---\n");
    role.showStatus();

    manager.addArchive(role.save());

    // 修改状态
    role.hp    = 80;
    role.mp    = 40;
    role.level = 2;
    printf("\n--- 升级后状态 ---\n");
    role.showStatus();

    manager.addArchive(role.save());

    role.hp    = 30;
    role.mp    = 10;
    role.level = 3;
    printf("\n--- 受伤后状态 ---\n");
    role.showStatus();

    // 恢复第一个存档
    printf("\n--- 恢复到初始存档 ---\n");
    role.restore(*manager.getArchive(0));
    role.showStatus();

    printf("\n--- 所有存档列表 ---\n");
    manager.showArchives();

    return 0;
}
```

执行结果：

```text
--- 初始状态 ---
当前角色状态：
HP: 100, MP: 50, Level: 1

--- 升级后状态 ---
当前角色状态：
HP: 80, MP: 40, Level: 2

--- 受伤后状态 ---
当前角色状态：
HP: 30, MP: 10, Level: 3

--- 恢复到初始存档 ---
当前角色状态：
HP: 100, MP: 50, Level: 1

--- 所有存档列表 ---
存档 0: 存档状态：HP: 100, MP: 50, Level: 1
存档 1: 存档状态：HP: 80, MP: 40, Level: 2
```

### 中介者模式

| 模式名称   | 使用场景         | 例子                                     |
| ---------- | ---------------- | ---------------------------------------- |
| 中介者模式 | 集中管理对象交互 | 聊天室服务器协调多个客户端之间的消息发送 |

```cpp
#include <cstdio>
#include <vector>
#include <string>
#include <memory>
#include <iostream>

using namespace std;

// 前向声明
class ChatMediator;

// 用户类（同事类 Colleague）
class User : public enable_shared_from_this<User> {
private:
    string name;
    shared_ptr<ChatMediator> mediator;

public:
    User(const string& name, const shared_ptr<ChatMediator>& mediator)
        : name(name), mediator(mediator) {}

    void send(const string& message);
    void receive(const string& from, const string& message);

    const string& getName() const { return name; }
};

// 聊天室中介者类（Mediator）
class ChatMediator {
private:
    vector<shared_ptr<User>> users;

public:
    void addUser(const shared_ptr<User>& user) { users.push_back(user); }

    void sendMessage(const string& from, const string& message,
                     const shared_ptr<User>& excludeUser = nullptr) {
        for (const auto& user : users) {
            if (user != excludeUser) {
                user->receive(from, message);
            }
        }
    }
};

void User::send(const string& message) {
    printf("[%s] 发送消息: %s\n", name.c_str(), message.c_str());
    mediator->sendMessage(name, message, shared_from_this());
}

void User::receive(const string& from, const string& message) {
    printf("[%s] 收到来自 [%s] 的消息: %s\n", name.c_str(), from.c_str(), message.c_str());
}

int main() {
    // 创建中介者
    auto mediator = make_shared<ChatMediator>();

    // 创建用户并加入聊天室
    auto alice    = make_shared<User>("Alice", mediator);
    auto bob      = make_shared<User>("Bob", mediator);
    auto charlie  = make_shared<User>("Charlie", mediator);

    mediator->addUser(alice);
    mediator->addUser(bob);
    mediator->addUser(charlie);

    // Alice 发送消息
    alice->send("大家好！这是测试消息。");

    // Bob 回复
    bob->send("Hi Alice，收到你的消息了。");

    return 0;
}
```

执行结果：

```text
[Alice] 发送消息: 大家好！这是测试消息。
[Bob] 收到来自 [Alice] 的消息: 大家好！这是测试消息。
[Charlie] 收到来自 [Alice] 的消息: 大家好！这是测试消息。
[Bob] 发送消息: Hi Alice，收到你的消息了。
[Alice] 收到来自 [Bob] 的消息: Hi Alice，收到你的消息了。
[Charlie] 收到来自 [Bob] 的消息: Hi Alice，收到你的消息了。
```

### 迭代器模式

| 模式名称   | 使用场景                   | 例子                                 |
| ---------- | -------------------------- | ------------------------------------ |
| 迭代器模式 | 遍历聚合对象，不暴露其结构 | 遍历树形结构菜单项而不暴露其内部实现 |

```cpp
#include <cstdio>
#include <vector>
#include <string>
#include <memory>

using namespace std;

// 菜单项类
class MenuItem {
private:
    string name;
    string description;
    bool isVegetarian;
    double price;

public:
    MenuItem(const string& name, const string& description, bool isVegetarian, double price)
        : name(name), description(description), isVegetarian(isVegetarian), price(price) {}

    const string& getName() const { return name; }
    const string& getDescription() const { return description; }
    bool getIsVegetarian() const { return isVegetarian; }
    double getPrice() const { return price; }

    void print() const {
        printf("%s, %.2f元 -- %s\n", name.c_str(), price, description.c_str());
        if (isVegetarian) {
            printf("  (素食)\n");
        }
    }
};

// 迭代器接口
template <typename T>
class Iterator {
public:
    virtual bool hasNext() const = 0;
    virtual T next()             = 0;
    virtual ~Iterator()          = default;
};

// 聚合接口
template <typename T>
class Aggregate {
public:
    virtual unique_ptr<Iterator<T>> createIterator() const = 0;
    virtual ~Aggregate()                                   = default;
};

// 具体迭代器：基于 vector 的 Menu 迭代器
class MenuIterator : public Iterator<MenuItem> {
private:
    const vector<MenuItem>& items;
    size_t position;

public:
    MenuIterator(const vector<MenuItem>& items) : items(items), position(0) {}

    bool hasNext() const override { return position < items.size(); }

    MenuItem next() override {
        if (hasNext()) {
            return items[position++];
        }
        throw out_of_range("迭代器已到末尾");
    }
};

// 菜单类（聚合类）
class Menu : public Aggregate<MenuItem> {
private:
    vector<MenuItem> menuItems;

public:
    void addItem(const MenuItem& item) { menuItems.push_back(item); }

    unique_ptr<Iterator<MenuItem>> createIterator() const override {
        return make_unique<MenuIterator>(this->menuItems);
    }
};

int main() {
    // 创建菜单
    Menu menu;

    // 添加菜单项
    menu.addItem(MenuItem("汉堡", "新鲜牛肉汉堡", false, 18.5));
    menu.addItem(MenuItem("沙拉", "蔬菜沙拉配酸奶酱", true, 12.0));
    menu.addItem(MenuItem("披萨", "意大利香肠披萨", false, 22.0));
    menu.addItem(MenuItem("水果汁", "鲜榨橙汁", true, 8.0));

    // 使用迭代器遍历菜单
    auto iterator = menu.createIterator();

    printf("菜单列表：\n");
    while (iterator->hasNext()) {
        MenuItem item = iterator->next();
        item.print();
    }

    return 0;
}
```

执行结果：

```text
菜单列表：
汉堡, 18.50元 -- 新鲜牛肉汉堡
沙拉, 12.00元 -- 蔬菜沙拉配酸奶酱
  (素食)
披萨, 22.00元 -- 意大利香肠披萨
水果汁, 8.00元 -- 鲜榨橙汁
  (素食)
```

### 命令模式

| 模式名称 | 使用场景                        | 例子                                   |
| -------- | ------------------------------- | -------------------------------------- |
| 命令模式 | 将请求封装为对象，支持撤销/重做 | 实现操作回退功能，如撤销上一步编辑操作 |

```cpp
#include <cstdio>
#include <vector>
#include <string>
#include <memory>
#include <stack>

using namespace std;

// 接收者类：实际执行操作的对象
class TextEditor {
private:
    string content;

public:
    void write(const string& text) {
        content += text;
        printf("当前内容: %s\n", content.c_str());
    }

    void deleteContent(int length) {
        if (length > (int)content.size()) length = content.size();
        content.erase(content.size() - length, length);
        printf("当前内容: %s\n", content.c_str());
    }

    string getContent() const { return content; }
};

// 命令接口
class Command {
public:
    virtual ~Command()     = default;
    virtual void execute() = 0;
    virtual void undo()    = 0;
};

// 具体命令类：写入操作
class WriteCommand : public Command {
private:
    TextEditor& editor;
    string text;

public:
    WriteCommand(TextEditor& editor, const string& text) : editor(editor), text(text) {}

    void execute() override { editor.write(text); }

    void undo() override { editor.deleteContent(text.size()); }
};

// 调用者类：管理命令的执行与撤销
class CommandInvoker {
private:
    stack<shared_ptr<Command>> history;

public:
    void executeCommand(shared_ptr<Command> command) {
        command->execute();
        history.push(command);
    }

    void undo() {
        if (!history.empty()) {
            shared_ptr<Command> command = history.top();
            command->undo();
            history.pop();
        } else {
            printf("没有可撤销的操作。\n");
        }
    }
};

int main() {
    TextEditor editor;
    CommandInvoker invoker;

    // 执行写入操作
    invoker.executeCommand(make_shared<WriteCommand>(editor, "Hello "));
    invoker.executeCommand(make_shared<WriteCommand>(editor, "World!"));
    invoker.executeCommand(make_shared<WriteCommand>(editor, " How are you?"));

    // 撤销操作
    printf("\n--- 开始撤销 ---\n");
    invoker.undo();
    invoker.undo();
    invoker.undo();
    invoker.undo(); // 没有更多可撤销的内容

    return 0;
}
```

执行结果：

```text
当前内容: Hello
当前内容: Hello World!
当前内容: Hello World! How are you?

--- 开始撤销 ---
当前内容: Hello World!
当前内容: Hello
当前内容:
没有可撤销的操作。
```

### 访问者模式

| 模式名称   | 使用场景                       | 例子                                       |
| ---------- | ------------------------------ | ------------------------------------------ |
| 访问者模式 | 在不修改结构的前提下增加新操作 | 对文档元素（如段落、图片）进行不同格式导出 |

```cpp
#include <cstdio>
#include <vector>
#include <string>
#include <memory>
#include <iostream>

using namespace std;

// 前向声明
class Paragraph;
class Image;
class ExporterVisitor;

// 元素接口
class DocumentElement {
public:
    virtual ~DocumentElement()                    = default;
    virtual void accept(ExporterVisitor& visitor) = 0;
};

// 段落类
class Paragraph : public DocumentElement {
private:
    string text;

public:
    Paragraph(const string& text) : text(text) {}

    const string& getText() const { return text; }

    void accept(ExporterVisitor& visitor) override;
};

// 图片类
class Image : public DocumentElement {
private:
    string url;

public:
    Image(const string& url) : url(url) {}

    const string& getUrl() const { return url; }

    void accept(ExporterVisitor& visitor) override;
};

// 访问者接口（导出器）
class ExporterVisitor {
public:
    virtual ~ExporterVisitor()                     = default;
    virtual void visit(const Paragraph& paragraph) = 0;
    virtual void visit(const Image& image)         = 0;
};

// HTML 导出器
class HtmlExporter : public ExporterVisitor {
public:
    void visit(const Paragraph& paragraph) override {
        printf("<p>%s</p>\n", paragraph.getText().c_str());
    }

    void visit(const Image& image) override {
        printf("<img src=\"%s\" />\n", image.getUrl().c_str());
    }
};

// 纯文本导出器
class PlainTextExporter : public ExporterVisitor {
public:
    void visit(const Paragraph& paragraph) override {
        printf("%s\n", paragraph.getText().c_str());
    }

    void visit(const Image& image) override { printf("[图片: %s]\n", image.getUrl().c_str()); }
};

// Markdown 导出器
class MarkdownExporter : public ExporterVisitor {
public:
    void visit(const Paragraph& paragraph) override {
        printf("%s\n\n", paragraph.getText().c_str());
    }

    void visit(const Image& image) override {
        printf("![图片](%s)\n", image.getUrl().c_str());
    }
};

// 为了能调用 accept 方法，需要在类外实现
void Paragraph::accept(ExporterVisitor& visitor) {
    visitor.visit(*this);
}

void Image::accept(ExporterVisitor& visitor) {
    visitor.visit(*this);
}

// 文档类，包含多个文档元素
class Document {
private:
    vector<shared_ptr<DocumentElement>> elements;

public:
    void addElement(const shared_ptr<DocumentElement>& element) {
        elements.push_back(element);
    }

    void exportWith(ExporterVisitor& visitor) {
        for (const auto& element : elements) {
            element->accept(visitor);
        }
    }
};

int main() {
    // 创建文档并添加内容
    Document doc;
    doc.addElement(make_shared<Paragraph>("欢迎使用文档导出系统"));
    doc.addElement(make_shared<Image>("https://example.com/logo.png"));
    doc.addElement(make_shared<Paragraph>("这是第二段文字"));

    printf("=== 导出为 HTML ===\n");
    HtmlExporter htmlExporter;
    doc.exportWith(htmlExporter);

    printf("\n=== 导出为纯文本 ===\n");
    PlainTextExporter plainExporter;
    doc.exportWith(plainExporter);

    printf("\n=== 导出为 Markdown ===\n");
    MarkdownExporter markdownExporter;
    doc.exportWith(markdownExporter);

    return 0;
}
```

执行结果：

```text
=== 导出为 HTML ===
<p>欢迎使用文档导出系统</p>
<img src="https://example.com/logo.png" />
<p>这是第二段文字</p>

=== 导出为纯文本 ===
欢迎使用文档导出系统
[图片: https://example.com/logo.png]
这是第二段文字

=== 导出为 Markdown ===
欢迎使用文档导出系统

![图片](https://example.com/logo.png)
这是第二段文字
```

```{toctree}
:titlesonly:
:glob:
:hidden:

design-patterns/*
```
