# -*- coding: utf-8 -*-
"""
04_regression_main.py
Hauptmodell: Logistische Regression der Shadow-AI-Nutzung.
Enthält auch Multikollinearitätsprüfungen (VIF).
"""

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from statsmodels.stats.outliers_influence import variance_inflation_factor

def run_main_regression(input_path="df_with_governance.pkl"):
    long_df = pd.read_pickle(input_path)
    id_col = long_df.columns[0]

    # Zielvariable Q32 (Shadow AI)
    sub = long_df[long_df["question_id"] == 32].copy()
    sub["shadow_ai"] = sub["answer"].apply(
        lambda x: 1 if "Ja" in str(x) else (0 if "Nein" in str(x) else None)
    )
    target = sub.dropna(subset=["shadow_ai"])[[id_col, "shadow_ai"]].drop_duplicates(subset=[id_col])

    # Digital Competence (Q17)
    q17 = long_df[long_df["question_id"] == 17][[id_col, "answer"]].rename(columns={"answer": "digital_competence"})
    q17["digital_competence"] = pd.to_numeric(q17["digital_competence"], errors='coerce')

    # Experience (Q9)
    age_map = {"0-4 Jahre": 2.0, "5-9 Jahre": 7.0, "10-14 Jahre": 12.0, "15-19 Jahre": 17.0, "20-25 Jahre": 22.5, ">25 Jahre": 25.0}
    q9 = long_df[long_df["question_id"] == 9][[id_col, "answer"]].rename(columns={"answer": "experience"})
    q9["experience"] = q9["experience"].map(age_map)

    # Governance Index
    gov = long_df[[id_col, "governance_index"]].drop_duplicates(subset=[id_col])

    # Dataset Merge
    model_data = target.merge(q17, on=id_col).merge(q9, on=id_col).merge(gov, on=id_col).dropna()

    # VIF Diagnostics
    vif_features = model_data[["digital_competence", "experience", "governance_index"]]
    vif_df = pd.DataFrame({
        "Feature": vif_features.columns,
        "VIF": [variance_inflation_factor(vif_features.values, i) for i in range(vif_features.shape[1])]
    })
    print("\n=== VIF DIAGNOSTICS ===")
    print(vif_df.to_string(index=False))

    # Logistische Regression
    formula = "shadow_ai ~ digital_competence + experience + governance_index"
    model = smf.logit(formula=formula, data=model_data).fit()

    print("\n=== REGRESSION RESULTS ===")
    print(model.summary())

    # Odds Ratios
    params = model.params
    conf = model.conf_int()
    conf['OR'] = params
    conf.columns = ['2.5%', '97.5%', 'OR']
    print("\nOdds Ratios (OR) and 95% CI:")
    print(np.exp(conf[['OR', '2.5%', '97.5%']]))

if __name__ == "__main__":
    run_main_regression()