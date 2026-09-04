# Dense Regulation, Sparse Governance: Shadow AI Among Physicians in the German Healthcare System
Supplementary materials, analysis code, and reproduction package


VERSION
    1.1
    Last updated: 4 September 2026

STATUS
    This repository accompanies the camera-ready version of the paper
    (Proceedings of the 60th Hawaii International Conference on System
    Sciences, HICSS 2027). See CITATION.cff.

--------------------------------------------------------------------------------
1. OVERVIEW OF THE STUDY
--------------------------------------------------------------------------------

This repository documents the data preparation, measurement, and statistical
analysis reported in the accompanying manuscript, a cross-sectional survey of
320 physicians in the German healthcare system conducted between December 2025
and March 2026. It provides the materials referenced in the manuscript as
"Supplements", the analysis code, and the aggregated tables required to
regenerate every published figure and table.

Individual-level microdata are NOT contained in this repository for privacy
reasons. See Section 6, Data availability.

--------------------------------------------------------------------------------
2. REPOSITORY STRUCTURE
--------------------------------------------------------------------------------

    shadow-ai-german-healthcare-supplementary/
    |
    |-- README.md                          this file
    |-- LICENSE.txt                        licence for code and materials
    |-- CITATION.cff                       how to cite the paper and this repository
    |
    |-- instrument/
    |     questionnaire_de.pdf             full questionnaire, German original
    |     questionnaire_en.pdf             full questionnaire, English translation
    |
    |-- documentation/
    |     strobe_flow_diagram.pdf          sample derivation, 403 to 320
    |     cleaning_and_aggregation_rules.pdf
    |     codebook.csv                     variable names, coding, value labels, key to the sensitivity report
    |     governance_index_construction.pdf
    |     nonresponse_bias_analysis.pdf    early versus late respondents
    |
    |-- data/
    |     README_data.txt                  microdata access conditions
    |     aggregated/
    |        table1_sample_characteristics.csv
    |        table2_governance_index_by_setting.csv
    |        table3_regression_main.csv
    |        federal_state_distribution.csv
    |        application_areas.csv
    |
    |-- code/
    |     requirements.txt                 pinned dependency versions
    |     01_data_cleaning.py
    |     02_sample_descriptives.py
    |     03_governance_index.py
    |     04_regression_main.py
    |     05_regression_sensitivity.py
    |     06_nonresponse_bias.py
    |
    |-- results/
    |     sensitivity_analysis_report.pdf  all regression specifications with diagnostics
    |     figures/
    |        figure1_translation_model.pdf
    |        figure2.pdf
    |
    |-- ethics/
          ethics_approval_references.txt
          participant_information_sheet.pdf
          privacy_notice.pdf

--------------------------------------------------------------------------------
3. CONTENT DESCRIPTION
--------------------------------------------------------------------------------

