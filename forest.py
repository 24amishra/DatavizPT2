import sklearn
import pandas as pd

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


monthData = monthData.groupby(['Year'])

x = monthData['Year'].value()
y = monthData['RecreationVisits'].tolist()
