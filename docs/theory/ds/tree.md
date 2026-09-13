# 树与字典树

> 二叉树遍历（递归/前中后序/层序）、最大深度、对称判定、路径、二叉搜索树操作、树状数组与字典树模板。

## 树

### 二叉树的递归遍历

::::{tab-set}
:::{tab-item} C++
:sync: cpp

```cpp
vector<int> ans;
vector<int> traverse(TreeNode* root) {
    if (root == nullptr) {
        return;
    }

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
    if (root == nullptr) {
        return {};
    }

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
        if (curr->left != nullptr) {
            stk.push(curr->left);
        }
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
    if (root == nullptr) {
        return {};
    }

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
    if (root == nullptr) {
        return {};
    }

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
        if (curr->right != nullptr) {
            stk.push(curr->right);
        }
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
    if (root == nullptr) {
        return {};
    }

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

            if (curr->left != nullptr) {
                dq.push_back(curr->left);
            }
            if (curr->right != nullptr) {
                dq.push_back(curr->right);
            }
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
    if (root == nullptr) {
        return 0;
    }

    int left  = maxDepth(root->left) + 1;
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
    if (root == nullptr) {
        return true;
    }
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
    if (root == nullptr) {
        return;
    }

    // 构造路径
    path += to_string(root->val);
    if (root->left == nullptr && root->right == nullptr) {
        paths.push_back(path);
    }
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
    if (root == nullptr) {
        return new TreeNode(val);
    }

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
    if (root == nullptr) {
        return nullptr;
    }

    // 递归：将其转为更小的问题（将递归放在递归终止条件 2 前面会提高效率）
    if (root->val < key) {
        root->right = deleteNode(root->right, key);
    }

    if (root->val > key) {
        root->left = deleteNode(root->left, key);
    }

    // 递归终止条件 2：考虑删除节点相等的情况，如何调整树的结构
    if (root->val == key) {
        // case 1: 左子树为空
        if (root->left == nullptr) {
            return root->right;
        }

        // case 2: 右子树为空
        if (root->right == nullptr) {
            return root->left;
        }

        // case3: 左子树和右子树都为空的情况，包含在 case1 或 case2 了

        // case4: 若左子树和右子树都不为空
        // 那么，将要删除的节点的左子树挂在右子树的最左子节点的左子树上
        TreeNode* p = root->right; // 找到右子树的最左子节点
        while (p->left != nullptr) {
            p = p->left;
        }
        p->left = root->left; // 重新挂载左子树
        root    = root->right;
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
    if (root == nullptr) {
        return nullptr;
    }

    if (root->val < low) { // 裁剪右子树
        return trimBST(root->right, low, high);
    }

    if (root->val > high) { // 裁剪左子树
        return trimBST(root->left, low, high);
    }

    // 下面两个递归其实并没有对节点进行改动，只是遍历
    root->left  = trimBST(root->left, low, high);
    root->right = trimBST(root->right, low, high);

    return root;
}
```

:::
::::

### 树状数组

树状数组（Fenwick Tree）利用 `lowbit(x) = x & -x` 对下标分组，支持 $O(\log n)$ 的**单点更新**与**前缀和查询**。与线段树相比代码更短、常数更小；不支持区间更新（需配合差分）与区间最值。

核心：`tree[i]` 维护区间 `[i - lowbit(i) + 1, i]` 的和。

```cpp
struct Fenwick {
    int n;
    vector<int> tree;
    Fenwick(int n) : n(n), tree(n + 1) {}

    void add(int i, int v) { // 单点加 v（下标从 1 开始）
        for (; i <= n; i += i & -i)
            tree[i] += v;
    }

    int pre(int i) { // 前缀和 [1, i]
        int s = 0;
        for (; i > 0; i -= i & -i)
            s += tree[i];
        return s;
    }

    int rangeSum(int l, int r) { return pre(r) - pre(l - 1); } // 区间和
};
```

```{note}
- 下标**必须从 1 开始**，原数组 `a[0..n-1]` 映射为 `i = idx + 1`；
- 求区间和用前缀和相减；配合差分数组可把"区间加、单点查"转为"单点加、前缀查"；
- 需要动态求第 k 小元素时，可在树状数组上做**倍增/二分**（权值树状数组）。
```

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
            if (!node->children.count(c)) {
                node->children[c] = new TrieNode();
            }
            node = node->children[c];
        }
        node->word = word;
    }
};

int main() {
    string words[] = {"oath", "pea", "eat", "rain"};

    Trie trie;

    // 构建 Trie
    for (string& word : words) {
        trie.insertWord(word);
    }

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
