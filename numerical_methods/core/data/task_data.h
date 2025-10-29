// core/data/task_data.h
#ifndef TASK_DATA_H
#define TASK_DATA_H

#include <vector>

class task_data {
public:
    std::vector<double> i;
    std::vector<double> x;
    std::vector<double> v;
    std::vector<double> u;
    std::vector<double> x2;
    std::vector<double> v2;
    std::vector<double> diff;

    enum class data_type { I, X, V, U, X2, V2, DIFF };

    task_data() = default;
    explicit task_data(int size) {
        i.reserve(size);
        x.reserve(size);
        v.reserve(size);
        u.reserve(size);
        x2.reserve(size);
        v2.reserve(size);
        diff.reserve(size);
    }

    void push(data_type type, double val) {
        switch (type) {
            case data_type::I:
                i.push_back(val);
                break;
            case data_type::X:
                x.push_back(val);
                break;
            case data_type::V:
                v.push_back(val);
                break;
            case data_type::U:
                u.push_back(val);
                break;
            case data_type::X2:
                x2.push_back(val);
                break;
            case data_type::V2:
                v2.push_back(val);
                break;
            case data_type::DIFF:
                diff.push_back(val);
                break;
        }
    }

    void clear() {
        i.clear();
        x.clear();
        v.clear();
        u.clear();
        x2.clear();
        v2.clear();
        diff.clear();
    }

    size_t size() const {
        return x.size();
    }
};

#endif