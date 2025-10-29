# Laboratory Work: Telephone Exchange Modeling (Poisson Process)

## Main Objectives

### 1. Poisson Process Simulation
- Model telephone call arrivals as a Poisson process with intensity λ
- Generate Poisson-distributed random variables for call counts over time interval t
- Implement efficient Poisson random variable generator using inverse transform method

### 2. Statistical Analysis of Generated Data
- Create frequency tables for discrete call counts
- Calculate key statistical characteristics:
  - Sample mean and variance
  - Sample median and range
  - Comparison with theoretical Poisson parameters
- Build empirical distribution function and compare with theoretical CDF

### 3. Distribution Hypothesis Testing
- Perform chi-square goodness-of-fit test for Poisson distribution
- Define interval boundaries for hypothesis testing
- Calculate theoretical and observed interval probabilities
- Determine hypothesis acceptance/rejection at specified significance level α
- Compute Kolmogorov-Smirnov distance between distributions

## Key Features

**Poisson Random Variable Generation:**
- Uses inverse transform method with cumulative probabilities
- Efficient algorithm for Poisson variate generation
- Handles different intensity parameters and time intervals

**Statistical Testing:**
- Chi-square test with user-defined intervals
- Multiple iterations for statistical significance
- Comprehensive hypothesis testing results
- Visual comparison of empirical vs theoretical distributions

**Visualization:**
- Empirical and theoretical CDF plots
- Histograms of call frequency distributions
- Statistical characteristic comparisons

## Practical Application
Models real-world telephone exchange systems where:
- Calls arrive randomly with constant average rate
- Call arrivals are independent events
- System follows Poisson process assumptions
- Useful for telecommunications capacity planning

## Technology Stack
- **Programming Language:** Python
- **Libraries:** NumPy, SciPy, matplotlib, collections
- **Statistical Methods:** Poisson distribution, chi-square test, Kolmogorov-Smirnov test
- **Visualization:** Histograms, CDF plots, frequency tables