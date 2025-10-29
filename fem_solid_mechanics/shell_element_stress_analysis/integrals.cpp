#include "integrals.h"
#include <cmath>

double integral_trapezoid(int n, double a, double b, double(*f)(double))
{
    int intervals = n - 1;
    double h = (b - a) / intervals;
    double result = f(a) / 2. + f(b) / 2.;
    
    for (int i = 1; i < intervals - 1; i++)
    {
        result += f(a + static_cast<double>(i) * h);
    }
    
    return h * result;
}

double integral_simpson(int n, double a, double b, double(*f)(double))
{
    int intervals = n - 1;
    
    if (intervals % 2) throw "Для формулы Cимпсона нужно четное количество интервалов";
    
    double h = (b - a) / static_cast<double>(intervals);
    
    double result = f(a) + f(b);
    
    for (int i = 1; i < intervals - 1; i++)
    {
        if (i % 2)
        {
            result += 4. * f(a + static_cast<double>(i) * h);
        }
        else
        {
            result += 2. * f(a + static_cast<double>(i) * h);
        }
    }
    
    return h * result / 3.;
}

double P0(double x)
{
    return 1.;
}

double P1(double x)
{
    return x;
}

double P2(double x)
{
    return 0.5 * (3. * pow(x, 2.) - 1.);
}

double P3(double x)
{
    return 0.5 * (5. * pow(x, 3.) - 3. * x);
}

double P4(double x)
{
    return 0.125 * (35. * pow(x, 4.) - 30. * pow(x, 2.) + 3.);
}

double P5(double x)
{
    return 0.125 * (63. * pow(x, 5) - 70. * pow(x, 3) + 15 * x);
}

double P(int n, double x)
{
    switch (n)
    {
        case 0:
            return P0(x);
        case 1:
            return P1(x);
        case 2:
            return P2(x);
        case 3:
            return P3(x);
        case 4:
            return P4(x);
        case 5:
            return P5(x);
        default:
            throw "smth wrong";
    }
}

double Ci(int n, int i)
{
    double tk = ti(n, i);
    return 2. * (1. - pow(tk, 2.)) / pow(n, 2.) / pow(P(n - 1, tk), 2.);
}

double ti(int n, int i)
{
    double t2[2] = {-pow(3., -0.5), pow(3., -0.5)};
    
    double t3[3] = { -sqrt(3. / 5.), 0., sqrt(3. / 5.) };
    
    double t4[4] = {-sqrt((15. + sqrt(120.)) / 35.),
                    -sqrt((15. - sqrt(120.)) / 35.),
                     sqrt((15. - sqrt(120.)) / 35.),
                     sqrt((15. + sqrt(120.)) / 35.)};
    
    double t5[5] = { -sqrt((35. + sqrt(280.)) / 63.),
                         -sqrt((35. - sqrt(280.)) / 63.),
                         0.,
                         sqrt((35. - sqrt(280.)) / 63.),
                         sqrt((35. + sqrt(280.)) / 63.) };
    
    switch(n)
    {
        case 0:
            return 1.;
        case 1:
            return 0.;
        case 2:
            return t2[i];
        case 3:
            return t3[i];
        case 4:
            return t4[i];
        case 5:
            return t5[i];
        default:
            throw "smth";
    }
}

double integral_Gauss(int n, double a, double b, double(*f)(double))
{
    double result = 0.;
    double x;
    
    for (int i = 0; i < n; i++)
    {
        x = b / 2. + a / 2. + ti(n, i) * (b / 2. - a / 2.);
        result += Ci(n, i) * f(x);
    }
    
    return (b - a) * result / 2.;
}

