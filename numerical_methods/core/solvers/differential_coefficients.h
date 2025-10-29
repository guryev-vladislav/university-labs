#ifndef DIFFERENTIAL_COEFFICIENTS_H
#define DIFFERENTIAL_COEFFICIENTS_H

class DifferentialCoefficients {
public:
    virtual double conductivity(double x) const = 0;
    virtual double reaction(double x) const = 0;  
    virtual double source(double x) const = 0;
    virtual double interfacePosition() const = 0;
    virtual ~DifferentialCoefficients() = default;
    
    // Эффективные коэффициенты для разрывных задач
    virtual double effectiveConductivity(double x, double h) const;
    virtual double effectiveReaction(double x, double h) const;
    virtual double effectiveSource(double x, double h) const;
};

#endif