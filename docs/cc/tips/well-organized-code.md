# 良好的编程风格

```cpp
// main.cpp

#include "matrix.h"
#include <stdio.h>

int main() {
    Matrix* matA = createMat(2, 3);
    Matrix* matB = createMat(2, 3);
    Matrix* matC = createMat(2, 3);
    Matrix* matD = createMat(3, 2);
    Matrix* matNULL = NULL;

    // initialization
    // You should have your own method to do it
    matA->data[3] = 2.3f;
    matB->data[3] = 3.1f;

    if (!add(matA, matB, matC))
        fprintf(stderr, "Matrix addition failed.");
    else {
        // You can have a better method to show the results
        printf("result=%f\n", matC->data[3]);
    }

    // more tests
    add(matA, matB, matD);

    add(matNULL, matB, matC);

    return 0;
}
```

```cpp
// matrix.h

#ifndef _MATRIX_H
#define _MATRIX_H

#include <stdbool.h> //for bool

// use typedef to simplify type name
typedef struct Matrix_ {
    size_t rows; // use size_t, not int
    size_t cols; // use size_t, not int
    float* data;
} Matrix;

Matrix* createMat(size_t rows, size_t cols);
bool releaseMat(Matrix* p);
bool add(const Matrix* input1, const Matrix* input2, Matrix* output);

#endif
```

```cpp
// matrix.c

#include "matrix.h"
#include <stdio.h>
#include <stdlib.h>

// return NULL if failed
Matrix* createMat(size_t rows, size_t cols) {
    Matrix* p = NULL;

    if (rows == 0 || cols == 0) {
        fprintf(stderr, "rows and/or cols is 0.\n");
        return NULL;
    }
    // allocate memory
    p = (Matrix*)malloc(sizeof(Matrix));
    if (p == NULL) {
        fprintf(stderr, "Failed to allocate memory for a matrix.\n");
        return NULL;
    }
    p->rows = rows;
    p->cols = cols;
    p->data = (float*)malloc(p->rows * p->cols * sizeof(float));

    if (p->data == NULL) {
        fprintf(stderr, "Failed to allocate memory for the matrix data.\n");
        free(p); // Don't forget to free memory here!
        return NULL;
    }

    return p;
}

bool releaseMat(Matrix* p) {
    // don't forget to check a pointer before using it
    if (!p) return false;

    if (p->data) free(p->data);

    free(p);

    return true;
}

bool add(const Matrix* input1, const Matrix* input2, Matrix* output) {
    // You much check all parameters carefully first
    // It's important, and can save a lot of time on debuging
    if (input1 == NULL) {
        // use stderr for error messages
        fprintf(stderr, "File %s, Line %d, Function %s(): The 1st parameter is NULL.\n",
                __FILE__, __LINE__, __FUNCTION__);
        return false;
    } else if (input1->data == NULL) {
        fprintf(stderr, "%s(): The 1st parameter has no valid data.\n", __FUNCTION__);
        return false;
    }

    if (input2 == NULL) {
        fprintf(stderr, "File %s, Line %d, Function %s(): The 2nd parameter is NULL.\n",
                __FILE__, __LINE__, __FUNCTION__);
        return false;
    } else if (input2->data == NULL) {
        fprintf(stderr, "%s(): The 2nd parameter has no valid data.\n", __FUNCTION__);
        return false;
    }

    if (output == NULL) {
        fprintf(stderr, "File %s, Line %d, Function %s(): The 3rd parameter is NULL.\n",
                __FILE__, __LINE__, __FUNCTION__);
        return false;
    } else if (output->data == NULL) {
        fprintf(stderr, "%s(): The 3rd parameter has no valid data.\n", __FUNCTION__);
        return false;
    }

    if (input1->rows != input2->rows || input2->rows != output->rows ||
        input1->cols != input2->cols || input2->cols != output->cols) {
        fprintf(stderr,
                "The input and the output do not match. They should have the same size.\n");
        fprintf(stderr, "Their sizes are (%zu, %zu), (%zu, %zu) and (%zu, %zu)\n",
                input1->rows, input1->cols, input2->rows, input2->cols, output->rows,
                output->cols);
        return false;
    }

    // version 1, the best one
    size_t length = input1->rows * input1->cols;
    const float* p1 = input1->data;
    const float* p2 = input2->data;
    float* p3 = output->data;
    for (size_t i = 0; i < length; i++) *(p3++) = *(p1++) + *(p2++);

    // version 2
    for (size_t r = 0; r < input1->rows; r++) {
        // to calculate (cols * r) here, don't put it into the inner loop
        const float* p1 = input1->data + input1->cols * r;
        const float* p2 = input2->data + input2->cols * r;
        float* p3 = output->data + +output->cols * r;

        for (size_t c = 0; c < input1->cols; c++) *(p3++) = *(p1++) + *(p2++);
    }

    // version 3, a bad one
    for (size_t r = 0; r < input1->rows; r++) {
        for (size_t c = 0; c < input1->cols; c++)
            output->data[output->cols * r + c] =
                input1->data[input1->cols * r + c] + input2->data[input2->cols * r + c];
    }

    return true;
}
```
