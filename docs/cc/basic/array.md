# array

## 一维数组

```cpp
#include <iostream>

using namespace std;

int main() {
    int num_array1[5];                   // uninitialized array, random values
    int num_array2[5] = {0, 1, 2, 3, 4}; // initialization

    for (int idx = 0; idx < 5; idx++) cout << num_array1[idx] << " ";
    cout << endl;

    for (int idx = 0; idx < 5; idx++) cout << num_array2[idx] << " ";
    cout << endl;

    return 0;
}
```

## 数值型二维数组

```cpp
#include <iostream>

using namespace std;

// You must tell the function the bound of an array, otherwise, elements cannot be accessed
// if the array is a variable-length one, it may be difficult to know the bound
void init_2d_array(float mat[][4], size_t rows, size_t cols) // error, arrays of unknown bound
{
    for (int r = 0; r < rows; r++)
        for (int c = 0; c < cols; c++) mat[r][c] = r * c;
}

int main() {
    int mat1[2][3] = {{11, 12, 13}, {14, 15, 16}};

    int rows = 5;
    int cols = 4;
    // float mat2[rows][cols]; // uninitialized array
    float mat2[rows][4]; // uninitialized array

    // init_2d_array(mat2, rows, cols);

    for (int r = 0; r < rows; r++)
        for (int c = 0; c < cols; c++) mat2[r][c] = r * c;

    for (int r = 0; r < rows; r++) {
        for (int c = 0; c < cols; c++) cout << mat2[r][c] << " ";
        cout << endl;
    }
    return 0;
}
```

## 字符串数组

```cpp
#include <stdio.h>

int main() {
    // 数组必须有第二个列数
    char city[][10] = {"Beijing", "Shenzhen", "Shanghai", "Guangzhou"};

    for (int i = 0; i < sizeof(city) / sizeof(city[0]); i++) { printf("%s\n", city[i]); }

    return 0;
}
```

## 变长数组

```cpp
#include <iostream>

using namespace std;

int main() {
    int num_array1[5] = {0, 1}; // fixed length array, initialized to {0,1,0,0,0}
    cout << "sizeof(num_array1) = " << sizeof(num_array1) << endl;

    int len = 0;
    while (len < 10) {
        int num_array2[len]; // variable-length array
        cout << "len = " << len;
        cout << ", sizeof(num_array2)) = " << sizeof(num_array2) << endl;
        len++;
    }
}
```

## 对象数组

```cpp
#include <cstring>
#include <iostream>

using namespace std;

class Student {
private:
    char* name;
    int born;
    bool male;

public:
    Student() {
        name = new char[1024]{0};
        born = 0;
        male = false;
        cout << "Constructor: Person()" << endl;
    }

    Student(const char* initName, int initBorn, bool isMale) {
        name = new char[1024];
        setName(initName);
        born = initBorn;
        male = isMale;
        cout << "Constructor: Person(const char, int , bool)" << endl;
    }

    ~Student() {
        cout << "To destroy object: " << name << endl;
        delete[] name;
    }

    void setName(const char* s) { strncpy(name, s, 1024); }

    void setBorn(int b) { born = b; }

    // the declarations, the definitions are out of the class
    void setGender(bool isMale);
    void printInfo();
};

void Student::setGender(bool isMale) {
    male = isMale;
}

void Student::printInfo() {
    std::cout << "Name: " << name << std::endl;
    std::cout << "Born in " << born << std::endl;
    std::cout << "Gender: " << (male ? "Male" : "Female") << std::endl;
}

int main() {
    Student* class1 = new Student[3]{
        {"Tom", 2000, true},
        {"Bob", 2001, true},
        {"Amy", 2002, false},
    };

    class1[1].printInfo();
    delete class1;
    // delete []class1;

    return 0;
}
```

## const 数组

```cpp
#include <iostream>

using namespace std;

// float array_sum(const float *values, size_t length)
// float array_sum(const float values[4], size_t length)
float array_sum(const float values[], size_t length) {
    float sum = 0.0f;
    for (int i = 0; i < length; i++) {
        sum += values[i];
        // values[i] = 0; //error
    }
    return sum;
}

int main() {
    // const float PI = 3.1415926f;
    // PI += 1.f; // error
    // const float values[4] = {1.1f, 2.2f, 3.3f, 4.4f};
    // values[0] = 1.0f; // error

    float values[4] = {1.1f, 2.2f, 3.3f, 4.4f};
    float sum = array_sum(values, 4);

    cout << "sum = " << sum << endl;
    return 0;
}
```

## 字符数组

```cpp
#include <cstring>
#include <iostream>

using namespace std;

int main() {
    char rabbit[16] = {'P', 'e', 't', 'e', 'r'};
    cout << "String length is " << strlen(rabbit) << endl;
    for (int i = 0; i < 16; i++)
        cout << i << ":" << +rabbit[i] << "(" << rabbit[i] << ")" << endl;

    char bad_pig[9] = {'P', 'e', 'p', 'p', 'a', ' ', 'P', 'i', 'g'};
    char good_pig[10] = {'P', 'e', 'p', 'p', 'a', ' ', 'P', 'i', 'g', '\0'};

    cout << "Rabbit is (" << rabbit << ")" << endl;
    cout << "Pig's bad name is (" << bad_pig << ")" << endl;
    cout << "Pig's good name is (" << good_pig << ")" << endl;

    char name[10] = {'Y', 'u', '\0', 'S', '.', '0'};
    cout << strlen(name) << endl;

    return 0;
}
```
