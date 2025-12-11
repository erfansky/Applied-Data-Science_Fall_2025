# Job Salary & Company Size Prediction – Machine Learning Homework

## Overview
This project is focused on applying **regression** and **classification** techniques to a real-world job dataset (`jobs`). The goal is to predict salaries and company sizes, as well as classify high-salary jobs, using various machine learning models.

The dataset contains hundreds of features about job postings, including minimum and maximum salaries, company size, and other relevant job characteristics.

---

## Sections

### 1. Regression Task
- **Target Variable:** Average salary (`avg_salary`) calculated as the mean of `min_salary` and `max_salary`.
- **Goal:** Predict a fair salary for each job position.
- **Models Used:**
  - Linear Regression
  - Ridge Regression
  - LASSO Regression
  - Kernel Regression
  - Support Vector Regression (SVR)
  - Random Forest Regressor
- **Evaluation Metrics:**
  - Mean Squared Error (MSE)
  - Root Mean Squared Error (RMSE)
  - Mean Absolute Error (MAE)
  - Mean Absolute Percentage Error (MAPE)
  - R² Score
- **Observations:**  
  Models perform well on common, low-to-medium salary positions but struggle with rare high-salary jobs. Feature importance analysis and specialized random forests were explored to improve predictions for high-salary roles.

---

### 2. Binary Classification Task
- **Target Variable:** High-salary indicator (top 20% of salaries labeled as 1, others as 0).
- **Goal:** Predict whether a job belongs to a high-salary category.
- **Techniques Used:**
  - Logistic Regression
  - Support Vector Machine (SVM)
  - Kernel SVM
  - K-Nearest Neighbors (KNN)
  - Decision Trees
  - Random Forests
- **Metrics:**
  - Accuracy
  - Precision
  - Recall
  - F1-Score
  - Confusion Matrix
  - ROC Curve
  - AUC
- **Observations:**  
  Oversampling was used to balance the classes. Gradient boosting and ensemble methods provided better predictions, while simpler models struggled with recall on the high-salary class.

---

### 3. Multiclass Classification Task
- **Target Variable:** Company size, categorized into four classes:
  1. Small (≤ 20 employees)
  2. Medium (21–100 employees)
  3. Large (101–200 employees)
  4. Very Large (> 300 employees)
- **Goal:** Predict company size based on job features.
- **Techniques Used:**
  - Multiclass SVM
  - Multiclass Logistic Regression (One-vs-Rest and Multinomial)
  - Multiclass KNN
  - Decision Trees
  - XGBoost
  - LightGBM
  - AdaBoost
  - CatBoost
- **Metrics:**
  - Accuracy
  - Precision per class
  - Recall per class
  - F1-Score (Macro, Weighted, Micro)
- **Observations:**  
  Gradient boosting methods (XGBoost, LightGBM, CatBoost) generally performed best. Class imbalances required oversampling to improve performance, especially for the smaller categories.

---

## Additional Notes
- **Scaling & Pipelines:** StandardScaler and pipelines were consistently used for proper preprocessing.
- **Hyperparameter Tuning:** GridSearchCV was applied to most models to find optimal parameters.
- **Feature Analysis:** Top correlated features were used for regression; all features were explored for high-salary predictions.
- **Libraries:** scikit-learn, XGBoost, LightGBM, CatBoost, matplotlib, seaborn, numpy, pandas, arabic-reshaper, python-bidi.

---

## How to Run
1. Install requirements:

```bash
pip install -r requirements.txt