**instrument/**
    The complete questionnaire as administered, in German, and the English
    translation prepared by the authors. The questionnaire was newly developed
    for this study and was not psychometrically validated. No back-translation
    was conducted. The core Shadow AI item is question 32.

**documentation/strobe_flow_diagram.pdf**
    Flow of respondents from the raw dataset (n = 403) to the final analytical
    sample (n = 320). Stages: exclusion of non-physicians, retired participants,
    Austrian and Swiss respondents, and records incomplete on key demographic
    variables (yielding n = 363); exclusion of respondents who selected "No
    answer" on the core Shadow AI item (n = 28, yielding n = 335); exclusion of
    heterogeneous low-frequency work settings (n = 15, yielding n = 320). One
    pilot participant who received the live link before the dispatch is
    retained in the sample.

**documentation/cleaning_and_aggregation_rules.pdf**
    The full set of inclusion and exclusion criteria applied at each stage, and
    the rules by which response categories were aggregated (inpatient and
    outpatient hospital settings combined into "Hospital"; single and group
    practices combined into "Practice").

**documentation/codebook.csv**
    Variable definitions and coding for every item used in the analysis,
    including: the ordinal coding of the six age bands; the reference category
    for healthcare setting (ambulatory practice); the two dependent variables
    (own unauthorised AI use, the primary outcome: 1 = own use, 0 = otherwise;
    Shadow AI exposure, the secondary outcome: 1 = own use or observation of a
    colleague, 0 = no case known); and the governance-index coding rule, under
    which responses of "do not know" or "cannot say" on a component item are
    coded as the measure not being in place. The codebook also maps the German
    variable labels used in the sensitivity report to the English labels used
    in the paper, and states that the flag "AI Users Only" in that report
    denotes the own use dependent variable, not a restricted sample.

**documentation/governance_index_construction.pdf**
    Construction of the composite governance index (0 to 3), its adaptation from
    the general governance dimensions of Klotz et al. (2019), and the stated
    omission of the monitoring and identification dimension as non-observable
    through physician self-report.

**documentation/nonresponse_bias_analysis.pdf**
    Comparison of early respondents (within 48 hours of the initial dispatch on
    17 December 2025, n = 126) and late respondents (on or after the reminder on
    27 January 2026, n = 145) on gender, age band, healthcare setting and the
    Shadow AI item, with chi-square tests of independence and Cramér's V.

**data/aggregated/**
    The aggregated tables required to regenerate the published descriptives,
    governance distributions and regression tables. These files allow the
    published numbers to be reproduced without access to the microdata. The
    reference statistics of the German Medical Association used for the
    goodness-of-fit tests and the age standardisation are published at
    https://www.bundesaerztekammer.de/fileadmin/user_upload/BAEK/Ueber_uns/Statistik/AErztestatistik_2025.pdf
    (last checked 4 September 2026).

**code/**
    Python scripts reproducing each analysis stage from a prepared dataset.
    Run order follows the file numbering. 04_regression_main.py estimates the
    exposure model (Table 3, right-hand columns; Specification 17 of the
    sensitivity report). 05_regression_sensitivity.py estimates the own use
    model, which is the primary specification in the paper (Table 3, left-hand
    columns; Specification 19), together with the further specifications in the
    sensitivity report. 06_nonresponse_bias.py reproduces
    documentation/nonresponse_bias_analysis.pdf. figure2_regenerate.py
    reproduces Figure 2 from the counts by setting.

**results/**
    The sensitivity analysis report with all regression specifications,
    coefficients, standard errors, z-values, p-values, odds ratios, confidence
    intervals, VIF diagnostics (all at or below 1.33) and Hosmer-Lemeshow tests.
    Specifications 17 and 19 correspond to Table 3 of the paper. Figure source
    files are provided.

**ethics/**
    Ethics approval references and the participant-facing documents preceding
    the questionnaire.

--------------------------------------------------------------------------------
4. SOFTWARE ENVIRONMENT
--------------------------------------------------------------------------------

    Language:   Python 3.12.13
    Libraries:  pandas, scipy (scipy.stats), statsmodels, matplotlib
    Original execution environment: Google Colab

    Exact versions are pinned in code/requirements.txt. To create a matching
    environment:

        python3.12 -m venv venv
        source venv/bin/activate
        pip install -r code/requirements.txt

--------------------------------------------------------------------------------
5. REPRODUCING THE ANALYSIS
--------------------------------------------------------------------------------

    Published figures and tables can be regenerated from the aggregated files in
    data/aggregated/ using the scripts in code/.

    Full re-estimation of the regression models and of the non-response
    comparison requires the individual-level microdata, which are not included
    in this repository (see Section 6). With the microdata placed in data/
    under the variable names given in the codebook, scripts 01 through 06
    reproduce the reported results when run in order.

--------------------------------------------------------------------------------
6. DATA AVAILABILITY
--------------------------------------------------------------------------------

    Individual-level microdata are not shared publicly. They are available from
    the corresponding authors on reasonable request, under a data-use agreement
    consistent with the ethics approvals governing the study.

    This repository contains aggregated data sufficient to reproduce every
    published figure and table. It does not contain data sufficient to re-run
    the participant-level regressions; those require the microdata above.

--------------------------------------------------------------------------------
7. ETHICS
--------------------------------------------------------------------------------

    The study received favourable ethics opinions from the University of
    Cambridge (Ref. 736, 15 May 2025) and Offenburg University of Applied
    Sciences (Ref. 04-25, 27 June 2025). Data collection was conducted in
    compliance with the General Data Protection Regulation (GDPR). A privacy
    notice and participant information sheet preceded the questionnaire;
    participation was conditional on informed consent.

--------------------------------------------------------------------------------
8. LICENCE
--------------------------------------------------------------------------------

    Code (code/) is released under the MIT License. Documentation, the
    questionnaire, aggregated data and results are released under the Creative
    Commons Attribution 4.0 International licence (CC BY 4.0). See LICENSE.txt.

--------------------------------------------------------------------------------
9. CITATION
--------------------------------------------------------------------------------

    See CITATION.cff. Paper:

    Perret, S., Siebert, J., Baumann, J., & Schinle, M. (2027). Dense
    Regulation, Sparse Governance: Shadow AI Among Physicians in the German
    Healthcare System. In Proceedings of the 60th Hawaii International
    Conference on System Sciences (HICSS). [pages and DOI to be added]

--------------------------------------------------------------------------------
10. CONTACT
--------------------------------------------------------------------------------

    Corresponding authors: Sophie Perret (scp64@cam.ac.uk) and
    Jonah Siebert (jonah.siebert@hs-offenburg.de)
================================================================================

