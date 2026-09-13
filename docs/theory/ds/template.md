# 刷题模板与工具函数

> C++/Java 刷题通用模板与常用工具函数（类型转换、最值、运算符重载、大数计算、排序辅助）。

## Template

::::{tab-set}
:::{tab-item} C++
:sync: cpp

```cpp
#include <bits/stdc++.h>
using namespace std;

typedef long long ll;
typedef long double ld;

const ll mod7 = 1e9 + 7;
const ll mod9 = 998244353;
const ll INF  = 2 * 1024 * 1024 * 1023;
const char nl = '\n';

int main() {
    cin.tie(nullptr)->sync_with_stdio(false);

    int t;
    cin >> t;

    auto solve = [&]() {
        // TODO
        cout << nl; // 使用 endl 会导致 tie 失效
    };

    while (t--) {
        solve();
    }
    return 0;
}
```

:::

:::{tab-item} Java
:sync: java

```java
// 类名必须为 Main，不含 package xxx 信息
public class Main {
    public static void main(String[] args) {
        Scanner in = new Scanner(System.in);
        // 若有下一个字符 hasNext 返回真
        // 若碰到行尾符号 hasNextLine 返回真
        // 注意 hasNextXXX 与 nextXXX 须同时出现
        while (in.hasNextInt()) { // 检查
            int a = in.nextInt();
            int b = in.nextInt(); // 指针向前移动
            // 四舍五入，保留两位小数
            String.format("%.2f", num);
        }
    }
}
```

:::
::::

## 工具函数

### 类型转换

::::{tab-set}
:::{tab-item} C++
:sync: cpp

| 原始类型 | 目标类型 | 转换方法      |
| -------- | -------- | ------------- |
| `string` | `int`    | `stoi()`      |
| `int`    | `string` | `to_string()` |

:::

:::{tab-item} Java
:sync: java

```java
Integer.parseInt(s) // String -> int
String.valueOf(chs) // int, char[] -> String
'8' - '0'           // char -> int
Double.valueOf(i)   // int -> double
foo.intValue()      // double -> int
list = Arrays.asList(arr) // [] -> ArrayList
```

:::
::::

### 最值

::::{tab-set}
:::{tab-item} C++
:sync: cpp

| 最大值      | 最小值      |
| ----------- | ----------- |
| `LONG_MAX`  | `LONG_MIN`  |
| `INT32_MAX` | `INT32_MIN` |

:::
::::

### 运算符重载

::::{tab-set}
:::{tab-item} C++
:sync: cpp

作为类成员时，重载二元运算符参数为另一个对象，一元运算符不需额外参数。

```cpp
Complex Complex::operator+(const Complex& a) const {
    return Complex(real + a.real, img + a.img);
}
```

作为全局函数时，重载二元运算符需要两个参数，一元运算符需要一个参数。

```cpp
Complex operator+(const Complex& a, int b) {
    return Complex(a.real + b, a.img);
}
```

```cpp
// 类中声明全局函数为友元
friend Complex operator+ <>(...);
```

:::
::::

### 大数计算

::::{tab-set}
:::{tab-item} Java
:sync: java

```java
BigInteger A = BigInteger.valueOf(23);
BigDecimal B = BigDecimal.valueOf(1234.56);
A.add(A);
A.subtract(A);
A.multiply(A);
A.divide(A);
```

:::

::::

### 排序

::::{tab-set}
:::{tab-item} C++
:sync: cpp

```cpp
sort(v1.begin(), v1.end(), greater<int>());
sort(v1.begin(), v1.end(), [](int a, int b) {
    return a > b;
});
reverse(v1.begin(), v1.end());
binary_search(v1.begin(), v1.end(), target);
```

:::

:::{tab-item} Java
:sync: java

```java
Arrays.sort(nums);       // 数组排序
Arrays.binarySearch(nums, 23);
Arrays.stream(nums).max().getAsInt();
Collections.sort(list); // 列表排序
list.sort(Collections.reverseOrder());// 逆序
Collections.reverse(list); // 翻转链表
```

:::
::::
