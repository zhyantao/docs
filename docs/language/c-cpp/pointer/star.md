# 指针

## 二级指针

```cpp
#include <iostream>

using namespace std;

int main()
{
    int num = 10;
    int *p = &num;
    int **pp = &p;
    *(*pp) = 20;

    cout << "num = " << num << endl;

    return 0;
}
```

## 指向数组的指针

```cpp
#include <iostream>

using namespace std;

struct Student
{
    char name[4];
    int born;
    bool male;
};

int main()
{
    // Part One
    Student students[128];
    Student *p0 = &students[0];
    Student *p1 = &students[1];
    Student *p2 = &students[2];
    Student *p3 = &students[3];

    printf("p0 = %p\n", p0);
    printf("p1 = %p\n", p1);
    printf("p2 = %p\n", p2);
    printf("p3 = %p\n", p3);

    // the same behavior
    students[1].born = 2000;
    p1->born = 2000;

    // Part Two
    printf("&students = %p\n", &students);
    printf("students = %p\n", students);
    printf("&students[0] = %p\n", &students[0]);

    Student *p = students;
    p[0].born = 2000;
    p[1].born = 2001;
    p[2].born = 2002;

    printf("students[0].born = %d\n", students[0].born);
    printf("students[1].born = %d\n", students[1].born);
    printf("students[2].born = %d\n", students[2].born);

    return 0;
}
```

## 指向结构体的指针

```cpp
#include <iostream>
#include <cstring>

using namespace std;

struct Student
{
    char name[4];
    int born;
    bool male;
};

int main()
{
    Student stu = {"Yu", 2000, true};
    Student *pStu = &stu;

    cout << stu.name << " was born in " << stu.born
         << ". Gender: " << (stu.male ? "male" : "female") << endl;

    strncpy(pStu->name, "Li", 4);
    pStu->born = 2001;
    (*pStu).born = 2002;
    pStu->male = false;

    cout << stu.name << " was born in " << stu.born
         << ". Gender: " << (stu.male ? "male" : "female") << endl;

    printf("Address of stu: %p\n", pStu);       // C style
    cout << "Address of stu: " << pStu << endl; // C++ style
    cout << "Address of stu: " << &stu << endl;
    cout << "Address of member name: " << &(pStu->name) << endl;
    cout << "Address of member born: " << &(pStu->born) << endl;
    cout << "Address of member male: " << &(pStu->male) << endl;

    cout << "sizeof(pStu) = " << sizeof(pStu) << endl;

    return 0;
}
```

## const 指针

```cpp
#include <iostream>

using namespace std;

int foo(const char *p)
{
    // the value that p points to cannot be changed
    // play a trick?
    char *p2 = p; // syntax error
    //...
    return 0;
}

int main()
{
    int num = 1;
    int another = 2;

    // You cannot change the value that p1 points to through p1
    const int *p1 = &num;
    *p1 = 3; // error
    num = 3; // okay

    // You cannot change value of p2 (address)
    int *const p2 = &num;
    *p2 = 3;       // okay
    p2 = &another; // error

    // You can change neither
    const int *const p3 = &num;
    *p3 = 3;       // error
    p3 = &another; // error

    return 0;
}
```

## 指向函数的指针

```cpp
#include <iostream>
#include <cmath>

using namespace std;

float norm_l1(float x, float y);     // declaration
float norm_l2(float x, float y);     // declaration
float (*norm_ptr)(float x, float y); // norm_ptr is a function pointer

int main()
{
    norm_ptr = norm_l1; // Pointer norm_ptr is pointing to norm_l1
    cout << "L1 norm of (-3, 4) = " << norm_ptr(-3.0f, 4.0f) << endl;

    norm_ptr = &norm_l2; // Pointer norm_ptr is pointing to norm_l2
    cout << "L2 norm of (-3, 4) = " << (*norm_ptr)(-3.0f, 4.0f) << endl;

    return 0;
}

float norm_l1(float x, float y)
{
    return fabs(x) + fabs(y);
}

float norm_l2(float x, float y)
{
    return sqrt(x * x + y * y);
}
```
