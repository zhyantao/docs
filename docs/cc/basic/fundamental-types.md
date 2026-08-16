# 基础数据类型

## bool

```cpp
#include <iostream>

using namespace std;

int main() {
    bool b1 = true;
    int i   = b1;
    bool b2 = -256;
    cout << "i=" << i << endl;
    cout << "b1=" << b1 << endl;
    cout << "b2=" << b2 << endl;
    cout << true << endl;
    return 0;
}
```

## char

```cpp
#include <iostream>

using namespace std;

int main() {
    char c1     = 'C';
    char c2     = 80;
    char c3     = 0x50;
    char16_t c4 = u'于';
    char32_t c5 = U'于';
    cout << c1 << ":" << c2 << ":" << c3 << endl;
    cout << +c1 << ":" << +c2 << ":" << +c3 << endl;
    cout << c4 << endl;
    cout << c5 << endl;

    return 0;
}
```

## union

```cpp
#include <iostream>

using namespace std;

union ipv4address {
    std::uint32_t address32;
    std::uint8_t address8[4];
};

int main() {
    union ipv4address ip;

    cout << "sizeof(ip) = " << sizeof(ip) << endl;

    ip.address8[3] = 127;
    ip.address8[2] = 0;
    ip.address8[1] = 0;
    ip.address8[0] = 1;

    cout << "The address is ";
    cout << +ip.address8[3] << ".";
    cout << +ip.address8[2] << ".";
    cout << +ip.address8[1] << ".";
    cout << +ip.address8[0] << endl;

    cout << std::hex;
    cout << "in hex " << ip.address32 << endl;

    return 0;
}
```

## struct

```cpp
#include <stdbool.h>
#include <stdio.h>
#include <string.h>

// typedef
// struct _Student{
//     char name[4];
//     int born;
//     bool male;
// } Student;

struct Student {
    char name[4];
    int born;
    bool male;
};

int main() {
    struct Student stu = {"Yu", 2000, true}; // initialization
    // strcpy(stu.name, "Yu");
    // stu.born = 2000;
    // stu.male = true;

    printf("Student %s, born in %d, gender %s\n", stu.name, stu.born,
           stu.male ? "male" : "female");

    struct Student students[100];
    students[50].born = 2002;

    return 0;
}
```

## enum

```cpp
// enum.cpp

#include <iostream>

using namespace std;

enum color { WHITE, BLACK, RED, GREEN, BLUE, YELLOW, NUM_COLORS };
enum datatype { TYPE_INT8 = 1, TYPE_INT16 = 2, TYPE_INT32 = 4, TYPE_INT64 = 8 };

struct Point {
    enum datatype type;
    union {
        std::int8_t data8[3];
        std::int16_t data16[3];
        std::int32_t data32[3];
        std::int64_t data64[3];
    };
};

size_t datawidth(struct Point pt) {
    return size_t(pt.type) * 3;
}

int64_t l1norm(struct Point pt) {
    int64_t result = 0;
    switch (pt.type) {
    case (TYPE_INT8): result = abs(pt.data8[0]) + abs(pt.data8[1]) + abs(pt.data8[2]); break;
    case (TYPE_INT16):
        result = abs(pt.data16[0]) + abs(pt.data16[1]) + abs(pt.data16[2]);
        break;
    case (TYPE_INT32):
        result = abs(pt.data32[0]) + abs(pt.data32[1]) + abs(pt.data32[2]);
        break;
    case (TYPE_INT64):
        result = abs(pt.data64[0]) + abs(pt.data64[1]) + abs(pt.data64[2]);
        break;
    }
    return result;
}

int main() {
    enum color pen_color = RED;
    pen_color            = color(3); // convert int to enum
    cout << "We have " << NUM_COLORS << " pens." << endl;
    // pen_color += 1; //error!
    int color_index  = pen_color;
    color_index     += 1;
    cout << "color_index = " << color_index << endl;

    // declaration and initialization
    struct Point point1 = {.type = TYPE_INT8, .data8 = {-2, 3, 4}};
    struct Point point2 = {.type = TYPE_INT32, .data32 = {1, -2, 3}};

    cout << "Data width = " << datawidth(point1) << endl;
    cout << "Data width = " << datawidth(point2) << endl;

    cout << "L1 norm = " << l1norm(point1) << endl;
    cout << "L1 norm = " << l1norm(point2) << endl;

    return 0;
}
```

```cpp
// enum.c

#include <stdio.h>

int main() {
    enum day { Monday = 1, Tuesday, Wednesday }; // 初始化
    enum day today = Tuesday;                    // 变量的使用
    printf("%d\n", Wednesday);
    return 0;
}
```

### 嵌套 enum

```cpp
#include <iostream>

class Mat {
public:
    enum DataType { TYPE8U, TYPE8S, TYPE32F, TYPE64F };

private:
    DataType type;
    void* data;

public:
    Mat(DataType type) : type(type), data(NULL) {}

    DataType getType() const { return type; }
};

int main() {
    Mat image(Mat::DataType::TYPE8U);

    if (image.getType() == Mat::DataType::TYPE8U)
        std::cout << "This is an 8U matrix." << std::endl;
    else
        std::cout << "I am not an 8U matrix." << std::endl;

    return 0;
}
```

## typedef

```cpp
#include <iostream>

using namespace std;

typedef int myint;
typedef unsigned char vec3b[3];
typedef struct _rgb_struct // name _rgb_struct can be omit
{
    unsigned char r;
    unsigned char g;
    unsigned char b;
} rgb_struct;

int main() {
    myint num   = 32;

    // the following two lines are identical
    // unsigned char color[3] = {255, 0, 255};
    vec3b color = {255, 0, 255};
    cout << hex;
    cout << "R=" << +color[0] << ", ";
    cout << "G=" << +color[1] << ", ";
    cout << "B=" << +color[2] << endl;

    rgb_struct rgb = {0, 255, 128};
    cout << "R=" << +rgb.r << ", ";
    cout << "G=" << +rgb.g << ", ";
    cout << "B=" << +rgb.b << endl;

    cout << sizeof(rgb.r) << endl;
    cout << sizeof(+rgb.r) << endl; // why 4?

    return 0;
}
```

## sizeof

```cpp
#include <iostream>

using namespace std;

int main() {
    int i   = 0;
    short s = 0;
    cout << "sizeof(int)=" << sizeof(int) << endl;
    cout << "sizeof(i)=" << sizeof(i) << endl;
    cout << "sizeof(short)=" << sizeof(s) << endl;
    cout << "sizeof(long)=" << sizeof(long) << endl;
    cout << "sizeof(size_t)=" << sizeof(size_t) << endl;
    return 0;
}
```

## sizeof...

`sizeof...` 是 C++11 引入的一种运算符，用于计算模板参数包中的元素数量。

```cpp
#include <iostream>

// 定义模板结构体 count
template <class... Types>
struct count {
    static const std::size_t value = sizeof...(Types);
};

int main() {
    // 使用 count 结构体计算不同类型的数量
    std::cout << "Number of types: " << count<int, double, char>::value << std::endl;

    return 0;
}
```

- `count` 是一个模板结构体，它接受任意数量的类型参数 (`Types...`)。
- 语句使用 `sizeof...` 操作符来计算模板参数包中类型的数量，并将结果保存在 `value` 成员中。

在 `main` 函数中，我们使用了 `count` 结构体来计算不同类型的数量。在这个例子中，我们传递了 `int`、`double` 和 `char` 三个类型，然后输出了它们的数量。
