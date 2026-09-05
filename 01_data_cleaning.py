# -*- coding: utf-8 -*-
"""
01_data_cleaning.py

Builds the analytical dataset from the cleaned Microsoft Forms export
dataClassified_2.csv (n = 335, semicolon separated, cp1252). The 15 records
with setting "Sonstige" are removed, yielding the analytical sample of n = 320
(Section 3.4 of the manuscript). All variables used in the manuscript are
derived here under the names given in documentation/codebook.csv and written
to analytical_sample.csv, which scripts 02 to 05 read.

Column positions in the export follow documentation/codebook.csv.
"""
import pandas as pd

RAW_CSV = "dataClassified_2.csv"
OUT_CSV = "analytical_sample.csv"

COL = {
    "id": 0, "start_time": 1, "age_band": 8, "federal_state": 9, "gender": 10,
    "setting": 11, "experience_band": 14, "tool_provision": 37,
    "ai_use_frequency": 42, "application_areas": 43, "training": 45,
    "training_mode": 46, "shadow_ai_item": 55, "guidelines": 56,
}

AGE_ORDER = ["20-29 Jahre", "30-39 Jahre", "40-49 Jahre", "50-59 Jahre",
             "60-69 Jahre", "70 Jahre oder älter"]
OWN_USE = "Ja, habe selbst schon mal KI ohne formelle Genehmigung genutzt."
OBSERVED = "Ja, habe andere schon mal KI ohne formelle Genehmigung nutzen sehen."
NO_CASE = "Nein, mir ist kein Fall bekannt"


def clean(s):
    """Strip non-breaking spaces and surrounding whitespace from a string column."""
    return s.astype(str).str.replace("\xa0", "", regex=False).str.strip()


def build_analytical_sample(raw_csv=RAW_CSV, out_csv=OUT_CSV):
    raw = pd.read_csv(raw_csv, encoding="cp1252", sep=";")
    assert len(raw) == 335, f"expected 335 cleaned records, got {len(raw)}"

    df = pd.DataFrame({name: clean(raw.iloc[:, pos]) for name, pos in COL.items()})
    df["id"] = df["id"].astype(int)

    # Analytical sample: exclusion of heterogeneous low-frequency settings
    df = df[df["setting"] != "Sonstige"].copy()
    assert len(df) == 320, f"expected analytical sample of 320, got {len(df)}"

    # Structural variables
    df["age_ordinal"] = df["age_band"].map({b: i + 1 for i, b in enumerate(AGE_ORDER)})
    df["male"] = (df["gender"] == "männlich").astype(int)
    df["institutional"] = (df["setting"] != "Praxis").astype(int)
    df["setting_en"] = df["setting"].map({
        "Krankenhaus": "Hospital",
        "MVZ (Medizinisches Versorgungszentrum)": "Medical care centre",
        "Praxis": "Practice"})

    # Governance components: 'do not know' and 'cannot say' coded 0 (Section 4.3)
    df["gov_ai_tools"] = (df["tool_provision"] == "Ja").astype(int)
    df["gov_training"] = (df["training"] == "Ja").astype(int)
    df["gov_guidelines"] = (df["guidelines"] == "Ja").astype(int)
    df["tools_dont_know"] = df["tool_provision"].str.startswith("Weiß").astype(int)
    df["guidelines_dont_know"] = df["guidelines"].str.startswith("Weiß").astype(int)

    # Dependent variables
    assert set(df["shadow_ai_item"]) == {OWN_USE, OBSERVED, NO_CASE}, \
        "unexpected response category on the Shadow AI item"
    df["shadow_own_use"] = (df["shadow_ai_item"] == OWN_USE).astype(int)
    df["shadow_exposure"] = df["shadow_ai_item"].isin([OWN_USE, OBSERVED]).astype(int)

    # Checks against the published figures (Section 4.2)
    assert df["shadow_own_use"].sum() == 95 and df["shadow_exposure"].sum() == 161
    assert df["age_ordinal"].notna().all() and df["setting_en"].notna().all()

    df.to_csv(out_csv, index=False, encoding="utf-8")
    print(f"Analytical sample written to {out_csv}: n = {len(df)}")
    print(df["setting_en"].value_counts().to_string())
    return df


if __name__ == "__main__":
    build_analytical_sample()
