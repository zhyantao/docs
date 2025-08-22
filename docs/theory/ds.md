# 数据结构与算法

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

    while (t--) { solve(); }
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
Complex operator+(const Complex& a, int b) { return Complex(a.real + b, a.img); }
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

## 数据结构

### 数组

虽然 C++ 和 Java 中都有静态数组，但是静态数组不太灵活。我们在刷题时，首要目的是把题解出来，因此，我们统一使用动态数组。同时，也方便我们调用各种库函数。

如果题目给的是静态数组，我们可以首先将其类型转换为动态数组。节省思考时间。

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

### 链表

::::{tab-set}
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

### 栈

::::{tab-set}
:::{tab-item} C++
:sync: cpp

```cpp
stack<string> stk;
```

:::
::::

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
priority_queue<int> PQ;
```

优先队列默认是降序排列的，也就是最大值在堆顶。如果想创建一个小根堆，声明方式如下：

```cpp
priority_queue<int, vector<int>, greater<int>> PQ;
```

在很多情况下，我们会想**在优先队列中存储自定义的数据类型，并按照某个属性排列**。这种情况下，我们需要重载运算符来达到要求：

```cpp
// 假设：我们想将 hashMap 中的 {key, value} 对存储到 priority queue 中
unordered_map<int, int> hashMap;
for (int num : nums) { hashMap[num]++; }

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
    if (minHeap.size() > k) { minHeap.pop(); }
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
if (map.find("hello") != map.end()) { cout << "Key exists." << endl; }

if (map.count("hello")) { cout << "Key exists." << endl; }

int val = map.at("hello");       // 抛出异常如果键不存在
int valOrDefault = map["hello"]; // 如果键不存在，将插入默认值 0 并返回 0
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
    int value = entry.second;
}
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
if (set.find("hello") != set.end()) { cout << "Key exists." << endl; }

// 或者使用 count 方法
if (set.count("hello")) { cout << "Key exists." << endl; }
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
for (const auto& element : set) { cout << element << endl; }
```

:::
::::

### 有序表

::::{tab-set}
:::{tab-item} Java
:sync: java

```java
Map<String> map = new TreeSet<>();
```

:::
::::

## 树

### 二叉树的递归遍历

::::{tab-set}
:::{tab-item} C++
:sync: cpp

```cpp
vector<int> ans;
vector<int> traverse(TreeNode* root) {
    if (root == nullptr) { return; }

    // ans.push_back(root->val); // 前序遍历
    traverse(root->left);
    ans.push_back(root->val); // 中序遍历
    traverse(root->right);
    // ans.push_back(root->val); // 后序遍历

    return ans;
}
```

:::

:::{tab-item} Java
:sync: java

```java
void traverse(TreeNode root) {
    if (root == null)
        return;

    // TODO: 前序遍历代码
    traverse(root.left);
    // TODO: 中序遍历代码
    traverse(root.right);
    // TODO: 后序遍历代码

    return;
}
```

:::
::::

### 二叉树的前序遍历

::::{tab-set}
:::{tab-item} C++

```cpp
vector<int> preorderTraversal(TreeNode* root) {
    if (root == nullptr) { return {}; }

    vector<int> ans;
    stack<TreeNode*> stk;
    TreeNode* curr = root;
    stk.push(root);
    while (!stk.empty()) {
        curr = stk.top();
        stk.pop();

        ans.push_back(curr->val);

        if (curr->right != nullptr) { // 先右后左
            stk.push(curr->right);
        }
        if (curr->left != nullptr) { stk.push(curr->left); }
    }

    return ans;
}
```

:::

:::{tab-item} Java

```java
void preorder(TreeNode root) {
    if (root == null)
        return;

    Stack<TreeNode> stack = new Stack<>();
    stack.push(root);
    while (!stack.isEmpty()) {
        TreeNode cur = stack.peek();
        stack.pop();

        // ans.add(cur.val);

        if (cur.right != null) { // 先右后左
            stack.push(cur.right);
        }
        if (cur.left != null) {
            stack.push(cur.left);
        }
    }
}
```

:::
::::

### 二叉树的中序遍历

::::{tab-set}
:::{tab-item} C++

```cpp
vector<int> inorderTraversal(TreeNode* root) {
    if (root == nullptr) { return {}; }

    vector<int> ans;
    stack<TreeNode*> stk;
    TreeNode* curr = root;
    while (curr != nullptr || !stk.empty()) {
        if (curr != nullptr) {
            stk.push(curr);
            curr = curr->left;
        } else {
            curr = stk.top();
            stk.pop();

            ans.push_back(curr->val);

            curr = curr->right;
        }
    }

    return ans;
}
```

:::

:::{tab-item} Java

```java
void inorder(TreeNode root) {
    Stack<TreeNode> stack = new Stack<>();
    TreeNode cur = root;
    while (cur != null || !stack.isEmpty()) {
        if (cur != null) {
            stack.push(cur);
            cur = cur.left;
        } else {
            cur = stack.peek();
            stack.pop();

            // ans.add(cur.val);

            cur = cur.right;
        }
    }
}
```

:::
::::

### 二叉树的后序遍历

::::{tab-set}
:::{tab-item} C++

```cpp
// 后序遍历代码和前序遍历代码几乎一样，有 2 点区别
vector<int> postorderTraversal(TreeNode* root) {
    if (root == nullptr) { return {}; }

    vector<int> ans;
    stack<TreeNode*> stk;
    TreeNode* curr = root;
    stk.push(root);
    while (!stk.empty()) {
        curr = stk.top();
        stk.pop();

        ans.push_back(curr->val);

        if (curr->left != nullptr) { // 区别 1：先左后右
            stk.push(curr->left);
        }
        if (curr->right != nullptr) { stk.push(curr->right); }
    }

    reverse(ans.begin(), ans.end()); // 区别 2：reverse
    return ans;
}
```

:::

:::{tab-item} Java

```java
void postorder(TreeNode root) {
    if (root == null)
        return;

    Stack<TreeNode> stack = new Stack<>();
    TreeNode cur = root;
    stack.push(root);
    while (!stack.isEmpty()) {
        cur = stack.peek();
        stack.pop();

        // ans.add(cur.val);

        if (cur.left != null) { // 先左后右
            stack.push(cur.left);
        }
        if (cur.right != null) {
            stack.push(cur.right);
        }

    }

    // reverse(ans); // 记得 reverse
}
```

:::
::::

### 二叉树的层序遍历

::::{tab-set}
:::{tab-item} C++

```cpp
vector<vector<int>> levelOrder(TreeNode* root) {
    if (root == nullptr) { return {}; }

    vector<vector<int>> ans;
    deque<TreeNode*> dq;
    TreeNode* curr = root;
    dq.push_back(root);
    while (!dq.empty()) {
        int sz = dq.size();
        vector<int> lvl;
        while (sz--) {
            curr = dq.front();
            dq.pop_front();

            lvl.push_back(curr->val);

            if (curr->left != nullptr) { dq.push_back(curr->left); }
            if (curr->right != nullptr) { dq.push_back(curr->right); }
        }
        ans.push_back(lvl);
    }

    return ans;
}
```

:::

:::{tab-item} Java

```java
Queue<Integer> queue = new LinkedList<>();

