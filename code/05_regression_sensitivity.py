# -*- coding: utf-8 -*-
"""
05_regression_sensitivity.py
Sensitivitätsanalysen: Prüft die Robustheit des Modells unter restriktiveren Kriterien.
"""

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

def run_sensitivity_analysis(input_path="df_with_governance.pkl"):
    long_df = pd.read_pickle(input_path)
    id_col = long_df.columns[0]

    # Strikte Definition für Zielvariable Q32 (Nur direkte Eigen-Nutzung)
    sub = long_df[long_df["question_id"] == 32].copy()
    sub["shadow_ai_strict"] = sub["answer"].apply(
        lambda x: 1 if "selbst schon mal" in str(x) else (0 if "Nein" in str(x) else None)
    )
    target_strict = sub.dropna(subset=["shadow_ai_strict"])[[id_col, "shadow_ai_strict"]].drop_duplicates(subset=[id_col])

    # Prädiktoren
    q17 = long_df[long_df["question_id"] == 17][[id_col, "answer"]].rename(columns={"answer": "digital_competence"})
    q17["digital_competence"] = pd.to_numeric(q17["digital_competence"], errors='coerce')

    gov = long_df[[id_col, "governance_index"]].drop_duplicates(subset=[id_col])

    sens_df = target_strict.merge(q17, on=id_col).merge(gov, on=id_col).dropna()

    model_sens = smf.logit(formula="shadow_ai_strict ~ digital_competence + governance_index", data=sens_df).fit()

    print("\n=== SENSITIVITÄTSANALYSE (STRIKTE SHADOW-AI DEFINITION) ===")
    print(model_sens.summary())

if __name__ == "__main__":
    run_sensitivity_analysis()