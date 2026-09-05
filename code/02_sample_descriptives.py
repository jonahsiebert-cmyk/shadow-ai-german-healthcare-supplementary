# -*- coding: utf-8 -*-
"""
02_sample_descriptives.py

Reproduces Table 1, the goodness-of-fit tests of Section 4.1, the prevalence
figures of Section 4.2 (including the by-setting rates shown in Figure 1 and
the age-standardised rates), the application areas, and the training mode
figure of Section 4.3.

Reference statistics: Bundesärztekammer, Ärztestatistik zum 31. Dezember 2025.
The gender and age shares below are those printed in Table 1; the federal-state
shares are those in data/aggregated/federal_state_distribution.csv.

Input: analytical_sample.csv from 01_data_cleaning.py.
"""
import numpy as np
import pandas as pd
from scipy.stats import chisquare

IN_CSV = "analytical_sample.csv"

# Bundesärztekammer 2025 reference shares (per cent)
BAEK_GENDER = {"Female": 50.52, "Male": 49.48}
BAEK_AGE4 = {"under 40": 33.14, "40 to 49": 23.33, "50 to 59": 20.16, "60 and over": 23.38}
AGE4 = {1: "under 40", 2: "under 40", 3: "40 to 49", 4: "50 to 59", 5: "60 and over", 6: "60 and over"}
STATE_FILE = "data/aggregated/federal_state_distribution.csv"


def pct(s, n=None):
    n = len(s) if n is None else n
    return (s.value_counts() / n * 100).round(2)


def gof(observed, expected_shares, label):
    obs = np.asarray(observed, dtype=float)
    exp = np.asarray(expected_shares, dtype=float)
    exp = exp / exp.sum() * obs.sum()
    chi2, p = chisquare(obs, exp)
    w = np.sqrt(chi2 / obs.sum())
    print(f"{label}: chi2({len(obs) - 1}) = {chi2:.2f}, p = {p:.3f}, Cohen's w = {w:.2f}")
    return chi2, p, w


def main():
    df = pd.read_csv(IN_CSV)
    n = len(df)
    assert n == 320

    print("=== Table 1 ===")
    print(pd.DataFrame({"n": df["gender"].value_counts(), "%": pct(df["gender"])}))
    print(pd.DataFrame({"n": df["age_band"].value_counts(), "%": pct(df["age_band"])}).sort_index())
    print(pd.DataFrame({"n": df["setting_en"].value_counts(), "%": pct(df["setting_en"])}))

    print("\n=== Section 4.1: goodness of fit against Bundesärztekammer 2025 ===")
    gof([(df["male"] == 0).sum(), (df["male"] == 1).sum()], list(BAEK_GENDER.values()), "Gender")
    age4 = df["age_ordinal"].map(AGE4)
    obs_age = [(age4 == k).sum() for k in BAEK_AGE4]
    chi2, p, w = gof(obs_age, list(BAEK_AGE4.values()), "Age (four bands)")
    assert round(chi2, 1) == 11.6 and round(p, 3) == 0.009
    try:
        fs = pd.read_csv(STATE_FILE)
        fs = fs[fs["Federal State"] != "Gesamt"]
        ref = fs["BÄK"].str.replace("%", "").str.replace(",", ".").astype(float)
        obs_fs = df["federal_state"].value_counts().reindex(fs["Federal State"]).fillna(0).values
        gof(obs_fs, ref.values, "Federal state (16 states)")
        dev = (obs_fs / n * 100 - ref.values)
        print(f"Maximum absolute deviation: {np.abs(dev).max():.2f} percentage points "
              f"({fs['Federal State'].iloc[np.abs(dev).argmax()]})")
    except FileNotFoundError:
        print("Federal state file not found; run from the repository root.")

    print("\n=== Section 4.2: AI use ===")
    print(pd.DataFrame({"n": df["ai_use_frequency"].value_counts(), "%": pct(df["ai_use_frequency"])}))
    any_use = df["ai_use_frequency"].str.startswith("Ja").mean() * 100
    print(f"Any use: {any_use:.2f}%")
    areas = df["application_areas"].str.split(";").explode().str.strip()
    areas = areas[areas != ""]
    print("Application areas (share of n = 320):")
    print(pct(areas, n))

    print("\n=== Section 4.2: Shadow AI ===")
    print(pd.DataFrame({"n": df["shadow_ai_item"].value_counts(), "%": pct(df["shadow_ai_item"])}))
    by_setting = df.groupby("setting_en")[["shadow_own_use", "shadow_exposure"]].mean() * 100
    print("By setting (%):\n" + by_setting.round(2).to_string())
    assert round(by_setting.loc["Hospital", "shadow_exposure"], 2) == 64.08
    assert round(by_setting.loc["Practice", "shadow_own_use"], 2) == 24.83

    print("\nAge-standardised to Bundesärztekammer 2025 (four bands):")
    for dv in ["shadow_own_use", "shadow_exposure"]:
        rates = df.groupby(age4)[dv].mean()
        std = sum(rates[k] * BAEK_AGE4[k] for k in BAEK_AGE4) / sum(BAEK_AGE4.values()) * 100
        print(f"  {dv}: {std:.2f}%")

    print("\n=== Section 4.3: governance components ===")
    for v in ["tool_provision", "training", "guidelines"]:
        print(pd.DataFrame({"n": df[v].value_counts(), "%": pct(df[v])}))
    trained = df[df["gov_training"] == 1]
    short = trained["training_mode"].str.contains("Kurzvortrag").sum()
    print(f"Short presentations among trained: n = {short} of {len(trained)} "
          f"({short / len(trained) * 100:.2f}%)")
    tp = df[df["gov_ai_tools"] == 1]
    k = tp["gov_training"] + tp["gov_guidelines"]
    print(f"Among tool-provided (n = {len(tp)}): neither {np.mean(k == 0) * 100:.2f}%, "
          f"one {np.mean(k == 1) * 100:.2f}%, both {np.mean(k == 2) * 100:.2f}%")


if __name__ == "__main__":
    main()
