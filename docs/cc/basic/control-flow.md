# 流程控制

## if

```cpp
#include <iostream>

using namespace std;

int main() {
    int num = 10;
    if (num < 5) cout << "The number is less than 5. " << endl;

    if (num == 5) {
        cout << "The number is 5." << endl;
    } else {
        cout << "The number is not 5." << endl;
    }

    if (num < 5)
        cout << "The number is less than 5." << endl;
    else if (num > 10)
        cout << "The number is greater than 10." << endl;
    else
        cout << "The number is in range [5, 10]." << endl;

    if (num < 20)
        if (num < 5)
            cout << "The number is less than 5" << endl;
        else
            cout << "Where I'm?" << endl;

    return 0;
}
```

```{note}
不要用 `if (p)` 来判断 `new` 是否成功：`new` 分配失败时会抛出 `std::bad_alloc` 异常，
并不会返回空指针，因此下面的判断是死代码。只有在使用 `new(std::nothrow)` 时才会返回空指针。

```cpp
int* p = new int[1024];   // 失败时抛出异常
// if (p) ...              // 该判断永远不会为假

int* q = new (std::nothrow) int[1024];
if (q == nullptr) { /* 处理分配失败 */ }
```
```

## for

```cpp
#include <iostream>

using namespace std;

int main() {
    int sum = 0;
    for (int i = 0; i < 10; i++) {
        sum += i;
        cout << "Line " << i << endl;
    }
    cout << "sum = " << sum << endl;

    return 0;
}
```

## while / do-while / break

```cpp
#include <iostream>

using namespace std;

int main() {
    int num = 10;
    while (num > 0) {
        cout << "num = " << num << endl;
        num--;
    }

    // num = 10;
    // do
    // {
    //     cout << "num = " << num << endl;
    //     num--;
    // } while (num > 0);

    // num = 10;
    // while (num > 0)
    // {
    //     if (num == 5)
    //         break;
    //     cout << "num = " << num << endl;
    //     num--;
    // }
    return 0;
}
```

## switch

```cpp
#include <iostream>

using namespace std;

int main() {
    unsigned char input_char = 0;

    cout << "Please input a character to start." << endl;
    cin >> input_char;
    while (input_char != 'q') {
        switch (input_char) {
        case 'a':
        case 'A': cout << "Move left. Input 'q' to quit." << endl; break;
        case 'd':
        case 'D': cout << "Move right. Input 'q' to quit." << endl; break;
        default: cout << "Undefined key. Input 'q' to quit." << endl; break;
        }
        cin >> input_char;
    }
}
```

## goto

`goto` 只能在函数内部跳转，常被用于统一错误处理出口，避免重复的清理代码。

```cpp
#include <iostream>

using namespace std;

float mysquare(float value) {
    float result = 0.0f;

    if (value >= 1.0f || value <= 0) {
        cerr << "The input is out of range." << endl;
        goto EXIT_ERROR;
    }
    result = value * value;
    return result;

EXIT_ERROR:
    // do sth such as closing files here
    return 0.0f;
}

int main() {
    float value;
    cout << "Input a floating-point number." << endl;
    cin >> value;

    float result = mysquare(value);

    if (result > 0) cout << "The square is " << result << "." << endl;

    return 0;
}
```

## 三目运算符 `? :`

```cpp
#include <iostream>

using namespace std;

int main() {
    bool isPositive = true;
    int factor      = 0;
    // some operations may change isPositive's value
    if (isPositive)
        factor = 1;
    else
        factor = -1;
    // the if-else statement can be replaced by a ternary conditional operation
    factor = isPositive ? 1 : -1;

    // sometimes the following code can be more efficient.
    factor = isPositive * 2 - 1;

    return 0;
}
```
