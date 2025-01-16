
import pandas as pd
from sklearn import tree
from sklearn.ensemble import AdaBoostRegressor
from sklearn.tree import DecisionTreeRegressor
import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import cross_val_score

monthData = pd.read_csv('/Users/agastyamishra/Downloads/US-National-Parks_Use_1979-2023_By-Month.csv', delimiter=',', quotechar='"', encoding='utf-8')

monthData['Region'] = monthData['Region'].str.strip()

# Split monthData into regions
regions = {
    'Intermountain': monthData[monthData['Region'] == 'Intermountain'],
    'Alaska': monthData[monthData['Region'] == 'Alaska'],
    'Midwest': monthData[monthData['Region'] == 'Midwest'],
    'Northeast': monthData[monthData['Region'] == 'Northeast'],
    'Pacific West': monthData[monthData['Region'] == 'Pacific West'],
    'Southeast': monthData[monthData['Region'] == 'Southeast']
}
pacWest = monthData[monthData['Region']=='Pacific West'] 




pacWest = pacWest.groupby(['Year']).sum()



x = np.arange(1,529)
y = monthData.groupby(['Month', 'Year'])['RecreationVisits'].sum()

