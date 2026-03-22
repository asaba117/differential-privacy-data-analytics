# Differential Privacy in Data Analytics

This repository contains our **CS4413 Winter 2026** project on **differential privacy in data analytics**.  
The project compares two widely used privacy mechanisms:

- **Laplace Mechanism**
- **Gaussian Mechanism**

We evaluate both mechanisms on the **Adult Income dataset** using three common statistical query types:

- **Count query**
- **Mean query**
- **Histogram query**

The goal is to study the **privacy-utility trade-off** by measuring how different privacy budgets affect the accuracy of released statistics.

---

## Project Overview

Differential privacy (DP) is a formal framework for protecting individual privacy when releasing information derived from datasets. In this project, we compare the Laplace and Gaussian mechanisms on simple aggregate queries and analyze how increasing or decreasing the privacy budget impacts utility.

### Queries Tested
- **Count:** Number of individuals earning more than \$50K
- **Mean:** Average age
- **Histogram:** Distribution of education levels

### Privacy Settings
- **Epsilon values:** `{0.1, 0.5, 1.0, 2.0}`
- **Delta (Gaussian only):** `1e-5`

### Evaluation Metrics
- **Mean Absolute Error (MAE)**
- **Mean Squared Error (MSE)**

---

## Dataset

This project uses the **Adult Income dataset** from the **UCI Machine Learning Repository**.

After preprocessing and removing missing values, the cleaned dataset contains:

- **30,162 records**
- attributes relevant to:
  - age
  - hours-per-week
  - income
  - education

---

## Methods

### Laplace Mechanism
Used for pure **ε-differential privacy**.

Noise added:

```math
\text{Laplace}(0, \Delta f / \varepsilon)
```
Gaussian Mechanism
Used for approximate (ε, δ)-differential privacy.
Noise added:

𝑁
(
0
,
𝜎
2
)
N(0,σ
2
)

with noise scale calibrated using query sensitivity, ε, and δ.

Sensitivity Used
Count query: Δf = 1
Mean age query: Δf = (max(age) - min(age)) / n
Histogram query: Δf = 1
Repository Structure
.
├── src/           # Source code
├── data/          # Dataset files / processed CSV files
├── results/       # Experimental outputs and result summaries
├── figures/       # Graphs and charts used in report/presentation
├── slides/        # Presentation materials
├── report/        # Final report
└── README.md

You can adjust this section if your folder names are slightly different.

Requirements

This project was implemented in Python 3 using:

pandas
numpy

Install dependencies with:

pip install pandas numpy
Running the Code

Run the main script with:

python test.py

Depending on your file layout, you may rename this to:

python src/main.py

The script:

loads and preprocesses the Adult Income dataset
computes non-private baseline statistics
applies Laplace and Gaussian mechanisms
runs repeated trials for each query and privacy budget
computes MAE and MSE
saves summary results to CSV files
Output Files

Typical outputs include:

dp_results_summary.csv
education_histogram_true.csv

These files are used to generate:

result tables
privacy-utility graphs
report figures
presentation charts
Key Results

Our experiments showed:

As ε increases, error decreases for both mechanisms
Laplace outperformed Gaussian across all tested queries and privacy budgets
The histogram query showed the clearest difference between the two mechanisms
The mean query had the smallest error because of its low sensitivity
Overall Conclusion

For the low-sensitivity aggregate queries tested in this project, the Laplace mechanism provided a better privacy-utility balance than the Gaussian mechanism.

Example Result Summary
Count Query MAE
Epsilon	Laplace	Gaussian
0.1	9.1136	37.0213
0.5	1.8797	7.1031
1.0	1.0359	4.1219
2.0	0.5650	2.0497
Mean Age MAE
Epsilon	Laplace	Gaussian
0.1	0.0235	0.0981
0.5	0.0050	0.0187
1.0	0.0025	0.0098
2.0	0.0013	0.0045
Education Histogram MAE
Epsilon	Laplace	Gaussian
0.1	9.8272	38.6114
0.5	1.9925	7.8826
1.0	0.9931	3.7743
2.0	0.5037	1.9694
Course Information
Course: CS4413 Winter 2026
Project Title: Differential Privacy in Data Analytics
Team Members
Khaled Al Tamimi
Omar Mattar
Afif Saba
References
C. Dwork, F. McSherry, K. Nissim, and A. Smith, Calibrating noise to sensitivity in private data analysis, TCC 2006.
K. Nissim, S. Raskhodnikova, and A. Smith, Smooth sensitivity and sampling in private data analysis, STOC 2007.
B. Balle and Y.-X. Wang, Improving the Gaussian mechanism for differential privacy, ICML 2018.
I. Mironov, Rényi differential privacy, CSF 2017.
License

This repository is for academic and educational use.
