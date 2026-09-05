# -*- coding: utf-8 -*-
"""
04_regression_main.py

Table 3 of the manuscript: two binary logistic regressions with an identical
predictor set, estimated by maximum likelihood on the analytical sample
(n = 320).

  Primary model    shadow_own_use  ~ gov_ai_tools + gov_guidelines + gov_training
                                     + male + age + institutional
  Secondary model  shadow_exposure ~ same predictors

These correspond to Specifications 19 (own use) and 17 (exposure) of
results/sensitivity_analysis_report.pdf. Age enters as a single ordinal
predictor; the odds ratio refers to a one-category increase. In the
sensitivity report the lowest band is coded 0, so age is entered here as
age_ordinal - 1 to reproduce the intercepts printed in Table 3. This affects
the intercept only.

Also reported: variance inflation factors (Section 4.4, all <= 1.33) and the
Hosmer-Lemeshow test (ten groups of predicted probability).

Input: analytical_sample.csv. Output: table3_regression_main.csv (both models).
"""
import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from scipy.stats import chi2
from statsmodels.stats.outliers_influence import variance_inflation_factor

IN_CSV = "analytical_sample.csv"
OUT_CSV = "table3_regression_main.csv"
PREDICTORS = ["gov_ai_tools", "gov_guidelines", "gov_training", "male", "age", "institutional"]
LABELS = {"Intercept": "(Intercept)", "gov_ai_tools": "AI provision by employer",
          "gov_guidelines": "Guidelines on AI use", "gov_training": "AI-specific training",
          "male": "Male", "age": "Age (ordinal)", "institutional": "Hospital or medical care centre"}
FORMULA = "{dv} ~ " + " + ".join(PREDICTORS)


def hosmer_lemeshow(y, p, groups=10):
    """Hosmer-Lemeshow goodness-of-fit statistic with groups of equal size."""
    order = np.argsort(p)
    y, p = np.asarray(y)[order], np.asarray(p)[order]
    bins = np.array_split(np.arange(len(p)), groups)
    stat = 0.0
    for b in bins:
        o1, e1 = y[b].sum(), p[b].sum()
        o0, e0 = len(b) - o1, len(b) - e1
        stat += (o1 - e1) ** 2 / e1 + (o0 - e0) ** 2 / e0
    return stat, 1 - chi2.cdf(stat, groups - 2)


def fit(df, dv):
    model = smf.logit(FORMULA.format(dv=dv), data=df).fit(disp=0)
    ci = np.exp(model.conf_int())
    table = pd.DataFrame({
        "Predictor": [LABELS[k] for k in model.params.index],
        "Coef": model.params.values, "SE": model.bse.values, "z": model.tvalues.values,
        "p": model.pvalues.values, "OR": np.exp(model.params.values),
        "OR 2.5%": ci[0].values, "OR 97.5%": ci[1].values})
    hl_stat, hl_p = hosmer_lemeshow(model.model.endog, model.predict())
    fitstats = {"N": int(model.nobs), "LLR chi2": model.llr, "LLR df": int(model.df_model),
                "LLR p": model.llr_pvalue, "Pseudo R2 (McFadden)": model.prsquared,
                "AIC": model.aic, "BIC": model.bic, "Hosmer-Lemeshow chi2": hl_stat,
                "Hosmer-Lemeshow p": hl_p}
    return model, table, fitstats


def main():
    df = pd.read_csv(IN_CSV)
    assert len(df) == 320
    df["age"] = df["age_ordinal"] - 1

    X = sm.add_constant(df[PREDICTORS])
    vif = pd.Series([variance_inflation_factor(X.values, i) for i in range(1, X.shape[1])],
                    index=[LABELS[k] for k in PREDICTORS])
    print("=== Variance inflation factors ===\n" + vif.round(2).to_string())
    assert vif.max() <= 1.33

    out = []
    for name, dv in [("Own use (primary)", "shadow_own_use"), ("Exposure (secondary)", "shadow_exposure")]:
        model, table, fs = fit(df, dv)
        print(f"\n=== {name}: {dv} ===")
        print(table.round(3).to_string(index=False))
        print("\n".join(f"{k}: {v:.3f}" if isinstance(v, float) else f"{k}: {v}" for k, v in fs.items()))
        table.insert(0, "Model", name)
        for k, v in fs.items():
            table[k] = v
        out.append(table)

    out = pd.concat(out, ignore_index=True)
    # Checks against Table 3
    own = out[out["Model"].str.startswith("Own")].set_index("Predictor")
    exp_ = out[out["Model"].str.startswith("Exposure")].set_index("Predictor")
    assert round(own.loc["Age (ordinal)", "OR"], 2) == 0.61 and round(own.loc["Male", "OR"], 2) == 1.75
    assert round(exp_.loc["AI provision by employer", "OR"], 2) == 1.83
    assert round(exp_.loc["Hospital or medical care centre", "OR"], 2) == 1.76
    assert round(own["AIC"].iloc[0], 2) == 375.50 and round(exp_["AIC"].iloc[0], 2) == 401.42
    out.to_csv(OUT_CSV, index=False, encoding="utf-8")
    print(f"\nTable 3 (both models) written to {OUT_CSV}.")


if __name__ == "__main__":
    main()
