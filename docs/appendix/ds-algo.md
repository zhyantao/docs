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

## 类型转换

::::{tab-set}
:::{tab-item} C++
:sync: cpp

```cpp
string str = "";
char *ptr = nullptr;
char chs[100] = { 0 };
ptr = const_cast< char * >(str.c_str()); // string -> char*
double d = atof("0.23");                 // string -> double
int i = atoi("1021");                    // string -> int
long l = atol("303992");                 // string -> long
sprintf(chs, "%f", 2.3);                 // double -> char[]
strcpy(chs, ptr);                        // char* -> char[]
string str(chs);                         // char[] -> string
```

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

## 运算符重载

::::{tab-set}
:::{tab-item} C++
:sync: cpp

作为类成员时，重载二元运算符参数为另一个对象，一元运算符不需额外参数。

```cpp
Complex Complex::operator+(const Complex &a) const {
  return Complex(real + a.real, img + a.img);
}
```

作为全局函数时，重载二元运算符需要两个参数，一元运算符需要一个参数。

```cpp
Complex operator+(const Complex &a, int b) {
  return Complex(a.real + b, a.img);
}
```

```cpp
// 类中声明全局函数为友元
friend Complex operator+<>(...);
```

:::

:::{tab-item} Java
:sync: java

```java

```

:::
::::

## 大数计算

::::{tab-set}
:::{tab-item} C++
:sync: cpp

```cpp

```

:::

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

## 数组

虽然 C++ 和 Java 中都有静态数组，但是静态数组不太灵活。我们在刷题时，首要目的是把题解出来，因此，我们统一使用动态数组。同时，也方便我们调用各种库函数。

如果题目给的是静态数组，我们可以首先将其类型转换为动态数组。节省思考时间。

::::{tab-set}
:::{tab-item} C++
:sync: cpp

```cpp
vector< int > arr(sz, val);                      // sz 和 val 可选
vector< vector< int > > dp(m, vector< int >(n)); // m * n 的数组
```

:::

:::{tab-item} Java
:sync: java

```java
ArrayList<Integer> v = new ArrayList<>();
```

:::
::::

## 字符串

::::{tab-set}
:::{tab-item} C++
:sync: cpp

```cpp
string str = "ABCDEFG";
str + 'B';
str.substr(start, len);
```

:::

:::{tab-item} Java
:sync: java

初始化字符串

```java
String str = "hello world";
StringBuilder sb = new StringBuilder(str);
```

类型转换

```java
sb.toString();
```

追加

```java
sb.append(true);
sb.insert(i, "abc");
```

删除

```java
sb.deleteCharAt(i);
sb.delete(i,j);
```

修改

```java
sb.setCharAt(i, 'a');
sb.replace(i, j, "abc");
```

查询

```java
sb.indexOf("abc");
sb.lastIndexOf("abc");
```

判空

```java
s1.isEmpty();
```

截取字符串

```java
str.substring(i);
str.substring(i,j);
```

拼接

```java
str.concat("abc");
```

:::
::::

## 链表

::::{tab-set}
:::{tab-item} C++
:sync: cpp

```cpp

```

:::

:::{tab-item} Java
:sync: java

哨兵节点

```java
TreeNode p = new TreeNode(-1, head);
TreeNode dummy = p; // 保存头结点位置，不移动
return dummy.next;
```

初始化

```java
// 双向链表
LinkedList<Integer> v = new LinkedList<>();
```

遍历

```java
void traverse(ListNode head) {
  // 前序遍历代码
  traverse(head.next);
  // 后序遍历代码
}
```

:::
::::

## 树

::::{tab-set}
:::{tab-item} C++
:sync: cpp

```cpp

```

:::

:::{tab-item} Java
:sync: java

遍历二叉树

```java
void traverse(TreeNode root) {
  if (root == null) return;
  // 前序遍历代码
  traverse(root.left);
  // 中序遍历代码
  traverse(root.right);
  // 后序遍历代码
}
```

遍历 N 叉树

