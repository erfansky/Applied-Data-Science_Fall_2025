# Applied-Data-Science — Job Ads EDA

Project notebook and helper functions for Exploratory Data Analysis (EDA) on a job-ads dataset collected from Iranian job postings.

**Contents**

- `1/EX1.ipynb` — Main Jupyter notebook containing EDA, data cleaning, feature extraction and visualizations.
- `1/utils.py` — Helper functions used by the notebook (parsers, normalizers, and exporters).
- `dataset/Job.csv` — Raw dataset (job ads) used for the analysis.
- `dataset/Job_cleaned.csv` — Produced by the notebook after running the data-cleaning pipeline.

**Project Goal**

Perform exploratory data analysis on `Job.csv`, clean and normalize textual fields (education, gender, salary, languages, softwares, industry, bonuses, locations), extract structured features for downstream modeling, and produce visual summaries.

**Key Steps Implemented**

- Load and inspect the dataset (`pandas`).
- Normalize Persian digits and text fields.
- Parse and standardize: `education`, `gender`, `salary` (min/max/mean), `min_age`/`max_age`, `language` (per-language proficiency columns), `softwares` (per-software proficiency columns), `industry`, and `bonus`.
- One-hot / indicator generation for industries, bonuses, languages and tools.
- Create flags: `business_trip_flag`, `military_service_req`, `location_primary`.
- Drop duplicate ads and save cleaned dataset to `dataset/Job_cleaned.csv`.
- Visualizations: distributions, top categories, salary by industry, heatmaps for bonuses, and more.

**Dependencies**

Minimum recommended Python packages (create a virtual env first):

- Python 3.9+
- pandas
- numpy
- matplotlib
- seaborn
- bidi
- arabic_reshaper

You can install the typical requirements with pip. (If you prefer, I can generate a `requirements.txt`.)

PowerShell example:

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
pip install -U pip
pip install pandas numpy matplotlib seaborn python-bidi arabic-reshaper
```

**How to run**

1. Open the repository folder in VS Code or start Jupyter Notebook from the `d:\Khatam\5\ADS\Assignments` folder.

```powershell
jupyter notebook
```

2. Open `1/EX1.ipynb` and run cells in order. The notebook contains a final cell titled "Data cleaning and Extra Visualization Plan" which:
   - Builds the cleaned features using `1/utils.py` helpers.
   - Saves the cleaned CSV to `dataset/Job_cleaned.csv`.

**Notes and recommendations**

- `utils.py` contains many language- and domain-specific parsing helpers. Review them if dataset variations occur.
- Salary parsing currently extracts digits and treats them as numeric values; if salaries use different currencies or units (e.g., monthly vs. yearly), adapt the parser.
- Consider adding a `requirements.txt` or `environment.yml` for reproducibility.
- If you plan to move to modeling, add a notebook that performs feature selection and trains baseline models.

**Next steps you might want me to do**

- Add `requirements.txt` and a small script to run the notebook end-to-end (nbconvert or papermill).
- Add a short markdown summary inside `EX1.ipynb` listing main findings and recommended features for modeling.
- Create a small example model pipeline (train/test split + baseline model) using the cleaned dataset.

**License**

Use as you wish for coursework and research. Add a license file (`LICENSE`) if you want open-source licensing.

---