void traverse(TreeNode root) {
    if (root != null)
        queue.offer(root);
    else
        return;

    TreeNode p = queue.poll();
    while (p != null) {
        if (p.left != null) {
            queue.offer(p.left);
        }
        if (p.right != null) {
            queue.offer(p.right);
        }
        if (!queue.isEmpty()) {
            p = queue.poll();
        }
    }
}
```

:::
::::

### 二叉树的最大深度

::::{tab-set}
:::{tab-item} C++

```cpp
int maxDepth(TreeNode* root) {
    if (root == nullptr) { return 0; }

    int left = maxDepth(root->left) + 1;
    int right = maxDepth(root->right) + 1;

    return left > right ? left : right;
}
```

:::

:::{tab-item} Java

```java
public int maxDepth(TreeNode root) {
    if (root == null)
        return 0;

    int left = maxDepth(root.left) + 1;
    int right = maxDepth(root.right) + 1;

    return left > right ? left : right;
}
```

:::
::::

### 对称二叉树的判定

::::{tab-set}
:::{tab-item} C++
:sync: cpp

```cpp
bool compare(TreeNode* left, TreeNode* right) {
    if (left == nullptr && right == nullptr) {
        return true;
    } else if (left != nullptr && right == nullptr) {
        return false;
    } else if (left == nullptr && right != nullptr) {
        return false;
    } else if (left->val != right->val) {
        return false;
    }

    bool oo = compare(left->left, right->right); // 对比外侧
    bool ii = compare(left->right, right->left); // 对比内侧

    return oo && ii;
}

bool isSymmetric(TreeNode* root) {
    if (root == nullptr) { return true; }
    return compare(root->left, root->right);
}
```

:::

:::{tab-item} Java
:sync: java

```java
public boolean isSymmetric(TreeNode root) {
    if (root == null)
        return true;
    return compare(root.left, root.right);
}

public boolean compare(TreeNode left, TreeNode right) {
    if (left == null && right != null)
        return false;
    else if (left != null && right == null)
        return false;
    else if (left == null && right == null)
        return true;
    else if (left.val != right.val)
        return false;

    // 后序遍历代码如下：

    // 比较外侧是否相同
    boolean outside = compare(left.left, right.right);

    // 比较内侧是否相同
    boolean inside = compare(left.right, right.left);

    return outside && inside;
}
```

:::
::::

### 二叉树的所有路径

::::{tab-set}
:::{tab-item} C++
:sync: cpp

```cpp
// path 变量的值，系统栈会自动帮我们维护，不管是压栈还是出栈
// paths 必须是引用，这个变量是需要我们手工维护的
void dfs(TreeNode* root, string path, vector<string>& paths) {
    if (root == nullptr) { return; }

    // 构造路径
    path += to_string(root->val);
    if (root->left == nullptr && root->right == nullptr) { paths.push_back(path); }
    path += "->";

    dfs(root->left, path, paths);
    dfs(root->right, path, paths);
}