```java
class TreeNode {
  int val;
  TreeNode[] children;
}

void traverse(TreeNode root) {
  for (TreeNode child : children)
    traverse(child);
}
```

求二叉树的深度

```java
// 利用这个例子学习如何使用递归的返回值
int traverse(TreeNode root) {
  // 叶节点相当于 dp 的最后一个状态
  if (root == null)
    return 0; // 实际意义： 0 层
  // 从叶结点到根结点逆向推理 left 和 right
  int left = traverse(root.left);
  int right = traverse(root.right);
  // 下一次递归利用上一次递归 return 的结果
  return left>right ? left+1 : right+1;
}
```

层序遍历

```java
Queue<Integer> queue = new LinkedList<>();
void traverse(TreeNode root) {
  if (root != null)
    queue.offer(root);
  else
    return;

  TreeNode p = queue.poll();
  while (p != null) {
    if (p.left != null)
      queue.offer(p.left);
    if (p.right != null)
      queue.offer(p.right);
    if ( ! queue.isEmpty())
      p = queue.poll();
  }
}
```

前序遍历

```java
void preorder(TreeNode root) {
  Stack<TreeNode> stack = new Stack<>();
  if (root == null)
    return;
  stack.push(root);
  while (!stack.isEmpty()) {
    TreeNode cur = stack.peek();
    stack.pop();
    // ans.add(cur.val);
    if (cur.right != null) // 先右后左
      stack.push(cur.right);
    if (cur.left != null)
      stack.push(cur.left);
  }
}
```

中序遍历

```java
// 需要借助栈和指针来实现
void inorder(TreeNode root) {
  Stack<TreeNode> stack = new Stack<>();
  TreeNode cur = root;
  while (cur != null || !stack.isEmpty()) {
    if (cur != null) { // 遍历左子节点，入栈
      stack.push(cur);
      cur = cur.left;
    }
    else { // 遍历完左子节点，出栈，保存结果
      cur = stack.peek();
      stack.pop();
      // ans.add(cur.val);
      cur = cur.right;
    }
  }
}
```

前序遍历

```java
void preorder(TreeNode root) {
  Stack<TreeNode> stack = new Stack<>();
  if (root == null)
    return;
  stack.push(root);
  while (!stack.isEmpty()) {
    TreeNode cur = stack.peek();
    stack.pop();
    // ans.add(cur.val);
    if (cur.right != null) // 先右后左
      stack.push(cur.right);
    if (cur.left != null)
      stack.push(cur.left);
  }
}
```

后序遍历

```java
// 和前序遍历类似的代码，也需要借助栈来实现
// 遍历顺序不一样，且多了一个 reverse 环节
void postorder(TreeNode root) {
  Stack<TreeNode> stack = new Stack<>();
  TreeNode cur = root;
  if (root == null)
    return;
  stack.push(root);
  while (!stack.isEmpty()) {
    TreeNode cur = stack.peek();
    stack.pop();
    // ans.add(cur.val);
    if (cur.left != null) // 先左后右
      stack.push(cur.left);
    if (cur.right != null)
      stack.push(cur.right);
  }
  reverse(ans);
}
```

:::
::::

### 树状数组

::::{tab-set}
:::{tab-item} C++
:sync: cpp

```cpp

```

:::

:::{tab-item} Java
:sync: java

```java

```

:::
::::

### 线段树

::::{tab-set}
:::{tab-item} C++
:sync: cpp

```cpp

```

:::

:::{tab-item} Java
:sync: java

```java

```

:::
::::

## 栈

::::{tab-set}
:::{tab-item} C++
:sync: cpp

```cpp
stack<string> stk;
```

:::

:::{tab-item} Java
:sync: java

```java

```

:::
::::

## 队列

### 双端队列

::::{tab-set}
:::{tab-item} C++
:sync: cpp

```cpp
queue<string> Q;
```

:::

:::{tab-item} Java
:sync: java

