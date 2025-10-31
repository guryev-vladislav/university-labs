// core/data/task_data.h
#pragma once
#ifndef DATA_TASK_H
#define DATA_TASK_H

#include <vector>

class TaskData
{
public:
    std::vector<double> i;
    std::vector<double> x;
    std::vector<double> v;
    std::vector<double> u;
    std::vector<double> x2;
    std::vector<double> v2;
    std::vector<double> diff;

    enum class DataType { I, X, V, U, X2, V2, DIFF };

    TaskData() = default;
    explicit TaskData(int size) {
        i.reserve(size);
        x.reserve(size);
        v.reserve(size);
        u.reserve(size);
        x2.reserve(size);
        v2.reserve(size);
        diff.reserve(size);
    }

    void push(DataType type, double val) {
        switch (type) {
        case DataType::I:
            i.push_back(val);
            break;
        case DataType::X:
            x.push_back(val);
            break;
        case DataType::V:
            v.push_back(val);
            break;
        case DataType::U:
            u.push_back(val);
            break;
        case DataType::X2:
            x2.push_back(val);
            break;
        case DataType::V2:
            v2.push_back(val);
            break;
        case DataType::DIFF:
            diff.push_back(val);
            break;
        }
    }
};
#endif