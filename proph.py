from prophet import Prophet
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load your data (assuming y_sorted contains the data)
monthData = pd.read_csv('/Users/agastyamishra/Downloads/US-National-Parks_Use_1979-2023_By-Month.csv', delimiter=',', quotechar='"', encoding='utf-8')
monthData['Region'] = monthData['Region'].str.strip()

y = monthData.groupby(['Month', 'Year'])['RecreationVisits'].sum()

