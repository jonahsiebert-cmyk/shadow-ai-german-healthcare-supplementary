# -*- coding: utf-8 -*-
"""
07_sensitivity_report.py

Builds results/sensitivity_analysis_report.pdf from the outputs of
04_regression_main.py (table3_regression_main.csv) and
05_regression_sensitivity.py (sensitivity_specifications.csv).

Contents: coding and conventions; overview of all specifications; the two
Table 3 models; the sixteen grid specifications; the two additional
specifications; variance inflation factors.
"""
import re
import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                TableStyle, PageBreak, KeepTogether)

SPEC_CSV = "sensitivity_specifications.csv"
SAMPLE_CSV = "analytical_sample.csv"
OUT_PDF = "sensitivity_analysis_report.pdf"

TERM_LABELS = {
    "Intercept": "Intercept",
    "gov_ai_tools": "AI provision by employer",
    "gov_guidelines": "Guidelines on AI use",
    "gov_training": "AI-specific training",
    "governance_index": "Governance index (0 to 3)",
    "male": "Male",
    "age0": "Age (ordinal, one category increase)",
    "institutional": "Hospital or medical care centre",
    "hospital": "Hospital",
    "mvz": "Medical care centre",
}
AGE_DUMMY = re.compile(r"\[T\.(.+?)\]")
AGE_EN = {"20-29 Jahre": "20 to 29", "30-39 Jahre": "30 to 39", "50-59 Jahre": "50 to 59",
          "60-69 Jahre": "60 to 69", "70 Jahre oder älter": "70 and over"}
OUTCOME_EN = {"shadow_own_use": "Own use", "shadow_exposure": "Exposure"}
TABLE3 = {"S14": "Table 3, primary model (own use)", "S13": "Table 3, secondary model (exposure)"}


def label(term):
    if term in TERM_LABELS:
        return TERM_LABELS[term]
    m = AGE_DUMMY.search(term)
    if m:
        return f"Age {AGE_EN[m.group(1)]} (ref. 40 to 49)"
    return term


def parse(desc):
    d = dict(kv.split("=") for kv in desc.split(", ")) if "age=" in desc else {}
    return d


def fmt(x, nd=3):
    return f"{x:.{nd}f}"


def fmt_p(p):
    return "<.001" if p < 0.001 else f"{p:.3f}"


