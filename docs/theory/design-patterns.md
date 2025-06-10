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

根据不同参数创建不同类型日志记录对象。

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
    void print_log() override {
        printf("DatabaseLog");
    }
};

class FileLog : public ILog {
public:
    void print_log() override {
        printf("FileLog");
    }
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
    void print_log() override {
        printf("DatabaseLog");
    }
};

class FileLog : public ILog {
public:
    void print_log() override {
        printf("FileLog");
    }
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

### 抽象工厂模式

跨平台 UI 库，创建按钮、文本框等组件族。

```cpp
#include <cstdio>
#include <memory> // for std::unique_ptr and std::make_unique
using namespace std;

// =================== 抽象产品类 ===================
class IButton {
public:
    virtual void render() = 0;
    virtual ~IButton() = default;
};

class IText {
public:
    virtual void display() = 0;
    virtual ~IText() = default;
};

// =================== 具体产品类 - Windows 风格 ======
class WinButton : public IButton {
public:
    void render() override {
        printf("Windows Button\n");
    }
};

class WinText : public IText {
public:
    void display() override {
        printf("Windows Text\n");
    }
};

// =================== 具体产品类 - Mac 风格 ==========
class MacButton : public IButton {
public:
    void render() override {
        printf("Mac Button\n");
    }
};

class MacText : public IText {
public:
    void display() override {
        printf("Mac Text\n");
    }
};

// =================== 抽象工厂类 ===================
class IUIFactory {
public:
    virtual unique_ptr<IButton> createButton() = 0;
    virtual unique_ptr<IText> createText() = 0;
    virtual ~IUIFactory() = default;
};

// =================== 具体工厂类 ===================
class WinUIFactory : public IUIFactory {
public:
    unique_ptr<IButton> createButton() override {
        return make_unique<WinButton>();
    }

    unique_ptr<IText> createText() override {
        return make_unique<WinText>();
    }
};

class MacUIFactory : public IUIFactory {
public:
    unique_ptr<IButton> createButton() override {
        return make_unique<MacButton>();
    }

    unique_ptr<IText> createText() override {
        return make_unique<MacText>();
    }
};

// =================== 客户端使用 ===================
void renderUI(IUIFactory& factory) {
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

构建不同配置的计算机，如 CPU、内存、硬盘组合。

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
    void setCPU(const string& cpuType) {
        cpu = cpuType;
    }

    void setRAM(const string& ramSize) {
        ram = ramSize;
    }

    void setStorage(const string& storageSize) {
        storage = storageSize;
    }

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
    virtual void buildCPU() = 0;
    virtual void buildRAM() = 0;
    virtual void buildStorage() = 0;
    virtual Computer* getComputer() = 0;
    virtual ~IComputerBuilder() = default;
};

// ================== 具体构建器：游戏电脑 ==================
class GamingComputerBuilder : public IComputerBuilder {
private:
    Computer* computer;

public:
    GamingComputerBuilder() {
        computer = new Computer();
    }

    void buildCPU() override {
        computer->setCPU("Intel i9-13900K");
    }

    void buildRAM() override {
        computer->setRAM("64GB DDR5");
    }

    void buildStorage() override {
        computer->setStorage("2TB NVMe SSD");
    }

    Computer* getComputer() override {
        return computer;
    }
};

// ================== 具体构建器：办公电脑 ==================
class OfficeComputerBuilder : public IComputerBuilder {
private:
    Computer* computer;

public:
    OfficeComputerBuilder() {
        computer = new Computer();
    }

    void buildCPU() override {
        computer->setCPU("Intel i5-13400");
    }

    void buildRAM() override {
        computer->setRAM("16GB DDR4");
    }

    void buildStorage() override {
        computer->setStorage("512GB SSD");
    }

    Computer* getComputer() override {
        return computer;
    }
};

// ================== 指挥者类 ==================
class Director {
private:
    IComputerBuilder* builder;

public:
    void setBuilder(IComputerBuilder* newBuilder) {
        builder = newBuilder;
    }

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

### 原型模式

复制已有用户配置生成新用户默认设置。

```cpp
#include <iostream>
#include <string>
using namespace std;

// ================== 原型接口 ==================
class UserConfigPrototype {
public:
    virtual UserConfigPrototype* clone() const = 0; // 克隆接口
    virtual void print() const = 0;
    virtual ~UserConfigPrototype() = default;
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

