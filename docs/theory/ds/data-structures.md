# 基础数据结构

> 数组、字符串、链表、栈、双端队列、单调队列、优先队列、哈希表、哈希集合、有序表的刷题模板。

## 数据结构

### 数组

虽然 C++ 和 Java 中都有静态数组，但是静态数组不太灵活。我们在刷题时，首要目的是把题解出来，因此，我们统一使用动态数组。同时，也方便我们调用各种库函数。

如果题目给的是静态数组，我们可以先将其转换为动态数组，以节省思考时间。

::::{tab-set}
:::{tab-item} C++
:sync: cpp

```cpp
vector<int> arr(sz, val);                  // sz 和 val 可选
vector<vector<int>> dp(m, vector<int>(n)); // m * n 的数组
```

:::

:::{tab-item} Java
:sync: java

```java
ArrayList<Integer> v = new ArrayList<>();
```

:::
::::

### 字符串

::::{tab-set}
:::{tab-item} C++
:sync: cpp

```cpp
string str  = "ABCDEFG";
str        += 'B';      // 末尾追加
str.substr(start, len); // 截取子串
str.find("CD");         // 查找子串，返回下标，找不到返回 string::npos
str.rfind('C');         // 从后往前查找
str.compare(other);     // 比较（<0 / 0 / >0）
stoi(str);
stoll(str);                      // 字符串转数字（数字转字符串用 to_string(n)）
sort(str.begin(), str.end());    // 字符串排序
reverse(str.begin(), str.end()); // 反转
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

### 链表

::::{tab-set}
:::{tab-item} Java
:sync: java

哨兵节点

哨兵节点（dummy）：在头节点前加一个虚拟节点，避免单独处理头节点，使头节点的插入/删除与普通节点一致

```java
ListNode dummy = new ListNode(-1, head); // 哨兵节点，指向原头节点
ListNode cur = dummy;                    // cur 负责向后移动，dummy 不动
// ... 操作链表的 cur.next ...
return dummy.next;                       // 返回真正的头节点
```

初始化

```java
// 双向链表
LinkedList<Integer> v = new LinkedList<>();
```

遍历

```java
for (ListNode cur = head; cur != null; cur = cur.next) {
    // 访问 cur.val
}
```

:::
::::

### 栈

后进先出（LIFO），用于括号匹配、函数调用栈、单调栈、撤销操作等。

::::{tab-set}
:::{tab-item} C++
:sync: cpp

```cpp
stack<int> stk;
stk.push(1); // 入栈
stk.pop();   // 出栈（不返回值）
stk.top();   // 查看栈顶
stk.empty();
stk.size();
```

:::

:::{tab-item} Java
:sync: java

```java
// Java 官方推荐用 Deque 实现栈（Stack 类已不推荐）
Deque<Integer> stk = new ArrayDeque<>();
stk.push(1);      // 入栈
stk.pop();        // 出栈
stk.peek();       // 查看栈顶
stk.isEmpty();
stk.size();
```

:::
::::

### 双端队列

双端队列（deque）支持在**两端**插入与删除，操作均为 $O(1)$。用于需要从两头维护数据的场景（滑动窗口、单调队列、回文匹配等）。

::::{tab-set}
:::{tab-item} C++
:sync: cpp

```cpp
deque<int> dq;
dq.push_back(1);  // 尾部入队
dq.push_front(2); // 头部入队
dq.pop_back();    // 尾部出队
dq.pop_front();   // 头部出队
dq.front();       // 查看队首
dq.back();        // 查看队尾
dq.empty();
dq.size();
```

:::

:::{tab-item} Java
:sync: java

```java
// Deque 接口，LinkedList 和 ArrayDeque 均可实现
Deque<Integer> dq = new ArrayDeque<>();
dq.addLast(1);      // 尾部入队
dq.addFirst(2);     // 头部入队
dq.removeLast();    // 尾部出队
dq.removeFirst();   // 头部出队
dq.getFirst();      // 查看队首
dq.getLast();       // 查看队尾
dq.isEmpty();
dq.size();
```

:::
::::

### 单调队列

**原理**：单调队列 = 滑动窗口 + 单调栈。维护队列内元素的单调性（求窗口最大值时维护**从大到小**，队首即当前窗口最大值），入队时弹出队尾所有"不如当前元素"的元素。每个元素最多入队、出队各一次，整体复杂度 $O(n)$。

```{note}
队列中存**下标**而非值：一是方便判断队首是否已滑出窗口（下标 < 左边界即弹出）；二是取值时通过下标访问原数组。
```

滑动窗口最大值模板（模板题 LC239）：

::::{tab-set}
:::{tab-item} C++
:sync: cpp

```cpp
vector<int> maxSlidingWindow(vector<int>& nums, int k) {
    vector<int> ans;
    deque<int> dq; // 存下标，维护从大到小
    for (int i = 0; i < nums.size(); i++) {
        // 队尾元素 ≤ 当前值时，它不可能再成为窗口最大值，弹出
        while (!dq.empty() && nums[dq.back()] <= nums[i])
            dq.pop_back();
        dq.push_back(i);
        if (dq.front() <= i - k) // 队首滑出窗口左边界
            dq.pop_front();
        if (i + 1 >= k) // 窗口已形成
            ans.push_back(nums[dq.front()]);
    }
    return ans;
}
```

:::

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
        deque.addLast(r); // 存储元素下标
        int l = r - sz + 1; // 窗口左边界
        if (deque.peekFirst() < l)// 超出左边界
            deque.removeFirst();
        if (r + 1 >= sz) // 若已经形成窗口
            ans[l] = arr[deque.peekFirst()];
    }
    return ans;
}
```

