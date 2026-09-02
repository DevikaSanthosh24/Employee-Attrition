# Employee Attrition Prediction

## Project Description

This project predicts whether an employee is likely to leave the organization using Machine Learning. The system analyzes various employee-related factors and predicts whether the employee is likely to **stay** or **leave** the organization.

## Objectives

* Predict employee attrition using Machine Learning.
* Identify factors that may influence employee turnover.
* Compare different Machine Learning algorithms.
* Develop a web-based prediction system using Django.
* Provide an easy-to-use interface for entering employee details and viewing predictions.

## Technologies Used

* Python
* Django
* Machine Learning
* Pandas
* NumPy
* Scikit-learn
* Joblib
* HTML
* CSS

## Dataset

The dataset contains employee-related information used to train the Machine Learning model.

The final dataset used for the project contains **15,000 employee records**.

## Features Used

The following features are used for prediction:

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
* Company Tenure (In Months)
* Remote Work
* Leadership Opportunities
* Employee Recognition

## Data Preprocessing

The dataset was processed before training the Machine Learning models. The main preprocessing steps included:

* Handling missing values
* Selecting relevant features
* Encoding categorical variables
* Preparing the target variable
* Splitting the dataset into training and testing sets

The dataset was divided into **80% training data and 20% testing data**.

## Machine Learning Models

Different Machine Learning algorithms were experimented with and evaluated to identify a suitable model for employee attrition prediction.

The models included:

* Logistic Regression
* K-Nearest Neighbors (KNN)
* Support Vector Machine (SVM)
* Decision Tree
* Random Forest
* Balanced Random Forest
* XGBoost
* Gradient Boosting
* Extra Trees

## Model Used

Random Forest was selected as the Machine Learning model used in the Django application.

The trained model was saved using Joblib and integrated into the Django application for making predictions on new employee data.

## Django Web Application

The Machine Learning model is integrated into a Django web application.

The application allows the user to:

1. Enter employee information.
2. Submit the information for prediction.
3. Process the input using the trained Machine Learning model.
4. Display whether the employee is likely to **Stay** or **Leave**.

## Project Structure

```text
Employee_attrition/
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
│   ├── views.py
│   ├── urls.py
│   └── ...
│
├── Data cleaning and model training.ipynb
├── README.md
└── manage.py
```

## How to Run the Project

Clone the repository and navigate to the project directory.

Install the required Python packages:

```bash
pip install django pandas numpy scikit-learn joblib
```

Run the Django development server:

```bash
python manage.py runserver
```

Open the application in a web browser and enter the required employee details to generate a prediction.

## Team Members

| Name            | Role      | Contact                                                           |
| --------------- | --------- | ----------------------------------------------------------------- |
| Devika Santhosh | Developer | [devikhasanthosh24@gmail.com](mailto:devikhasanthosh24@gmail.com) |
| Reenu Sebu      | Guide     | [reenusebu@mbits.ac.in](mailto:reenusebu@mbits.ac.in)             |

## Future Scope

* Improve prediction performance using additional Machine Learning techniques.
* Add more employee-related features.
* Provide graphical analysis of attrition factors.
* Deploy the application online.
* Add authentication and employee management features.
