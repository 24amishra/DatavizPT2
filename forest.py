import pandas as pd
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import cross_val_score
import matplotlib.pyplot as plt
import numpy as np

# Load the dataset
monthData = pd.read_csv('/Users/agastyamishra/Downloads/US-National-Parks_Use_1979-2023_By-Month.csv', delimiter=',', quotechar='"', encoding='utf-8')

monthData['Region'] = monthData['Region'].str.strip()

# Group by Month and Year, then sum the RecreationVisits
y = monthData.groupby(['Month', 'Year'])['RecreationVisits'].sum()

# Reset index and sort chronologically by Year and Month
y_reset = y.reset_index()
y_sorted = y_reset.sort_values(by=['Year', 'Month'])

# Create a date index (Month-Year) for 'x'
y_sorted['Date'] = pd.to_datetime(y_sorted['Year'].astype(str) + '-' + y_sorted['Month'].astype(str), format='%Y-%m')

# Extract the 'RecreationVisits' values into an array (target variable)
visits_sorted = y_sorted['RecreationVisits'].values

# Create a numerical 'x' (the number of months from January 1979 to the end of your dataset)
x = np.arange(len(y_sorted)).reshape(-1, 1)

# Fit a DecisionTreeRegressor model
model = DecisionTreeRegressor(max_depth=3)

# Train the model
model.fit(x, visits_sorted)

# Predict for future months (next 500 months)
future_x = np.arange(len(y_sorted), len(y_sorted) + 500).reshape(-1, 1)

# Predict future 'RecreationVisits'
future_y = model.predict(future_x)

# Create future date range for prediction (future months)
last_date = y_sorted['Date'].max()
future_dates = pd.date_range(start=last_date, periods=500, freq='M')


""" 
# Plot training data and predictions


plt.figure(figsize=(10, 6))
plt.plot(y_sorted['Date'], visits_sorted, label="Training data", color='blue')
plt.plot(future_dates, future_y, label="Future predictions", color='red', linewidth=2)
plt.xlabel("Date (Month-Year)")
plt.ylabel("Recreation Visits")
plt.title("Decision Tree Regression for Recreation Visits (Month-Year)")
plt.legend()
plt.xticks(rotation=45)  # Rotate the x-axis labels for better readability
plt.show()

# Cross-validation to evaluate model performance
cv_scores = cross_val_score(model, x, visits_sorted, cv=5, scoring='neg_mean_absolute_error')

# Print cross-validation results
print("Cross-validation scores:", cv_scores)
print("Mean CV score:", np.mean(cv_scores))
print("Standard deviation of CV score:", np.std(cv_scores))
 """