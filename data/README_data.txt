================================================================================
DATA README: REPOSITORY APPENDIX
================================================================================

Last Updated: 2026-06-24

--------------------------------------------------------------------------------
1. GENERAL INFORMATION
--------------------------------------------------------------------------------
This directory contains the aggregated datasets and reference statistics utilized
for the tables and analyses presented in the main manuscript. All data files 
are provided in CSV format (UTF-8 encoded, comma-delimited).

--------------------------------------------------------------------------------
2. DIRECTORY AND FILE STRUCTURE
--------------------------------------------------------------------------------

aggregated/
│
├── table1_sample_characteristics.csv
│   └── Sociodemographic characteristics of the sample (N = 320) compared 
│       against the reference data from the German Medical Association (BÄK).
│
├── table2_governance_index_by_setting.csv
│   └── Calculated governance indices, broken down by work context 
│       (Hospital, Private Practice, Medical Care Center/MVZ).
│
├── table3_regression_main.csv
│   └── Coefficients, standard errors, and significance levels of the 
│       primary regression model.
│
├── federal_state_distribution.csv
│   └── Distribution of respondents across individual federal states, including 
│       the aggregation rules applied for anonymization.
│
├── application_areas.csv
│   └── Overview and descriptive statistics regarding the specified fields 
│       of application.
│
└── reference_statistics_baek_2025.csv
    └── External reference statistics from the German Medical Association (2025), 
        used for data weighting and representativeness assessments.

--------------------------------------------------------------------------------
3. DATA USAGE & ANONYMIZATION NOTES
--------------------------------------------------------------------------------
* Missing Values: Empty cells (,,) within the CSV files represent structurally 
  blank fields (e.g., resulting from format translations of multi-row cells).
* Anonymization: To protect participant anonymity, low-frequency cells in 
  regional evaluations have been grouped according to the aggregation rules 
  detailed in 'federal_state_distribution.csv'.
* Character Encoding: All files are encoded in standard UTF-8. Special characters, 
  German umlauts (ä, ö, ü, ß), and mathematical symbols (e.g., Delta, >=) are 
  fully preserved and machine-readable.


--------------------------------------------------------------------------------
4. MICRODATA ACCESS CONDITIONS
--------------------------------------------------------------------------------
The individual level survey responses are not deposited in this
repository. They are personal data collected under participant consent
which provides for publication in aggregated form only.

Requests for access may be addressed to the principal investigator,
Prof. Dr.-Ing. Markus Schinle, Offenburg University of Applied Sciences
(markus.schinle@hs-offenburg.de), for the data controller, Hochschule
Offenburg. A request should state the applicant's affiliation, the
research question and the intended analysis. Each request is decided
individually and within the limits of the consent obtained. Access is
confined to non-commercial scientific use and requires a written
undertaking not to attempt re-identification and not to transfer the data
to third parties.

Ethics approval: Offenburg University of Applied Sciences, application
04-25, 27 June 2025; Department of Engineering, University of Cambridge,
application 736, 15 May 2025.
================================================================================
