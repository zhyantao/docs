# template

## 函数模板-显式特例化

```cpp
#include <iostream>
#include <typeinfo>

using namespace std;

template <typename T>
T sum(T x, T y)
{
    cout << "The input type is " << typeid(T).name() << endl;
    return x +
           y;
}
// Explicitly instantiate
template double sum<double>(double, double);

int main()
{
    auto val = sum(4.1, 5.2);
    cout << val << endl;
    return 0;
}
```

## 函数模板-隐式特例化

```cpp
#include <iostream>
#include <typeinfo>

using namespace std;

template <typename T>
T sum(T x, T y)
{
    cout << "The input type is " << typeid(T).name() << endl;
    return x + y;
}

int main()
{
    // Implicitly instantiates product<int>(int, int)
    cout << "sum = " << sum<int>(2.2f, 3.0f) << endl;
    // Implicitly instantiates product<float>(float, float)
    cout << "sum = " << sum(2.2f, 3.0f) << endl;

    return 0;
}
```

## 特例化函数

```cpp
#include <iostream>
#include <typeinfo>

using namespace std;

template <typename T>
T sum(T x, T y)
{
    cout << "The input type is " << typeid(T).name() << endl;
    return x + y;
}

struct Point
{
    int x;
    int y;
};

// Specialization for Point + Point operation
template <>
Point sum<Point>(Point pt1, Point pt2)
{
    cout << "The input type is " << typeid(pt1).name() << endl;
    Point pt;
    pt.x = pt1.x + pt2.x;
    pt.y = pt1.y + pt2.y;
    return pt;
}

int main()
{
    // Explicit instantiated functions
    cout << "sum = " << sum(1, 2) << endl;
    cout << "sum = " << sum(1.1, 2.2) << endl;

    Point pt1{1, 2};
    Point pt2{2, 3};
    Point pt = sum(pt1, pt2);
    cout << "pt = (" << pt.x << ", " << pt.y << ")" << endl;
    return 0;
}
```

## 特例化类

```cpp
#include <iostream>

using namespace std;

// Class Template
template <typename T>
class MyVector
{
    size_t length;
    T *data;

public:
    MyVector(size_t length) : length(length)
    {
        data = new T[length]{};
    }
    ~MyVector()
    {
        delete[] data;
    }
    MyVector(const MyVector &) = delete;
    MyVector &operator=(const MyVector &) = delete;
    T getElement(size_t index);
    bool setElement(size_t index, T value);
};

template <typename T>
T MyVector<T>::getElement(size_t index)
{
    if (index >= this->length)
    {
        cerr << "getElement(): Indices are out of range" << endl;
        return 0;
    }
    return data[index];
}

template <typename T>
bool MyVector<T>::setElement(size_t index, T value)
{
    if (index >= this->length)
    {
        cerr << "setElement(): Indices are out of range" << endl;
        return false;
    }

    data[index] = value;
    return true;
}

template class MyVector<int>; // Explicitly instantiate template Mat<int>

// class specialization
template <>
class MyVector<bool>
{
    size_t length;
    unsigned char *data;

public:
    MyVector(size_t length) : length(length)
    {
        int num_bytes = (length - 1) / 8 + 1;
        data = new unsigned char[num_bytes]{};
    }

    ~MyVector()
    {
        delete[] data;
    }

    MyVector(const MyVector &) = delete;
    MyVector &operator=(const MyVector &) = delete;
    bool getElement(size_t index);
    bool setElement(size_t index, bool value);
};

bool MyVector<bool>::getElement(size_t index)
{
    if (index >= this->length)
    {
        cerr << "getElement(): Indices are out of range" << endl;
        return 0;
    }
    size_t byte_id = index / 8;
    size_t bit_id = index % 8;
    unsigned char mask = (1 << bit_id);
    return bool(data[byte_id] & mask);
}

bool MyVector<bool>::setElement(size_t index, bool value)
{
    if (index >= this->length)
    {
        cerr << "setElement(): Indices are out of range" << endl;
        return false;
    }

    size_t byte_id = index / 8;
    size_t bit_id = index % 8;
    unsigned char mask = (1 << bit_id);

    if (value)
        data[byte_id] |= mask;
    else
        data[byte_id] &= ~mask;

    return true;
}

int main()
{
    MyVector<int> vec(16);
    vec.setElement(3, 256);
    cout << vec.getElement(3) << endl;

    MyVector<bool> boolvec(17);
    boolvec.setElement(15, false);
    boolvec.setElement(16, true);

    cout << boolvec.getElement(15) << endl;
    cout << boolvec.getElement(16) << endl;
    return 0;
}
```

## 类模板

```cpp
#include <iostream>

using namespace std;

// Class Template
template <typename T>
class Mat
{
    size_t rows;
    size_t cols;
    T *data;

public:
    Mat(size_t rows, size_t cols) : rows(rows), cols(cols)
    {
        data = new T[rows * cols]{};
    }

    ~Mat()
    {
        delete[] data;
    }

    Mat(const Mat &) = delete;
    Mat &operator=(const Mat &) = delete;
    T getElement(size_t r, size_t c);
    bool setElement(size_t r, size_t c, T value);
};

template <typename T>
T Mat<T>::getElement(size_t r, size_t c)
{
    if (r >= this->rows || c >= this->cols)
    {
        cerr << "getElement(): Indices are out of range" << endl;
        return 0;
    }
    return data[this->cols * r + c];
}

template <typename T>
bool Mat<T>::setElement(size_t r, size_t c, T value)
{
    if (r >= this->rows || c >= this->cols)
    {
        cerr << "setElement(): Indices are out of range" << endl;
        return false;
    }

    data[this->cols * r + c] = value;
    return true;
}

template class Mat<int>; // Explicitly instantiate template Mat<int>
// template Mat<float> and Mat<double> will be instantiate implicitly
int main()
{
    Mat<int> imat(3, 4);
    imat.setElement(1, 2, 256);
    Mat<float> fmat(2, 3);
    fmat.setElement(1, 2, 3.14159f);
    Mat<double> dmat(2, 3);
    dmat.setElement(1, 2, 2.718281828);

    // Mat<float> fmat2(fmat); //error

    // Mat<float> fmat3(2,3);
    // fmat3 = fmat; //error

    cout << imat.getElement(1, 2) << endl;
    cout << fmat.getElement(1, 2) << endl;
    cout << dmat.getElement(1, 2) << endl;

    return 0;
}
```

