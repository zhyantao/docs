# Mermaid

## 流程图

### 节点和连线

```{mermaid}
flowchart TB
  root
  node_a[This is node A]
  node_b["This is node B ❤ "]
  node_c(This is node C)
  node_d(This is node D)
  node_e([This is node E])
  node_f([This is node F])
  node_g[\This is node G/]
  node_h[\This is node H/]
  node_i[/This is node I/]
  node_j[/This is node J/]
  node_k[\This is node K\]
  node_l[\This is node L\]
  node_m[/This is node M\]
  node_n[/This is node N\]
  node_o[[This is node O]]
  node_p[[This is node P]]
  node_q{{This is node Q}}
  node_r{{This is node R}}
  node_s{This is node S}
  node_t((This is node T))
  node_u[(This is node U)]
  node_v>This is node V]
  node_w(((This is node W)))

  root --- node_a
  root --- node_b
  node_a --- node_c
  node_a --- node_d
  node_b -- B to E --- node_e
  node_b ---|B to F| node_f
  node_c --> node_g
  node_c --> node_h
  node_d -- D to I --> node_i
  node_d -->|D to J| node_j
  node_e -.->  node_k
  node_e -.-> node_l
  node_f -. F to M .-> node_m
  node_f -.->|F to N| node_n
  node_g ==> node_o
  node_h ==> node_o
  node_i == I to P ==> node_p
  node_j ==>|J to P| node_p
  node_k --o node_q
  node_l --o node_q
  node_m o--o node_r
  node_n o--o node_r
  node_o --x node_s
  node_p --x node_s
  node_q x--x node_t
  node_r x--x node_t
  node_s <--> node_u
  node_t <--> node_v

  subgraph sub
    node_u --- node_w
    node_v --- node_w
  end
```

### 方向

::::{grid} 1 2 3 4

:::{grid-item}

从上往下

```{mermaid}
flowchart TD
    Start --> Stop
```

:::

:::{grid-item}

从左往右

```{mermaid}
flowchart LR
    Start --> Stop
```

:::

::::

### 子图

::::{grid} auto

:::{grid-item}

标准子图

```{mermaid}
flowchart TB
    c1-->a2
    subgraph one
    a1-->a2
    end
    subgraph two
    b1-->b2
    end
    subgraph three
    c1-->c2
    end
    one --> two
    three --> two
    two --> c2
```

:::

:::{grid-item}

定义嵌套子图的方向

```{mermaid}
flowchart LR
  subgraph TOP
    direction TB
    subgraph B1
        direction RL
        i1 -->f1
    end
    subgraph B2
        direction BT
        i2 -->f2
    end
  end
  A --> TOP --> B
  B1 --> B2
```

:::

::::

## 序列图

```{mermaid}
sequenceDiagram
    autonumber
    Alice->>John: Hello John, how are you?
    loop HealthCheck
        John->>John: Fight against hypochondria
    end
    Note right of John: Rational thoughts!
    John-->>Alice: Great!
    John->>Bob: How about you?
    Bob-->>John: Jolly good!
```

## 类图

```{mermaid}
classDiagram
classA --|> classB : Inheritance
classC --* classD : Composition
classE --o classF : Aggregation
classG --> classH : Association
classI -- classJ : Link(Solid)
classK ..> classL : Dependency
classM ..|> classN : Realization
classO .. classP : Link(Dashed)
```

## 状态图

```{mermaid}
stateDiagram
    direction LR
    [*] --> A
    A --> B
    B --> C
    state B {
      direction LR
      a --> b
    }
    B --> D
```

## ER 图

```{mermaid}
erDiagram
    CAR ||--o{ NAMED-DRIVER : allows
    CAR {
        string registrationNumber PK
        string make
        string model
        string[] parts
    }
    PERSON ||--o{ NAMED-DRIVER : is
    PERSON {
        string driversLicense PK "The license #"
        string(99) firstName "Only 99 characters are allowed"
        string lastName
        string phone UK
        int age
    }
    NAMED-DRIVER {
        string carRegistrationNumber PK, FK
        string driverLicence PK, FK
    }
    MANUFACTURER only one to zero or more CAR : makes
```

## 甘特图

```{mermaid}
gantt
    dateFormat  YYYY-MM-DD
    title       Adding GANTT diagram functionality to mermaid
    excludes    weekends
    %% (`excludes` accepts specific dates in YYYY-MM-DD format, days of the week ("sunday") or "weekends", but not the word "weekdays".)

    section A section
    Completed task            :done,    des1, 2014-01-06,2014-01-08
    Active task               :active,  des2, 2014-01-09, 3d
    Future task               :         des3, after des2, 5d
    Future task2              :         des4, after des3, 5d

    section Critical tasks
    Completed task in the critical line :crit, done, 2014-01-06,24h
    Implement parser and jison          :crit, done, after des1, 2d
    Create tests for parser             :crit, active, 3d
    Future task in critical line        :crit, 5d
    Create tests for renderer           :2d
    Add to mermaid                      :until isadded
    Functionality added                 :milestone, isadded, 2014-01-25, 0d

    section Documentation
    Describe gantt syntax               :active, a1, after des1, 3d
    Add gantt diagram to demo page      :after a1  , 20h
    Add another diagram to demo page    :doc1, after a1  , 48h

    section Last section
    Describe gantt syntax               :after doc1, 3d
    Add gantt diagram to demo page      :20h
    Add another diagram to demo page    :48h
```

## 用例图

```{mermaid}
usecaseDiagram
    title My Use Case Diagram
    [System] (system)
    (system) -- "1" : is used by --> (Actor1: Customer)
    (system) -- "2" : is used by --> (Actor2: Employee)
```

## 饼图

```{mermaid}
pie showData
    title Key elements in Product X
    "Calcium" : 42.96
    "Potassium" : 50.05
    "Magnesium" : 10.01
    "Iron" :  5
```

## Git Graph

```{mermaid}
gitGraph:
    commit "Ashish"
    branch newbranch
    checkout newbranch
    commit id:"1111"
    commit tag:"test"
    checkout main
    commit type: HIGHLIGHT
    commit
    merge newbranch
    commit
    branch b2
    commit
```

## 思维导图

```{mermaid}
mindmap
  root((mindmap))
    Origins
      Long history
      ::icon(fa fa-book)
      Popularisation
        British popular psychology author Tony Buzan
    Research
      On effectiveness<br/>and features
      On Automatic creation
        Uses
            Creative techniques
            Strategic planning
            Argument mapping
    Tools
      Pen and paper
      Mermaid
```

## 坐标轴

```{mermaid}
xychart-beta
    title "Sales Revenue"
    x-axis [jan, feb, mar, apr, may, jun, jul, aug, sep, oct, nov, dec]
    y-axis "Revenue (in $)" 4000 --> 11000
    bar [5000, 6000, 7500, 8200, 9500, 10500, 11000, 10200, 9200, 8500, 7000, 6000]
    line [5000, 6000, 7500, 8200, 9500, 10500, 11000, 10200, 9200, 8500, 7000, 6000]
```

## 块状图

```{mermaid}
block-beta
  columns 3
  a:3
  block:group1:2
    columns 2
    h i j k
  end
  g
  block:group2:3
    %% columns auto (default)
    l m n o p q r
  end
```
