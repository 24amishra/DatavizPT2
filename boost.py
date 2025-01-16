import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from prophet import Prophet

# Load your dataset
monthData = pd.read_csv('/Users/agastyamishra/Downloads/US-National-Parks_Use_1979-2023_By-Month.csv', delimiter=',', quotechar='"', encoding='utf-8')

monthData['Region'] = monthData['Region'].str.strip()

# Group by Month and Year, then sum the RecreationVisits
y = monthData.groupby(['Month', 'Year'])['RecreationVisits'].sum()

# Reset index and sort chronologically by Year and Month
y_reset = y.reset_index()
y_sorted = y_reset.sort_values(by=['Year', 'Month'])

# Create a date index (Month-Year) for 'ds' (the date column)
y_sorted['Date'] = pd.to_datetime(y_sorted['Year'].astype(str) + '-' + y_sorted['Month'].astype(str), format='%Y-%m')

# Prepare the data in the required format for Prophet
df = y_sorted[['Date', 'RecreationVisits']].rename(columns={'Date': 'ds', 'RecreationVisits': 'y'})

# Create and fit the Prophet model
model = Prophet(yearly_seasonality=True)  # You can enable weekly seasonality if needed
model.fit(df)

# Make future predictions (e.g., for the next 12 months)
future = model.make_future_dataframe(periods=240, freq='M')  # Forecasting 240 months ahead
forecast = model.predict(future)
values = forecast['yhat']

#Plot the forecast
plt.figure(figsize=(10, 6))

 # Plot the historical data
#plt.plot(df['ds'], df['y'], label="Historical Data", color="blue")

# Plot the forecasted data
#plt.plot(forecast['ds'], forecast['yhat'], label="Forecasted Data", color="red", linestyle="--")

# Add labels and title
#plt.xlabel('Date (Month-Year)')
#plt.ylabel('Recreation Visits')
#plt.title('Recreation Visits Forecast and Historical Data')
#plt.xticks(rotation=45)
#plt.legend()

# Show the plot
#plt.show() 

#Optionally, plot the forecast components (trends, seasonal effects, etc.)
model.plot_components(forecast)
plt.show()  
