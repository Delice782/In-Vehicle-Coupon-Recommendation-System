                           
# -*- coding: utf-8 -*-
"""Coupon_Recommendation_System.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1jikczD71G4lAH-0bsE3cjrBbXcjp2O2Z

# Week1: Data Understanding and Cleaning

#### A. Importing Required Libraries and Dataset
"""

import pandas as pd
from sklearn.preprocessing import StandardScaler
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report
from sklearn.preprocessing import OneHotEncoder
import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# Load the dataset
data = pd.read_csv('/content/in-vehicle-coupon-recommendation (2).csv')

"""#### Exploring the Dataset

"""

# Get information about the entire dataset
print(data.info())

# Display the first few rows of the dataset
print(data.head())

# Display the data types of each column
print(data.dtypes)

"""#### Identify Categorical and Numerical Columns"""

# Identify categorical and numerical columns
categorical_cols = data.select_dtypes(include=['object']).columns.tolist()
numerical_cols = data.select_dtypes(include=['int64', 'float64']).columns.tolist()

print("Categorical Columns:", categorical_cols)
print("Numerical Columns:", numerical_cols)

"""#### B. Handle Missing Values
###### Drop Columns with Too Many Missing Values
"""

# Define a threshold for dropping columns with >50% missing values
threshold = 0.5 * len(data)
data = data.dropna(thresh=threshold, axis=1)
data.head()

"""##### Fill Missing Values in Categorical Columns with Mode"""

categorical_cols = [
    'destination', 'passanger', 'weather', 'time', 'coupon',
    'expiration', 'gender', 'maritalStatus', 'education', 'occupation', 'income', 'CarryAway', 'RestaurantLessThan20', 'CoffeeHouse'
]

# Find the mode and fill missing values
for col in categorical_cols:
    mode_value = data[col].mode()[0]
    data[col].fillna(mode_value, inplace=True)
    print(f"Filled missing values for {col} with mode: {mode_value}")

"""#### C. Handle Inconsistencies in Categorical Data"""

# Standardizing categorical values in the 'coupon' column
data['coupon'] = data['coupon'].replace({'less1': 'Less than 1', 'Less1': 'Less than 1'})
data.head()

"""#### D. Encode categorical variables using one-hot encoding for features such as destination, weather, and coupon."""

# One-hot encoding for categorical variables
data = pd.get_dummies(data, columns=['destination', 'weather', 'coupon'], drop_first=True)

"""#### E.  Scale numerical variables like temperature, toCoupon_GEQ5min, toCoupon_GEQ15min, and toCoupon_GEQ25min using StandardScaler"""

scaler = StandardScaler()
numerical_cols = ['temperature', 'toCoupon_GEQ5min', 'toCoupon_GEQ15min', 'toCoupon_GEQ25min']
data[numerical_cols] = scaler.fit_transform(data[numerical_cols])

# Save the cleaned dataset to a CSV file
data.to_csv('cleaned_dataset.csv', index=False)

"""# Week 2: Exploratory Data Analysis (EDA)

#### A. Visualize relationships between the target variable (Y) and categorical features like weather, time, passenger, and age
"""

# Set up the plot style
sns.set(style="whitegrid")

# Define the categorical features to visualize
categorical_features = ['time', 'passanger', 'weather_Snowy', 'weather_Sunny']

# Visualize the relationship between the target variable (Y) and each categorical feature
for feature in categorical_features:
    if feature in data.columns:
        plt.figure(figsize=(10, 6))
        sns.countplot(data=data, x=feature, hue='Y', palette='Set2')
        plt.title(f'Relationship between {feature.capitalize()} and Coupon Acceptance (Y)')
        plt.xlabel(feature.capitalize())
        plt.ylabel('Count')
        plt.legend(title='Coupon Accepted (Y)')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    else:
        print(f"Column '{feature}' does not exist in the DataFrame and will be skipped.")

"""#### B. Analyze Trends in Coupon Acceptance Based on Categorical Features

##### Using bar plots to visualize the distribution of coupon acceptance (Y) across different categorical features.
"""

# Set up the plot style
sns.set(style="whitegrid")

# Including more categorical features for better analysis
categorical_features = [
    'time', 'passanger', 'age', 'gender', 'maritalStatus',
    'has_children', 'education', 'occupation', 'Bar',
    'CoffeeHouse', 'CarryAway', 'RestaurantLessThan20',
    'Restaurant20To50', 'destination_No Urgent Place',
    'destination_Work', 'weather_Snowy', 'weather_Sunny'
]

# Visualize coupon acceptance trends for each categorical feature
for feature in categorical_features:
    if feature in data.columns:
        plt.figure(figsize=(8, 6))
        sns.countplot(data=data, x=feature, hue='Y', palette='Set2')
        plt.title(f'Trend of Coupon Acceptance (Y) by {feature.capitalize()}')
        plt.xlabel(feature.capitalize())
        plt.ylabel('Count')
        plt.legend(title='Coupon Accepted (Y)')
        plt.show()
    else:
        print(f"Column '{feature}' does not exist in the DataFrame and will be skipped.")