vector<string> binaryTreePaths(TreeNode* root) {
    vector<string> paths;
    dfs(root, "", paths); // 为了把 paths 保存在栈里，所以把 paths 当做参数传递
    return paths;
}
```

:::
::::

### 二叉搜索树中的插入操作

::::{tab-set}
:::{tab-item} C++
:sync: cpp

```cpp
TreeNode* insertIntoBST(TreeNode* root, int val) {
    // 一定会到叶子结点上，因为树上的所有的值都不相等，而连接两个节点的值又是邻值
    if (root == nullptr) { return new TreeNode(val); }

    if (root->val > val) {
        root->left = insertIntoBST(root->left, val);
    } else {
        root->right = insertIntoBST(root->right, val);
    }

    return root;
}
```

:::
::::

### 二叉搜索树中的删除操作

::::{tab-set}
:::{tab-item} C++
:sync: cpp

```cpp
TreeNode* deleteNode(TreeNode* root, int key) {
    // 递归终止条件 1
    if (root == nullptr) { return nullptr; }

    // 递归：将其转为更小的问题（将递归放在递归终止条件 2 前面会提高效率）
    if (root->val < key) { root->right = deleteNode(root->right, key); }

    if (root->val > key) { root->left = deleteNode(root->left, key); }

    // 递归终止条件 2：考虑删除节点相等的情况，如何调整树的结构
    if (root->val == key) {
        // case 1: 左子树为空
        if (root->left == nullptr) { return root->right; }

        // case 2: 右子树为空
        if (root->right == nullptr) { return root->left; }

        // case3: 左子树和右子树都为空的情况，包含在 case1 或 case2 了

        // case4: 若左子树和右子树都不为空
        // 那么，将要删除的节点的左子树挂在右子树的最左子节点的左子树上
        TreeNode* p = root->right; // 找到右子树的最左子节点
        while (p->left != nullptr) { p = p->left; }
        p->left = root->left; // 重新挂载左子树
        root = root->right;
        return root;
    }

    return root;
}
```

:::
::::

### 裁剪二叉搜索树

::::{tab-set}
:::{tab-item} C++
:sync: cpp

```cpp
TreeNode* trimBST(TreeNode* root, int low, int high) {
    if (root == nullptr) { return nullptr; }

    if (root->val < low) { // 裁剪右子树
        return trimBST(root->right, low, high);
    }

    if (root->val > high) { // 裁剪左子树
        return trimBST(root->left, low, high);
    }

    // 下面两个递归其实并没有对节点进行改动，只是遍历
    root->left = trimBST(root->left, low, high);
    root->right = trimBST(root->right, low, high);

    return root;
}
```

:::
::::

### 树状数组

### 字典树

字典树模板：

```cpp
#include <bits/stdc++.h>
using namespace std;

class TrieNode {
public:
    unordered_map<char, TrieNode*> children;
    string word = ""; // 如果该节点是一个完整单词结尾，则保存该单词
};

class Trie {
public:
    TrieNode* root = new TrieNode();

    // 插入单词到 Trie 中
    void insertWord(string& word) {
        TrieNode* node = root;
        for (char c : word) {
            if (!node->children.count(c)) { node->children[c] = new TrieNode(); }
            node = node->children[c];
        }
        node->word = word;
    }
};

int main() {
    string words[] = {"oath", "pea", "eat", "rain"};

    Trie trie;

    // 构建 Trie
    for (string& word : words) { trie.insertWord(word); }

    return 0;
}
```

```{uml}
@startuml
digraph Trie {
    graph [rankdir = TD, nodesep = 0.3, ranksep = 0.5];
    node [shape = circle, height = 0.6, width = 0.6, fontsize = 12];

    // 根节点
    root [label = "root", shape = plaintext];

    // Trie 节点
    node0 [label = ""];
    node1 [label = "o"];
    node2 [label = "a"];
    node3 [label = "t"];
    node4 [label = "h\n(word: oath)"];
    node5 [label = "p"];
    node6 [label = "e"];
    node7 [label = "a"];
    node8 [label = "a\n(word: pea)"];
    node15 [label = "e"];
    node9 [label = "a"];
    node10 [label = "t\n(word: eat)"];
    node11 [label = "r"];
    node12 [label = "a"];
    node13 [label = "i"];
    node14 [label = "n\n(word: rain)"];

    // 边连接
    root -> node0;

    node0 -> node1;
    node1 -> node2;
    node2 -> node3;
    node3 -> node4;

    node0 -> node5;
    node5 -> node6;
    node6 -> node7;
    node7 -> node8;

    node0 -> node15;
    node15 -> node9;
    node9 -> node10;

    node0 -> node11;
    node11 -> node12;
    node12 -> node13;
    node13 -> node14;
}
@enduml
```

## 回溯算法

### 组合 k 个数

::::{tab-set}
:::{tab-item} C++
:sync: cpp

```cpp
// n 个数字的组合问题，其实等价于 n 个数字的全连接图问题
// 每个数字都可以作为起点，每个数字都可以作为终点，但是两条路径不能重合
void dfs(vector<vector<int>>& paths, vector<int>& path, int start, int n, int k) {
    if (path.size() == k) {
        paths.push_back(path);
        return;
    }

    // for (int i = start; i <= n - (k - path.size()) + 1; i++) { // 剪枝优化
    for (int i = start; i <= n; i++) {
        path.push_back(i);
        dfs(paths, path, i + 1, n, k); // dfs(i+1) 表示不可重复选
        path.pop_back();               // 回溯
    }

    return;
}

