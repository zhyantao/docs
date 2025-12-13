# 破除循环引用：智能指针与友元函数的实践

## 方法一：使用 weak_ptr 破除智能指针循环引用

在对象间存在父子关系时，使用智能指针可能导致循环引用。通过让 parent 持有 child 的 shared_ptr，而 child 持有 parent 的 weak_ptr，可以安全地破除循环引用，避免内存泄漏。

```cpp
#include <iostream>
#include <memory>

class Child; // 前向声明

class Parent {
private:
    std::shared_ptr<Child> child; // parent 持有 child 的 shared_ptr

public:
    Parent() { std::cout << "Parent created\n"; }

    ~Parent() { std::cout << "Parent destroyed\n"; }

    void setChild(const std::shared_ptr<Child>& c) { child = c; }
};

class Child {
private:
    std::weak_ptr<Parent> parent; // child 持有 parent 的 weak_ptr，避免循环引用

public:
    Child(const std::shared_ptr<Parent>& p) : parent(p) { std::cout << "Child created\n"; }

    ~Child() { std::cout << "Child destroyed\n"; }

    void useParent() {
        if (auto sp = parent.lock()) { // 安全地获取 parent
            std::cout << "Using parent\n";
        } else {
            std::cout << "Parent already destroyed\n";
        }
    }
};

int main() {
    // 创建 parent 和 child
    auto parent = std::make_shared<Parent>();
    auto child = std::make_shared<Child>(parent);

    // 建立双向关系
    parent->setChild(child);

    // 使用 child 访问 parent
    child->useParent();

    // 当 main 函数结束时，parent 和 child 都能正确销毁
    // 不会发生内存泄漏
    return 0;
}
```

**关键点说明：**

- `Parent` 持有 `Child` 的 `shared_ptr`，拥有 `Child` 的所有权
- `Child` 持有 `Parent` 的 `weak_ptr`，仅观察而不拥有所有权
- 当 `Parent` 被销毁时，`Child` 的 `weak_ptr` 自动失效
- 使用 `weak_ptr::lock()` 安全地访问 `Parent` 对象

## 方法二：使用 boost::scoped_ptr 实现单向所有权

`boost::scoped_ptr` 提供严格的独占所有权语义，不能复制或转移所有权，非常适合表达明确的单向拥有关系。这可以天然地避免循环引用问题。

```cpp
#include <iostream>
#include <boost/scoped_ptr.hpp>

class Component; // 前向声明

class Owner {
private:
    boost::scoped_ptr<Component> component; // 独占拥有 Component

public:
    Owner();
    ~Owner() { std::cout << "Owner destroyed\n"; }

    void useComponent();
};

class Component {
private:
    Owner* owner; // 只持有原始指针，不拥有所有权

public:
    Component(Owner* own) : owner(own) { std::cout << "Component created\n"; }

    ~Component() { std::cout << "Component destroyed\n"; }

    void doSomething() {
        if (owner) {
            std::cout << "Component accessing owner\n";
        }
    }
};

Owner::Owner() : component(new Component(this)) {
    std::cout << "Owner created\n";
}

void Owner::useComponent() {
    if (component) {
        component->doSomething();
    }
}

int main() {
    {
        Owner owner; // 创建 Owner，自动创建 Component
        owner.useComponent();

        // 当 owner 离开作用域时：
        // 1. owner 被销毁
        // 2. component 自动被销毁
        // 3. 没有循环引用问题
    }

    std::cout << "Both Owner and Component properly destroyed\n";
    return 0;
}
```

**scoped_ptr 特点：**

- **独占所有权**：不能复制或赋值，天然避免所有权共享
- **自动管理**：离开作用域时自动释放资源
- **明确语义**：清晰地表达"拥有"关系
- **性能优越**：开销几乎与原始指针相同

## 方法三：使用友元函数破除循环引用

当类之间存在紧密协作但不需要共享所有权时，可以使用友元函数来破除循环依赖，同时保持封装性。

