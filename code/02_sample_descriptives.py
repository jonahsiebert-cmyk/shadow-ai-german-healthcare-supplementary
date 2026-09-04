# -*- coding: utf-8 -*-
"""
02_sample_descriptives.py
Deskriptive Statistiken (Häufigkeiten, Mittelwerte) und BÄK-Repräsentativitätsvergleich.
"""

import numpy as np
import pandas as pd
from scipy.stats import chisquare

def run_descriptives(input_path="processed_long_df.pkl"):
    long_df = pd.read_pickle(input_path)

    print("\n=== DESKRIPTIVE HÄUFIGKEITEN ===")
    for q in range(1, 34):
        mask_q = long_df["question_id"] == q
        if long_df[mask_q].empty:
            continue

        stats = long_df[mask_q]["answer"].value_counts()
        pcts = long_df[mask_q]["answer"].value_counts(normalize=True) * 100

        final_table = pd.DataFrame({"N": stats, "Percentage": pcts.map("{:.1f}%".format)})
        print(f"\n--- Frage ID: {q} ---")
        print(final_table)

    # Berufserfahrung (Metrisch)
    age_mapping = {
        "0-4 Jahre": 2.0, "5-9 Jahre": 7.0, "10-14 Jahre": 12.0,
        "15-19 Jahre": 17.0, "20-25 Jahre": 22.5, ">25 Jahre": 25.0
    }
    df_age = long_df[long_df["question_id"] == 9].copy()
    df_age["age_numeric"] = df_age["answer"].map(age_mapping)
    print(f"\nBerufserfahrung Mean: {df_age['age_numeric'].mean():.2f} Jahre (SD: {df_age['age_numeric'].std():.2f})")

    # Digitale Kompetenz
    df_dig = long_df[long_df["question_id"] == 17].copy()
    print(f"Digitale Kompetenz Mean: {df_dig['answer'].mean():.2f} (SD: {df_dig['answer'].std():.2f})")

    # BÄK Repräsentativitäts-Prüfung
    obs_sex = long_df[long_df['question_id'] == 5]['answer'].value_counts()
    cm, cw = obs_sex.get("männlich", 0), obs_sex.get("weiblich", 0)
    obs_sex_arr = np.array([cm, cw])
    bak_cm, bak_cw = 446120 - 225397, 225397
    exp_sex = (np.array([bak_cm, bak_cw]) / (bak_cm + bak_cw)) * obs_sex_arr.sum()
    chi2_sex, p_sex = chisquare(f_obs=obs_sex_arr, f_exp=exp_sex)
    print(f"\nGeschlecht vs. BÄK: Chi2(1) = {chi2_sex:.2f}, p = {p_sex:.4f}")

if __name__ == "__main__":
    run_descriptives()