vector<vector<int>> combine(int n, int k) {
    vector<vector<int>> paths;
    vector<int> path;
    dfs(paths, path, 1, n, k);
    return paths;
}
```

:::
::::

### 组合总和（可重复选）

::::{tab-set}
:::{tab-item} C++
:sync: cpp

```cpp
void dfs(vector<vector<int>>& paths, vector<int>& path, int start, vector<int>& candidates,
         int target) {
    if (target < 0) { return; }

    if (target == 0) {
        paths.push_back(path);
        return;
    }

    for (int i = start; i < candidates.size(); i++) {
        path.push_back(candidates[i]);
        dfs(paths, path, i, candidates, target - candidates[i]); // dfs(i) 表示可重复选
        path.pop_back();
    }
}

vector<vector<int>> combinationSum(vector<int>& candidates, int target) {
    vector<vector<int>> paths;
    vector<int> path;
    dfs(paths, path, 0, candidates, target);
    return paths;
}
```

:::
::::

### 非递减子序列（去重）

::::{tab-set}
:::{tab-item} C++
:sync: cpp

```cpp
// 判断是否为递增序列
bool isValid(vector<int>& path) {
    for (int i = 1; i < path.size(); i++) {
        if (path[i] < path[i - 1]) { return false; }
    }
    return true;
}

void dfs(vector<vector<int>>& paths, vector<int>& path, int start, vector<int>& nums) {
    if (path.size() > 1) {
        if (isValid(path)) { paths.push_back(path); }
    }

    unordered_set<int> used_set; // 对本层应用去重
    for (int i = start; i < nums.size(); i++) {
        if (used_set.find(nums[i]) != used_set.end()) { // 已经使用过 nums[i] 了
            continue;
        }

        path.push_back(nums[i]);
        used_set.insert(nums[i]);
        dfs(paths, path, i + 1, nums);
        // used_set.erase(nums[i]); // 不能解开注释
        path.pop_back();
    }
}

vector<vector<int>> findSubsequences(vector<int>& nums) {
    vector<vector<int>> paths;
    vector<int> path;
    dfs(paths, path, 0, nums);
    return paths;
}
```

:::
::::

### 全排列（不含重复元素）

::::{tab-set}
:::{tab-item} C++
:sync: cpp

```cpp
void dfs(vector<vector<int>>& paths, vector<int>& path, vector<int>& nums,
         vector<bool>& used) {
    if (path.size() == nums.size()) {
        paths.push_back(path);
        return;
    }

    for (int i = 0; i < nums.size(); i++) {
        if (used[i]) { continue; }
        path.push_back(nums[i]);
        used[i] = true;
        dfs(paths, path, nums, used);
        used[i] = false;
        path.pop_back();
    }
}

vector<vector<int>> permute(vector<int>& nums) {
    vector<vector<int>> paths;
    vector<int> path;
    vector<bool> used(nums.size(), false);
    dfs(paths, path, nums, used);
    return paths;
}
```

:::
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

:::
::::

### 全排列（含重复元素）

::::{tab-set}
:::{tab-item} C++
:sync: cpp

```cpp
void dfs(vector<vector<int>>& paths, vector<int>& path, vector<int>& nums,
         vector<bool>& used) {
    if (path.size() == nums.size()) {
        paths.push_back(path);
        return;
    }

    for (int i = 0; i < nums.size(); i++) {
        if (used[i] || (i > 0 && nums[i] == nums[i - 1] && !used[i - 1])) { continue; }

        path.push_back(nums[i]);
        used[i] = true;
        dfs(paths, path, nums, used);
        used[i] = false;
        path.pop_back();
    }
}

vector<vector<int>> permuteUnique(vector<int>& nums) {
    vector<vector<int>> paths;
    vector<int> path;
    vector<bool> used(nums.size(), false);
    sort(nums.begin(), nums.end());
    dfs(paths, path, nums, used);
    return paths;
}
```

:::
::::

### N 皇后问题

::::{tab-set}
:::{tab-item} C++
:sync: cpp

```cpp
void dfs(vector<vector<string>>& paths, vector<string>& path, int row, int n) {
    if (row == n) { // 遍历到最后一行，说明已经找到了一种解法
        paths.push_back(path);
        return;
    }

    // 遍历当前行的每一列，判断当前位置是否可以放置皇后
    for (int col = 0; col < n; col++) {
        // 判断当前位置是否可以放置皇后
        if (path[row][col] == '.') {
            bool flag = true; // flag 为 true 表示当前位置可以放置皇后

            // 判断同一列上是否有皇后
            for (int i = 0; i < row; i++) {
                if (path[i][col] == 'Q') {
                    flag = false;
                    break;
                }
            }

            // 判断同一斜线上是否有皇后
            if (flag) {
                for (int i = row - 1, j = col - 1; i >= 0 && j >= 0; i--, j--) {
                    if (path[i][j] == 'Q') {
                        flag = false;
                        break;
                    }
                }
            }
            if (flag) {
                for (int i = row - 1, j = col + 1; i >= 0 && j < n; i--, j++) {
                    if (path[i][j] == 'Q') {
                        flag = false;
                        break;
                    }
                }
            }

            // 如果当前位置可以放置皇后，则递归调用 dfs 函数，继续向下一行进行遍历
            if (flag) {
                path[row][col] = 'Q';
                dfs(paths, path, row + 1, n);
                path[row][col] = '.';
            }
        }
    }
}