"""#### C. Perform Correlation Analysis between numerical features and the target variable (Y)"""

# Columns for correlation analysis
numerical_columns = ['temperature', 'has_children', 'toCoupon_GEQ5min',
                     'toCoupon_GEQ15min', 'toCoupon_GEQ25min',
                     'direction_same', 'direction_opp', 'Y']

# Calculate the correlation matrix
correlation_matrix = data[numerical_columns].corr()

# Extract the correlation with the target variable Y
correlation_with_target = correlation_matrix['Y'].drop('Y')

# Print the correlation with target variable (Y)
print("Correlation with Target Variable (Y):")
print(correlation_with_target)

# Visualize the correlation matrix
plt.figure(figsize=(10, 6))
sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap='coolwarm', square=True)
plt.title('Correlation Matrix')
plt.show()

"""#### D.  Visualize distributions of key numerical features (e.g., temperature, toCoupon_GEQXmin) and their impact on coupon acceptance"""

correlation_matrix = data[['temperature', 'has_children', 'toCoupon_GEQ5min',
                            'toCoupon_GEQ15min', 'toCoupon_GEQ25min',
                            'direction_same', 'direction_opp', 'Y']].corr()

correlation_with_target = correlation_matrix['Y'].drop('Y')
print("Correlation with Target Variable (Y):")
print(correlation_with_target)

# Visualize distributions of key numerical features
sns.set(style='whitegrid')

# Create a figure to hold multiple plots
plt.figure(figsize=(15, 6))

# Temperature Distribution
plt.subplot(1, 3, 1)
sns.histplot(data['temperature'], bins=10, kde=True)
plt.title('Temperature Distribution')
plt.xlabel('Temperature')
plt.ylabel('Frequency')

# toCoupon_GEQ5min Distribution
plt.subplot(1, 3, 2)
sns.histplot(data['toCoupon_GEQ5min'], bins=10, kde=True)
plt.title('toCoupon_GEQ5min Distribution')
plt.xlabel('toCoupon_GEQ5min')
plt.ylabel('Frequency')

# Visualizing impact of toCoupon_GEQ5min on coupon acceptance (Y)
plt.subplot(1, 3, 3)
sns.boxplot(x='Y', y='toCoupon_GEQ5min', data=data)
plt.title('Impact of toCoupon_GEQ5min on Coupon Acceptance')
plt.xlabel('Coupon Accepted (Y)')
plt.ylabel('toCoupon_GEQ5min')

# Show plots
plt.tight_layout()
plt.show()

"""# Week 3: Machine Learning Models

##### A. Split the data into training and test sets (80% training, 20% testing)
"""

# Prepare features and target variable
X = data.drop('Y', axis=1)
y = data['Y']

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Display the shapes of the resulting sets
print(f"Training set shape: {X_train.shape}")
print(f"Test set shape: {X_test.shape}")

"""#### B. Implement and evaluate different machine learning models:"""

# Initialize the models
logistic_model = LogisticRegression()
decision_tree_model = DecisionTreeClassifier()
random_forest_model = RandomForestClassifier()

"""#####  Logistic Regression: A basic linear model to predict coupon acceptance"""

# Convert categorical columns to dummy variables
X_train = pd.get_dummies(X_train)
X_test = pd.get_dummies(X_test)

# Align the train and test data, filling any missing columns with 0
X_train, X_test = X_train.align(X_test, join='left', axis=1, fill_value=0)

# Fit the logistic regression model
logistic_model.fit(X_train, y_train)
y_pred_logistic = logistic_model.predict(X_test)

"""#### C. Evaluate model performance using metrics such as accuracy, precision, recall, and F1-score."""

# Print metrics
print("Logistic Regression Metrics:")
print(f"Accuracy: {accuracy_score(y_test, y_pred_logistic)}")
print(f"Precision: {precision_score(y_test, y_pred_logistic)}")
print(f"Recall: {recall_score(y_test, y_pred_logistic)}")
print(f"F1 Score: {f1_score(y_test, y_pred_logistic)}")
print(classification_report(y_test, y_pred_logistic))

"""##### DecisionTreeClassifier: A tree-based model for classification.

"""

# Decision Tree Classifier
decision_tree_model.fit(X_train, y_train)
y_pred_tree = decision_tree_model.predict(X_test)

"""##### Evaluate model performance using metrics such as accuracy, precision, recall, and F1-score."""

print("\nDecision Tree Classifier Metrics:")
print(f"Accuracy: {accuracy_score(y_test, y_pred_tree)}")
print(f"Precision: {precision_score(y_test, y_pred_tree)}")
print(f"Recall: {recall_score(y_test, y_pred_tree)}")
print(f"F1 Score: {f1_score(y_test, y_pred_tree)}")
print(classification_report(y_test, y_pred_tree))

"""##### RandomForestClassifier: An ensemble modelthat builds multiple decision trees to improve accuracy"""

# Random Forest Classifier
random_forest_model.fit(X_train, y_train)
y_pred_forest = random_forest_model.predict(X_test)

