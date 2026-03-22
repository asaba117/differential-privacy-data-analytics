import pandas as pd
import numpy as np
from math import sqrt, log

# -----------------------------
# Config
# -----------------------------
ADULT_URL = "https://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.data"

COLS = [
    "age", "workclass", "fnlwgt", "education", "education-num",
    "marital-status", "occupation", "relationship", "race", "sex",
    "capital-gain", "capital-loss", "hours-per-week", "native-country", "income"
]

EPSILONS = [0.1, 0.5, 1.0, 2.0]
DELTA = 1e-5
TRIALS = 200
SEED = 42

# Use fixed bounds for age to avoid unbounded / unstable sensitivity
AGE_MIN = 17
AGE_MAX = 90


# -----------------------------
# DP mechanisms
# -----------------------------
def laplace_mechanism(true_value, sensitivity, epsilon, rng):
    if epsilon <= 0:
        raise ValueError("epsilon must be > 0")
    scale = sensitivity / epsilon
    noise = rng.laplace(loc=0.0, scale=scale)
    return true_value + noise


def gaussian_sigma(sensitivity, epsilon, delta):
    """
    Simple standard Gaussian calibration used in many basic DP examples:
    sigma = sensitivity * sqrt(2 * ln(1.25/delta)) / epsilon
    """
    if epsilon <= 0:
        raise ValueError("epsilon must be > 0")
    if not (0 < delta < 1):
        raise ValueError("delta must be between 0 and 1")
    return sensitivity * sqrt(2 * log(1.25 / delta)) / epsilon


def gaussian_mechanism(true_value, sensitivity, epsilon, delta, rng):
    sigma = gaussian_sigma(sensitivity, epsilon, delta)
    noise = rng.normal(loc=0.0, scale=sigma)
    return true_value + noise


# -----------------------------
# Data loading / preprocessing
# -----------------------------
def load_adult_data():
    df = pd.read_csv(
        ADULT_URL,
        header=None,
        names=COLS,
        na_values="?",          # important: treat ? as missing
        skipinitialspace=True
    ).dropna()

    # Clip age so sensitivity is well-defined
    df["age"] = df["age"].clip(AGE_MIN, AGE_MAX)

    return df


def baseline_stats(df):
    count_over_50k = int((df["income"] == ">50K").sum())
    count_under_50k = int((df["income"] == "<=50K").sum())
    mean_age = float(df["age"].mean())
    mean_hours = float(df["hours-per-week"].mean())
    education_hist = df["education"].value_counts().sort_index()

    return {
        "count_over_50k": count_over_50k,
        "count_under_50k": count_under_50k,
        "mean_age": mean_age,
        "mean_hours": mean_hours,
        "education_hist": education_hist,
        "n": len(df),
    }


# -----------------------------
# Evaluation helpers
# -----------------------------
def evaluate_scalar_query(true_value, sensitivity, epsilons, mechanism, rng, delta=None, trials=200):
    rows = []

    for eps in epsilons:
        samples = []

        for _ in range(trials):
            if mechanism == "Laplace":
                dp_value = laplace_mechanism(true_value, sensitivity, eps, rng)
            elif mechanism == "Gaussian":
                dp_value = gaussian_mechanism(true_value, sensitivity, eps, delta, rng)
            else:
                raise ValueError("Unknown mechanism")

            samples.append(dp_value)

        samples = np.array(samples, dtype=float)
        abs_errors = np.abs(samples - true_value)
        mse = np.mean((samples - true_value) ** 2)

        rows.append({
            "mechanism": mechanism,
            "epsilon": eps,
            "true_value": true_value,
            "mean_dp_value": samples.mean(),
            "mean_absolute_error": abs_errors.mean(),
            "mse": mse,
        })

    return rows


