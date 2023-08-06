/*
    Copyright 2016-2020 Intel Corporation.
    
    This software and the related documents are Intel copyrighted materials, and
    your use of them is governed by the express license under which they were
    provided to you (License). Unless the License provides otherwise, you may
    not use, modify, copy, publish, distribute, disclose or transmit this
    software or the related documents without Intel's prior written permission.
    
    This software and the related documents are provided as is, with no express
    or implied warranties, other than those that are expressly stated in the
    License.
*/
#pragma once

#include <cstring>
#include <iostream>
#include <string>

namespace ccl {

namespace v1 {

class string {
public:
    ~string() {
        delete[] storage;
        storage = nullptr;
        len = 0;
    }

    string() {
        storage = new char[1];
        *storage = '\0';
        len = 0;
    }

    string(const char* str) {
        len = strlen(str);
        storage = new char[len + 1];
        memcpy(storage, str, len * sizeof(char));
        storage[len] = '\0';
    }

    string(const string& str) {
        len = str.len;
        storage = new char[len + 1];
        memcpy(storage, str.storage, len * sizeof(char));
        storage[len] = '\0';
    }

    string(string&& str) noexcept {
        len = str.len;
        storage = str.storage;
        str.len = 0;
        str.storage = nullptr;
    }

    string(const std::string& str) {
        len = str.length();
        storage = new char[len + 1];
        memcpy(storage, str.c_str(), len * sizeof(char));
        storage[len] = '\0';
    }

    string& operator=(const string& str) {
        if (this != &str) {
            if (len != str.len) {
                len = str.len;
                delete[] storage;
                storage = new char[len + 1];
            }
            memcpy(storage, str.storage, len * sizeof(char));
            storage[len] = '\0';
        }
        return *this;
    }

    string& operator=(string&& str) noexcept {
        len = str.len;
        storage = str.storage;
        str.len = 0;
        str.storage = nullptr;
        return *this;
    }

    size_t length() const {
        return len;
    }

    const char* c_str() const {
        return storage;
    };

    operator std::string() const {
        return std::string(storage);
    }

    friend std::ostream& operator<<(std::ostream& out, const string& str) {
        out << str.storage;
        return out;
    }

    string operator+(const char* str) {
        auto str_len = strlen(str);
        if (str_len > 0) {
            auto new_storage = new char[len + str_len + 1];
            memcpy(new_storage, storage, len * sizeof(char));
            memcpy(&new_storage[len], str, str_len * sizeof(char));
            new_storage[len + str_len] = '\0';
            string res(new_storage);
            delete[] new_storage;
            return res;
        }
        return string(storage);
    }

    string operator+(const string& str) {
        return (*this + str.c_str());
    }

    string operator+(const std::string& str) {
        return (*this + str.c_str());
    }

    friend std::string operator+(const std::string& str1, const string& str2) {
        return (str1 + str2.c_str());
    }

    friend bool operator>(const string& str1, const string& str2) {
        return strcmp(str1.c_str(), str2.c_str()) > 0;
    }

    friend bool operator<=(const string& str1, const string& str2) {
        return strcmp(str1.c_str(), str2.c_str()) <= 0;
    }

    friend bool operator<(const string& str1, const string& str2) {
        return strcmp(str1.c_str(), str2.c_str()) < 0;
    }

    friend bool operator>=(const string& str1, const string& str2) {
        return strcmp(str1.c_str(), str2.c_str()) >= 0;
    }

    friend bool operator==(const string& str1, const string& str2) {
        return strcmp(str1.c_str(), str2.c_str()) == 0;
    }

private:
    size_t len;
    char* storage;
};

} // namespace v1

using v1::string;

} // namespace ccl
