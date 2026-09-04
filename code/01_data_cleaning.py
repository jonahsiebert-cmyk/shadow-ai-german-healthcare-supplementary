# -*- coding: utf-8 -*-
"""
01_data_cleaning.py
Importiert, bereinigt und transformiert die Rohdaten von Wide in Long.
Erstellt den Pickle-Speicherstand 'processed_long_df.pkl'.
"""

import pandas as pd

def clean_data(input_path="dataClassified_2.csv", output_path="processed_long_df.pkl"):
    df = pd.read_csv(input_path, encoding='latin1', sep=';')

    id_col = df.columns[0]
    all_cols = df.columns[1:]

    long_df_raw = df.melt(
        id_vars=id_col,
        value_vars=all_cols,
        var_name="question",
        value_name="answer"
    )

    long_df_raw["question"] = long_df_raw["question"].str.strip()

    # Mapping der Fragen-IDs
    unique_questions = long_df_raw["question"].unique()
    q_map = {}
    m = 0

    for idx, q in enumerate(unique_questions):
        if 0 <= idx <= 4:
            q_map[q] = 0
        elif 5 <= idx <= 16:
            m += 1
            q_map[q] = m
        elif 16 <= idx <= 34:
            q_map[q] = 13
        else:
            m += 1
            q_map[q] = m

    long_df_raw["question_id"] = long_df_raw["question"].map(q_map)

    # Split von Multiple-Choice-Antworten
    skip_ids = [17, 18, 30, 31]
    can_transform = ~long_df_raw["question_id"].isin(skip_ids)

    long_df_raw.loc[can_transform, "answer"] = (
        long_df_raw.loc[can_transform, "answer"].astype(str).str.split(";")
    )

    long_df_raw = long_df_raw.explode("answer")
    long_df_raw["answer"] = long_df_raw["answer"].astype(str).str.strip()
    long_df_raw = long_df_raw[long_df_raw["answer"] != ""]

    # Numerische Konvertierung
    numeric_ids = [17]
    mask_numeric = long_df_raw["question_id"].isin(numeric_ids)
    long_df_raw.loc[mask_numeric, "answer"] = pd.to_numeric(
        long_df_raw.loc[mask_numeric, "answer"], errors='coerce'
    )

    long_df = long_df_raw.dropna(subset=["question_id"]).copy()

    # Stichproben-Filterung nach Anbieter-Typ
    required_answers = [
        "Krankenhaus", "MVZ", "MVZ (Medizinisches Versorgungszentrum)", 
        "Praxis", "Krankenhaus (stationär)", "Krankenhaus (ambulant)"
    ]
    valid_ids = long_df[
        (long_df["question_id"] == 6) & 
        (long_df["answer"].isin(required_answers))
    ]["ID"].unique()

    long_df = long_df[long_df["ID"].isin(valid_ids)].copy()
    long_df.to_pickle(output_path)
    print(f"[SUCCESS] Daten erfolgreich aufbereitet und unter '{output_path}' gespeichert.")

if __name__ == "__main__":
    clean_data()