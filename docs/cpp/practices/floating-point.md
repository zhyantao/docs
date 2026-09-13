# 浮点数的精度、无穷大与非数字

## float 精度

```cpp
#include <iomanip>
#include <iostream>

using namespace std;

int main() {
    float f1 = 1.2f;
    float f2 = f1 * 1000000000000000;
    cout << std::fixed << std::setprecision(15) << f1 << endl;
    cout << std::fixed << std::setprecision(1) << f2 << endl;
    return 0;
}
```

## 精度损失

浮点数只有约 7 位（`float`）/ 15 位（`double`）有效十进制数字，大数加小数时，小数部分可能被完全"吞掉"。

```cpp
#include <iostream>

using namespace std;

int main() {
    float f1 = 23400000000;
    float f2 = f1 + 10;

    cout.setf(ios_base::fixed, ios_base::floatfield); // fixed-point
    cout << "f1 = " << f1 << endl;
    cout << "f2 = " << f2 << endl;
    cout << "f1 - f2 = " << f1 - f2 << endl;
    cout << "(f1 - f2 == 0) = " << (f1 - f2 == 0) << endl;
    return 0;
}
```

## 无穷大和非数字

IEEE 754 规定：非零数除以零得到无穷大（inf），零除以零得到非数字（nan），它们都可以被打印出来。

```cpp
#include <iostream>

using namespace std;

int main() {
    float f1 = 2.0f / 0.0f;
    float f2 = 0.0f / 0.0f;
    cout << f1 << endl;
    cout << f2 << endl;
    return 0;
}
```
