import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score


df = pd.read_csv('data0.csv')

X = df[['employee_turnover_rate', 'customer_complaints', 'employee_satisfaction', 'annual_revenue_vnd']]
y = df['behavioral_risk']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

# Tạo và huấn luyện mô hình
model = LinearRegression()
model.fit(X_train, y_train)

# Trích xuất các trọng số beta

intercept = model.intercept_
coefficients = model.coef_


print("Coefficients (beta_1, beta_2, beta_3, beta_4):", coefficients)
