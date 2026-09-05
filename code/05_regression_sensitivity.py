# -*- coding: utf-8 -*-
"""
05_regression_sensitivity.py

Re-estimates the specification grid of results/sensitivity_analysis_report.pdf
and two additional specifications.

Grid (report Specifications 1 to 24; 18 and 20 duplicate 17 and 19, see
results/note_to_sensitivity_analysis_report.md):
  age            ordinal (one category increase, lowest band coded 0) or
                 categorical (five dummies, reference 40 to 49 years)
  setting        hospital and medical care centre bundled (institutional) or
                 entered as two separate dummies (reference: practice)
  governance     three binary components or the composite index (0 to 3)
  outcome        shadow_own_use ("AI Users Only" = 1 in the report) or
                 shadow_exposure

Additional specifications (A1, A2): the Table 3 models with 'do not know'
responses on tool provision and guidelines treated as missing rather than as
0, which reduces the sample (Section 4.3 of the manuscript states the coding
decision; these specifications show its consequence).

Input: analytical_sample.csv (after 03_governance_index.py).
Output: sensitivity_specifications.csv, one row per coefficient.
"""
import itertools
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

IN_CSV = "analytical_sample.csv"
OUT_CSV = "sensitivity_specifications.csv"
CHECKS = {  # (age_ordinal, bundled, gov_index, own_use): (pseudo R2, AIC) from the report
    (0, 0, 0, 0): (0.1366, 407.03), (0, 0, 0, 1): (0.0922, 377.37),
    (0, 0, 1, 0): (0.1213, 409.79), (0, 0, 1, 1): (0.0891, 374.56),
    (1, 1, 0, 0): (0.1266, 401.42), (1, 1, 0, 1): (0.0713, 375.50),
    (1, 1, 1, 0): (0.1121, 403.88), (1, 1, 1, 1): (0.0680, 372.77),
}


def formula(dv, age_ordinal, bundled, gov_index):
    age = "age0" if age_ordinal else "C(age_band, Treatment(reference='40-49 Jahre'))"
    setting = "institutional" if bundled else "hospital + mvz"
    gov = "governance_index" if gov_index else "gov_ai_tools + gov_guidelines + gov_training"
    return f"{dv} ~ {gov} + male + {age} + {setting}"


def tidy(model, spec, label):
    ci = np.exp(model.conf_int())
    return pd.DataFrame({
        "Specification": spec, "Description": label, "Term": model.params.index,
        "Coef": model.params.values, "SE": model.bse.values, "z": model.tvalues.values,
        "p": model.pvalues.values, "OR": np.exp(model.params.values),
        "OR 2.5%": ci[0].values, "OR 97.5%": ci[1].values, "N": int(model.nobs),
        "Pseudo R2": model.prsquared, "AIC": model.aic, "BIC": model.bic,
        "LLR p": model.llr_pvalue})


def main():
    df = pd.read_csv(IN_CSV)
    assert len(df) == 320 and "governance_index" in df.columns
    df["age0"] = df["age_ordinal"] - 1
    df["hospital"] = (df["setting_en"] == "Hospital").astype(int)
    df["mvz"] = (df["setting_en"] == "Medical care centre").astype(int)

    rows, spec = [], 0
    for age_ordinal, bundled, gov_index, own in itertools.product([0, 1], repeat=4):
        spec += 1
        dv = "shadow_own_use" if own else "shadow_exposure"
        label = (f"age={'ordinal' if age_ordinal else 'categorical'}, "
                 f"setting={'bundled' if bundled else 'separate'}, "
                 f"governance={'index' if gov_index else 'components'}, outcome={dv}")
        m = smf.logit(formula(dv, age_ordinal, bundled, gov_index), data=df).fit(disp=0)
        print(f"S{spec:02d} {label}: N = {int(m.nobs)}, pseudo R2 = {m.prsquared:.4f}, AIC = {m.aic:.2f}")
        key = (age_ordinal, bundled, gov_index, own)
        if key in CHECKS:
            r2, aic = CHECKS[key]
            assert round(m.prsquared, 4) == r2 and round(m.aic, 2) == aic, f"S{spec} deviates from the report"
        rows.append(tidy(m, f"S{spec:02d}", label))

    # Additional specifications: 'do not know' treated as missing
    sub = df[(df["tools_dont_know"] == 0) & (df["guidelines_dont_know"] == 0)]
    for tag, dv in [("A1", "shadow_own_use"), ("A2", "shadow_exposure")]:
        m = smf.logit(formula(dv, 1, 1, 0), data=sub).fit(disp=0)
        label = f"Table 3 model, 'do not know' on tools and guidelines set to missing, outcome={dv}"
        print(f"{tag} {label}: N = {int(m.nobs)}, pseudo R2 = {m.prsquared:.4f}, AIC = {m.aic:.2f}")
        t = tidy(m, tag, label)
        print(t[["Term", "OR", "OR 2.5%", "OR 97.5%", "p"]].round(3).to_string(index=False))
        rows.append(t)

    pd.concat(rows, ignore_index=True).to_csv(OUT_CSV, index=False, encoding="utf-8")
    print(f"\nAll specifications written to {OUT_CSV}.")


if __name__ == "__main__":
    main()
