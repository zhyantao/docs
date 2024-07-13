# 常用算法模板

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
const ll INF = 2 * 1024 * 1024 * 1023;
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
::::

## Priority Queue

::::{tab-set}
:::{tab-item} C++
:sync: cpp

优先队列支持以下几种操作：

- `push` 向优先队列中插入一个元素。
- `pop` 删除并返回优先队列中优先级最高的元素。
- `top` 查看优先队列中优先级最高的元素。
- `empty` 判断优先队列是否为空。
- `size` 返回优先队列中的元素数量。

优先队列的声明方式：

```cpp
priority_queue< int > PQ;
```

优先队列默认是降序排列的，也就是最大值在堆顶。如果想创建一个小根堆，声明方式如下：

```cpp
priority_queue< int, vector< int >, greater< int > > PQ;
```

在很多情况下，我们会想**在优先队列中存储自定义的数据类型，并按照某个属性排列**。这种情况下，我们需要重载运算符来达到要求：

```cpp
// 假设：我们想将 hashMap 中的 {key, value} 对存储到 priority queue 中
unordered_map< int, int > hashMap;
for (int num : nums) {
    hashMap[num]++;
}

// 创建一个根据哈希表的值升序排列的小根堆，并且只保存 k 个元素
struct HashEntry {
    int key;
    int value;

    // 重载 > 运算符
    bool operator>(const HashEntry &other) const {
        return value > other.value;
    }
};

priority_queue< HashEntry, vector< HashEntry >, greater< HashEntry > > minHeap;

for (const auto &entry : hashMap) {
    minHeap.push({ entry.first, entry.second });
    if (minHeap.size() > k) {
        minHeap.pop();
    }
}

// 取出小根堆中的元素
vector< int > ans;
while (!minHeap.empty()) {
    ans.push_back(minHeap.top().key);
    minHeap.pop();
}
```
:::
:::{tab-item} Java
:sync: java

```java
// 默认的初始化方法
PriorityQueue<Integer> pq = new PriorityQueue<>();

// 自定义排序规则
PriorityQueue<Integer> pq = new PriorityQueue<>(
  new Comparator<Integer>() {
    @Override
    public int compare(Integer o1, Integer o2) {
        return o1 - o2; // (升序) 谁小谁优先
    }
  }
);
```
:::
::::

## 堆排序

::::{tab-set}
:::{tab-item} Java
:sync: java

`PriorityQueue` 就是一个小根堆结构，可以直接使用。

```java
heapSort(int[] arr) {
  if (arr == null || arr.length < 2)
    return;
  // 构建大根堆（方法一）
  //for (int i = 0; i < arr.length; i++)
  //  heapInsert(arr, i);
  // 构建大根堆（方法二，更快）
  for (int i = arr.length - 1; i >= 0; i--)
    heapify(arr, i, arr.length);
  // 每次选择并移除堆顶元素，放到末尾
  int heapSize = arr.length;
  swap(arr, 0, --heapSize);
  while (heapSize > 0) {
    heapify(arr, 0, heapSize);
    swap(arr, 0, --heapSize);
  }
}
```
:::
::::

## 归并排序

::::{tab-set}
:::{tab-item} Java
:sync: java

```java
mergeSort(int[] arr, int[] tmp,
          int left, int right) {
  if (left < right) {
    int mid = left + (right - left) / 2;
    mergeSort(arr, tmp, left, mid);
    mergeSort(arr, tmp, mid+1, right);
    merge(arr, tmp, left, mid, right);
  }
}
merge(int[] arr, int[] tmp,
      int left, int mid, int right) {
  int pLeft = left
  int pRight = mid + 1;
  int pTmp = left;
  // 将左右子数组较小的元素依次插入到 tmp 中
  while (pLeft <= mid && pRight <= right) {
    if (arr[pLeft] <= arr[pRight])
      tmp[pTmp++] = arr[pLeft++];
    else
      tmp[pTmp++] = arr[pRight++];
  }
  // 复制剩余元素到 tmp 中
  while (pLeft <= mid)
    tmp[pTmp++] = arr[pLeft++];
  while (pRight <= right)
    tmp[pTmp++] = arr[pRight++];
  // 必须保存局部的排序结果，否则下次还是乱序
  for (int i = left; i <= right; i++)
    arr[i] = tmp[i];
}
// 调用：int[] arr = new int[]{7, 3, 2, 6};
int[] tmp = new int[arr.length]; // 辅助空间
mergeSort(arr, tmp, 0, arr.length - 1);
```
::::



