# Laboratory Work: Monte Carlo Methods

## Completed Tasks

### 1. Area Calculation of Complex Shapes
**Variant 8:** `r = 2 cos(t), ϕ = sin(t), t ∈ [-π, π]`

**Objectives:**
- Plot the parametric curve defined by polar equations
- Calculate exact area using numerical integration
- Estimate area using Monte Carlo method with random point sampling
- Analyze accuracy and error of the method
- Visualize points inside/outside the region

**Implementation:** `area_calculation.py`

### 2. Random Walk Analysis  
**Variant 1:** `X₀ = 0, Xₙ₊₁ = Xₙ + ξₙ₊₁, ξᵢ ∼ R[a, b]`

**Objectives:**
- Model random walk with uniform step distribution
- Analyze first hitting time τ = min{n : |Xₙ| ≥ T}
- Compute empirical distribution of hitting times
- Calculate sample mean and variance
- Compare with normal and lognormal distributions

**Implementation:** `random_walk_analysis.py`

### 3. String Pattern Search in Random Sequences
**Variant 2:** Random binary sequence with probability p of '1'

**Objectives:**
- Generate random binary sequences of length N
- Count occurrences of specified substring patterns
- Analyze distribution of substring occurrences
- Compare empirical distribution with normal approximation
- Compute sample mean and variance of occurrence counts

**Implementation:** `binary_sequence_generator.py`

## Common Methodology
All implementations demonstrate core Monte Carlo principles:
- Statistical sampling for complex computational problems
- Error analysis and convergence estimation
- Empirical distribution analysis
- Visualization of results and distributions
- Comparison between theoretical and empirical approaches

## Technology Stack
- **Programming Language:** Python
- **Libraries:** NumPy, SciPy, matplotlib
- **Methods:** Monte Carlo integration, random walk simulation, statistical distribution analysis
- **Visualization:** CDF plots, histograms, scatter plots