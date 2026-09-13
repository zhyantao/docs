# 图论

> 存图方式（邻接表/矩阵/边）、DFS/BFS 遍历、Bellman-Ford、Dijkstra、Floyd、多叉树、生成树、拓扑排序与强连通。

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
    for (auto u : adj[s]) {
        dfs(u);
    }
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
    visited[x]  = true;
    distance[x] = 0;
    q.push(x);
    while (!q.empty()) {
        int s = q.front();
        q.pop();
        // process node s
        for (auto u : adj[s]) {
            if (visited[u]) continue;
            visited[u]  = true;
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

用于解决单源最短路径问题（不能包含负权环）。

```cpp
for (int i = 1; i <= n; i++)
    distance[i] = INF;
distance[x] = 0;
for (int i = 1; i <= n - 1; i++) {
    for (auto e : edges) { // 用边存图
        int a, b, w;
        tie(a, b, w) = e;
        distance[b]  = min(distance[b], distance[a] + w);
    }
}
```

```{note}
SPFA 算法是 Bellman-Ford 的优化版本。
```

#### Dijkstra 算法

Dijkstra 比 Bellman-Ford 更加高效，因为它只遍历每条边一次。

```cpp
for (int i = 1; i <= n; i++)
    distance[i] = INF;
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

### Floyd 算法

```c++
// LeetCode 1334
// 状态转移方程
vector memo(n, vector(n, vector<int>(n))); // 记忆化搜索去掉重复计算
auto dfs = [&](this auto&& dfs, int k, int i, int j) -> int {
    if (k < 0) { // 递归边界
        return w[i][j];
    }
    auto& res = memo[k][i][j]; // 注意这里是引用（不用引用时是值传递，无法修改 memo[k][i][j]）
    if (res) {                 // 之前计算过
        return res;
    }
    return res = min(dfs(k - 1, i, j), dfs(k - 1, i, k) + dfs(k - 1, k, j));
};
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

最小生成树（MST）：连接所有顶点且边权和最小的树。两种经典算法：

#### 并查集

**并查集（Union-Find / DSU）**：维护元素所属集合，支持近似 $O(1)$（反阿克曼函数）的**查询**与**合并**，是 Kruskal 与连通性问题的基石。

```cpp
struct DSU {
    vector<int> parent, sz;          // sz 记录集合大小（按大小合并）
    DSU(int n) : parent(n), sz(n, 1) { iota(parent.begin(), parent.end(), 0); }

    int find(int x) {                // 路径压缩
        return parent[x] == x ? x : parent[x] = find(parent[x]);
    }

    bool unite(int a, int b) {       // 合并，返回是否真的合并了
        a = find(a); b = find(b);
        if (a == b) return false;
        if (sz[a] < sz[b]) swap(a, b);   // 小集合并入大集合
        parent[b] = a;
        sz[a] += sz[b];
        return true;
    }

    bool same(int a, int b) { return find(a) == find(b); }
};
```

```{note}
路径压缩 + 按大小（或按秩）合并后，单次操作复杂度为 $O(\alpha(n))$，可视为常数。
并查集还可维护**带权**（到根的距离）与**种类**（边权并查集，如食物链问题）。
```

#### Kruskal 算法

按边权从小到大排序，依次尝试加入，用并查集判环（两点已连通则跳过）。复杂度 $O(m \log m)$，适用于**稀疏图**。

```cpp
// edges: {w, u, v}
int kruskal(int n, vector<array<int, 3>>& edges) {
    sort(edges.begin(), edges.end());
    DSU dsu(n);
    int ans = 0, cnt = 0;
    for (auto& [w, u, v] : edges) {
        if (dsu.unite(u, v)) {
            ans += w;
            if (++cnt == n - 1) break;   // 已连成树
        }
    }
    return cnt == n - 1 ? ans : -1;      // -1 表示图不连通
}
```

#### Prim 算法

从任意顶点出发，每次把"距离当前树最近"的边纳入（用优先队列取最小），复杂度 $O(m \log n)$，适用于**稠密图**（朴素版 $O(n^2)$ 更优）。

```cpp
// 邻接表 g[u]: {v, w}
int prim(int n, vector<vector<pair<int, int>>>& g) {
    priority_queue<pair<int, int>, vector<pair<int, int>>, greater<>> pq;
    vector<int> vis(n, 0), dis(n, INT_MAX);
    dis[0] = 0;
    pq.push({0, 0});
    int ans = 0, cnt = 0;
    while (!pq.empty()) {
        auto [d, u] = pq.top(); pq.pop();
        if (vis[u]) continue;
        vis[u] = 1;
        ans += d;
        if (++cnt == n) break;
        for (auto& [v, w] : g[u])
            if (!vis[v] && w < dis[v]) {
                dis[v] = w;
                pq.push({w, v});
            }
    }
    return cnt == n ? ans : -1;
}
```

### 有向图

#### 拓扑排序

对有向无环图（DAG）按依赖关系排序：**Kahn 算法**用队列维护入度为 0 的节点，逐层删除并更新入度。若最终入队节点数 < n，说明图中有环。

```cpp
// 邻接表 g，入度数组 indeg
vector<int> topoSort(int n, vector<vector<int>>& g, vector<int>& indeg) {
    queue<int> q;
    for (int i = 0; i < n; i++)
        if (indeg[i] == 0) q.push(i);
    vector<int> order;
    while (!q.empty()) {
        int u = q.front(); q.pop();
        order.push_back(u);
        for (int v : g[u])
            if (--indeg[v] == 0) q.push(v);
    }
    return order.size() == n ? order : vector<int>(); // 空表示有环
}
```

```{note}
- 拓扑排序可用于**课程表**（LC207/210）、任务依赖、DAG 上的 DP 顺序；
- 要求字典序最小拓扑序时，把队列换成**小根堆**；
- 求图中是否有环：拓扑排序后节点数不足 n 即有环；DFS 三色法亦可判环。
```

### 强连通图

**强连通分量（SCC）**：有向图中两两互相可达的极大子图。缩点（把每个 SCC 压缩成一个点）后原图变成 DAG，可用于 2SAT、连通性问题。

#### Kosaraju 算法

两次 DFS：① 按完成时间记录出栈序；② 在**反向图**上按出栈序逆序 DFS，每次遍历到的一个连通块即一个 SCC。复杂度 $O(n + m)$。

```cpp
// g 原图，rg 反向图；seq 为第一次 DFS 的出栈序
void kosaraju(int n, vector<vector<int>>& g, vector<vector<int>>& rg) {
    vector<int> vis(n, 0), seq;
    function<void(int)> dfs1 = [&](int u) {
        vis[u] = 1;
        for (int v : g[u]) if (!vis[v]) dfs1(v);
        seq.push_back(u);                    // 记录出栈序
    };
    for (int i = 0; i < n; i++) if (!vis[i]) dfs1(i);

    vector<int> comp(n, -1);
    int cnt = 0;
    function<void(int, int)> dfs2 = [&](int u, int c) {
        comp[u] = c;
        for (int v : rg[u]) if (comp[v] == -1) dfs2(v, c);
    };
    for (int i = n - 1; i >= 0; i--)         // 按出栈序逆序在反向图 DFS
        if (comp[seq[i]] == -1) dfs2(seq[i], cnt++);
    // comp[u] 即 u 所属 SCC 编号，cnt 为 SCC 个数
}
```

#### 2SAT 问题

每个布尔变量 $x_i$ 拆成两个节点（$x_i$ 真 / 假），把形如 $(a \lor b)$ 的限制转为蕴含边 $(\neg a \to b,\ \neg b \to a)$，然后求 SCC：若 $x_i$ 与其否定在同一 SCC 则无解；否则按拓扑序（SCC 编号）赋值——SCC 编号小的为真（Kosaraju 中先被访问的 SCC 拓扑序靠后，取 `comp[x] > comp[¬x]` 为真即可）。

```{note}
2SAT 的典型应用：安排互斥事件、配对问题（如每个点选 0/1 且满足若干"至少一个为真"的限制）。
完整模板：建图 → Kosaraju/Tarjan 求 SCC → 逐变量比较两节点 SCC 编号判断可满足性并赋值。
```