:::
::::

```{note}
求窗口最小值时只需把弹出条件改成 `>=`（维护从大到小改为从小到大），其余逻辑不变。
```

### 单调栈

**原理**：维护栈内元素单调（递增或递减）。常用于求**每个元素左右两侧最近的更大/更小元素**，进而解决接雨水、柱状图最大矩形、贡献法计数等问题。每个元素最多入栈、出栈各一次，整体复杂度 $O(n)$。

**技巧**：在栈底预先压入一个边界下标（如 `-1` 或 `n`）作为**哨兵**，保证循环中栈永不为空，简化边界判断。

**应用 1：左右两侧最近更小元素**（以 $a[i]$ 为最小值的区间范围）：

::::{tab-set}
:::{tab-item} C++
:sync: cpp

```cpp
// left[i]  = 左侧第一个 < a[i] 的下标，不存在为 -1
// right[i] = 右侧第一个 < a[i] 的下标，不存在为 n
vector<int> a(n);
vector<int> left(n), right(n);

// 从左到右求 left：维护严格递增栈，弹出 >= 当前值的下标
stack<int> st;
st.push(-1); // 哨兵
for (int i = 0; i < n; i++) {
    while (st.top() != -1 && a[st.top()] >= a[i])
        st.pop();
    left[i] = st.top();
    st.push(i);
}

// 从右到左求 right：同理
stack<int> st2;
st2.push(n); // 哨兵
for (int i = n - 1; i >= 0; i--) {
    while (st2.top() != n && a[st2.top()] >= a[i])
        st2.pop();
    right[i] = st2.top();
    st2.push(i);
}
// 此时 a[i] 是区间 [left[i]+1, right[i]-1] 内的最小值，
// 以 a[i] 为最小值的子数组个数 = (i-left[i]) * (right[i]-i)
```

:::

:::{tab-item} Java
:sync: java

```java
// 单调栈（存下标），思路同 C++ 版
int n = a.length;
int[] left = new int[n], right = new int[n];
Deque<Integer> st = new ArrayDeque<>();
st.push(-1); // 哨兵
for (int i = 0; i < n; i++) {
    while (st.peek() != -1 && a[st.peek()] >= a[i])
        st.pop();
    left[i] = st.peek();
    st.push(i);
}
```

:::
::::

**应用 2：下一个更大元素**（LC496 模板）：

::::{tab-set}
:::{tab-item} C++
:sync: cpp

```cpp
// 从右往左维护递减栈：栈中保留"右边比当前元素大的候选"
vector<int> nextGreater(vector<int>& nums) {
    int n = nums.size();
    vector<int> ans(n, -1);
    stack<int> st;
    for (int i = n - 1; i >= 0; i--) {
        // 弹出所有 <= 当前值的（它们不可能成为更左边元素的下一个更大元素）
        while (!st.empty() && st.top() <= nums[i])
            st.pop();
        ans[i] = st.empty() ? -1 : st.top();
        st.push(nums[i]);
    }
    return ans;
}
```

:::

:::{tab-item} Java
:sync: java

```java
int[] nextGreater(int[] nums) {
    int n = nums.length;
    int[] ans = new int[n];
    Arrays.fill(ans, -1);
    Deque<Integer> st = new ArrayDeque<>();
    for (int i = n - 1; i >= 0; i--) {
        while (!st.isEmpty() && st.peek() <= nums[i])
            st.pop();
        ans[i] = st.isEmpty() ? -1 : st.peek();
        st.push(nums[i]);
    }
    return ans;
}
```

:::
::::

```{note}
- 求"左侧/更小"时把比较符号反过来即可；
- 若要处理相等元素，把弹出条件中的 `>=` 改为 `>`（或反之），可控制左右两侧的严格/非严格边界，避免重复计数。
```

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
priority_queue<int> PQ;
```

优先队列默认是降序排列的，也就是最大值在堆顶。如果想创建一个小根堆，声明方式如下：

```cpp
priority_queue<int, vector<int>, greater<>> PQ;
```

在很多情况下，我们会想**在优先队列中存储自定义的数据类型，并按照某个属性排列**。这种情况下，我们需要重载运算符来达到要求：

```cpp
// 假设：我们想将 hashMap 中的 {key, value} 对存储到 priority queue 中
unordered_map<int, int> hashMap;
for (int num : nums) {
    hashMap[num]++;
}