"""#####  Evaluate model performance using metrics such as accuracy, precision, recall, and F1-score."""

print("\nRandom Forest Classifier Metrics:")
print(f"Accuracy: {accuracy_score(y_test, y_pred_forest)}")
print(f"Precision: {precision_score(y_test, y_pred_forest)}")
print(f"Recall: {recall_score(y_test, y_pred_forest)}")
print(f"F1 Score: {f1_score(y_test, y_pred_forest)}")
print(classification_report(y_test, y_pred_forest))

"""##### Visualize Model Performance across Metrics

"""

# Data for the models
models = ['Logistic Regression', 'Decision Tree', 'Random Forest']
accuracy = [0.685849, 0.689791, 0.741821]
precision = [0.693426, 0.719943, 0.740434]
recall = [0.778566, 0.722498, 0.823989]
f1_score = [0.733534, 0.721219, 0.779980]

# Set the position of the bars on the x-axis
x = np.arange(len(models))

# Bar width
width = 0.2

# Create the plot
fig, ax = plt.subplots(figsize=(10,6))

# Plot the bars
bar1 = ax.bar(x - 1.5*width, accuracy, width, label='Accuracy')
bar2 = ax.bar(x - 0.5*width, precision, width, label='Precision')
bar3 = ax.bar(x + 0.5*width, recall, width, label='Recall')
bar4 = ax.bar(x + 1.5*width, f1_score, width, label='F1 Score')

# Labeling the plot
ax.set_xlabel('Models')
ax.set_ylabel('Metrics Values')
ax.set_title('Model Performance Across Metrics')
ax.set_xticks(x)
ax.set_xticklabels(models)
ax.legend()

# Display the plot
plt.tight_layout()
plt.show()

"""#### D. Compare models to determine which one performs best for predicting coupon acceptance.

"""

model_metrics = {
    "Model": ["Logistic Regression", "Decision Tree", "Random Forest"],
    "Accuracy": [0.6858494284588096, 0.6897910918407568, 0.7418210484824596],
    "Precision": [0.6934260429835651, 0.7199434229137199, 0.7404336734693877],
    "Recall": [0.7785663591199432, 0.7224982256919801, 0.8239886444286728],
    "F1 Score": [0.7335339351387495, 0.7212185618136734, 0.7799798454820289]
}

# Create a DataFrame to store the metrics
performance_df = pd.DataFrame(model_metrics)

# View each model's performance
print("Model Performance Comparison:")
print(performance_df)

# Find the best model for each metric
best_f1 = performance_df.loc[performance_df['F1 Score'].idxmax()]
best_recall = performance_df.loc[performance_df['Recall'].idxmax()]
best_precision = performance_df.loc[performance_df['Precision'].idxmax()]
best_accuracy = performance_df.loc[performance_df['Accuracy'].idxmax()]

# View the best models based on different metrics
print("\nBest Model Based on F1 Score:")
print(best_f1)

print("\nBest Model Based on Recall:")
print(best_recall)

print("\nBest Model Based on Precision:")
print(best_precision)

print("\nBest Model Based on Accuracy:")
print(best_accuracy)

# Check if the best models are indeed different
if best_f1.equals(best_recall) and best_recall.equals(best_precision) and best_precision.equals(best_accuracy):
    print("\nAll metrics point to the same best model.")
else:
    print("\nDifferent models may be the best for different metrics.")

"""# Week 4: Fine-Tuning and Reporting

##### A. Fine-tune the best-performing model (Random Forest Model) using GridSearchCV to search for optimal hyperparameters (e.g., number of trees, max depth, minimum samples per split, etc.)
"""

X = pd.get_dummies(X, drop_first=True)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize the RandomForestClassifier
rf = RandomForestClassifier(random_state=42)

# Set up the hyperparameter grid: Numer of trees, Maximum depth of the tree, Minimum samples required to split an internal node, and Minimum samples required to be at a leaf node
param_grid = {
    'n_estimators': [100, 200],
    'max_depth': [None, 10, 20],
    'min_samples_split': [2, 5],
    'min_samples_leaf': [1, 2]
}

# Perform GridSearchCV to find the best hyperparameters
grid_search = GridSearchCV(estimator=rf, param_grid=param_grid, cv=5, scoring='accuracy', verbose=2, n_jobs=-1)
grid_search.fit(X_train, y_train)

# Get the best model from grid search
best_rf = grid_search.best_estimator_

# View the best hyperparameters found
print(f"Best Hyperparameters: {grid_search.best_params_}")

"""##### B. Evaluate the Tuned Model on the Test Data and Compare Its Performance with previous models"""

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# Predict using the best model
y_pred = best_rf.predict(X_test)

# Calculate evaluation metrics
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)

# View performance metrics for the tuned model
print("Best Random Forest Model Performance (After Tuning):")
print(f"Accuracy: {accuracy}")
print(f"Precision: {precision}")
print(f"Recall: {recall}")
print(f"F1 Score: {f1}")
