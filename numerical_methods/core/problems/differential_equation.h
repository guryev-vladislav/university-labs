// core/problems/differential_equation.h
#ifndef DIFFERENTIAL_EQUATION_H
#define DIFFERENTIAL_EQUATION_H

class differential_equation {
public:
    virtual ~differential_equation() = default;
    virtual double get_left_boundary() const = 0;
    virtual double get_right_boundary() const = 0;
    virtual int get_min_nodes() const { return 3; }
};

#endif