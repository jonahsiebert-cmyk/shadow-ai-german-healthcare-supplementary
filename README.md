# Dense Regulation, Sparce Governance: Shadow AI among Physicians in the German Healthcare System
Supplementary materials, analysis code, and reproduction package


VERSION
    1.0
    Last updated: 16. Juni 2026

STATUS
    This repository accompanies a manuscript under double-blind review. All
    author names, institutional affiliations, and identifying contact details
    have been removed. They are to be completed for the camera-ready version.


--------------------------------------------------------------------------------
1. OVERVIEW OF THE STUDY
--------------------------------------------------------------------------------

This repository documents the data preparation, measurement, and statistical
analysis reported in the accompanying manuscript, a cross-sectional survey of
320 physicians in the German healthcare system conducted between December 2025
and February 2026. It provides the materials referenced in the manuscript as
"Supplements", the analysis code, and the aggregated tables required to
regenerate every published figure and table.

Individual-level microdata are NOT contained in this repository for privacy reasons. 
See Section 6, Data availability.

--------------------------------------------------------------------------------
2. REPOSITORY STRUCTURE
--------------------------------------------------------------------------------

    shadow-ai-physicians-germany/
    |
    |-- README.txt                         this file
    |-- LICENSE.txt                        licence for code and materials
    |-- CITATION.txt                       how to cite this repository
    |
    |-- instrument/
    |     questionnaire_de.pdf             full questionnaire, German original
    |     questionnaire_en.pdf             full questionnaire, English translation
    |
    |-- documentation/
    |     strobe_flow_diagram.pdf          sample derivation, 403 to 320
    |     cleaning_and_aggregation_rules.pdf
    |     codebook.csv                     variable names, coding, value labels
    |     governance_index_construction.pdf
    |     nonresponse_bias_analysis.pdf    early vs late respondents
    |
    |-- data/
    |     README_data.txt                  microdata access conditions
    |     aggregated/
    |        table1_sample_characteristics.csv
    |        table2_governance_index_by_setting.csv
    |        table3_regression_main.csv
    |        federal_state_distribution.csv
    |        application_areas.csv
    |        reference_statistics_baek_2025.csv
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
    |     regression_main_full.csv         all coefficients, SE, z, p, OR, CI
    |     regression_sensitivity_full.csv  own-use-only model
    |     vif_diagnostics.csv              multicollinearity check
    |     goodness_of_fit_tests.csv        age and federal-state chi-square
    |     figures/
    |        figure1_translation_model.pdf
    |        figure2_exposure_governance_by_setting.pdf
    |
    |-- ethics/
          ethics_approval_references.txt
          participant_information_sheet.pdf
          privacy_notice.pdf


--------------------------------------------------------------------------------
3. CONTENT DESCRIPTION
--------------------------------------------------------------------------------

**instrument**/
    The complete questionnaire as administered, in German, and the English
    translation prepared by the authors. The questionnaire was newly developed
    for this study and was not psychometrically validated. No back-translation
    was conducted.

**documentation/strobe_flow_diagram.pdf**
    Flow of respondents from the raw dataset (n = 403) to the final analytical
    sample (n = 320). Stages: exclusion of non-physicians, retired participants,
    Austrian and Swiss respondents, and records incomplete on key demographic
    variables (yielding n = 363); exclusion of respondents not answering the
    core Shadow AI item (n = 28, yielding n = 335); exclusion of heterogeneous
    low-frequency work settings (n = 15, yielding n = 320).

**documentation/cleaning_and_aggregation_rules.pdf**
    The full set of inclusion and exclusion criteria applied at each stage, and
    the rules by which response categories were aggregated (inpatient and
    outpatient hospital settings combined into "Hospital"; single and group
    practices combined into "Practice").

**documentation/codebook.csv**
    Variable definitions and coding for every item used in the analysis. This
    includes: the ordinal coding of the six age bands; the reference category
    for healthcare setting (ambulatory practice); the binary dependent variable
    (Shadow AI exposure: 1 = own unauthorised use or observation of a colleague,
    0 = no case known); and the governance-index coding rule, under which
    responses of "do not know" or "cannot say" on a component item are coded as
    the measure not being in place.

**documentation/governance_index_construction.pdf**
    Construction of the composite governance index (0 to 3), its adaptation from
    the general governance dimensions of Klotz et al. (2019), and the stated
    omission of the monitoring and identification dimension as non-observable
    through physician self-report.

**documentation/nonresponse_bias_analysis.pdf**
    Comparison of early respondents (within 48 hours of the initial dispatch)
    and late respondents (following the reminder) on key demographic variables
    and on the primary outcome.

**data/aggregated/**
    The aggregated tables required to regenerate the published descriptives,
    governance distributions, regression tables, and goodness-of-fit tests, and
    the German Medical Association (BAEK) reference figures used as the
    comparison distribution. These files allow the published numbers to be
    reproduced without access to the microdata.

**code/**
    Python scripts reproducing each analysis stage from a prepared dataset.
    Run order follows the file numbering. The intercept and all model fit
    statistics (LLR chi-square, McFadden pseudo-R-squared, AIC, BIC) are
    reproduced by 04_regression_main.py. The sensitivity model using
    respondents' own unauthorised use as the sole outcome is reproduced by
    05_regression_sensitivity.py.

**results/**
    Full numeric output underlying Tables 1 to 3 and the in-text statistics,
    including all coefficients, standard errors, z-values, p-values, odds
    ratios, confidence intervals, the VIF diagnostics (all below 1.3), and the
    two goodness-of-fit tests (age and federal state). Figure source files are
    provided; these figures also appear in the main manuscript.

**ethics/**
    Ethics approval references and the participant-facing documents preceding
    the questionnaire.


--------------------------------------------------------------------------------
4. SOFTWARE ENVIRONMENT
--------------------------------------------------------------------------------

    Language:   Python 3.12.13
    Libraries:  pandas, scipy (scipy.stats), statsmodels
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

    Full re-estimation of the regression models requires the individual-level
    microdata, which are not included in this repository (see Section 6). With
    the microdata placed in data/ under the variable names given in the
    codebook, scripts 01 through 06 reproduce the reported results when run in
    order.


--------------------------------------------------------------------------------
6. DATA AVAILABILITY
--------------------------------------------------------------------------------

    Individual-level microdata are not shared publicly. They are available from
    the corresponding author on reasonable request, under a data-use agreement
    consistent with the ethics approvals governing the study.

    This repository contains aggregated data sufficient to reproduce every
    published figure and table. It does not contain data sufficient to re-run
    the participant-level regressions; those require the microdata above.


--------------------------------------------------------------------------------
7. ETHICS
--------------------------------------------------------------------------------

    The study received favourable ethics opinions from two institutions
    [ANONYMISED FOR REVIEW; references and dates in ethics/]. Data collection
    complied with the General Data Protection Regulation. A privacy notice and
    participant information sheet preceded the questionnaire, and participation
    was conditional on informed consent. Participation was voluntary and
    anonymous, and no incentives were offered.


--------------------------------------------------------------------------------
8. LICENCE
--------------------------------------------------------------------------------

    [SPECIFY, e.g. code under MIT; documentation and aggregated data under
    CC BY 4.0. See LICENSE.txt.]


--------------------------------------------------------------------------------
9. CITATION
--------------------------------------------------------------------------------

    [ANONYMISED FOR REVIEW]. To be completed for the camera-ready version.
    See CITATION.txt.


--------------------------------------------------------------------------------
10. CONTACT
--------------------------------------------------------------------------------

    [ANONYMISED FOR REVIEW]
================================================================================