def evaluate_histogram_query(true_hist, epsilons, mechanism, rng, delta=None, trials=200):
    rows = []
    true_counts = true_hist.to_numpy(dtype=float)

    # Under add/remove adjacency:
    # Laplace per-bin: use sensitivity 1
    # Gaussian vector query: L2 sensitivity is 1 for one-hot contribution
    laplace_sensitivity = 1.0
    gaussian_l2_sensitivity = 1.0

    for eps in epsilons:
        trial_mae = []
        trial_mse = []

        for _ in range(trials):
            if mechanism == "Laplace":
                noise = rng.laplace(
                    loc=0.0,
                    scale=laplace_sensitivity / eps,
                    size=len(true_counts)
                )
            elif mechanism == "Gaussian":
                sigma = gaussian_sigma(gaussian_l2_sensitivity, eps, delta)
                noise = rng.normal(
                    loc=0.0,
                    scale=sigma,
                    size=len(true_counts)
                )
            else:
                raise ValueError("Unknown mechanism")

            dp_counts = true_counts + noise

            mae = np.mean(np.abs(dp_counts - true_counts))
            mse = np.mean((dp_counts - true_counts) ** 2)

            trial_mae.append(mae)
            trial_mse.append(mse)

        rows.append({
            "mechanism": mechanism,
            "query": "education_histogram",
            "epsilon": eps,
            "num_bins": len(true_counts),
            "mean_absolute_error": np.mean(trial_mae),
            "mse": np.mean(trial_mse),
        })

    return rows


def print_table(title, df):
    print(f"\n{title}")
    print(df.to_string(index=False, float_format=lambda x: f"{x:.4f}"))


# -----------------------------
# Main
# -----------------------------
def main():
    rng = np.random.default_rng(SEED)

    df = load_adult_data()
    stats = baseline_stats(df)

    print("Income labels:", df["income"].unique())
    print(f"Count >50K: {stats['count_over_50k']}")
    print(f"Count <=50K: {stats['count_under_50k']}")
    print(f"Mean age: {stats['mean_age']:.4f}")
    print(f"Mean hours: {stats['mean_hours']:.4f}")
    print(f"Rows after cleaning: {stats['n']}")

    # Sensitivities
    count_sensitivity = 1.0
    age_sensitivity = (AGE_MAX - AGE_MIN) / stats["n"]

    # Count query
    count_rows = []
    count_rows += evaluate_scalar_query(
        true_value=stats["count_over_50k"],
        sensitivity=count_sensitivity,
        epsilons=EPSILONS,
        mechanism="Laplace",
        rng=rng,
        trials=TRIALS,
    )
    count_rows += evaluate_scalar_query(
        true_value=stats["count_over_50k"],
        sensitivity=count_sensitivity,
        epsilons=EPSILONS,
        mechanism="Gaussian",
        rng=rng,
        delta=DELTA,
        trials=TRIALS,
    )
    count_df = pd.DataFrame(count_rows)
    count_df.insert(0, "query", "count_over_50k")

    # Mean query
    mean_rows = []
    mean_rows += evaluate_scalar_query(
        true_value=stats["mean_age"],
        sensitivity=age_sensitivity,
        epsilons=EPSILONS,
        mechanism="Laplace",
        rng=rng,
        trials=TRIALS,
    )
    mean_rows += evaluate_scalar_query(
        true_value=stats["mean_age"],
        sensitivity=age_sensitivity,
        epsilons=EPSILONS,
        mechanism="Gaussian",
        rng=rng,
        delta=DELTA,
        trials=TRIALS,
    )
    mean_df = pd.DataFrame(mean_rows)
    mean_df.insert(0, "query", "mean_age")

    # Histogram query
    hist_rows = []
    hist_rows += evaluate_histogram_query(
        true_hist=stats["education_hist"],
        epsilons=EPSILONS,
        mechanism="Laplace",
        rng=rng,
        trials=TRIALS,
    )
    hist_rows += evaluate_histogram_query(
        true_hist=stats["education_hist"],
        epsilons=EPSILONS,
        mechanism="Gaussian",
        rng=rng,
        delta=DELTA,
        trials=TRIALS,
    )
    hist_df = pd.DataFrame(hist_rows)

    # Print results
    print_table("COUNT QUERY RESULTS", count_df)
    print_table("MEAN AGE QUERY RESULTS", mean_df)
    print_table("HISTOGRAM QUERY RESULTS", hist_df)

    # Save CSVs for report tables / plotting
    all_results = pd.concat([count_df, mean_df, hist_df], ignore_index=True)
    all_results.to_csv("dp_results_summary.csv", index=False)
    stats["education_hist"].rename("true_count").to_csv("education_histogram_true.csv")

    print("\nSaved: dp_results_summary.csv")
    print("Saved: education_histogram_true.csv")


if __name__ == "__main__":
    main()