// 创建一个根据哈希表的值升序排列的小根堆，并且只保存 k 个元素
struct HashEntry {
    int key;
    int value;

    // 重载 > 运算符
    bool operator>(const HashEntry& other) const { return value > other.value; }
};

priority_queue<HashEntry, vector<HashEntry>, greater<HashEntry>> minHeap;

for (const auto& entry : hashMap) {
    minHeap.push({entry.first, entry.second});
    if (minHeap.size() > k) {
        minHeap.pop();
    }
}

// 取出小根堆中的元素
vector<int> ans;
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
        });
```

:::
::::

### 哈希表

::::{tab-set}
:::{tab-item} C++
:sync: cpp

初始化

```cpp
unordered_map<string, int> map;
```

插入

```cpp
map["hello"] = 1; // 最简单，常用
map.insert({"hello", 1});
map.emplace("hello", 1);
map.insert(std::make_pair("hello", 1));
```

修改值

```cpp
map["hello"] = 2;
```

查找

```cpp
if (map.find("hello") != map.end()) {
    cout << "Key exists." << endl;
}

if (map.count("hello")) {
    cout << "Key exists." << endl;
}

int val          = map.at("hello"); // 抛出异常如果键不存在
int valOrDefault = map["hello"];    // 如果键不存在，将插入默认值 0 并返回 0
```

删除一个键

```cpp
map.erase("hello");
```

清空哈希表

```cpp
map.clear();
```

获取哈希表的大小

```cpp
size_t size = map.size();
```

遍历

```cpp
for (const auto& entry : map) {
    const string& key = entry.first;
    int value         = entry.second;
}
```

:::

:::{tab-item} Java
:sync: java

初始化

```java
Map<Integer, String> map = new HashMap<>();
```

常用操作

```java
map.put(1, "a");            // 插入 / 覆盖
map.get(1);                 // 取值，键不存在返回 null
map.getOrDefault(1, "默认"); // 键不存在时返回默认值
map.containsKey(1);         // 判断键是否存在
map.remove(1);              // 删除键
map.size();
map.isEmpty();
```

遍历

```java
Map<String, String> map = new HashMap<>();
for (Map.Entry<String, String> entry : map.entrySet()) {
    String key = entry.getKey();
    String value = entry.getValue();
}
```

:::
::::

### 哈希集合

::::{tab-set}
:::{tab-item} C++
:sync: cpp

初始化

```cpp
unordered_set<string> set;
```

插入

```cpp
set.insert("hello");
```

删除一个键

```cpp
set.erase("hello");
```

查找

```cpp
if (set.find("hello") != set.end()) {
    cout << "Key exists." << endl;
}

// 或者使用 count 方法
if (set.count("hello")) {
    cout << "Key exists." << endl;
}
```

清空哈希集合

```cpp
set.clear();
```

获取哈希集合的大小

```cpp
size_t size = set.size();
```

遍历

```cpp
for (const auto& element : set) {
    cout << element << endl;
}
```

:::

:::{tab-item} Java
:sync: java

初始化

```java
Set<String> set = new HashSet<>();
```

常用操作

```java
set.add("hello");       // 插入，已存在则忽略
set.remove("hello");    // 删除
set.contains("hello");  // 查找
set.size();
set.isEmpty();
```

遍历

```java
for (String element : set) {
    System.out.println(element);
}
```

:::
::::

### 有序表

有序集合/映射基于平衡树（红黑树）实现，按键有序，支持 $O(\log n)$ 的插入、删除、查找，以及"找前驱/后继、第 k 小"等有序操作。用于需要动态维护有序数据的场景（TopK、区间统计）。

::::{tab-set}
:::{tab-item} Java
:sync: java

```java
// 有序集合（元素不重复，自动升序）
TreeSet<Integer> ts = new TreeSet<>();
ts.add(3);
ts.add(1);
ts.first();            // 最小值（1）
ts.last();             // 最大值（3）
ts.ceiling(2);         // >= 2 的最小元素（3）
ts.floor(2);           // <= 2 的最大元素（1）
ts.contains(1);
ts.remove(1);
```

```java
// 有序映射（按键升序）
TreeMap<String, Integer> tm = new TreeMap<>();
tm.put("b", 2);
tm.put("a", 1);
tm.firstKey();         // 最小的键（"a"）
tm.lastKey();          // 最大的键（"b"）
tm.ceilingKey("ab");   // >= "ab" 的最小键（"b"）
```

:::
::::

```{note}
C++ 对应为 `set` / `map`（有序），与 `unordered_set` / `unordered_map`（哈希、无序）区别开：
前者按键有序、支持有序操作但为 $O(\log n)$；后者 $O(1)$ 均摊但无序。
```
