# Tech Jobs Salary Prediction

Predicting tech job salaries using machine learning.

## Stack

| Component | Technology |
|-----------|------------|
| ML Model | XGBoost |
| Feature Extraction | LLM (on real-world job posting data) |
| Data Management | Django ORM |
| EDA & Training | Jupyter Notebook |

## Data

Job postings scraped from Stack Overflow, stored and managed via Django ORM.

Raw job fields include title, company, location, description, and applicant count.

## Feature Engineering with LLM

An LLM was used to extract structured features from unstructured job descriptions (see `jobs/management/commands/extend_jobs.py`):

- Job category (e.g. DevOps, PM, SWE)
- Tech stack
- Minimum experience years
- Education requirements (bachelor/master/PhD)
- Employment type
- Location restrictions (US-only)
- Salary and currency
- Benefits (medical insurance)

These extended features are stored in the `ExtendedJob` model and used as ML inputs.

## Prediction

XGBoost is used to predict hourly salary from the engineered features. EDA, preprocessing, training, and hyperparameter optimization are done in `predictions/main.ipynb`.

### Results (test set)

| Metric | Value |
|--------|-------|
| MAE    | $8.97 (12.5%) |
| RMSE   | $14.49 (20.2%) |
| R²     | 0.856 |
