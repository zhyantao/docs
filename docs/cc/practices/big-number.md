# 大数运算

## 加法和乘法

```cpp
#include <cmath>
#include <iostream>
#include <string>

// 将十六进制字符 '0' ~ 'F' 转换为相应的整数，即 0 ~ 15
int char2int(char ch) {
    if (!(('0' <= ch && ch <= '9') || ('a' <= ch && ch <= 'f') || ('A' <= ch && ch <= 'F'))) {
        std::cout << __FILE__ << ":" << __LINE__ << ":"
                  << "invalid character: " << ch << ", it should between '0' ~ 'F'"
                  << std::endl;
        return -1;
    }
    int ret = 0;
    switch (ch) {
    case 'F':
    case 'f': ret = 15; break;
    case 'E':
    case 'e': ret = 14; break;
    case 'D':
    case 'd': ret = 13; break;
    case 'C':
    case 'c': ret = 12; break;
    case 'B':
    case 'b': ret = 11; break;
    case 'A':
    case 'a': ret = 10; break;
    default: ret = (ch - '0'); break;
    }
    return ret;
}

// 将十进制整数 0 ~ 15 转换为相应的十六进制字符 '0' ~ 'F'
char int2char(int num) {
    if (num < 0 || num > 15) {
        std::cout << __FILE__ << ":" << __LINE__ << ":"
                  << "invalid number: " << num << ", it should between 0 ~ 15" << std::endl;
        return -1;
    }
    char ret = '0';
    switch (num) {
    case 15: ret = 'F'; break;
    case 14: ret = 'E'; break;
    case 13: ret = 'D'; break;
    case 12: ret = 'C'; break;
    case 11: ret = 'B'; break;
    case 10: ret = 'A'; break;
    default: ret = static_cast<char>(num + '0'); break;
    }
    return ret;
}

// 计算 num1 + num2，如果 base = 16，则使用 16 进制的运算法则
std::string add(std::string num1, std::string num2, int base) {
    std::string str;
    int len1 = num1.length();
    int len2 = num2.length();

    // 检查输入的合法性
    for (int i = 0; i < len1; i++) {
        if (char2int(num1[i]) < 0 || char2int(num1[i]) > base) {
            std::cout << "the element in number " << num1;
            std::cout << " should between 0 and " << base << std::endl;
            return str;
        }
    }
    for (int i = 0; i < len2; i++) {
        if (char2int(num2[i]) < 0 || char2int(num2[i]) > base) {
            std::cout << "the element in number " << num2;
            std::cout << " should between 0 and " << base << std::endl;
            return str;
        }
    }

    int carry = 0;
    int i = 0;
    while (i < len1 && i < len2) {
        int tmp1 = char2int(num1[len1 - 1 - i]);
        if (tmp1 < 0) {
            std::cout << __FILE__ << ":" << __LINE__ << ":"
                      << "the invalid number is " << num1 << std::endl;
            return str;
        }
        int tmp2 = char2int(num2[len2 - 1 - i]);
        if (tmp2 < 0) {
            std::cout << __FILE__ << ":" << __LINE__ << ":"
                      << "the invalid number is " << num2 << std::endl;
            return str;
        }
        int sum = carry + tmp1 + tmp2;
        carry = sum / base;
        int digit = sum % base;
        char tmp3 = int2char(digit);
        if (tmp3 < 0) {
            std::cout << __FILE__ << ":" << __LINE__ << ":"
                      << "the invalid character is " << digit << std::endl;
            return str;
        }
        str.push_back(tmp3);
        i++;
    }

    for (int j = i; j < len1; j++) {
        int sum = carry + char2int(num1[len1 - 1 - j]);
        carry = sum / base;
        int digit = sum % base;
        char tmp = int2char(digit);
        if (tmp < 0) {
            std::cout << __FILE__ << ":" << __LINE__ << ":"
                      << "the invalid character is " << digit << std::endl;
            return str;
        }
        str.push_back(tmp);
    }

    for (int j = i; j < len2; j++) {
        int sum = carry + char2int(num2[len2 - 1 - j]);
        carry = sum / base;
        int digit = sum % base;
        char tmp = int2char(digit);
        if (tmp < 0) {
            std::cout << __FILE__ << ":" << __LINE__ << ":"
                      << "the invalid character is " << digit << std::endl;
            return str;
        }
        str.push_back(tmp);
    }

    if (carry > 0) str.push_back(int2char(carry));

    std::string ret(str.rbegin(), str.rend());

    return ret;
}

// 计算 num1 和 num2 的乘积，如果 base = 10 则使用 10 进制的运算法则
std::string multiply(std::string num1, std::string num2, int base) {
    std::string ret = "0";
    int len1 = num1.length();
    int len2 = num2.length();

    // 检查输入的合法性
    for (int i = 0; i < len1; i++) {
        if (char2int(num1[i]) < 0 || char2int(num1[i]) > base) {
            std::cout << "the element in number " << num1;
            std::cout << " should between 0 and " << base << std::endl;
            return ret;
        }
    }
    for (int i = 0; i < len2; i++) {
        if (char2int(num2[i]) < 0 || char2int(num2[i]) > base) {
            std::cout << "the element in number " << num2;
            std::cout << " should between 0 and " << base << std::endl;
            return ret;
        }
    }

    for (int i = 0; i < len1; i++) {
        int tmp1 = char2int(num1[len1 - 1 - i]);
        char carry = '0';
        std::string str;
        for (int j = 0; j < len2; j++) {
            int tmp2 = char2int(num2[len2 - 1 - j]);
            int times = tmp1 * tmp2;
            int sum = char2int(carry) + times;
            carry = int2char(sum / base);
            char digit = int2char(sum % base);
            str.push_back(digit);
        }

        std::string rev(str.rbegin(), str.rend());
        for (int k = 0; k < i; k++)
            rev.push_back(int2char(0));
        ret = add(ret, rev, base);

        std::string tmp3;
        if (char2int(carry) > 0) {
            tmp3.push_back(carry);
            for (size_t k = 0; k < rev.length(); k++)
                tmp3.push_back(int2char(0));
        }
        ret = add(tmp3, ret, base);
    }

    return ret;
}

// 计算 base 的 n 次幂，即 base^n
std::string power(std::string base, int n) {
    std::string ret = "1";
    for (int i = 0; i < n; i++) {
        ret = multiply(ret, base, 10);
    }
    return ret;
}

// 使用自定义的运算法则
std::string get_phonenumber2(std::string hexdata) {
    int len = hexdata.length();
    std::string ret = "0";
    std::string base = "16";
    for (int i = len - 1; i >= 0; i--) {
        int j = len - 1 - i;
        std::string res = power(base, j);
        std::string num = std::to_string(char2int(hexdata[i]));
        ret = add(multiply(num, res, 10), ret, 10);
    }
    return ret;
}

// 使用标准库中的 power 函数
int get_phonenumber(std::string hexdata, std::string& phonenumber) {
    int ret = -1;
    int len = hexdata.length();
    long long sum = 0;
    for (int i = len - 1; i >= 0; i--) {
        int j = len - 1 - i;
        sum = char2int(hexdata[i]) * pow(16, j) + sum;
    }
    phonenumber = std::to_string(sum);
    return ret;
}

int main() {
    std::string hexdata = "3368D6510";
    std::string phonenumber;
    int ret = get_phonenumber(hexdata, phonenumber);
    std::cout << "hexdata: " << hexdata << "\t"
              << "phonenumber:" << phonenumber << std::endl;

    std::string str1 = add(hexdata, hexdata, 16); // 66D1ACA20
    std::cout << "str1: " << str1 << std::endl;

    std::string str2 = multiply(hexdata, hexdata, 16); // A52F0531B3B85A100
    std::cout << "str2: " << str2 << std::endl;

    hexdata = "FFFFFF";
    std::string str3 = multiply(hexdata, hexdata, 16); // FFFFFE000001
    std::cout << "str3: " << str3 << std::endl;

    std::string str4 = power("16", 6); // 16777216
    std::cout << "str4: " << str4 << std::endl;

    std::string str5 = get_phonenumber2("3368D6510"); // 13800138000
    std::cout << "str5: " << str5 << std::endl;

    return ret;
}
```
