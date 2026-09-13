# 滑动窗口与双指针

> 双指针分为**相向**（两端向中间）与**同向**（快慢/左右指针）两类；同向双指针维护一个窗口即**滑动窗口**。
> 这是灵茶山艾府题单中的第一大分类，覆盖定长/不定长/双序列等子类，每类都有固定套路。

## 一、相向双指针

两个指针分别从数组两端向中间移动，常用于**有序数组**（两数之和）与**回文/容器**问题。

两数之和 II（有序数组）：

::::{tab-set}
:::{tab-item} C++
:sync: cpp

```cpp
vector<int> twoSum(vector<int>& nums, int target) {
    int l = 0, r = nums.size() - 1;
    while (l < r) {
        int sum = nums[l] + nums[r];
        if (sum == target) return {l + 1, r + 1}; // 下标从 1 开始
        sum < target ? l++ : r--;
    }
    return {};
}
```

:::

:::{tab-item} Java
:sync: java

```java
int[] twoSum(int[] nums, int target) {
    int l = 0, r = nums.length - 1;
    while (l < r) {
        int sum = nums[l] + nums[r];
        if (sum == target) return new int[]{l + 1, r + 1};
        if (sum < target) l++; else r--;
    }
    return new int[]{};
}
```

:::
::::

```{note}
移动哪一侧由"当前和与 target 的关系"决定：和太小只能增大（左指针右移），和太大只能减小（右指针左移）。
**核心是排除法**：每轮排除一侧不可能的解，保证 $O(n)$ 内必能找到。
```

## 二、定长滑动窗口

窗口大小固定为 $k$，右端点每步右移一格。套路固定：**入窗口 → 更新答案 → 出窗口**。

最大值（或按题意统计）模板：

::::{tab-set}
:::{tab-item} C++
:sync: cpp

```cpp
// 求窗口内元素和的模板（窗口大小固定为 k）
long long fixedWindowSum(vector<int>& nums, int k) {
    long long sum = 0, ans = 0;
    for (int r = 0; r < nums.size(); r++) {
        sum += nums[r];          // 1. 入窗口（右端点进入）
        if (r < k - 1) continue; // 窗口未成形
        ans  = max(ans, sum);    // 2. 更新答案
        sum -= nums[r - k + 1];  // 3. 出窗口（左端点移出）
    }
    return ans;
}
```

:::

:::{tab-item} Java
:sync: java

```java
long fixedWindowSum(int[] nums, int k) {
    long sum = 0, ans = 0;
    for (int r = 0; r < nums.length; r++) {
        sum += nums[r];              // 1. 入窗口
        if (r < k - 1) continue;     // 窗口未成形
        ans = Math.max(ans, sum);    // 2. 更新答案
        sum -= nums[r - k + 1];      // 3. 出窗口
    }
    return ans;
}
```

:::
::::

## 三、不定长滑动窗口（求最长）

窗口不固定，**右端点扩张、左端点收缩**，维护窗口内满足约束的最大长度。

无重复字符的最长子串（LC3）：

::::{tab-set}
:::{tab-item} C++
:sync: cpp

```cpp
int lengthOfLongestSubstring(string s) {
    int ans = 0, l = 0;
    unordered_map<char, int> cnt;
    for (int r = 0; r < s.size(); r++) {
        cnt[s[r]]++;            // 入窗口
        while (cnt[s[r]] > 1) { // 不满足约束：收缩左端点
            cnt[s[l++]]--;
        }
        ans = max(ans, r - l + 1); // 更新答案（窗口合法）
    }
    return ans;
}
```

:::

:::{tab-item} Java
:sync: java

```java
int lengthOfLongestSubstring(String s) {
    int ans = 0, l = 0;
    int[] cnt = new int[128];
    for (int r = 0; r < s.length(); r++) {
        cnt[s.charAt(r)]++;                 // 入窗口
        while (cnt[s.charAt(r)] > 1) {      // 不满足约束：收缩左端点
            cnt[s.charAt(l++)]--;
        }
        ans = Math.max(ans, r - l + 1);     // 更新答案
    }
    return ans;
}
```

:::
::::

```{note}
**模板口诀**：`for r 循环：加入 nums[r] → while 不满足约束：移除 nums[l++] → 更新答案`。
窗口始终满足约束，答案在所有窗口长度中取最大。
```

## 四、不定长滑动窗口（求最短）

与求最长相反：窗口满足条件时尝试**收缩**以逼近最短。

长度最小的子数组（LC209）：

::::{tab-set}
:::{tab-item} C++
:sync: cpp

```cpp
int minSubArrayLen(int target, vector<int>& nums) {
    int ans = INT_MAX, l = 0, sum = 0;
    for (int r = 0; r < nums.size(); r++) {
        sum += nums[r];         // 入窗口
        while (sum >= target) { // 满足条件：尝试收缩
            ans  = min(ans, r - l + 1);
            sum -= nums[l++];
        }
    }
    return ans == INT_MAX ? 0 : ans;
}
```

:::

:::{tab-item} Java
:sync: java

```java
int minSubArrayLen(int target, int[] nums) {
    int ans = Integer.MAX_VALUE, l = 0, sum = 0;
    for (int r = 0; r < nums.length; r++) {
        sum += nums[r];                     // 入窗口
        while (sum >= target) {             // 满足条件：尝试收缩
            ans = Math.min(ans, r - l + 1);
            sum -= nums[l++];
        }
    }
    return ans == Integer.MAX_VALUE ? 0 : ans;
}
```

:::
::::

## 五、双序列双指针

两个指针分别遍历两个有序序列（合并、找交集、比较）。

合并两个有序数组（LC88，从后往前避免覆盖）：

```cpp
void merge(vector<int>& nums1, int m, vector<int>& nums2, int n) {
    int i = m - 1, j = n - 1, k = m + n - 1;
    while (j >= 0) {
        if (i >= 0 && nums1[i] > nums2[j])
            nums1[k--] = nums1[i--];
        else
            nums1[k--] = nums2[j--];
    }
}
```

```{note}
进阶技巧：**三指针**（如三数之和：外层枚举 + 内层相向双指针）与**分组循环**（把相同结构的元素分组处理）
是灵神题单中同向双指针的两个扩展方向，遇到"连续相同结构"的题目可优先考虑分组循环。
```
