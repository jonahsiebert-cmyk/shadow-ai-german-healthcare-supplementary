# -*- coding: utf-8 -*-
"""
03_governance_index.py

Composite governance index (Section 4.3, Table 2): the unweighted sum of the
three binary components gov_ai_tools, gov_training and gov_guidelines, each
coded 1 where the respondent reported the measure as in place and 0 otherwise,
with 'do not know' and 'cannot say' coded 0. Construction is documented in
documentation/governance_index_construction.pdf. The index is descriptive; it
is not entered into the regression models of Table 3.

Input: analytical_sample.csv. Output: analytical_sample.csv with the column
governance_index added, and table2_governance_index_by_setting.csv.
"""
import pandas as pd

IN_CSV = "analytical_sample.csv"
OUT_TABLE = "table2_governance_index_by_setting.csv"
SETTING_ORDER = ["Hospital", "Medical care centre", "Practice"]


def main():
    df = pd.read_csv(IN_CSV)
    df["governance_index"] = df["gov_ai_tools"] + df["gov_training"] + df["gov_guidelines"]

    idx = pd.crosstab(df["setting_en"], df["governance_index"], normalize="index") * 100
    idx = idx.reindex(SETTING_ORDER).reindex(columns=[0, 1, 2, 3], fill_value=0)
    idx.loc["Overall"] = df["governance_index"].value_counts(normalize=True).reindex([0, 1, 2, 3]) * 100

    comp = df.groupby("setting_en")[["gov_ai_tools", "gov_training", "gov_guidelines"]].mean() * 100
    comp = comp.reindex(SETTING_ORDER)
    comp.loc["Overall"] = df[["gov_ai_tools", "gov_training", "gov_guidelines"]].mean() * 100
    comp.columns = ["Tools", "Training", "Guidelines"]

    counts = df["setting_en"].value_counts().reindex(SETTING_ORDER)
    counts.loc["Overall"] = len(df)

    table2 = pd.concat([idx.round(2), comp.round(2), counts.rename("n")], axis=1)
    table2.index.name = "Setting"
    print("=== Table 2 ===\n" + table2.to_string())

    # Checks against the published figures. Note that the Overall row of the
    # three component columns must read 30.63 / 18.44 / 8.75 (n = 320).
    assert list(table2.loc["Overall", [0, 1, 2, 3]].round(2)) == [60.31, 26.25, 8.75, 4.69]
    assert list(table2.loc["Overall", ["Tools", "Training", "Guidelines"]].round(2)) == [30.63, 18.44, 8.75]
    assert list(table2.loc["Hospital", [0, 1, 2, 3]].round(2)) == [64.08, 26.06, 7.04, 2.82]

    table2.to_csv(OUT_TABLE, encoding="utf-8")
    df.to_csv(IN_CSV, index=False, encoding="utf-8")
    print(f"\nTable 2 written to {OUT_TABLE}; governance_index added to {IN_CSV}.")


if __name__ == "__main__":
    main()
