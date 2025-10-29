# Laboratory Work 1: Finite Element Method - Shell Element Analysis

## Main Objectives

### 1. Numerical Integration Implementation
Develop a program that calculates forces and moments in a shell finite element based on given normal and shear stress distributions.

**Key formulas:**
- Forces: `Nij = ∫ σij(ξ) dξ` from -h/2 to h/2
- Moments: `Mij = ∫ σij(ξ) ξd` from -h/2 to h/2

### 2. Integration Methods
Implement two numerical integration approaches:

**a) Newton-Cotes Formulas** (on uniform grid):
- Composite formulas for n = 3, 5, 7 integration nodes
- Includes trapezoidal rule and Simpson's rule variants

**b) Gaussian Quadrature** (at Legendre polynomial nodes):
- Formulas for n = 3, 5, 7 integration nodes
- Using roots of Legendre polynomials as integration points

### 3. Program Testing & Validation
Test the implementation on:
- **Uniform stress distribution** across shell thickness
- **Linear stress distribution** across shell thickness
- **Arbitrary stress distribution** to demonstrate general functionality

### 4. Mathematical Components
- Derive recurrence relations for Legendre polynomials
- Calculate explicit Legendre polynomials for n = 0-5
- Compute roots of Legendre polynomials for n = 3, 5, 7
- Determine Gaussian quadrature coefficients and error terms

## Technology Stack
- **Programming Language:** C++
- **Mathematical Methods:** Numerical integration, Legendre polynomials
- **Applications:** Finite element analysis, structural mechanics