```cpp
#include <iostream>

class Sniper; // 前向声明

class Supplier {
private:
    int storage;

public:
    Supplier(int storage = 1000) : storage(storage) {}

    // 声明友元关系
    bool provide(Sniper& sniper);

    int getStorage() const { return storage; }
};

class Sniper {
private:
    int bullets;

    // 声明 Supplier::provide 为友元函数
    friend bool Supplier::provide(Sniper& sniper);

public:
    Sniper(int bullets = 0) : bullets(bullets) {}

    int getBullets() const { return bullets; }
};

// 友元函数实现 - 可以访问 Sniper 的私有成员
bool Supplier::provide(Sniper& sniper) {
    if (sniper.bullets < 20) { // 直接访问私有成员
        if (storage > 100) {
            sniper.bullets += 100;
            storage -= 100;
        } else if (storage > 0) {
            sniper.bullets += storage;
            storage = 0;
        } else {
            return false;
        }
    }

    std::cout << "Sniper has " << sniper.bullets << " bullets, Supplier has " << storage
              << " storage left.\n";
    return true;
}

int main() {
    Sniper sniper(5);       // 初始只有 5 发子弹
    Supplier supplier(250); // 初始有 250 库存

    std::cout << "Initial state:\n";
    std::cout << "Sniper bullets: " << sniper.getBullets() << "\n";
    std::cout << "Supplier storage: " << supplier.getStorage() << "\n\n";

    // 供应商为狙击手补充弹药
    supplier.provide(sniper);

    return 0;
}
```

## 三种方法的对比与选择

| 特性             | weak_ptr 方法        | boost::scoped_ptr 方法 | 友元函数方法           |
| ---------------- | -------------------- | ---------------------- | ---------------------- |
| **所有权语义**   | 共享所有权 + 弱引用  | 严格独占所有权         | 无所有权关系           |
| **内存安全**     | 自动管理，防止泄漏   | 自动管理，无泄漏风险   | 需手动管理生命周期     |
| **灵活性**       | 高，支持共享和弱引用 | 低，所有权不可转移     | 中等，仅提供访问权限   |
| **性能开销**     | 中等（引用计数）     | 极低（近似原始指针）   | 无额外开销             |
| **适用场景**     | 需要共享访问的对象图 | 明确的独占拥有关系     | 紧密协作的独立对象     |
| **循环引用风险** | 可安全破除           | 天然避免（单向拥有）   | 无智能指针，无循环引用 |

## 实际应用建议

### 1. **根据所有权关系选择**

- **明确父子关系** → 使用 `boost::scoped_ptr`（父拥有子）或 `weak_ptr`（双向弱引用）
- **资源共享** → 使用 `shared_ptr` + `weak_ptr`
- **独立协作** → 使用友元函数 + 原始指针

### 2. **现代 C++ 替代方案**

在 C++11 及以上版本，可以使用 `std::unique_ptr` 替代 `boost::scoped_ptr`：

```cpp
#include <memory>

class ModernOwner {
private:
    std::unique_ptr<Component> component; // C++11 独占指针

public:
    ModernOwner() : component(std::make_unique<Component>(this)) {}
    // unique_ptr 提供移动语义，比 scoped_ptr 更灵活
};
```

### 3. **混合模式示例**

```cpp
#include <memory>
#include <boost/scoped_ptr.hpp>

class ComplexSystem {
private:
    // 独占核心组件
    boost::scoped_ptr<CoreComponent> core;

    // 共享可替换模块
    std::shared_ptr<PluginModule> plugin;

    // 观察者使用弱引用
    std::vector<std::weak_ptr<Observer>> observers;

public:
    ComplexSystem() : core(new CoreComponent()) {}

    void setPlugin(std::shared_ptr<PluginModule> p) { plugin = p; }

    // 友元函数用于深度优化
    friend void optimizeSystem(ComplexSystem& sys);
};
```

## 总结

破除循环引用是 C++ 资源管理的关键技能。三种方法各有优势：

1. **`weak_ptr` 方案**：适用于复杂的对象网络，提供安全的共享访问
2. **`boost::scoped_ptr` 方案**：简洁高效，适合明确的单向拥有关系
3. **友元函数方案**：适用于紧密协作但生命周期独立的对象

在实际开发中，应优先考虑使用智能指针（特别是独占指针）来管理资源，只在必要时使用友元函数。对于新项目，推荐使用 C++11 的 `std::unique_ptr` 和 `std::shared_ptr`/`weak_ptr` 组合；对于已有 Boost 的项目，`boost::scoped_ptr` 仍然是可靠的选择。

无论选择哪种方案，关键是清晰地表达对象间的所有权关系，这是编写安全、高效 C++ 代码的基础。