vector<vector<string>> solveNQueens(int n) {
    vector<vector<string>> paths;
    vector<string> path(n, string(n, '.'));
    dfs(paths, path, 0, n);
    return paths;
}
```

:::
::::

### 解数独

::::{tab-set}
:::{tab-item} C++
:sync: cpp

```cpp
bool isValid(vector<vector<char>>& board, int row, int col, char num) {
    // 检查当前行或列是否有重复的数字
    for (int i = 0; i < 9; i++) {
        if (board[row][i] == num || board[i][col] == num) { return false; }
    }

    // 检查 3 x 3 宫格内是否有重复的数字
    int startRow = row - row % 3, startCol = col - col % 3;
    for (int i = startRow; i < startRow + 3; i++) {
        for (int j = startCol; j < startCol + 3; j++) {
            if (board[i][j] == num) { return false; }
        }
    }

    return true;
}

void dfs(vector<vector<char>>& temp, vector<vector<char>>& board, int row, int col) {
    if (row == 9) {
        temp = board;
        return;
    }

    if (col == 9) {
        dfs(temp, board, row + 1, 0);
        return;
    }

    if (board[row][col] != '.') {
        dfs(temp, board, row, col + 1);
        return;
    }

    for (char num = '1'; num <= '9'; num++) {
        if (isValid(board, row, col, num)) {
            board[row][col] = num;
            dfs(temp, board, row, col + 1);
            board[row][col] = '.'; // 回溯
        }
    }
}

