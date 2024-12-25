# PlantUML

本文仅提供一些基本图形的绘制方法，更多内容参考 [PlantUML.pdf](https://gitee.com/zhyantao/pdf/raw/master/uml/plantuml.pdf)

## 时序图

```{uml}
@startuml
Alice -> Bob: 认证请求

alt 成功情况

    Bob -> Alice: 认证接受

else 某种失败情况

    Bob -> Alice: 认证失败
    group 我自己的标签
        Alice -> Log : 开始记录攻击日志
        loop 1000次
            Alice -> Bob: DNS 攻击
        end
        Alice -> Log : 结束记录攻击日志
    end

else 另一种失败

    Bob -> Alice: 请重复

end
@enduml
```

````{dropdown} 源代码
```bash
@startuml
Alice -> Bob: 认证请求

alt 成功情况

    Bob -> Alice: 认证接受

else 某种失败情况

    Bob -> Alice: 认证失败
    group 我自己的标签
        Alice -> Log : 开始记录攻击日志
        loop 1000次
            Alice -> Bob: DNS 攻击
        end
        Alice -> Log : 结束记录攻击日志
    end

else 另一种失败

    Bob -> Alice: 请重复

end
@enduml
```
````

## 用例图

```{uml}
@startuml
left to right direction
skinparam packageStyle rectangle
actor customer
actor clerk
rectangle checkout {
    customer -- (checkout)
    (checkout) .> (payment) : include
    (help) .> (checkout) : extends
    (checkout) -- clerk
}
@enduml
```

````{dropdown} 源代码
```bash
@startuml
left to right direction
skinparam packageStyle rectangle
actor customer
actor clerk
rectangle checkout {
    customer -- (checkout)
    (checkout) .> (payment) : include
    (help) .> (checkout) : extends
    (checkout) -- clerk
}
@enduml
```
````

## 类图

```{uml}
@startuml
class 汽车

发动机 - 汽车 : 驱动 >
汽车 *- 轮子 : 拥有 4 >
汽车 -- 人 : < 所属

@enduml
```

````{dropdown} 源代码
```bash
@startuml
class 汽车

发动机 - 汽车 : 驱动 >
汽车 *- 轮子 : 拥有 4 >
汽车 -- 人 : < 所属

@enduml
```
````

## 活动图

```{uml}
@startuml

start
:ClickServlet.handleRequest();
:new page;
if (Page.onSecurityCheck) then (true)
    :Page.onInit();
    if (isForward?) then (no)
        :Process controls;
        if (continue processing?) then (no)
            stop
        endif

        if (isPost?) then (yes)
            :Page.onPost();
        else (no)
            :Page.onGet();
        endif
        :Page.onRender();
    endif
else (false)
endif

if (do redirect?) then (yes)
    :redirect process;
else
    if (do forward?) then (yes)
        :Forward request;
    else (no)
        :Render page template;
    endif
endif

stop

@enduml
```

````{dropdown} 源代码
```bash
@startuml

start
:ClickServlet.handleRequest();
:new page;
if (Page.onSecurityCheck) then (true)
    :Page.onInit();
    if (isForward?) then (no)
        :Process controls;
        if (continue processing?) then (no)
            stop
        endif

        if (isPost?) then (yes)
            :Page.onPost();
        else (no)
            :Page.onGet();
        endif
        :Page.onRender();
    endif
else (false)
endif

if (do redirect?) then (yes)
    :redirect process;
else
    if (do forward?) then (yes)
        :Forward request;
    else (no)
        :Render page template;
    endif
endif

stop

@enduml
```
````

## 组件图

```{uml}
@startuml

package "Some Group" {
    HTTP - [First Component]
    [Another Component]
}

node "Other Groups" {
    FTP - [Second Component]
    [First Component] --> FTP
}

cloud {
    [Example 1]
}


database "MySql" {
    folder "This is my folder" {
        [Folder 3]
    }
    frame "Foo" {
        [Frame 4]
    }
}


[Another Component] --> [Example 1]
[Example 1] --> [Folder 3]
[Folder 3] --> [Frame 4]

@enduml
```

````{dropdown} 源代码
```bash
@startuml

package "Some Group" {
    HTTP - [First Component]
    [Another Component]
}

node "Other Groups" {
    FTP - [Second Component]
    [First Component] --> FTP
}

cloud {
    [Example 1]
}


database "MySql" {
    folder "This is my folder" {
        [Folder 3]
    }
    frame "Foo" {
        [Frame 4]
    }
}


[Another Component] --> [Example 1]
[Example 1] --> [Folder 3]
[Folder 3] --> [Frame 4]

@enduml
```
````

## 状态图

```{uml}
@startuml
state start1  <<start>>
state choice1 <<choice>>
state fork1   <<fork>>
state join2   <<join>>
state end3    <<end>>

[*]     --> choice1 : from start\nto choice
start1  --> choice1 : from start stereo\nto choice

choice1 --> fork1   : from choice\nto fork
choice1 --> join2   : from choice\nto join
choice1 --> end3    : from choice\nto end stereo

fork1   ---> State1 : from fork\nto state
fork1   --> State2  : from fork\nto state

State2  --> join2   : from state\nto join
State1  --> [*]     : from state\nto end

join2   --> [*]     : from join\nto end
@enduml
```

````{dropdown} 源代码
```bash
@startuml
state start1  <<start>>
state choice1 <<choice>>
state fork1   <<fork>>
state join2   <<join>>
state end3    <<end>>

[*]     --> choice1 : from start\nto choice
start1  --> choice1 : from start stereo\nto choice

choice1 --> fork1   : from choice\nto fork
choice1 --> join2   : from choice\nto join
choice1 --> end3    : from choice\nto end stereo

fork1   ---> State1 : from fork\nto state
fork1   --> State2  : from fork\nto state

State2  --> join2   : from state\nto join
State1  --> [*]     : from state\nto end

join2   --> [*]     : from join\nto end
@enduml
```
````

## 对象图

```{uml}
@startuml PERT
left to right direction
' Horizontal lines: -->, <--, <-->
' Vertical lines: ->, <-, <->
title PERT: Project Name

map Kick.Off {
}
map task.1 {
    Start => End
}
map task.2 {
    Start => End
}
map task.3 {
    Start => End
}
map task.4 {
    Start => End
}
map task.5 {
    Start => End
}
Kick.Off --> task.1 : Label 1
Kick.Off --> task.2 : Label 2
Kick.Off --> task.3 : Label 3
task.1 --> task.4
task.2 --> task.4
task.3 --> task.4
task.4 --> task.5 : Label 4
@enduml
```

````{dropdown} 源代码
```bash
@startuml PERT
left to right direction
' Horizontal lines: -->, <--, <-->
' Vertical lines: ->, <-, <->
title PERT: Project Name

map Kick.Off {
}
map task.1 {
    Start => End
}
map task.2 {
    Start => End
}
map task.3 {
    Start => End
}
map task.4 {
    Start => End
}
map task.5 {
    Start => End
}
Kick.Off --> task.1 : Label 1
Kick.Off --> task.2 : Label 2
Kick.Off --> task.3 : Label 3
task.1 --> task.4
task.2 --> task.4
task.3 --> task.4
task.4 --> task.5 : Label 4
@enduml
```
````

## 部署图

```{uml}
@startuml
[i]
node node {
    portin p1
    portin p2
    portin p3
    portout po1
    portout po2
    portout po3
    file f1
}
[o]

i --> p1
i --> p2
i --> p3
p1 --> f1
p2 --> f1
po1 --> o
po2 --> o
po3 --> o
f1 --> po1
@enduml
```

````{dropdown} 源代码
```bash
@startuml
[i]
node node {
    portin p1
    portin p2
    portin p3
    portout po1
    portout po2
    portout po3
    file f1
}
[o]

i --> p1
i --> p2
i --> p3
p1 --> f1
p2 --> f1
po1 --> o
po2 --> o
po3 --> o
f1 --> po1
@enduml
```
````

## 定时图

```{uml}
@startuml
concise "Client" as Client
concise "Server" as Server
concise "Response freshness" as Cache

Server is idle
Client is idle

@Client
0 is send
Client -> Server@+25 : GET
+25 is await
+75 is recv
+25 is idle
+25 is send
Client -> Server@+25 : GET\nIf-Modified-Since: 150
+25 is await
+50 is recv
+25 is idle
@100 <-> @275 : no need to re-request from server

@Server
25 is recv
+25 is work
+25 is send
Server -> Client@+25 : 200 OK\nExpires: 275
+25 is idle
+75 is recv
+25 is send
Server -> Client@+25 : 304 Not Modified
+25 is idle

@Cache
75 is fresh
+200 is stale
@enduml
```

````{dropdown} 源代码
```bash
@startuml
concise "Client" as Client
concise "Server" as Server
concise "Response freshness" as Cache

Server is idle
Client is idle

@Client
0 is send
Client -> Server@+25 : GET
+25 is await
+75 is recv
+25 is idle
+25 is send
Client -> Server@+25 : GET\nIf-Modified-Since: 150
+25 is await
+50 is recv
+25 is idle
@100 <-> @275 : no need to re-request from server

@Server
25 is recv
+25 is work
+25 is send
Server -> Client@+25 : 200 OK\nExpires: 275
+25 is idle
+75 is recv
+25 is send
Server -> Client@+25 : 304 Not Modified
+25 is idle

@Cache
75 is fresh
+200 is stale
@enduml
```
````

## 架构图

```{uml}
@startuml
skinparam rectangle<<behavior>> {
    roundCorner 25
}
sprite $bProcess jar:archimate/business-process
sprite $aService jar:archimate/application-service
sprite $aComponent jar:archimate/application-component

rectangle "Handle claim"  as HC <<$bProcess>><<behavior>> #Business
rectangle "Capture Information"  as CI <<$bProcess>><<behavior>> #Business
rectangle "Notify\nAdditional Stakeholders" as NAS <<$bProcess>><<behavior>> #Business
rectangle "Validate" as V <<$bProcess>><<behavior>> #Business
rectangle "Investigate" as I <<$bProcess>><<behavior>> #Business
rectangle "Pay" as P <<$bProcess>><<behavior>> #Business

HC *-down- CI
HC *-down- NAS
HC *-down- V
HC *-down- I
HC *-down- P

CI -right->> NAS
NAS -right->> V
V -right->> I
I -right->> P

rectangle "Scanning" as scanning <<$aService>><<behavior>> #Application
rectangle "Customer admnistration" as customerAdministration <<$aService>><<behavior>> #Application
rectangle "Claims admnistration" as claimsAdministration <<$aService>><<behavior>> #Application
rectangle Printing <<$aService>><<behavior>> #Application
rectangle Payment <<$aService>><<behavior>> #Application

scanning -up-> CI
customerAdministration  -up-> CI
claimsAdministration -up-> NAS
claimsAdministration -up-> V
claimsAdministration -up-> I
Payment -up-> P

Printing -up-> V
Printing -up-> P

rectangle "Document\nManagement\nSystem" as DMS <<$aComponent>> #Application
rectangle "General\nCRM\nSystem" as CRM <<$aComponent>>  #Application
rectangle "Home & Away\nPolicy\nAdministration" as HAPA <<$aComponent>> #Application
rectangle "Home & Away\nFinancial\nAdministration" as HFPA <<$aComponent>>  #Application

DMS .up.|> scanning
DMS .up.|> Printing
CRM .up.|> customerAdministration
HAPA .up.|> claimsAdministration
HFPA .up.|> Payment

legend left
Example from the "Archisurance case study" (OpenGroup).
See
====
<$bProcess> :business process
====
<$aService> : application service
====
<$aComponent> : application component
endlegend
@enduml
```

````{dropdown} 源代码
```bash
@startuml
skinparam rectangle<<behavior>> {
    roundCorner 25
}
sprite $bProcess jar:archimate/business-process
sprite $aService jar:archimate/application-service
sprite $aComponent jar:archimate/application-component

rectangle "Handle claim"  as HC <<$bProcess>><<behavior>> #Business
rectangle "Capture Information"  as CI <<$bProcess>><<behavior>> #Business
rectangle "Notify\nAdditional Stakeholders" as NAS <<$bProcess>><<behavior>> #Business
rectangle "Validate" as V <<$bProcess>><<behavior>> #Business
rectangle "Investigate" as I <<$bProcess>><<behavior>> #Business
rectangle "Pay" as P <<$bProcess>><<behavior>> #Business

HC *-down- CI
HC *-down- NAS
HC *-down- V
HC *-down- I
HC *-down- P

CI -right->> NAS
NAS -right->> V
V -right->> I
I -right->> P

rectangle "Scanning" as scanning <<$aService>><<behavior>> #Application
rectangle "Customer admnistration" as customerAdministration <<$aService>><<behavior>> #Application
rectangle "Claims admnistration" as claimsAdministration <<$aService>><<behavior>> #Application
rectangle Printing <<$aService>><<behavior>> #Application
rectangle Payment <<$aService>><<behavior>> #Application

scanning -up-> CI
customerAdministration  -up-> CI
claimsAdministration -up-> NAS
claimsAdministration -up-> V
claimsAdministration -up-> I
Payment -up-> P

Printing -up-> V
Printing -up-> P

rectangle "Document\nManagement\nSystem" as DMS <<$aComponent>> #Application
rectangle "General\nCRM\nSystem" as CRM <<$aComponent>>  #Application
rectangle "Home & Away\nPolicy\nAdministration" as HAPA <<$aComponent>> #Application
rectangle "Home & Away\nFinancial\nAdministration" as HFPA <<$aComponent>>  #Application

DMS .up.|> scanning
DMS .up.|> Printing
CRM .up.|> customerAdministration
HAPA .up.|> claimsAdministration
HFPA .up.|> Payment

legend left
Example from the "Archisurance case study" (OpenGroup).
See
====
<$bProcess> :business process
====
<$aService> : application service
====
<$aComponent> : application component
endlegend
@enduml
```
````

## 甘特图

```{uml}
@startgantt
[Prototype design] requires 15 days
[Test prototype] requires 10 days
-- All example --
[Task 1 (1 day)] requires 1 day
[T2 (5 days)] requires 5 days
[T3 (1 week)] requires 1 week
[T4 (1 week and 4 days)] requires 1 week and 4 days
[T5 (2 weeks)] requires 2 weeks
@endgantt
```

````{dropdown} 源代码
```bash
@startgantt
[Prototype design] requires 15 days
[Test prototype] requires 10 days
-- All example --
[Task 1 (1 day)] requires 1 day
[T2 (5 days)] requires 5 days
[T3 (1 week)] requires 1 week
[T4 (1 week and 4 days)] requires 1 week and 4 days
[T5 (2 weeks)] requires 2 weeks
@endgantt
```
````

## 坐标图

```{uml}
@startchronology
title Chronology Diagram
[A: 2024-01-15 01:08:12] happens on 2024-01-15 01:08:12
[B] happens on 2024-01-15 13:08:12
[C] happens on 2024-01-15 22:12:08
@endchronology
```

````{dropdown} 源代码
```bash
@startchronology
title Chronology Diagram
[A: 2024-01-15 01:08:12] happens on 2024-01-15 01:08:12
[B] happens on 2024-01-15 13:08:12
[C] happens on 2024-01-15 22:12:08
@endchronology
```
````

## 思维导图

```{uml}
@startmindmap
* root node
    * some first level node
        * second level node
        * another second level node
    * another first level node
@endmindmap
```

````{dropdown} 源代码
```bash
@startmindmap
* root node
    * some first level node
        * second level node
        * another second level node
    * another first level node
@endmindmap
```
````

## 组织架构图

```{uml}
@startwbs
* Business Process Modelling WBS
** Launch the project
*** Complete Stakeholder Research
*** Initial Implementation Plan
** Design phase
*** Model of AsIs Processes Completed
**** Model of AsIs Processes Completed1
**** Model of AsIs Processes Completed2
*** Measure AsIs performance metrics
*** Identify Quick Wins
** Complete innovate phase
@endwbs
```

````{dropdown} 源代码
```bash
@startwbs
* Business Process Modelling WBS
** Launch the project
*** Complete Stakeholder Research
*** Initial Implementation Plan
** Design phase
*** Model of AsIs Processes Completed
**** Model of AsIs Processes Completed1
**** Model of AsIs Processes Completed2
*** Measure AsIs performance metrics
*** Identify Quick Wins
** Complete innovate phase
@endwbs
```
````

## JSON

```{uml}
@startjson
#highlight "lastName"
#highlight "address" / "city"
#highlight "phoneNumbers" / "0" / "number"
{
    "firstName": "John",
    "lastName": "Smith",
    "isAlive": true,
    "age": 28,
    "address": {
        "streetAddress": "21 2nd Street",
        "city": "New York",
        "state": "NY",
        "postalCode": "10021-3100"
    }
    ,
    "phoneNumbers": [
    {
        "type": "home",
        "number": "212 555-1234"
    }
    ,
    {
        "type": "office",
        "number": "646 555-4567"
    }
    ],
    "children": [],
    "spouse": null
}
@endjson
```

````{dropdown} 源代码
```bash
@startjson
#highlight "lastName"
#highlight "address" / "city"
#highlight "phoneNumbers" / "0" / "number"
{
    "firstName": "John",
    "lastName": "Smith",
    "isAlive": true,
    "age": 28,
    "address": {
        "streetAddress": "21 2nd Street",
        "city": "New York",
        "state": "NY",
        "postalCode": "10021-3100"
    }
    ,
    "phoneNumbers": [
    {
        "type": "home",
        "number": "212 555-1234"
    }
    ,
    {
        "type": "office",
        "number": "646 555-4567"
    }
    ],
    "children": [],
    "spouse": null
}
@endjson
```
````

## YAML

```{uml}
@startyaml
#highlight "french-hens"
#highlight "xmas-fifth-day" / "partridges"

doe: "a deer, a female deer"
ray: "a drop of golden sun"
pi: 3.14159
xmas: true
french-hens: 3
calling-birds:
- huey
- dewey
- louie
- fred
xmas-fifth-day:
calling-birds: four
french-hens: 3
golden-rings: 5
partridges:
count: 1
location: "a pear tree"
turtle-doves: two
@endyaml
```

````{dropdown} 源代码
```bash
@startyaml
#highlight "french-hens"
#highlight "xmas-fifth-day" / "partridges"

doe: "a deer, a female deer"
ray: "a drop of golden sun"
pi: 3.14159
xmas: true
french-hens: 3
calling-birds:
- huey
- dewey
- louie
- fred
xmas-fifth-day:
calling-birds: four
french-hens: 3
golden-rings: 5
partridges:
count: 1
location: "a pear tree"
turtle-doves: two
@endyaml
```
````

## EBNF

```{uml}
@startebnf
title All EBNF elements managed by PlantUML

(* Nodes *)
litteral = "a";
special = ? a ?;
rule = a;

(* Edges *)
required = a;
optional = [a];

zero_or_more = {a};
one_or_more = a, {a};
one_or_more_ebnf = {a}-;

zero_or_more_with_separator = [a, {',', a}];
one_or_more_with_separator = a, {',', a};
zero_or_more_with_terminator = {a, ','};
one_or_more_with_terminator = a, ',', {a, ','};
one_or_more_with_terminator_ebnf = {a, ','}-;

alternative = a | b;
group = (a | b) , c;
without_group = a | b , c;
@endebnf
```

````{dropdown} 源代码
```bash
@startebnf
title All EBNF elements managed by PlantUML

(* Nodes *)
litteral = "a";
special = ? a ?;
rule = a;

(* Edges *)
required = a;
optional = [a];

zero_or_more = {a};
one_or_more = a, {a};
one_or_more_ebnf = {a}-;

zero_or_more_with_separator = [a, {',', a}];
one_or_more_with_separator = a, {',', a};
zero_or_more_with_terminator = {a, ','};
one_or_more_with_terminator = a, ',', {a, ','};
one_or_more_with_terminator_ebnf = {a, ','}-;

alternative = a | b;
group = (a | b) , c;
without_group = a | b , c;
@endebnf
```
````

## Regex

```{uml}
@startregex
title repetitionEquivalance
a{0,1}b{1,} is the same as a?b+
@endregex
```

````{dropdown} 源代码
```bash
@startregex
title repetitionEquivalance
a{0,1}b{1,} is the same as a?b+
@endregex
```
````

## nwdiag

```{uml}
@startuml
nwdiag {
    network dmz {
        address = "210.x.x.x/24"

        web01 [address = "210.x.x.1"];
        web02 [address = "210.x.x.2"];
    }
    network internal {
        address = "172.x.x.x/24";

        web01 [address = "172.x.x.1"];
        web02 [address = "172.x.x.2"];
        db01;
        db02;
    }
}
@enduml
```

````{dropdown} 源代码
```bash
@startuml
nwdiag {
    network dmz {
        address = "210.x.x.x/24"

        web01 [address = "210.x.x.1"];
        web02 [address = "210.x.x.2"];
    }
    network internal {
        address = "172.x.x.x/24";

        web01 [address = "172.x.x.1"];
        web02 [address = "172.x.x.2"];
        db01;
        db02;
    }
}
@enduml
```
````

## JLaTeXMath

```{uml}
@startuml
Bob -> Alice : Can you solve: <math>ax^2+bx+c=0</math>
Alice --> Bob: <math>x = (-b+-sqrt(b^2-4ac))/(2a)</math>
@enduml
```

````{dropdown} 源代码
```bash
@startuml
Bob -> Alice : Can you solve: <math>ax^2+bx+c=0</math>
Alice --> Bob: <math>x = (-b+-sqrt(b^2-4ac))/(2a)</math>
@enduml
```
````

## ER 图

```{uml}
@startchen movies
<style>
.red {
    BackGroundColor Red
    FontColor White
}
.blue {
    BackGroundColor Blue
    FontColor White
}
</style>

entity "Director" as DIRECTOR {
    "No." as Number <<key>>
    Name {
        Fname
        Lname
    }
    Born : DATE
    Died<<red>>
    Age<<blue>>
}

entity "Customer" as CUSTOMER {
    Number <<key>>
    Bonus <<derived>>
    Name <<multi>>
}

entity "Movie" as MOVIE {
    Code
}

relationship "was-rented-to" as RENTED_TO {
    Date
}

RENTED_TO -1- CUSTOMER
RENTED_TO -N- MOVIE
RENTED_TO -(N,M)- DIRECTOR

entity "Parent" as PARENT {
}

entity "Member" as MEMBER {
}

CUSTOMER ->- PARENT
MEMBER -<- CUSTOMER

entity "Kid" as CHILD <<weak>> {
    Name <<key>>
}

relationship "is-parent-of" as PARENT_OF <<identifying>> {
}

PARENT_OF -1- PARENT
PARENT_OF =N= CHILD

entity "Little Kid" as TODDLER {
    FavoriteToy
}

entity "Primary-Aged Kid" as PRIMARY_AGE {
    FavoriteColor
}

entity "Teenager" as TEEN {
    Hobby
}

CHILD =>= d { TODDLER, PRIMARY_AGE, TEEN }

entity "Human" as PERSON {
}

PERSON ->- U { CUSTOMER, DIRECTOR }
@endchen
```

````{dropdown} 源代码
```bash
@startchen movies
<style>
.red {
    BackGroundColor Red
    FontColor White
}
.blue {
    BackGroundColor Blue
    FontColor White
}
</style>

entity "Director" as DIRECTOR {
    "No." as Number <<key>>
    Name {
        Fname
        Lname
    }
    Born : DATE
    Died<<red>>
    Age<<blue>>
}

entity "Customer" as CUSTOMER {
    Number <<key>>
    Bonus <<derived>>
    Name <<multi>>
}

entity "Movie" as MOVIE {
    Code
}

relationship "was-rented-to" as RENTED_TO {
    Date
}

RENTED_TO -1- CUSTOMER
RENTED_TO -N- MOVIE
RENTED_TO -(N,M)- DIRECTOR

entity "Parent" as PARENT {
}

entity "Member" as MEMBER {
}

CUSTOMER ->- PARENT
MEMBER -<- CUSTOMER

entity "Kid" as CHILD <<weak>> {
    Name <<key>>
}

relationship "is-parent-of" as PARENT_OF <<identifying>> {
}

PARENT_OF -1- PARENT
PARENT_OF =N= CHILD

entity "Little Kid" as TODDLER {
    FavoriteToy
}

entity "Primary-Aged Kid" as PRIMARY_AGE {
    FavoriteColor
}

entity "Teenager" as TEEN {
    Hobby
}

CHILD =>= d { TODDLER, PRIMARY_AGE, TEEN }

entity "Human" as PERSON {
}

PERSON ->- U { CUSTOMER, DIRECTOR }
@endchen
```
````

## 箭头样式

```{uml}
@startuml
participant Alice as a
participant Bob   as b
a ->     b : ""->   ""
a ->>    b : ""->>  ""
a -\     b : ""-\   ""
a -\\    b : ""-\\\\""
a -/     b : ""-/   ""
a -//    b : ""-//  ""
a ->x    b : ""->x  ""
a x->    b : ""x->  ""
a o->    b : ""o->  ""
a ->o    b : ""->o  ""
a o->o   b : ""o->o ""
a <->    b : ""<->  ""
a o<->o  b : ""o<->o""
a x<->x  b : ""x<->x""
a ->>o   b : ""->>o ""
a -\o    b : ""-\o  ""
a -\\o   b : ""-\\\\o""
a -/o    b : ""-/o  ""
a -//o   b : ""-//o ""
a x->o   b : ""x->o ""
@enduml
```

````{dropdown} 源代码
```bash
@startuml
participant Alice as a
participant Bob   as b
a ->     b : ""->   ""
a ->>    b : ""->>  ""
a -\     b : ""-\   ""
a -\\    b : ""-\\\\""
a -/     b : ""-/   ""
a -//    b : ""-//  ""
a ->x    b : ""->x  ""
a x->    b : ""x->  ""
a o->    b : ""o->  ""
a ->o    b : ""->o  ""
a o->o   b : ""o->o ""
a <->    b : ""<->  ""
a o<->o  b : ""o<->o""
a x<->x  b : ""x<->x""
a ->>o   b : ""->>o ""
a -\o    b : ""-\o  ""
a -\\o   b : ""-\\\\o""
a -/o    b : ""-/o  ""
a -//o   b : ""-//o ""
a x->o   b : ""x->o ""
@enduml
```
````

## 箭头颜色

```{uml}
@startuml
Bob -[#red]> Alice : hello
Alice -[#0000FF]->Bob : ok
@enduml
```

````{dropdown} 源代码
```bash
@startuml
Bob -[#red]> Alice : hello
Alice -[#0000FF]->Bob : ok
@enduml
```
````

## 填充色

```{uml}
@startuml
agent a
cloud c #pink;line:red;line.bold;text:red [
c
cloud description
]
file  f #palegreen;line:green;line.dashed;text:green {
    [c1]
    [c2]
}
frame frame {
    node  n #aliceblue;line:blue;line.dotted;text:blue
}
@enduml
```

````{dropdown} 源代码
```bash
@startuml
agent a
cloud c #pink;line:red;line.bold;text:red [
c
cloud description
]
file  f #palegreen;line:green;line.dashed;text:green {
    [c1]
    [c2]
}
frame frame {
    node  n #aliceblue;line:blue;line.dotted;text:blue
}
@enduml
```
````

## ArchiMate

```{uml}
@startuml
listsprite
@enduml
```

````{dropdown} 源代码
```bash
@startuml
listsprite
@enduml
```
````

## Intersections

```{uml}
@startuml
!include <edgy/edgy>

$experienceFacet(Experience, experience)
$architectureFacet(Architecture, architecture)
$identityFacet(Identity, identity)

$organisationFacet(Organisation, org) {
    $organisation(Organisation, organisation)
}

$brandFacet(Brand) {
    $brand(Brand, brand)
}

$productFacet(Product){
    $product(Product, product)
}

$flow(brand, identity, "represents/evokes")
$flow(brand, experience, "Supports/appears in")

$flowLeft(organisation, identity, "pursues/authors")
$flowRight(organisation, architecture, "has/performs")

$flow(product, experience, "serves/features in")
$linkUp(product, architecture, "requires/creates")

$flow(organisation, brand, "builds")
$flow(organisation, product, "makes")
$flowLeft(product, brand, "embodies")

@enduml
```

````{dropdown} 源代码
```bash
@startuml
!include <edgy/edgy>

$experienceFacet(Experience, experience)
$architectureFacet(Architecture, architecture)
$identityFacet(Identity, identity)

$organisationFacet(Organisation, org) {
    $organisation(Organisation, organisation)
}

$brandFacet(Brand) {
    $brand(Brand, brand)
}

$productFacet(Product){
    $product(Product, product)
}

$flow(brand, identity, "represents/evokes")
$flow(brand, experience, "Supports/appears in")

$flowLeft(organisation, identity, "pursues/authors")
$flowRight(organisation, architecture, "has/performs")

$flow(product, experience, "serves/features in")
$linkUp(product, architecture, "requires/creates")

$flow(organisation, brand, "builds")
$flow(organisation, product, "makes")
$flowLeft(product, brand, "embodies")

@enduml
```
````
