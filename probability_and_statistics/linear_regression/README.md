# Laboratory Work: Linear Regression

## Main Objectives

### 1. Simple Linear Regression
- Implement one-dimensional linear regression model `y(x) = ax + b`
- Generate sample data `y₁, y₂, ..., yₙ` with normal distribution `ξᵢ ∼ N(y(i), σ²)`
- Estimate regression coefficients `a` and `b` from data `X = (1, 2, ..., n)`, `Y = (y₁, y₂, ..., yₙ)`
- Calculate coefficient of determination `R²`
- Generate additional test sample and compare predicted values `ŷ = a*x + b` with actual data
- Repeat analysis for randomly generated `x` values on interval `[t₁, t₂]`

### 2. Multiple Linear Regression  
- Implement multidimensional linear regression model `y(x₁, x₂) = a₁x₁ + a₂x₂ + b`
- Generate sample data with normal distribution `ξᵢ ∼ N(y(x₁, x₂), σ²)` where `x₁ ∼ R(t₁, t₂)`, `x₂ ∼ R(s₁, s₂)`
- Estimate regression coefficients `a₁`, `a₂` and `b`
- Calculate coefficient of determination `R²`
- Generate additional test sample and compare predicted values `ŷ = a₁*x₁ + a₂*x₂ + b` with actual data

### 3. Real Data Analysis
- Find and analyze real-world datasets
- Perform comprehensive regression analysis on actual data
- Validate model performance with real-world examples

## Technology Stack
- **Programming Language:** Python
- **Libraries:** NumPy, SciPy, scikit-learn, pandas, matplotlib
- **Methods:** Statistical modeling, normal distribution, regression analysis
- **Metrics:** Coefficient of determination (R²), prediction accuracy