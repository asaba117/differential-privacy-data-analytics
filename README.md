# Differential Privacy in Data Analytics

This repository contains a CS4413 Winter 2026 project that compares the Laplace and Gaussian mechanisms for differential privacy on simple aggregate queries over the Adult Income dataset.

The analysis focuses on the privacy-utility trade-off for:

- count queries
- mean queries
- histogram queries

## What the Project Does

The Python script evaluates both mechanisms on the UCI Adult Income dataset and measures accuracy under different privacy budgets.

Queries included:

- Count of individuals with income `>50K`
- Mean age
- Histogram of education levels

Privacy parameters:

- `epsilon`: `0.1`, `0.5`, `1.0`, `2.0`
- `delta`: `1e-5` for the Gaussian mechanism

Evaluation metrics:

- Mean Absolute Error (MAE)
- Mean Squared Error (MSE)

## Repository Contents

This repo is organized as follows:

- `src/test.py`: main experiment script
- `data/dp_results_summary.csv`: summary of DP experiment results
- `data/education_histogram_true.csv`: true education histogram counts
- `data/CS4413_Final_Report_DP_Results.xlsx`: spreadsheet version of the results
- `figures/`: charts used in the report and presentation
- `report/`: project reports in PDF form
- `slides/`: presentation materials
- `README.md`: project documentation

## Dataset

The project uses the Adult Income dataset from the UCI Machine Learning Repository. The script downloads the data directly from:

`https://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.data`

Preprocessing performed in `src/test.py`:

- treats `?` as missing data
- removes rows with missing values
- clips age to the range `17` to `90` to keep sensitivity bounded

After cleaning, the dataset contains `30,162` rows.

## Differential Privacy Methods

### Laplace Mechanism

Used for pure `epsilon`-differential privacy:

```math
\text{Laplace}(0, \Delta f / \varepsilon)
```

### Gaussian Mechanism

Used for approximate `(epsilon, delta)`-differential privacy. The script uses the standard calibration:

```math
\sigma = \frac{\Delta f \sqrt{2 \ln(1.25/\delta)}}{\varepsilon}
```

Noise is then sampled from:

```math
\mathcal{N}(0, \sigma^2)
```

### Sensitivities Used

- Count query: `1`
- Mean age query: `(AGE_MAX - AGE_MIN) / n`
- Education histogram:
  - Laplace per-bin sensitivity: `1`
  - Gaussian vector `L2` sensitivity: `1`

## Requirements

This project uses Python 3 and requires:

- `pandas`
- `numpy`

Install dependencies with:

```bash
pip install pandas numpy
```

Or use:

```bash
pip install -r requirements.txt
```

## Running the Project

Run the experiment with:

```bash
python3 src/test.py
```

The script:

- downloads and cleans the Adult dataset
- computes non-private baseline statistics
- applies Laplace and Gaussian noise
- repeats each experiment across multiple trials
- reports MAE and MSE
- writes output CSV files

## Output Files

Running the script generates:

- `data/dp_results_summary.csv`
- `data/education_histogram_true.csv`

`data/dp_results_summary.csv` contains per-query results for each mechanism and privacy budget, including:

- query name
- mechanism
- epsilon
- true value when applicable
- mean noisy value for scalar queries
- MAE
- MSE

## Example Findings

The current saved results in `data/dp_results_summary.csv` show:

- error decreases as `epsilon` increases
- Laplace has lower error than Gaussian for the tested queries and settings
- histogram queries show a larger utility gap between the two mechanisms

Example count-query MAE values:

| Epsilon | Laplace | Gaussian |
| --- | ---: | ---: |
| 0.1 | 9.1136 | 37.0213 |
| 0.5 | 1.8797 | 7.1031 |
| 1.0 | 1.0359 | 4.1219 |
| 2.0 | 0.5650 | 2.0497 |

## Course Information

- Course: CS4413 Winter 2026
- Project Title: Differential Privacy in Data Analytics

Team members:

- Khaled Al Tamimi
- Omar Mattar
- Afif Saba

## References

1. C. Dwork, F. McSherry, K. Nissim, and A. Smith, “Calibrating noise to sensitivity in private data analysis,” in Theory of Cryptography (TCC 2006), 2006, pp. 265–284.

2.  K. Nissim, S. Raskhodnikova, and A. Smith, “Smooth sensitivity and sampling in private data analysis,” in Proceedings of the ACM Symposium on Theory of Computing, 2007, pp. 75–84.

3.  B. Balle and Y.-X. Wang, “Improving the Gaussian mechanism for differential privacy: Analytical calibration and optimal denoising,” in Proceedings of the 35th International Conference on Machine Learning, 2018.

4.  I. Mironov, “Rényi differential privacy,” in Proceedings of the IEEE 30th Computer Security Foundations Symposium, 2017, pp. 263–275.

5.  J. Near, D. Darais, N. Lefkovitz, and G. Howarth, Guidelines for Evaluating Differential Privacy Guarantees, NIST Special Publication 800-226, 2025.

6. OpenDP, “A framework to understand DP,” OpenDP Documentation.

7. Google, “Google’s differential privacy libraries,” GitHub repository.

8.  S. Haney, D. Desfontaines, L. Hartman, R. Shrestha, and M. Hay, “Precision-based attacks and interval refining: how to break, then fix, differential privacy on finite computers,” arXiv:2207.13793, 2022.

9. UCI Machine Learning Repository, “Adult Data Set.”

## Notes

The script downloads the Adult dataset from UCI at runtime, so regenerating the results requires an internet connection.
