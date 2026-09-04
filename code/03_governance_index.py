# -*- coding: utf-8 -*-
"""
03_governance_index.py
Berechnet den Composite Governance Index aus Governance-/Richtlinien-Items
und speichert das erweiterte Dataset.
"""

import pandas as pd

def compute_governance_index(input_path="processed_long_df.pkl", output_path="df_with_governance.pkl"):
    long_df = pd.read_pickle(input_path)
    id_col = long_df.columns[0]

    # Auswahl der Governance-relevanten Fragen (z.B. Q20, Q21, Q22)
    gov_ids = [20, 21, 22]
    gov_sub = long_df[long_df["question_id"].isin(gov_ids)].copy()

    # Binarisierung / Scoring
    gov_sub["score"] = gov_sub["answer"].apply(
        lambda x: 1 if any(pos in str(x).lower() for pos in ["ja", "vorhanden", "geregelt"]) else 0
    )

    # Aggregation pro Respondent
    gov_index = gov_sub.groupby(id_col)["score"].sum().reset_index()
    gov_index.rename(columns={"score": "governance_index"}, inplace=True)

    print("\n=== GOVERNANCE INDEX DESKRIPTION ===")
    print(gov_index["governance_index"].describe())

    # Zusammenführung mit dem Hauptdatensatz
    merged_df = long_df.merge(gov_index, on=id_col, how="left")
    merged_df["governance_index"] = merged_df["governance_index"].fillna(0)
    
    merged_df.to_pickle(output_path)
    print(f"[SUCCESS] Governance Index berechnet und unter '{output_path}' gespeichert.")

if __name__ == "__main__":
    compute_governance_index()