# AVX2 和 OpenMP

```cpp
// main.cpp

#include "matoperation.hpp"
#include <chrono>
#include <cstdlib>
#include <iostream>

using namespace std;

#define TIME_START start = std::chrono::steady_clock::now();
#define TIME_END(NAME)                                                                     \
    end = std::chrono::steady_clock::now();                                                \
    duration = std::chrono::duration_cast<std::chrono::milliseconds>(end - start).count(); \
    cout << (NAME) << ": result=" << result << ", duration = " << duration << "ms" << endl;

int main(int argc, char** argv) {
    size_t nSize = 200000000;
    float* p1 = new float[nSize](); // the memory is not aligned
    float* p2 = new float[nSize](); // the memory is not aligned

    // // 256bits aligned, C++17 standard
    // float * p1 = static_cast<float*>(aligned_alloc(256, nSize*sizeof(float)));
    // float * p2 = static_cast<float*>(aligned_alloc(256, nSize*sizeof(float)));
    float result = 0.0f;

    p1[2] = 2.3f;
    p2[2] = 3.0f;
    p1[nSize - 1] = 2.0f;
    p2[nSize - 1] = 1.1f;

    auto start = std::chrono::steady_clock::now();
    auto end = std::chrono::steady_clock::now();
    auto duration = 0L;

    result = dotproduct(p1, p2, nSize);
    result = dotproduct(p1, p2, nSize);

    TIME_START
    result = dotproduct(p1, p2, nSize);
    TIME_END("normal")

    TIME_START
    result = dotproduct_unloop(p1, p2, nSize);
    TIME_END("unloop")

    TIME_START
    result = dotproduct_neon(p1, p2, nSize);
    TIME_END("SIMD")

    TIME_START
    result = dotproduct_neon_omp(p1, p2, nSize);
    TIME_END("SIMD+OpenMP")

    delete[] p1;
    delete[] p2;

    return 0;
}
```

```cpp
// matoperation.cpp

#include "matoperation.hpp"
#include <iostream>

#ifdef WITH_AVX2
#include <immintrin.h>
#endif

#ifdef WITH_NEON
#include <arm_neon.h>
#endif

#ifdef _OPENMP
#include <omp.h>
#endif

float dotproduct(const float* p1, const float* p2, size_t n) {
    float sum = 0.0f;
    for (size_t i = 0; i < n; i++)
        sum += (p1[i] * p2[i]);
    return sum;
}

float dotproduct_unloop(const float* p1, const float* p2, size_t n) {
    if (n % 8 != 0) {
        std::cerr << "The size n must be a multiple of 8." << std::endl;
        return 0.0f;
    }

    float sum = 0.0f;
    for (size_t i = 0; i < n; i += 8) {
        sum += (p1[i] * p2[i]);
        sum += (p1[i + 1] * p2[i + 1]);
        sum += (p1[i + 2] * p2[i + 2]);
        sum += (p1[i + 3] * p2[i + 3]);
        sum += (p1[i + 4] * p2[i + 4]);
        sum += (p1[i + 5] * p2[i + 5]);
        sum += (p1[i + 6] * p2[i + 6]);
        sum += (p1[i + 7] * p2[i + 7]);
    }
    return sum;
}

float dotproduct_avx2(const float* p1, const float* p2, size_t n) {
#ifdef WITH_AVX2
    if (n % 8 != 0) {
        std::cerr << "The size n must be a multiple of 8." << std::endl;
        return 0.0f;
    }

    float sum[8] = {0};
    __m256 a, b;
    __m256 c = _mm256_setzero_ps();

    for (size_t i = 0; i < n; i += 8) {
        a = _mm256_loadu_ps(p1 + i);
        b = _mm256_loadu_ps(p2 + i);
        c = _mm256_add_ps(c, _mm256_mul_ps(a, b));
    }
    _mm256_storeu_ps(sum, c);
    return (sum[0] + sum[1] + sum[2] + sum[3] + sum[4] + sum[5] + sum[6] + sum[7]);
#else
    std::cerr << "AVX2 is not supported" << std::endl;
    return 0.0;
#endif
}

float dotproduct_avx2_omp(const float* p1, const float* p2, size_t n) {
#ifdef WITH_AVX2
    if (n % 8 != 0) {
        std::cerr << "The size n must be a multiple of 8." << std::endl;
        return 0.0f;
    }

    float sum[8] = {0};
    __m256 a, b;
    __m256 c = _mm256_setzero_ps();

#pragma omp parallel for
    for (size_t i = 0; i < n; i += 8) {
        a = _mm256_loadu_ps(p1 + i);
        b = _mm256_loadu_ps(p2 + i);
        c = _mm256_add_ps(c, _mm256_mul_ps(a, b));
    }
    _mm256_storeu_ps(sum, c);
    return (sum[0] + sum[1] + sum[2] + sum[3] + sum[4] + sum[5] + sum[6] + sum[7]);
#else
    std::cerr << "AVX2 is not supported" << std::endl;
    return 0.0;
#endif
}

float dotproduct_neon(const float* p1, const float* p2, size_t n) {
#ifdef WITH_NEON
    if (n % 4 != 0) {
        std::cerr << "The size n must be a multiple of 4." << std::endl;
        return 0.0f;
    }

    float sum[4] = {0};
    float32x4_t a, b;
    float32x4_t c = vdupq_n_f32(0);

    for (size_t i = 0; i < n; i += 4) {
        a = vld1q_f32(p1 + i);
        b = vld1q_f32(p2 + i);
        c = vaddq_f32(c, vmulq_f32(a, b));
    }
    vst1q_f32(sum, c);
    return (sum[0] + sum[1] + sum[2] + sum[3]);
#else
    std::cerr << "NEON is not supported" << std::endl;
    return 0.0;
#endif
}

float dotproduct_neon_omp(const float* p1, const float* p2, size_t n) {
#ifdef WITH_NEON
    if (n % 4 != 0) {
        std::cerr << "The size n must be a multiple of 4." << std::endl;
        return 0.0f;
    }

    float sum[4] = {0};
    float32x4_t a, b;
    float32x4_t c = vdupq_n_f32(0);

#pragma omp parallel for
    for (size_t i = 0; i < n; i += 4) {
        a = vld1q_f32(p1 + i);
        b = vld1q_f32(p2 + i);
        c = vaddq_f32(c, vmulq_f32(a, b));
    }
    vst1q_f32(sum, c);
    return (sum[0] + sum[1] + sum[2] + sum[3]);
#else
    std::cerr << "NEON is not supported" << std::endl;
    return 0.0;
#endif
}
```

```cpp
// matoperation.hpp

#pragma once

float dotproduct(const float* p1, const float* p2, size_t n);
float dotproduct_unloop(const float* p1, const float* p2, size_t n);
float dotproduct_avx2(const float* p1, const float* p2, size_t n);
float dotproduct_avx2_omp(const float* p1, const float* p2, size_t n);
float dotproduct_neon(const float* p1, const float* p2, size_t n);
float dotproduct_neon_omp(const float* p1, const float* p2, size_t n);
```

```cmake
# CMakeLists.txt

cmake_minimum_required(VERSION 3.12)

add_definitions(-DWITH_NEON)
# add_definitions(-DWITH_AVX2)

set(CMAKE_CXX_STANDARD 11)

project(dotp)

ADD_EXECUTABLE(dotp main.cpp matoperation.cpp)

find_package(OpenMP)
if(OpenMP_CXX_FOUND)
    message("OpenMP found.")
    target_link_libraries(dotp PUBLIC OpenMP::OpenMP_CXX)
endif()
```
