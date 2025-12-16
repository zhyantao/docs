# RAII：资源管理机制

**RAII（Resource Acquisition Is Initialization，资源获取即初始化）** 是 C++ 的核心编程理念，通过对象的生命周期来管理资源（内存、文件句柄、锁等），确保资源在对象构造时获取，在对象析构时自动释放。

## 核心思想

- **构造函数获取资源**：对象创建时初始化并获取资源
- **析构函数释放资源**：对象销毁时自动释放资源
- **所有权明确**：资源所有权绑定到对象生命周期

## 简单例子：管理动态内存

```cpp
#include <iostream>

class SmartArray {
private:
    int* data;
    size_t size;

public:
    // 构造函数获取资源
    SmartArray(size_t n) : size(n) {
        data = new int[n];
        std::cout << "分配了 " << n << " 个整数的内存\n";
    }

    // 析构函数释放资源
    ~SmartArray() {
        delete[] data;
        std::cout << "释放了内存\n";
    }

    // 访问元素
    int& operator[](size_t index) { return data[index]; }
};

int main() {
    {
        SmartArray arr(10); // 构造时分配内存

        for (int i = 0; i < 10; i++) {
            arr[i] = i * 2; // 使用数组
        }

        // 离开作用域时，arr自动析构，内存自动释放
    } // 这里 arr 析构函数自动调用，释放内存

    std::cout << "内存已自动清理\n";
    return 0;
}
```

## 更多实用例子

### 1. 文件管理

```cpp
#include <fstream>
#include <iostream>
#include <string>

class FileHandler {
private:
    std::fstream file;

public:
    FileHandler(const std::string& filename, std::ios::openmode mode) {
        file.open(filename, mode);
        if (!file.is_open()) {
            throw std::runtime_error("无法打开文件");
        }
        std::cout << "文件已打开\n";
    }

    ~FileHandler() {
        if (file.is_open()) {
            file.close();
            std::cout << "文件已关闭\n";
        }
    }

    void write(const std::string& content) { file << content; }
};

int main() {
    try {
        FileHandler fh("test.txt", std::ios::out);
        fh.write("Hello RAII");
        // 离开作用域时文件自动关闭
    } catch (const std::exception& e) {
        std::cerr << e.what() << std::endl;
    }
    return 0;
}
```

### 2. 锁管理（线程安全）

```cpp
#include <iostream>
#include <mutex>
#include <thread>

class LockGuard {
private:
    std::mutex& mtx;

public:
    explicit LockGuard(std::mutex& m) : mtx(m) {
        mtx.lock();
        std::cout << "锁已获取\n";
    }

    ~LockGuard() {
        mtx.unlock();
        std::cout << "锁已释放\n";
    }

    // 禁止拷贝
    LockGuard(const LockGuard&) = delete;
    LockGuard& operator=(const LockGuard&) = delete;
};

std::mutex g_mutex;
int shared_data = 0;

void increment() {
    LockGuard lock(g_mutex); // 构造时加锁
    ++shared_data;           // 安全访问
    // 离开作用域时自动解锁
}

int main() {
    std::thread t1(increment);
    std::thread t2(increment);

    t1.join();
    t2.join();

    std::cout << "最终值: " << shared_data << std::endl;
    return 0;
}
```

### 3. 数据库连接管理

```cpp
#include <iostream>
#include <stdexcept>

class DatabaseConnection {
private:
    bool connected;

public:
    DatabaseConnection(const std::string& connectionString) : connected(false) {
        // 模拟连接数据库
        std::cout << "连接到数据库: " << connectionString << std::endl;
        connected = true;
    }

    ~DatabaseConnection() {
        if (connected) {
            std::cout << "断开数据库连接\n";
            // 实际会调用数据库断开连接
        }
    }

    void executeQuery(const std::string& query) {
        if (!connected) throw std::runtime_error("未连接数据库");
        std::cout << "执行查询: " << query << std::endl;
    }

    // 移动语义支持
    DatabaseConnection(DatabaseConnection&& other) noexcept : connected(other.connected) {
        other.connected = false;
    }

    DatabaseConnection& operator=(DatabaseConnection&& other) noexcept {
        if (this != &other) {
            if (connected) {
                std::cout << "断开旧连接\n";
            }
            connected = other.connected;
            other.connected = false;
        }
        return *this;
    }

    // 禁止拷贝
    DatabaseConnection(const DatabaseConnection&) = delete;
    DatabaseConnection& operator=(const DatabaseConnection&) = delete;
};
```

## RAII 的优势

| 优势             | 说明                           |
| ---------------- | ------------------------------ |
| **自动资源管理** | 避免忘记释放资源               |
| **异常安全**     | 即使发生异常，资源也能正确释放 |
| **代码简洁**     | 减少手动资源管理代码           |
| **所有权清晰**   | 资源生命周期与对象绑定         |

## 现代 C++ 中的 RAII 工具

- **智能指针**：`std::unique_ptr`, `std::shared_ptr`, `std::weak_ptr`
- **容器**：`std::vector`, `std::map`, `std::string`
- **锁管理**：`std::lock_guard`, `std::unique_lock`
- **文件流**：`std::ifstream`, `std::ofstream`

## 最佳实践

1. 为每个资源类型创建 RAII 类
2. 在构造函数中获取资源，析构函数中释放
3. 使用移动语义而非拷贝来转移资源所有权
4. 优先使用标准库提供的 RAII 类

RAII 是 C++ 区别于其他语言的重要特性，它通过对象的确定性析构来管理资源，是编写安全、高效 C++ 代码的基石。
