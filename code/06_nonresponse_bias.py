# -*- coding: utf-8 -*-
"""
06_nonresponse_bias.py

Early versus late respondent comparison as described in Section 3.3 of the
manuscript. Early = responses started within 48 hours of the initial dispatch
(17 December 2025); late = responses started on or after the reminder
(27 January 2026). Dispatch times are taken as the time of the first response
on each day. Responses between the two windows are reported and excluded from
the comparison.

Chi square tests of independence with Cramer's V on gender, age band,
healthcare setting and the Shadow AI item, analytical sample (n = 320).

Input: the cleaned dataset dataClassified_2.csv (n = 335, semicolon separated,
cp1252). The 15 records with setting "Sonstige" are removed here, yielding the
analytical sample. Output: nonresponse_bias_results.csv and console tables.
"""
import numpy as np
import pandas as pd
from scipy.stats import chi2_contingency

RAW_CSV = "dataClassified_2.csv"
DISPATCH_1 = pd.Timestamp("2025-12-17 10:37:57")
DISPATCH_2 = pd.Timestamp("2026-01-27 11:28:00")
EARLY_WINDOW_HOURS = 48

# column positions in the export (see documentation/codebook.csv)
COL_TIME, COL_AGE, COL_GENDER, COL_SETTING, COL_SHADOW = 1, 8, 10, 11, 55
TIME_FORMAT = "%m.%d.%y %H:%M:%S"

LABELS = {
    "Gender": {"weiblich": "Female", "männlich": "Male"},
    "Age band": {"20-29 Jahre": "20 to 29", "30-39 Jahre": "30 to 39", "40-49 Jahre": "40 to 49",
                 "50-59 Jahre": "50 to 59", "60-69 Jahre": "60 to 69", "70 Jahre oder älter": "70 and over"},
    "Healthcare setting": {"Krankenhaus": "Hospital", "MVZ (Medizinisches Versorgungszentrum)": "Medical care centre",
                           "Praxis": "Practice"},
    "Shadow AI item": {"Ja, habe selbst schon mal KI ohne formelle Genehmigung genutzt.": "Own use",
                       "Ja, habe andere schon mal KI ohne formelle Genehmigung nutzen sehen.": "Observation of colleagues",
                       "Nein, mir ist kein Fall bekannt": "No case known"},
}
COLS = {"Gender": COL_GENDER, "Age band": COL_AGE, "Healthcare setting": COL_SETTING, "Shadow AI item": COL_SHADOW}


def clean(s):
    return s.astype(str).str.replace("\\xa0", "", regex=False).str.replace("\xa0", "").str.strip()


def cramers_v(chi2, n, r, c):
    return float(np.sqrt(chi2 / (n * (min(r, c) - 1))))


def main():
    df = pd.read_csv(RAW_CSV, encoding="cp1252", sep=";")
    df = df[clean(df.iloc[:, COL_SETTING]) != "Sonstige"].copy()
    assert len(df) == 320, f"expected analytical sample of 320, got {len(df)}"

    t = pd.to_datetime(df.iloc[:, COL_TIME], format=TIME_FORMAT)
    early = (t >= DISPATCH_1) & (t < DISPATCH_1 + pd.Timedelta(hours=EARLY_WINDOW_HOURS))
    late = t >= DISPATCH_2
    df["wave"] = np.select([early, late], ["Early", "Late"], default="Between")
    print("Wave assignment:\n" + df["wave"].value_counts().to_string())
    print(f"Responses before the first dispatch: {(t < DISPATCH_1).sum()} (pilot participant with early live link)")

    sub = df[df["wave"].isin(["Early", "Late"])]
    rows = []
    for name, ci in COLS.items():
        s = clean(sub.iloc[:, ci]).map(LABELS[name])
        ct = pd.crosstab(s, sub["wave"]).reindex(list(LABELS[name].values()))[["Early", "Late"]]
        chi2, p, dof, expected = chi2_contingency(ct)
        v = cramers_v(chi2, ct.values.sum(), *ct.shape)
        print(f"\n=== {name} ===\n{ct.to_string()}")
        print(f"chi2({dof}) = {chi2:.2f}, p = {p:.3f}, Cramer's V = {v:.2f}, n = {ct.values.sum()}, "
              f"min expected = {expected.min():.1f}")
        rows.append({"Variable": name, "chi2": round(chi2, 2), "df": dof, "p": round(p, 3),
                     "Cramers_V": round(v, 2), "n": int(ct.values.sum()), "min_expected": round(float(expected.min()), 1)})

    pd.DataFrame(rows).to_csv("nonresponse_bias_results.csv", index=False)
    print("\nSummary written to nonresponse_bias_results.csv")


if __name__ == "__main__":
    main()