    void print() const override {
        cout << "当前 IP 配置: " << ipAddress << endl;
    }
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

### 单例模式

数据库连接池，确保全局唯一访问。

```cpp
#include <iostream>
#include <cstdio>
using namespace std;

// ================== 单例类：数据库连接池 ==================
class DatabaseConnectionPool {
private:
    // 私有构造函数，防止外部创建实例
    DatabaseConnectionPool() {
        printf("数据库连接池已初始化\n");
    }

    // 删除拷贝构造函数和赋值操作符，防止复制
    DatabaseConnectionPool(const DatabaseConnectionPool&) = delete;
    DatabaseConnectionPool& operator=(const DatabaseConnectionPool&) = delete;

public:
    // 静态方法，提供全局访问点（C++11 起保证线程安全）
    static DatabaseConnectionPool& getInstance() {
        static DatabaseConnectionPool instance; // 局部静态变量，延迟加载
        return instance;
    }

    // 示例方法：显示连接池状态
    void connect() {
        printf("连接到数据库...\n");
    }
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

## 结构型模式

### 适配器模式

将旧支付接口适配为支持新支付网关调用。

```cpp
#include <cstdio>
using namespace std;

// ================== 老支付接口（旧系统）==================
class LegacyPayment {
public:
    void makeOldPayment(double amount) {
        printf("旧系统支付 %.2f 元\n", amount);
    }
};

// ================== 新支付网关接口（新系统期望的格式）==================
class INewPaymentGateway {
public:
    virtual void pay(double amount) = 0;
    virtual ~INewPaymentGateway() = default;
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

### 组合模式

文件系统管理，处理文件夹包含文件的结构。

```cpp
#include <cstdio>
#include <string>
#include <vector>
using namespace std;

// ================== 抽象组件：文件系统组件 ==================
class IFileSystemComponent {
public:
    virtual void showDetail(int depth = 0) const = 0;
    virtual ~IFileSystemComponent() = default;
};

// ================== 叶子组件：文件 ==================
class File : public IFileSystemComponent {
private:
    string name;

public:
    explicit File(const string& fileName) : name(fileName) {}

    void showDetail(int depth = 0) const override {
        for (int i = 0; i < depth; ++i) printf("  ");
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

    void add(IFileSystemComponent* component) {
        components.push_back(component);
    }

    void showDetail(int depth = 0) const override {
        for (int i = 0; i < depth; ++i) printf("  ");
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
    Directory* root = new Directory("根目录");
    Directory* documents = new Directory("文档");
    Directory* pictures = new Directory("图片");

    File* file1 = new File("report.docx");
    File* file2 = new File("photo.jpg");
    File* file3 = new File("notes.txt");

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

### 外观模式

简化下单流程，统一调用库存、支付、物流接口。

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

    void reduceStock(int productId) {
        printf("减少商品 %d 的库存\n", productId);
    }
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

    int productId = 101;
    double amount = 99.9;
    string address = "北京市朝阳区某某街道";

    bool success = orderSystem.placeOrder(productId, amount, address);

    if (success) {
        printf("订单已完成。\n");
    } else {
        printf("订单失败。\n");
    }

    return 0;
}
```

### 桥接模式

不同形状（圆形、方形）与颜色（红、蓝）组合。

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
    string applyColor() const override {
        return "红色";
    }
};

// 具体实现类：蓝色
class BlueColor : public IColor {
public:
    string applyColor() const override {
        return "蓝色";
    }
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

    string draw() const override {
        return "圆形，填充为" + color.applyColor();
    }
};

// 扩展抽象类：方形
class Square : public IShape {
public:
    Square(IColor& c) : IShape(c) {}

