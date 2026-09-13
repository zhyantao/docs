# 前缀和与差分

> **前缀和**：预处理 $O(n)$，之后每次区间和查询 $O(1)$，以空间换时间。
> **差分数组**：前缀和的逆运算，用于 $O(1)$ 完成区间增量，最后前缀和还原。
> 二者是灵茶山艾府"常用数据结构"题单的第一类，也是子数组问题的两大基础工具。

## 一、一维前缀和

令 `pre[i] = a[0] + a[1] + ... + a[i-1]`（**pre[0] = 0**，长度 n+1，避免越界判断），则区间 `[l, r]` 的和为：

$$
\text{sum}(l, r) = pre[r+1] - pre[l]
$$

::::{tab-set}
:::{tab-item} C++
:sync: cpp

```cpp
vector<int> a = {1, 2, 3, 4};
int n = a.size();
vector<int> pre(n + 1, 0);
for (int i = 0; i < n; i++)
    pre[i + 1] = pre[i] + a[i];

// 区间 [l, r] 的和
auto rangeSum = [&](int l, int r) { return pre[r + 1] - pre[l]; };
```

:::

:::{tab-item} Java
:sync: java

```java
int[] a = {1, 2, 3, 4};
int n = a.length;
int[] pre = new int[n + 1];
for (int i = 0; i < n; i++)
    pre[i + 1] = pre[i] + a[i];

// 区间 [l, r] 的和
int rangeSum(int l, int r) { return pre[r + 1] - pre[l]; }
```

:::
::::

## 二、二维前缀和

子矩阵和用**容斥**（加减重叠区）：

$$
S(x_1,y_1,x_2,y_2) = pre[x_2+1][y_2+1] - pre[x_1][y_2+1] - pre[x_2+1][y_1] + pre[x_1][y_1]
$$

```cpp
// pre[i+1][j+1] = pre[i][j+1] + pre[i+1][j] - pre[i][j] + a[i][j]
vector<vector<int>> pre(m + 1, vector<int>(n + 1, 0));
for (int i = 0; i < m; i++)
    for (int j = 0; j < n; j++)
        pre[i + 1][j + 1] = pre[i][j + 1] + pre[i + 1][j] - pre[i][j] + a[i][j];
```

## 三、差分数组

差分数组 `diff`：`diff[i] = a[i] - a[i-1]`。对区间 `[l, r]` 整体加 `v`，只需：

$$
diff[l] += v, \quad diff[r+1] -= v
$$

最后对 `diff` 求前缀和即还原原数组。用于**多次区间增量 + 一次查询**的场景（如航班预订统计 LC1109）。

::::{tab-set}
:::{tab-item} C++
:sync: cpp

```cpp
// 对长度为 n 的数组做 k 次区间 [l, r] 加 v，最后输出结果数组
vector<int> diff(n + 1, 0);   // 多开一位避免 r+1 越界
for (auto& op : ops) {        // ops: {l, r, v}
    int l = op[0], r = op[1], v = op[2];
    diff[l] += v;
    diff[r + 1] -= v;
}
vector<int> ans(n, 0);
int cur = 0;
for (int i = 0; i < n; i++) {
    cur += diff[i];
    ans[i] = cur;
}
```

:::

:::{tab-item} Java
:sync: java

```java
int[] diff = new int[n + 1];
for (int[] op : ops) {        // ops: {l, r, v}
    diff[op[0]] += op[2];
    diff[op[1] + 1] -= op[2];
}
int[] ans = new int[n];
int cur = 0;
for (int i = 0; i < n; i++) {
    cur += diff[i];
    ans[i] = cur;
}
```

:::
::::

## 四、前缀和 + 哈希表

"和为 k 的子数组个数"（LC560）这类问题，前缀和配合哈希表把**两数之差问题**转为**查找**：

$$ pre[r] - pre[l] = k \iff pre[l] = pre[r] - k $$

遍历时用哈希表记录每个前缀和出现的次数，累计 `cnt[pre[r] - k]` 即可。

::::{tab-set}
:::{tab-item} C++
:sync: cpp

```cpp
int subarraySum(vector<int>& nums, int k) {
    unordered_map<int, int> cnt;  // 前缀和 -> 出现次数
    cnt[0] = 1;                   // 前缀和为 0 出现一次（空前缀）
    int sum = 0, ans = 0;
    for (int x : nums) {
        sum += x;
        ans += cnt[sum - k];      // 之前有多少个前缀和 = sum - k
        cnt[sum]++;
    }
    return ans;
}
```

:::

:::{tab-item} Java
:sync: java

```java
int subarraySum(int[] nums, int k) {
    Map<Integer, Integer> cnt = new HashMap<>();
    cnt.put(0, 1);
    int sum = 0, ans = 0;
    for (int x : nums) {
        sum += x;
        ans += cnt.getOrDefault(sum - k, 0);
        cnt.merge(sum, 1, Integer::sum);
    }
    return ans;
}
```

:::
::::

```{note}
灵神称这类技巧为**"枚举右，维护左"**：对双变量问题，枚举右边的元素，把左边需要的信息用哈希表（或有序集合）维护，
将双变量问题降为单变量问题。两数之和、和可被 k 整除的子数组等均可套用。
```