```java
// 双端队列
Deque<String> stack = new ArrayDeque<>();
Deque<String> queue = new LinkedDeque<>();
```

:::
::::

### 单调队列

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

### 优先队列

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

## 哈希函数

### 哈希表

::::{tab-set}
:::{tab-item} C++
:sync: cpp

```cpp
unordered_map<string, int> map;
```

:::

:::{tab-item} Java
:sync: java

初始化

```java
Map<Integer, String> map = new HashMap<>();
```

遍历

```java
Map<String, String> map = new HashMap<>();
for (Map.Entry<String, String> entry : map.entrySet()) {
  int key = entry.getKey();
  int value = entry.getValue();
}
```

:::
::::

### 哈希集合

::::{tab-set}
:::{tab-item} C++
:sync: cpp

```cpp
unordered_set<string> set;
```

:::

:::{tab-item} Java
:sync: java

```java

```

:::
::::

### 有序表

::::{tab-set}
:::{tab-item} C++
:sync: cpp

```cpp

```

:::

:::{tab-item} Java
:sync: java

```java
Map<String> map = new TreeSet<>();
```

:::
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

### 树形 DP

::::{tab-set}
:::{tab-item} C++
:sync: cpp

```cpp

```

:::

:::{tab-item} Java
:sync: java

```java

```

:::
::::

### 状压 DP

::::{tab-set}
:::{tab-item} C++
:sync: cpp

```cpp

```

:::

:::{tab-item} Java
:sync: java

```java

```

:::
::::

## 排序算法

### 排序工具包

::::{tab-set}
:::{tab-item} C++
:sync: cpp

```cpp
sort(v1.begin(), v1.end(), greater<int>());
sort(v1.begin(), v1.end(), [](int a, int b) { return a > b; });
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

### 堆排序

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

### 归并排序

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

### 插入排序

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

### 快速排序

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

### 全排列

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

### 重建大根堆

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

### 希尔排序

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

## 查找算法

### 二分查找

::::{tab-set}
:::{tab-item} Java
:sync: java

```java
// 注意这里有多处使用 return
int binarySearch(int[] arr, int target,
                 int left, int right) {
  if (left <= right) {
    int mid = left + (right - left) / 2;
    if (arr[mid] == target)
      return mid;
    if (arr[mid] > target) // 向左查找
      return binarySearch(arr, target,
                          left, mid - 1);
    if (arr[mid] < target) // 向右查找
      return binarySearch(arr, target,
                          mid + 1, right);
  }
  return -1; // 没找到
}
```

:::
::::

### KMP 算法

::::{tab-set}
:::{tab-item} C++
:sync: cpp

```cpp
// next[] = 构建最长公共前后缀长度数组
void getNext(vector< int > &next, string pat) {
    // 初始化 next 数组的第一个元素为 0
    int j = 0;
    next[0] = 0;

    for (int i = 1; i < pat.size(); i++) {
        // 当前字符不匹配时，回退 j 到 next[j-1] 的位置
        while (j > 0 && pat[i] != pat[j]) {
            j = next[j - 1];
        }
        // 当前字符匹配时，则 j 自增
        if (pat[i] == pat[j]) {
            j++;
        }
        // next[i] 表示当前位置与模式串匹配的起始位置
        next[i] = j;
    }
}

// 返回 pat 匹配 txt 的起始位置，若匹配失败则返回 -1
int kmp(string pat, string txt) {
    int n = txt.size();
    int m = pat.size();
    vector< int > next(m);
    getNext(next, pat);
    int j = 0;
    for (int i = 0; i < n; i++) {
        // 当当前字符不匹配且 j 大于 0 时，调整 j 的位置
        while (j > 0 && txt[i] != pat[j]) {
            j = next[j - 1];
        }
        // 当前字符匹配时，j 自增
        if (txt[i] == pat[j]) {
            j++;
        }
        // 匹配成功，返回匹配的起始位置
        if (j == m) {
            return i - m + 1;
        }
    }
    // 匹配失败，返回 -1
    return -1;
}
```

:::

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