def coef_table(sub, styles):
    rows = [["Predictor", "Coef.", "SE", "z", "p", "OR", "95% CI"]]
    for _, r in sub.iterrows():
        rows.append([label(r["Term"]), fmt(r["Coef"]), fmt(r["SE"]), fmt(r["z"], 2),
                     fmt_p(r["p"]), fmt(r["OR"], 2), f"[{r['OR 2.5%']:.2f}, {r['OR 97.5%']:.2f}]"])
    t = Table(rows, colWidths=[62 * mm, 16 * mm, 14 * mm, 14 * mm, 14 * mm, 14 * mm, 28 * mm])
    t.setStyle(TableStyle([
        ("FONT", (0, 0), (-1, -1), "Helvetica", 8.5),
        ("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 8.5),
        ("LINEBELOW", (0, 0), (-1, 0), 0.6, colors.black),
        ("LINEABOVE", (0, 0), (-1, 0), 0.6, colors.black),
        ("LINEBELOW", (0, -1), (-1, -1), 0.6, colors.black),
        ("ALIGN", (1, 0), (-1, -1), "RIGHT"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2), ("TOPPADDING", (0, 0), (-1, -1), 2),
    ]))
    return t


def fit_line(r):
    return (f"N = {int(r['N'])}. LLR test p {fmt_p(r['LLR p'])}. McFadden pseudo R<super>2</super> = "
            f"{r['Pseudo R2']:.3f}. AIC = {r['AIC']:.2f}. BIC = {r['BIC']:.2f}.")


def spec_block(spec_id, sub, styles, title):
    d = parse(sub["Description"].iloc[0])
    r = sub.iloc[0]
    if d:
        conf = (f"Outcome: {OUTCOME_EN[d['outcome']]}. Age: {d['age']}"
                f"{' (youngest band coded 0)' if d['age'] == 'ordinal' else ' (five dummies, reference 40 to 49 years)'}. "
                f"Setting: {'hospital and medical care centre bundled' if d['setting'] == 'bundled' else 'hospital and medical care centre entered separately'} "
                f"(reference: practice). Governance: {'three binary components' if d['governance'] == 'components' else 'composite index, 0 to 3'}.")
    else:
        conf = sub["Description"].iloc[0].replace("outcome=shadow_own_use", "Outcome: Own use") \
            .replace("outcome=shadow_exposure", "Outcome: Exposure")
    return KeepTogether([
        Paragraph(f"<b>{spec_id}.</b> {title}", styles["spech"]),
        Paragraph(conf, styles["small"]),
        Spacer(1, 2 * mm),
        coef_table(sub, styles),
        Paragraph(fit_line(r), styles["small"]),
        Spacer(1, 5 * mm),
    ])


def main():
    spec = pd.read_csv(SPEC_CSV)
    df = pd.read_csv(SAMPLE_CSV)
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle("spech", parent=styles["Heading3"], spaceBefore=4, spaceAfter=2))
    styles.add(ParagraphStyle("small", parent=styles["BodyText"], fontSize=8.5, leading=11))
    body = styles["BodyText"]; body.fontSize = 9.5; body.leading = 12.5

    doc = SimpleDocTemplate(OUT_PDF, pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm,
                            topMargin=18 * mm, bottomMargin=18 * mm,
                            title="Sensitivity analysis report", author="Perret, Siebert, Baumann, Schinle")
    el = []
    el.append(Paragraph("Sensitivity Analysis Report", styles["Title"]))
    el.append(Paragraph("Dense Regulation, Sparse Governance: Shadow AI Among Physicians in the German "
                        "Healthcare System. Supplement to Section 4.4 and Table 3.", body))
    el.append(Spacer(1, 4 * mm))

    el.append(Paragraph("1. Sample, variables and conventions", styles["Heading2"]))
    el.append(Paragraph(
        "All models are binary logistic regressions estimated by maximum likelihood on the analytical "
        "sample of n = 320 physicians (Section 3.4 of the manuscript). Two outcomes are used. "
        "<b>Own use</b> is 1 where the respondent reported having used AI without formal approval "
        "(n = 95) and 0 otherwise. <b>Exposure</b> is 1 where the respondent reported own use or "
        "observation of colleagues (n = 161) and 0 where no case was known (n = 159). The exposure "
        "outcome is a superset of the own use outcome.", body))
    el.append(Paragraph(
        "Predictors. <b>AI provision by employer</b>, <b>AI-specific training</b> and <b>Guidelines on AI "
        "use</b> are binary; responses of 'do not know' or 'cannot say' are coded 0 (Section 4.3). The "
        "<b>governance index</b> is their unweighted sum (0 to 3) and replaces the three components in "
        "the specifications marked accordingly. <b>Male</b> is coded against female. <b>Age</b> enters "
        "either as one ordinal predictor across the six bands of the questionnaire, with the youngest "
        "band (20 to 29 years) coded 0 so that the odds ratio refers to a one category increase, or as "
        "five dummies with 40 to 49 years as the reference. <b>Setting</b> enters either as one dummy "
        "for hospital or medical care centre against ambulatory practice, or as two separate dummies "
        "for hospital and for medical care centre against practice.", body))
    el.append(Paragraph(
        "Specifications S01 to S16 cover every combination of outcome, age coding, setting coding and "
        "governance coding. S14 and S13 are the primary and secondary models of Table 3. A1 and A2 "
        "re-estimate the Table 3 models with 'do not know' responses on tool provision and guidelines "
        "treated as missing rather than as absent, which reduces the sample to n = 261. Variance "
        "inflation factors for the Table 3 predictor set are given in Section 6. All figures are "
        "produced by 04_regression_main.py, 05_regression_sensitivity.py and 07_sensitivity_report.py "
        "in the code directory of the repository.", body))

    # Overview table
    el.append(Paragraph("2. Overview of specifications", styles["Heading2"]))
    rows = [["Spec.", "Outcome", "Age", "Setting", "Governance", "N", "LLR p", "Pseudo R²", "AIC", "BIC"]]
    for sid, sub in spec.groupby("Specification", sort=False):
        r = sub.iloc[0]; d = parse(r["Description"])
        if d:
            rows.append([sid + (" *" if sid in TABLE3 else ""), OUTCOME_EN[d["outcome"]], d["age"], d["setting"],
                         d["governance"], int(r["N"]), fmt_p(r["LLR p"]), fmt(r["Pseudo R2"]), fmt(r["AIC"], 2), fmt(r["BIC"], 2)])
        else:
            rows.append([sid, OUTCOME_EN["shadow_own_use" if "own_use" in r["Description"] else "shadow_exposure"],
                         "ordinal", "bundled", "components, DK missing", int(r["N"]), fmt_p(r["LLR p"]),
                         fmt(r["Pseudo R2"]), fmt(r["AIC"], 2), fmt(r["BIC"], 2)])
    t = Table(rows, colWidths=[14 * mm, 18 * mm, 20 * mm, 18 * mm, 36 * mm, 10 * mm, 14 * mm, 18 * mm, 16 * mm, 16 * mm])
    t.setStyle(TableStyle([
        ("FONT", (0, 0), (-1, -1), "Helvetica", 8), ("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 8),
        ("LINEBELOW", (0, 0), (-1, 0), 0.6, colors.black), ("LINEABOVE", (0, 0), (-1, 0), 0.6, colors.black),
        ("LINEBELOW", (0, -1), (-1, -1), 0.6, colors.black), ("ALIGN", (5, 0), (-1, -1), "RIGHT"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 1.5), ("TOPPADDING", (0, 0), (-1, -1), 1.5),
    ]))
    el.append(t)
    el.append(Paragraph("* Table 3 of the manuscript: S14 primary model (own use), S13 secondary model (exposure). "
                        "DK missing: 'do not know' responses treated as missing.", styles["small"]))
    el.append(PageBreak())

    el.append(Paragraph("3. Table 3 models", styles["Heading2"]))
    for sid in ["S14", "S13"]:
        el.append(spec_block(sid, spec[spec["Specification"] == sid], styles, TABLE3[sid]))

    el.append(Paragraph("4. Specification grid", styles["Heading2"]))
    for sid, sub in spec.groupby("Specification", sort=False):
        if sid.startswith("S") and sid not in TABLE3:
            d = parse(sub["Description"].iloc[0])
            el.append(spec_block(sid, sub, styles,
                                 f"{OUTCOME_EN[d['outcome']]}, age {d['age']}, setting {d['setting']}, governance {d['governance']}"))

    el.append(Paragraph("5. Additional specifications: 'do not know' treated as missing", styles["Heading2"]))
    el.append(Paragraph(
        "Respondents answering 'do not know' or 'cannot say' on tool provision (n = 43) or 'do not know' "
        "on guidelines (n = 27) are excluded (59 respondents, some answering both), leaving n = 261. "
        "Predictor set and coding otherwise as in Table 3.", body))
    for sid, title in [("A1", "Own use, Table 3 specification, n = 261"), ("A2", "Exposure, Table 3 specification, n = 261")]:
        el.append(spec_block(sid, spec[spec["Specification"] == sid], styles, title))

    el.append(Paragraph("6. Variance inflation factors, Table 3 predictor set", styles["Heading2"]))
    df["age0"] = df["age_ordinal"] - 1
    preds = ["gov_ai_tools", "gov_guidelines", "gov_training", "male", "age0", "institutional"]
    X = sm.add_constant(df[preds])
    vifs = [variance_inflation_factor(X.values, i) for i in range(1, X.shape[1])]
    rows = [["Predictor", "VIF"]] + [[label(p), f"{v:.2f}"] for p, v in zip(preds, vifs)]
    t = Table(rows, colWidths=[80 * mm, 20 * mm])
    t.setStyle(TableStyle([("FONT", (0, 0), (-1, -1), "Helvetica", 8.5), ("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 8.5),
                           ("LINEBELOW", (0, 0), (-1, 0), 0.6, colors.black), ("LINEABOVE", (0, 0), (-1, 0), 0.6, colors.black),
                           ("LINEBELOW", (0, -1), (-1, -1), 0.6, colors.black), ("ALIGN", (1, 0), (1, -1), "RIGHT")]))
    el.append(t)
    el.append(Paragraph(f"Maximum VIF = {max(vifs):.2f}. The predictors are identical in both Table 3 models, "
                        "so the factors apply to both.", styles["small"]))

    doc.build(el)
    print(f"Report written to {OUT_PDF}")


if __name__ == "__main__":
    main()
