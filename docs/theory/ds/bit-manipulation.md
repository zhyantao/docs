# 位运算

> 位运算是 $O(1)$ 的底层操作，常数极小。灵茶山艾府将其单列为专题
> （基础/性质/拆位/试填/恒等式/思维），常用于优化枚举、状态压缩（DP 的 mask）与按位统计。

## 一、基础操作

| 运算 | 符号 | 说明                         | 例子                   |
| ---- | ---- | ---------------------------- | ---------------------- |
| 与   | `&`  | 同 1 才 1，可**清位/取交集** | `x & 1` 判断奇偶       |
| 或   | `\|` | 有 1 即 1，可**置位/取并集** | `x \| 1` 把最低位变 1  |
| 异或 | `^`  | 不同为 1，可**翻转/去重**    | `x ^ 1` 翻转最低位     |
| 取反 | `~`  | 按位取反                     | `~x = -x - 1`          |
| 左移 | `<<` | 乘 $2^k$                     | `1 << k` 表示第 k 位   |
| 右移 | `>>` | 整除 $2^k$                   | `x >> k & 1` 取第 k 位 |

**异或恒等式**（灵神"恒等式"专题核心）：

$$
x \oplus x = 0, \quad x \oplus 0 = x, \quad x \oplus y = y \oplus x, \quad (x \oplus y) \oplus z = x \oplus (y \oplus z)
$$

利用 `x^x=0` 可以 $O(n)$ 找出**只出现一次**的元素（其余均出现两次）。

## 二、常用技巧

```cpp
// lowbit：取 x 最低位的 1（树状数组、枚举二进制位的基础）
int lowbit(int x) {
    return x & -x;
}

// 判断第 k 位是否为 1（k 从 0 开始）
bool getBit(int x, int k) {
    return (x >> k) & 1;
}

// 置位 / 清位 / 翻转第 k 位
int setBit(int x, int k) {
    return x | (1 << k);
}
int clearBit(int x, int k) {
    return x & ~(1 << k);
}
int flipBit(int x, int k) {
    return x ^ (1 << k);
}

// 统计二进制中 1 的个数（内置函数更快）
int popcount(int x) {
    return __builtin_popcount(x);
} // Java: Integer.bitCount(x)
```

```{note}
**判断 x 是否为 2 的幂**：`x > 0 && (x & (x - 1)) == 0`。
**判断 x 是否整除 2^k**：`(x & ((1 << k) - 1)) == 0`。
```

## 三、枚举子集 / 状态压缩

用一个整数的二进制位表示集合：第 k 位为 1 表示元素 k 被选中（状压 DP 的基础）。

```cpp
int n = 5;
// 枚举所有子集（0 ~ 2^n-1）
for (int mask = 0; mask < (1 << n); mask++) {
    // 处理子集 mask
}

// 枚举一个集合 mask 的所有非空子集（灵神模板：不断减 lowbit）
for (int sub = mask; sub > 0; sub = (sub - 1) & mask) {
    // 处理子集 sub
}
```

## 四、拆位（按位统计）

对每位独立统计贡献，常用于"数组中所有数两两异或之和"类问题：

```cpp
// 统计数组所有元素在每一位上 1 的个数，再按位计算贡献
long long xorSum(vector<int>& nums) {
    long long ans = 0;
    for (int k = 0; k < 31; k++) {
        long long cnt1 = 0;
        for (int x : nums)
            if ((x >> k) & 1) cnt1++;
        long long cnt0  = nums.size() - cnt1;
        ans            += cnt1 * cnt0 * (1LL << k); // 该位对异或和的贡献
    }
    return ans;
}
```

```{note}
拆位的本质是把"按值计算"拆成"按二进制位独立计算"，配合异或/与/或的性质可把复杂度从 $O(n^2)$ 降到 $O(n \cdot 31)$。
```