## 插入排序

::::{tab-set}
:::{tab-item} Java
:sync: java

```java
void insertSort(int[] arr) {
  int j; // 用于扫描 i 之前的元素
  for (int i = 1; i < arr.length; i++) {
    int tmp = arr[i];
    for (j = i; j > 0 && arr[j-1] > tmp; j--)
      arr[j] = arr[j-1]; // 向后移动元素
    arr[j] = tmp;
  }
}
```
::::

## 快速排序

::::{tab-set}
:::{tab-item} Java
:sync: java

```java
quickSort(int[] arr, int left, int right) {
  if (left < right) {
    int pivot = arr[left];   // 随机选基准点
    int i = left, j = right; // 不修改原变量
    while (i < j) {
      while (i < j && arr[j] > pivot)
        j--; // 从右往左：首个比 pivot 小的值
      if (i < j) {
        arr[i] = arr[j]; // 丢失 arr[i]
        i++;
      }
      while (i < j && arr[i] < pivot)
        i++; // 从左往右：首个比 pivot 大的值
      if (i < j) {
        arr[j] = arr[i];
        j--;
      }
    }
    arr[i] = pivot; // 找回 arr[i]
    // -- partition 和递归代码的分割线 -- //
    quickSort(arr, left, i - 1);
    quickSort(arr, i + 1, right);
  }
}
// 调用：quickSort(arr, 0, arr.length - 1);
```
::::

## 单调队列

::::{tab-set}
:::{tab-item} Java
:sync: java

```java
// 单调队列，要始终维持队列递增或递减的状态。
// 递增（减）队列的队头是最小（大）值。
int[] maxSlidingWindow(int[] arr, int sz) {
    int[] ans = new int[arr.length - sz + 1];
    Deque<Integer> deque = new LinkedList<>();
    // r 表示滑动窗口右边界
    for (int r = 0; r < arr.length; r++) {
      // 移除队尾比当前值小的元素的索引
      while (!deque.isEmpty()
          && arr[r] >= arr[deque.peekLast()])
        deque.removeLast();
      deque.addLast(r);      // 存储元素下标
      int l = r - sz + 1;    // 窗口左边界
      if (deque.peekFirst() < l)//超出左边界
        deque.removeFirst();
      if (r + 1 >= sz) // 若已经形成窗口
        ans[l] = arr[deque.peekFirst()];
    }
    return ans;
}
```
::::

## 动态规划

::::{tab-set}
:::{tab-item} Java
:sync: java

```java
// 1. 暴力递归求斐波那契数列：0 1 1 2 3 ...
int fib(int n) { // 求最后状态 dp[n] 的值
  if (n <= 1)
    return n;
  return fib(n - 1) + fib(n - 2);
}
// 2. 将递归转为动态规划（消除重复计算）
int fib(int n) {
  int[] dp = new int[3];
  dp[0] = 0; dp[1] = 1; // 初始记忆
  dp[2] = dp[0] + dp[1]; // dp[2] 是最新记忆
  for (int i = 2; i <= n; i++) {
    dp[0] = dp[1]; dp[1] = dp[2];// 更新记忆
    dp[2] = dp[0] + dp[1]; // 依赖前两个记忆
  }
  return dp[2];
}
```
::::

## 全排列

::::{tab-set}
:::{tab-item} Java
:sync: java