    string draw() const override {
        return "方形，填充为" + color.applyColor();
    }
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

### 装饰模式

给文本添加滚动条或边框等附加功能。

```cpp
#include <cstdio>
#include <string>
using namespace std;

// 组件接口：所有具体组件和装饰器都实现这个接口
class ITextDisplay {
public:
    virtual string getContent() const = 0;
    virtual void show() const {
        printf("%s\n", getContent().c_str());
    };
    virtual ~ITextDisplay() = default;
};

// 具体组件：基础文本显示
class PlainTextDisplay : public ITextDisplay {
private:
    string text;

public:
    PlainTextDisplay(const string& t) : text(t) {}

    string getContent() const override {
        return text;
    }
};

// 装饰器基类：保持对组件的引用
class TextDisplayDecorator : public ITextDisplay {
protected:
    ITextDisplay* decoratedText;

public:
    TextDisplayDecorator(ITextDisplay* decorated) : decoratedText(decorated) {}

    string getContent() const override {
        return decoratedText->getContent();
    }

    void show() const override {
        printf("%s\n", getContent().c_str());
    }
};

// 具体装饰器1：添加滚动条
class ScrollBarDecorator : public TextDisplayDecorator {
public:
    ScrollBarDecorator(ITextDisplay* decorated)
        : TextDisplayDecorator(decorated) {}

    string getContent() const override {
        return "[滚动条开始]" + decoratedText->getContent() + "[滚动条结束]";
    }
};

// 具体装饰器2：添加边框
class BorderDecorator : public TextDisplayDecorator {
public:
    BorderDecorator(ITextDisplay* decorated)
        : TextDisplayDecorator(decorated) {}

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

### 享元模式

文字编辑器中共享相同字体格式的对象。

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
        printf("应用格式: 字体=%s, 大小=%d, 颜色=%s\n", fontName.c_str(), fontSize, color.c_str());
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
    shared_ptr<FontFormat> getFontFormat(const string& fontName, int fontSize, const string& color) {
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
    Character(char c, shared_ptr<FontFormat> format)
        : value(c), fontFormat(format) {}

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

### 代理模式

远程调用服务代理，隐藏网络通信细节。

```cpp
#include <iostream>
#include <cstdio>
using namespace std;

class IService {
public:
    virtual void doCall() = 0;
    virtual ~IService() = default;
};

class RealService : public IService {
public:
    void doCall() override {
        printf("Calling Real Service\n");
    }
    ~RealService() override {
        printf("Destroying Real Service\n");
    }
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
            realService = new RealService(); // 延迟加载
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

## 行为模式

### 策略模式

支付方式选择，如支付宝、微信、银联策略切换。

```cpp
#include <iostream>
#include <cstdio>
using namespace std;

// ================== 策略接口 ==================
class IPaymentStrategy {
public:
    virtual void payAmount(int amount) = 0; // 支付指定金额
    virtual ~IPaymentStrategy() = default;
};

// ================== 具体策略类 ==================
class AlipayStrategy : public IPaymentStrategy {
public:
    void payAmount(int amount) override {
        printf("通过支付宝支付: %d 元\n", amount);
    }
};

class WechatPayStrategy : public IPaymentStrategy {
public:
    void payAmount(int amount) override {
        printf("通过微信支付: %d 元\n", amount);
    }
};

class UnionPayStrategy : public IPaymentStrategy {
public:
    void payAmount(int amount) override {
        printf("通过银联支付: %d 元\n", amount);
    }
};

// ================== 上下文 Context ==================
class PaymentContext {
private:
    IPaymentStrategy* currentStrategy;

public:
    PaymentContext(IPaymentStrategy* strategy) : currentStrategy(strategy) {}

    void setStrategy(IPaymentStrategy* strategy) {
        currentStrategy = strategy;
    }

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

### 观察者模式

天气预报系统，多个设备自动更新天气数据。

```cpp
#include <vector>
#include <algorithm>
#include <cstdio>
using namespace std;

class ISubscriber {
public:
    virtual void update() = 0;
    virtual ~ISubscriber() = default;
};

class IPublisher {
public:
    virtual void registerObserver(ISubscriber* subscriber) = 0;
    virtual void removeObserver(ISubscriber* subscriber) = 0;
    virtual void notifyObservers() = 0;
    virtual ~IPublisher() = default;
};

class Subscriber : public ISubscriber {
public:
    void update() override {
        printf("Device updated\n");
    }
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

    ~Publisher() override {
        subscribers.clear();
    }
};

int main() {
    // 创建具体的订阅者（设备）
    ISubscriber* airConditioner = new Subscriber(); // 空调
    ISubscriber* waterHeater = new Subscriber();    // 热水器

    // 创建发布者（天气站）
    IPublisher* weatherStation = new Publisher();

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

### 状态模式

订单状态变更，如待付款、已发货、已完成。

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
    virtual ~OrderState() = default;
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

    void setState(OrderState* newState) {
        currentState = newState;
    }

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

### 模板方法模式

单元测试框架定义测试执行流程，子类实现用例。

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

    virtual void setup() {
        printf("IUTest: Setup resources.\n");
    }

    virtual void executeTest() = 0; // 子类必须实现

    virtual void teardown() {
        printf("IUTest: Teardown resources.\n");
    }

    virtual ~IUTest() = default;
};

// 子类实现具体步骤
class AppTest : public IUTest {
public:
    void executeTest() override {
        printf("Running test in AppTest.\n");
    }

    void setup() override {
        printf("AppTest: Custom setup.\n");
    }

    void teardown() override {
        printf("AppTest: Custom teardown.\n");
    }
};

int main() {
    AppTest test;
    test.runTestCase(); // 调用模板方法，执行完整流程

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