void solveSudoku(vector<vector<char>>& board) {
    // 回溯后 board 会恢复原样，因此需要创建一个临时变量保存 board 的状态
    vector<vector<char>> temp = board;
    dfs(temp, board, 0, 0);
    board = temp;
}
```

:::
::::

## 动态规划

动态规划（Dynamic Programming，简称 DP）是一种在计算机科学和数学中**用来求解最优化问题的方法**（即求最值或统计解的数量）。它通常用于解决那些具有**重叠子问题**（即同一个子问题会被多次求解）和**最优子结构**（即问题的最优解可以通过其子问题的最优解来构造）的问题。

### 基本思想

1. **最优子结构**：如果问题的最优解所包含的子问题的解也是最优的，那么这个问题就具有最优子结构性质。
2. **重叠子问题**：当一个递归算法重复地访问同样的子问题时，这些问题就可以通过动态规划方法来高效解决，避免重复计算。

### 解题思路

1. **确定状态**：首先需要定义状态，即用一组变量来描述问题的关键信息，这些变量的不同取值组合可以表示不同的子问题。
2. **定义状态转移方程**：这是动态规划的核心，描述了如何根据较小的子问题的解来得到更大规模问题的解。
3. **边界条件**：找出问题的基础情况或边界条件，也就是最小规模的子问题，它们可以直接求解而不需要进一步分解。
4. **计算顺序**：按照从小到大的顺序计算出所有子问题的解，通常使用自底向上（从简单子问题开始逐步求解复杂问题）的方式进行。
5. **存储结果**：为了避免重复计算相同子问题，需要将已经解决的子问题的结果存储起来以供后续使用，这通常通过数组或表来实现。

### 背包 DP

#### 0-1 背包问题

已知第 `i` 件物品的重量是 `weight[i - 1]`，价值是 `value[i - 1]`，背包的总容量为 `capacity`。

现要求选若干物品放入背包（**物品只能被选 1 次**），使背包中物品的总价值最大且背包中物品的总重量不超过背包的总容量。

- **状态定义**：设 `dp[i][j]` 表示在前 `i` 个物品中选择一些，装入容量为 `j` 的背包可以获得的最大价值。
- **状态转移方程**：

假设当前已经处理好了前 `i - 1` 个物品的所有状态，那么对于第 `i` 个物品，

case 1: 当第 `i` 个物品不放入背包时，状态转移至 `[i - 1, j]`。可以获得的最大价值为：

```cpp
dp[i][j] = dp[i - 1][j]
```

case 2: 当第 `i` 个物品放入背包时，状态转移至 `[i - 1, j - weight[i - 1]]`。可以获得的最大价值为：

```cpp
dp[i][j] = dp[i - 1][j - weight[i - 1]] + value[i - 1]
```

- **边界条件**：如果没有物品或者背包容量为 0，则最大价值为 0，即 `dp[0][j] = 0` 和 `dp[i][0] = 0`。
- **计算顺序**：从 `i=1, j=1` 开始，按行或列的顺序依次填充表格。
- **存储结果**：最终答案位于 `dp[n][capacity]`，其中 `n` 是物品总数，`capacity` 是背包的最大承重。

::::{tab-set}
:::{tab-item} C++
:sync: cpp

```cpp
int zeroOneKnapsack(vector<int>& weight, vector<int>& value, int capacity) {
    // 创建一个 (n + 1) * (capacity + 1) 的二维数组，行：物品索引，列：容量（包括 0）
    // 第一维通常是物品的数量
    // 第二维表示中间结果的种类数，由于容量不可能为负数，因此中间结果可能是 0...capacity
    int n = weight.size();
    vector<vector<int>> dp(n + 1, vector<int>(capacity + 1, 0));

    // 边界条件：如果没有物品或者背包容量为 0，则最大价值为 0

    // 状态定义：dp[i][j] 表示在前 i 个物品中选择一些，放入容量为 j 的背包中，可获得的最大价值
    // 根据状态转移方程，填充 dp 数组
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= capacity; j++) {
            if (j - weight[i - 1] >= 0) {
                // 当前物品的重量小于等于背包容量时，可以放，也可以不放
                dp[i][j] = max(dp[i - 1][j], dp[i - 1][j - weight[i - 1]] + value[i - 1]);
            } else {
                // 当前物品的重量大于背包容量时，只能选择不放该物品
                dp[i][j] = dp[i - 1][j];
            }
        }
    }

    return dp[n][capacity];
}
```

::::

空间优化请参考：<https://www.hello-algo.com/chapter_dynamic_programming/knapsack_problem/#4>

```cpp
int zeroOneKnapsack2(vector<int>& weight, vector<int>& value, int capacity) {
    int n = weight.size();
    vector<int> dp(capacity + 1, 0);

    for (int i = 1; i <= n; i++) {
        for (int j = capacity; j >= 1; j--) {
            if (j >= weight[i - 1]) {
                dp[j] = max(dp[j], dp[j - weight[i - 1]] + value[i - 1]);
            }
        }
    }

    return dp[capacity];
}
```

#### 完全背包问题

已知第 `i` 件物品的重量是 `weight[i - 1]`，价值是 `value[i - 1]`，背包的总容量为 `capacity`。

现要求选若干物品放入背包（**物品可以无限次使用**），使背包中物品的总价值最大且背包中物品的总重量不超过背包的总容量。

- **状态定义**：`dp[i][j]` 表示在前 `i` 种物品中选择一些，装入容量为 `j` 的背包可以获得的最大价值。
- **状态转移方程**：

在完全背包问题中，每种物品的数量是无限的，因此将物品 `i` 放入背包后，**仍可以从前 `i` 个物品中选择**。

case 1: 当第 `i` 个物品不放入背包时，背包总容量不变，背包中物品的总价值不变。可以获得的最大价值为：

```cpp
dp[i][j] = dp[i - 1][j]
```

case 2: 当第 `i` 个物品放入背包时，状态转移至 `[i, j - weight[i - 1]]`。可以获得的最大价值为：

```cpp
dp[i][j] = dp[i, j - weight[i - 1]] + value[i - 1]
```

- **边界条件**：如果没有物品或者背包容量为 0，则最大价值为 0，即 `dp[0][j] = 0` 和 `dp[i][0] = 0`。
- **计算顺序**：从 `i=1, j=1` 开始，按行或按列的顺序依次填充表格。
- **存储结果**：最终结果存储在 `dp[n][capacity]` 中，其中 `n` 是物品总数，`capacity` 是背包的最大承重。

```cpp
int unboundedKnapsack(vector<int>& weight, vector<int>& value, int capacity) {
    // 创建一个 (n + 1) * (capacity + 1) 的二维数组，行：物品索引，列：容量（包括 0）
    // 第一维通常是物品的数量
    // 第二维表示中间结果的种类数，由于容量不可能为负数，因此中间结果可能是 0...capacity
    int n = weight.size();
    vector<vector<int>> dp(n + 1, vector<int>(capacity + 1, 0));

    // 边界条件：如果没有物品或者背包容量为 0，则最大价值为 0

    // 状态定义：dp[i][j] 表示在前 i 个物品中选择一些，放入容量为 j 的背包中，可获得的最大价值
    // 根据状态转移方程，填充 dp 数组
    for (int i = 1; i <= n; ++i) {
        for (int j = 1; j <= capacity; ++j) {
            if (j - weight[i - 1] >= 0) {
                // 当前物品的重量小于等于背包容量时，可以放，也可以不放
                dp[i][j] = max(dp[i - 1][j], dp[i][j - weight[i - 1]] + value[i - 1]);
            } else {
                // 当前物品的重量大于背包容量时，只能选择不放该物品
                dp[i][j] = dp[i - 1][j];
            }
        }
    }

    return dp[n][capacity];
}
```

### 区间 DP

### DAG 上的 DP

### 树形 DP

### 状压 DP

### 数位 DP

### 插头 DP

### 计数 DP

### 动态 DP

### 概率 DP

## 排序算法

### 堆排序

::::{tab-set}
:::{tab-item} Java
:sync: java

`PriorityQueue` 就是一个小根堆结构，可以直接使用。

```java
void heapSort(int[] arr) {
    if (arr == null || arr.length < 2)
        return;
    // 构建大根堆（方法一）
    // for (int i = 0; i < arr.length; i++)
    // heapInsert(arr, i);
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
void mergeSort(int[] arr, int[] tmp, int left, int right) {
    if (left < right) {
        int mid = left + (right - left) / 2;
        mergeSort(arr, tmp, left, mid);
        mergeSort(arr, tmp, mid + 1, right);
        merge(arr, tmp, left, mid, right);
    }
}

void merge(int[] arr, int[] tmp, int left, int mid, int right) {
    int pLeft = left;
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
        for (j = i; j > 0 && arr[j - 1] > tmp; j--)
            arr[j] = arr[j - 1]; // 向后移动元素
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
void quickSort(int[] arr, int left, int right) {
    if (left < right) {
        int pivot = arr[left]; // 随机选基准点
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
void heapify(int[] arr, int i, int heapSize) {
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
    for (int step = arr.length / 2; step >= 1; step /= 2) {
        for (int r = step; r < arr.length; r++) {
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
int binarySearch(int[] arr, int target, int left, int right) {
    if (left <= right) {
        int mid = left + (right - left) / 2;

        if (arr[mid] == target)
            return mid;

        if (arr[mid] > target) // 向左查找
            return binarySearch(arr, target, left, mid - 1);

        if (arr[mid] < target) // 向右查找
            return binarySearch(arr, target, mid + 1, right);
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
void getNext(vector<int>& next, string pat) {
    // 初始化 next 数组的第一个元素为 0
    int j = 0;
    next[0] = 0;

    for (int i = 1; i < pat.size(); i++) {
        // 当前字符不匹配时，回退 j 到 next[j-1] 的位置
        while (j > 0 && pat[i] != pat[j]) { j = next[j - 1]; }
        // 当前字符匹配时，则 j 自增
        if (pat[i] == pat[j]) { j++; }
        // next[i] 表示当前位置与模式串匹配的起始位置
        next[i] = j;
    }
}

// 返回 pat 匹配 txt 的起始位置，若匹配失败则返回 -1
int kmp(string pat, string txt) {
    int n = txt.size();
    int m = pat.size();
    vector<int> next(m);
    getNext(next, pat);
    int j = 0;
    for (int i = 0; i < n; i++) {
        // 当当前字符不匹配且 j 大于 0 时，调整 j 的位置
        while (j > 0 && txt[i] != pat[j]) { j = next[j - 1]; }
        // 当前字符匹配时，j 自增
        if (txt[i] == pat[j]) { j++; }
        // 匹配成功，返回匹配的起始位置
        if (j == m) { return i - m + 1; }
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

## 图论

### 存图方式

#### 邻接表

::::{grid} auto
:::{grid-item}

无权图：

```{mermaid}
flowchart LR
    node1((1))
    node2((2))
    node3((3))
    node4((4))

    node1 --> node2 --> node3 --> node4
    node2 --> node4
    node4 --> node1
```

```cpp
vector<int> adj[N];

adj[1].push_back(2);
adj[2].push_back(3);
adj[2].push_back(4);
adj[3].push_back(4);
adj[4].push_back(1);
```

:::
:::{grid-item}

带权图：

```{mermaid}
flowchart LR
    node1((1))
    node2((2))
    node3((3))
    node4((4))

    node1 -- 5 --> node2 -- 7 --> node3 -- 5 --> node4
    node2 -- 6 --> node4
    node4 -- 2 --> node1
```

```cpp
vector<pair<int, int>> adj[N];

adj[1].push_back({2, 5});
adj[2].push_back({3, 7});
adj[2].push_back({4, 6});
adj[3].push_back({4, 5});
adj[4].push_back({1, 2});
```

:::
::::

遍历从节点 `s` 出发能够到达的所有节点：

```cpp
for (auto u : adj[s]) {
    // process node u
}
```

#### 邻接矩阵

::::{grid} auto
:::{grid-item}

无权图：

```{mermaid}
flowchart LR
    node1((1))
    node2((2))
    node3((3))
    node4((4))

    node1 --> node2 --> node3 --> node4
    node2 --> node4
    node4 --> node1
```

:::
:::{grid-item}

带权图：

```{mermaid}
flowchart LR
    node1((1))
    node2((2))
    node3((3))
    node4((4))

    node1 -- 5 --> node2 -- 7 --> node3 -- 5 --> node4
    node2 -- 6 --> node4
    node4 -- 2 --> node1
```

:::
::::

不论是无权图还是带权图，都可以用下面的二维数组表示：

```cpp
int adj[N][N];
```

#### 边

::::{grid} auto
:::{grid-item}

无权图：

```{mermaid}
flowchart LR
    node1((1))
    node2((2))
    node3((3))
    node4((4))

    node1 --> node2 --> node3 --> node4
    node2 --> node4
    node4 --> node1
```

```cpp
vector<pair<int, int>> edges;

edges.push_back({1, 2});
edges.push_back({2, 3});
edges.push_back({2, 4});
edges.push_back({3, 4});
edges.push_back({4, 1});
```

:::
:::{grid-item}

带权图：

```{mermaid}
flowchart LR
    node1((1))
    node2((2))
    node3((3))
    node4((4))

    node1 -- 5 --> node2 -- 7 --> node3 -- 5 --> node4
    node2 -- 6 --> node4
    node4 -- 2 --> node1
```

```cpp
vector<tuple<int, int, int>> edges;

edges.push_back({1, 2, 5});
edges.push_back({2, 3, 7});
edges.push_back({2, 4, 6});
edges.push_back({3, 4, 5});
edges.push_back({4, 1, 2});
```

:::
::::

### 图的遍历

::::{grid} auto
:::{grid-item}

深度优先遍历：

```{mermaid}
flowchart LR
    node1((1))
    node2((2))
    node3((3))
    node4((4))
    node5((5))

    node1 --- node2 --- node3 --- node5
    node2 --- node5
    node1 --- node4
```

```cpp
vector<int> adj[N];
bool visited[N];

void dfs(int s) {
    if (visited[s]) return;
    visited[s] = true;
    // process node s
    for (auto u : adj[s]) { dfs(u); }
}
```

:::
:::{grid-item}

广度优先遍历：

```{mermaid}
flowchart LR
    node1((1))
    node2((2))
    node3((3))
    node4((4))
    node5((5))
    node6((6))

    node1 --- node2 --- node3 --- node6
    node2 --- node5
    node5 --- node6
    node1 --- node4
```

```cpp
queue<int> q;
bool visited[N];
int distance[N];

void bfs(queue<int>& q, bool& visited, int& distance) {
    visited[x] = true;
    distance[x] = 0;
    q.push(x);
    while (!q.empty()) {
        int s = q.front();
        q.pop();
        // process node s
        for (auto u : adj[s]) {
            if (visited[u]) continue;
            visited[u] = true;
            distance[u] = distance[s] + 1;
            q.push(u);
        }
    }
}
```

:::
::::

### 最短路径算法

#### Bellman-Ford 算法

用于解决单源最短路径问题。（不能包含负权边）

```cpp
for (int i = 1; i <= n; i++) distance[i] = INF;
distance[x] = 0;
for (int i = 1; i <= n - 1; i++) {
    for (auto e : edges) { // 用边存图
        int a, b, w;
        tie(a, b, w) = e;
        distance[b] = min(distance[b], distance[a] + w);
    }
}
```

```{note}
SPFA 算法是 Bellman-Ford 的优化版本。
```

#### Dijkstra 算法

Dijsktra 比 Bellman-Ford 更加高效，因为它只遍历每条边一次。

```cpp
for (int i = 1; i <= n; i++) distance[i] = INF;
distance[x] = 0;
q.push({0, x}); // 必须使用优先队列
while (!q.empty()) {
    int a = q.top().second;
    q.pop();
    if (processed[a]) continue;
    processed[a] = true;
    for (auto u : adj[a]) { // 邻接表
        int b = u.first, w = u.second;
        if (distance[a] + w < distance[b]) {
            distance[b] = distance[a] + w;
            q.push({-distance[b], b});
        }
    }
}
```

#### Floyd-Warshall 算法

多源最短路径算法。（仅适用于小图，因为时间复杂度太高了 $O(n^3)$）

```cpp
// 初始化 distance 矩阵
for (int i = 1; i <= n; i++) {
    for (int j = 1; j <= n; j++) {
        if (i == j)
            distance[i][j] = 0;
        else if (adj[i][j]) // 邻接矩阵
            distance[i][j] = adj[i][j];
        else
            distance[i][j] = INF;
    }
}

// 填充 distance 矩阵
for (int k = 1; k <= n; k++) {
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= n; j++) {
            distance[i][j] = min(distance[i][j], distance[i][k] + distance[k][j]);
        }
    }
}
```

### 多叉树

#### 遍历多叉树

```cpp
void dfs(int s, int e) {
    // process node s
    for (auto u : adj[s]) {
        if (u != e) dfs(u, s);
    }
}
```

`s` 表示当前节点，`e` 表示前一个节点。`u != e` 表示不能访问已经访问过的节点。初始条件如下：

```cpp
dfs(x, 0);
```

#### 动态规划

计算每个节点的子节点数量。

```cpp
void dfs(int s, int e) {
    count[s] = 1;
    for (auto u : adj[s]) {
        if (u == e) continue;
        dfs(u, s);
        count[s] += count[u];
    }
}
```

### 生成树

#### Kruskal 算法

#### 并查集

#### Prim 算法

### 有向图

#### 拓扑排序

### 强连通图

#### Kosaraju 算法

#### 2SAT 问题