```java
// 比如：模拟从黑箱子中取球的过程（有放回）
// 回溯不同于动态规划，动态规划有公式可循
// 用 arr 表示原始数组，用 used 剪枝优化
// 用 i == arr.length 判断递归是否终止
List<List<Integer>> ans = new ArrayList<>();
List<Integer> path = new ArrayList<>();
void dfs(int[] arr, boolean[] used, int i) {
  if (i == arr.length) {
    // 注意，深拷贝
    ans.add(new ArrayList<>(path));
    return;
  }
  // 每次都向 path 的第 j 个位置推送不同数字
  for (int j = 0; j < nums.length; j++) {
    if (!used[j]) {
      path.add(nums[j]);
      used[j] = true;
      dfs(nums, used, i + 1);
      used[j] = false; // 撤销原操作
      path.remove(path.size() - 1);
    }
  }
}
```
::::

## 岛问题

::::{tab-set}
:::{tab-item} Java
:sync: java

```java
// "感染" 每个可连通的单元，由 1 变成 2
void infect(int[][] arr, int i, int j,
                         int N, int M) {
  if (i < 0 || i >= N || j < 0 || j >= M
            || arr[i][j] != 1)
    return;
  arr[i][j] = 2; // 感染
  infect(arr, i+1, j, N, M);
  infect(arr, i-1, j, N, M);
  infect(arr, i, j+1, N, M);
  infect(arr, i, j-1, N, M);
}
int count(int[][] arr) {
  if (arr == null || arr[0] == null)
    return 0;
  int N = arr.length;
  int M = arr[0].length;
  int ans = 0;
  for (int i = 0; i < N; i++)
    for (int j = 0; j < M; j++)
      if (arr[i][j] == 1) {
        ans++;
        infect(arr, i, j, N, M);
      }
}
```
::::

## 重建大根堆

::::{tab-set}
:::{tab-item} Java
:sync: java

```java
// 向已有堆的末尾插入元素，重建大根堆
void heapInsert(int[] arr, int i) {
  while (arr[i] > arr[(i - 1) / 2]) {
    swap(arr, i, (i - 1) / 2);
    i = (i - 1) / 2;
  }
}
// 移除堆顶元素(放在末尾)，重建大根堆
heapify(int[] arr, int i, int heapSize) {
  while (i < heapSize) {
    int l = 2 * i + 1; // 左孩子指针
    int r = 2 * i + 2; // 右孩子指针
    int max = i;
    if (l < heapSize && arr[l] > arr[max])
      max = l;
    if (r < heapSize && arr[r] > arr[max])
      max = r;
    if (max == i)
      break;
    swap(arr, i, max);
    i = max;
  }
}
```
::::

## KMP 算法

::::{tab-set}
:::{tab-item} Java
:sync: java

```java
// next 数组记录最长相等的前后缀长度
void getNext(int[] next, String pat) {
  next[0] = 0;
  int j = 0; // 失配后的回退点
  // 循环从 1 开始，不是 0
  for (int i = 1; i < pat.length(); i++) {
    char chi = pat.charAt(i);
    char chj = pat.charAt(j);
    while (j > 0 && chi != chj)
      j = next[j - 1]; // 回退
    if (chi == chj)
      j++;
    next[i] = j;
  }
}
int strStr(String txt, String pat) {
  if (pat.length() == 0)
    return 0;
  int[] next = new int[pat.length()];
  getNext(next, pat);
  int j = 0;
  for (int i = 0; i < txt.length(); i++) {
    chi = txt.charAt(i);
    chj = pat.charAt(j);
    while (j > 0 && chi != chj)
      j = next[j - 1];
    if (chi == chj)
      j++;
    if (j == pat.length())
      return i - pat.length() + 1;
  }
  return -1;
}
```
::::

## 希尔排序

::::{tab-set}
:::{tab-item} Java
:sync: java

```java
void shellSort(int[] arr) {
  for (int step = arr.length / 2;
           step >= 1; step /= 2) {
    for (int r = step; r < len; r++) {
      int tmp = arr[r]; // 把 r 放到最终位置
      int l = r - step;
      while (l >= 0 && arr[l] > tmp) {
        arr[l + step] = arr[l]; // 将 l 右移
        l -= step;
      }
      arr[l + step] = tmp; // 放置
    }
  }
}
```
::::
