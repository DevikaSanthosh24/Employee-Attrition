# Employee Attrition Prediction Using Machine Learning

An AI-powered web application that predicts whether an employee is likely to stay with or leave an organization using machine learning. The application integrates a trained classification model with a Django web interface to generate predictions based on employee-related attributes.

## 1. Project Overview

Employee attrition is an important challenge for organizations because employee turnover can affect productivity, recruitment costs, and workforce stability.

This project uses machine learning to analyze employee-related information and predict attrition status. Users can enter employee details through a web interface and receive a prediction indicating whether the employee is likely to stay with or leave the organization.

The application also includes a dashboard for presenting employee and attrition-related information.

## 2. Objectives

* Predict employee attrition using machine learning.
* Analyze employee-related attributes associated with attrition.
* Experiment with different classification algorithms.
* Evaluate model performance using appropriate classification metrics.
* Integrate the selected machine learning model into a Django web application.
* Provide a user-friendly interface for entering employee details and viewing predictions.

## 3. Key Features

* Employee attrition prediction.
* Stay/Leave classification.
* Employee information input form.
* Django-based web application.
* Dashboard displaying employee and attrition-related information.
* Integration of a trained machine learning model.
* Prediction results displayed through a web interface.

## 4. Technologies Used

### Programming Language

* Python

### Backend

* Django

### Frontend

* HTML
* CSS

### Machine Learning and Data Processing

* XGBoost
* Pandas
* NumPy
* Scikit-learn
* Joblib

### Development Tools

* Visual Studio Code
* Git
* GitHub

## 5. Dataset Description

The project uses an employee attrition dataset containing employee-related attributes and a target variable representing attrition status.

* **Dataset:** Employee Attrition Dataset
* **Number of records:** 15,000
* **Number of fields:** 22
* **Target variable:** `Attrition`
* **Prediction classes:** Stay and Leave

The dataset is used for data exploration, preprocessing, model training, and evaluation.

The dataset statistics should correspond to the exact CSV file used in the final model-training process.

## 6. Features Used

The employee-related attributes considered in the project include:

* Age
* Years at Company
* Job Role
* Monthly Income
* Work-Life Balance
* Job Satisfaction
* Performance Rating
* Number of Promotions
* Overtime
* Distance from Home
* Job Level
* Company Tenure (in Months)
* Remote Work
* Leadership Opportunities
* Employee Recognition

The actual input features depend on the final model configuration. The prediction form and Django backend must use the same features, in the correct order and format, as the trained model.

## 7. Data Preprocessing

The dataset is prepared before training the machine learning models.

The preprocessing workflow includes:

1. Loading the dataset using Pandas.
2. Examining the dataset structure and target distribution.
3. Handling missing values, if present.
4. Preparing the input features and target variable.
5. Encoding categorical variables where required.
6. Splitting the dataset into training and testing sets.
7. Preparing the data for model training and evaluation.

The dataset is divided into training and testing sets using an 80:20 split.

## 8. Machine Learning Models

Different classification algorithms are explored to evaluate their suitability for employee attrition prediction.

The models experimented with include:

* Logistic Regression
* K-Nearest Neighbors (KNN)
* Support Vector Machine (SVM)
* Decision Tree
* Random Forest
* Gradient Boosting
* Extra Trees
* XGBoost

Only algorithms actually trained and evaluated should be listed here.

## 9. Final Machine Learning Model

The project uses an XGBoost classification model to predict employee attrition.

XGBoost is a gradient-boosting algorithm that builds an ensemble of decision trees to learn patterns from the training data.

The model analyzes employee-related attributes and predicts one of two outcomes:

* **Stay:** The employee is predicted to remain with the organization.
* **Leave:** The employee is predicted to leave the organization.

The model's performance is evaluated using suitable classification metrics, including accuracy, precision, recall, F1-score, and ROC-AUC where applicable.

The final reported performance should be based on the actual evaluation results obtained during testing.

## 10. Django Web Application

The trained machine learning model is integrated into a Django web application.

The application allows users to enter employee information through a prediction form and view the resulting attrition prediction.

### Application Workflow

1. The user opens the employee prediction form.
2. The user enters the required employee details.
3. The Django backend receives the submitted information.
4. The input data is prepared in the format expected by the trained model.
5. The model generates an attrition prediction.
6. The application displays whether the employee is predicted to stay or leave.

The application also includes a dashboard for presenting employee and attrition-related information.

## 11. Project Structure

The project includes the Django application, machine learning notebook, and supporting files.

The structure below is illustrative. Update it to match the actual files and folders in the repository.

```text
Employee-Attrition/
│
├── attrition/
│   ├── settings.py
│   ├── urls.py
│   └── ...
│
├── predictor/
│   ├── model/
│   │   └── employee_attrition_model.pkl
│   ├── templates/
│   ├── static/
│   ├── views.py
│   ├── urls.py
│   └── ...
│
├── Data cleaning and model training.ipynb
├── employee_attrition_dataset.csv
├── manage.py
├── requirements.txt
├── .gitignore
└── README.md
```

## 12. Installation and Setup

### Prerequisites

Install the following software:

* Python
* Git
* Visual Studio Code (recommended)

### Step 1: Clone the Repository

```bash
git clone https://github.com/DevikaSanthosh24/Employee-Attrition.git
```

### Step 2: Navigate to the Project Directory

```bash
cd Employee-Attrition
```

### Step 3: Create a Virtual Environment

```bash
python -m venv venv
```

### Step 4: Activate the Virtual Environment

On Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

On Windows Command Prompt:

```bat
venv\Scripts\activate
```

### Step 5: Install Dependencies

If a `requirements.txt` file is provided, run:

```bash
pip install -r requirements.txt
```

Otherwise, install the packages required by the application:

```bash
pip install django pandas numpy scikit-learn joblib xgboost
```

### Step 6: Apply Database Migrations

From the directory containing `manage.py`, run:

```bash
python manage.py migrate
```

### Step 7: Start the Development Server

```bash
python manage.py runserver
```

Open the local development address displayed in the terminal in your web browser.

**Note:** These instructions assume that `manage.py` is located in the repository root and that the trained model file is available at the path expected by the Django application. Adjust the commands if your project structure differs.

## 13. AI-Assisted Development

AI tools were used during development to support code understanding, debugging, and exploration of implementation approaches.

They assisted with tasks such as understanding Django application structure, troubleshooting Python errors, improving the user interface, and exploring machine learning implementation approaches.

Suggested changes were reviewed and tested as part of the development process.

The tools and activities described in this section should reflect the actual development experience.

## 14. Learning Outcomes

This project provided practical experience in:

* Python programming.
* Data preprocessing and exploratory data analysis.
* Machine learning model training and evaluation.
* Classification using XGBoost.
* Django-based web application development.
* Integrating a trained machine learning model into a web application.
* Debugging and testing application functionality.
* Using Git and GitHub for source code management.

## 15. Future Enhancements

* Deploy the application to a suitable hosting platform.
* Improve the prediction interface and user experience.
* Add authentication and access control.
* Introduce additional visualizations for attrition analysis.
* Explore model explainability and feature importance.
* Improve model evaluation and validation.
* Add automated tests for application functionality.

## 16. Author

**Devika Santhosh**

MCA Student | Aspiring Software Developer

GitHub: [DevikaSanthosh24](https://github.com/DevikaSanthosh24)

## 17. Project Repository

[Employee Attrition Prediction — GitHub](https://github.com/DevikaSanthosh24/Employee-Attrition)
