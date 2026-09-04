# -*- coding: utf-8 -*-
"""
06_nonresponse_bias.py
Überprüft zeitbasierte Gruppenunterschiede (Early vs. Late Responders)
mittels Chi-Quadrat-Tests zur Erkennung eines Non-Response Biases.
"""

import pandas as pd
from scipy.stats import chi2_contingency

def run_nonresponse_bias(raw_csv_path="dataClassified_2.csv", processed_path="processed_long_df.pkl"):
    long_df = pd.read_pickle(processed_path)
    
    # Timing-Einteilung über Rohdaten
    df_raw = pd.read_csv(raw_csv_path, encoding='latin1', sep=';')
    id_col = df_raw.columns[0]
    time_col = df_raw.columns[1]
    
    df_raw[time_col] = pd.to_datetime(df_raw[time_col])
    df_sorted = df_raw.sort_values(time_col)
    
    early_ids = df_sorted.iloc[:len(df_sorted)//2][id_col].tolist()
    long_df["response_group"] = long_df[id_col].apply(lambda x: "Early" if x in early_ids else "Late")

    bias_results = []
    for q_id in range(1, 33):
        subset = long_df[long_df["question_id"] == q_id]
        if subset.empty:
            continue

        contingency = pd.crosstab(subset["response_group"], subset["answer"])
        if contingency.shape[0] < 2 or contingency.shape[1] < 2:
            continue

        chi2, p, dof, ex = chi2_contingency(contingency)
        bias_results.append({
            "Question ID": q_id,
            "Chi2": round(chi2, 2),
            "p-value": round(p, 4),
            "Status": "SIGNIFICANT DIFFERENCE" if p < 0.05 else "Consistent"
        })

    report_df = pd.DataFrame(bias_results)
    print("\n=== NON-RESPONSE BIAS REPORT (EARLY VS. LATE RESPONDERS) ===")
    print(report_df.to_string(index=False))

if __name__ == "__main__":
    run_nonresponse_bias()