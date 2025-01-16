import streamlit as st
import plotly.express as px
import pandas as pd
from prophet import Prophet
import plotly.graph_objects as go


# Load data
monthData = pd.read_csv('US-National-Parks_Use_1979-2023_By-Month.csv', delimiter=',', quotechar='"', encoding='utf-8')
yearData = pd.read_csv('US-National-Parks_RecreationVisits_1979-2023.csv')

# Strip any spaces from region names
monthData['Region'] = monthData['Region'].str.strip()

# Group data by Year and Region
monthData_grouped = monthData.groupby(['Year', 'Region'], as_index=False).sum()
yearData = yearData.groupby(['Year', 'Region'], as_index=False).sum()
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
forecast_filtered = forecast[(forecast['ds'] >= '2024-01-01')]




# Streamlit app setup
st.set_page_config(page_title="National Parks Analysis", layout="wide")

# Tabs for navigation
tabs = st.tabs(["Main Page", "Analysis","Future Trends", "Sources"])

# Main Page
with tabs[0]:
    # Title and description
    st.title('National Parks Analysis')
    st.markdown('An interactive exploration of visitor trends in the U.S. National Parks System.')
    st.markdown('Created by Agastya Mishra and Nikhil Kasam')

    # Line graph for recreation visits
    st.subheader("Annual Recreation Visits by Region")
    fig1 = px.line(yearData, x='Year', y='RecreationVisits', color='Region', title='Annual Recreation Visits by Region')
    st.plotly_chart(fig1, use_container_width=True)

    # Interactive hover graph
    st.subheader("Sorted by Parks in a Region")
    hover_region = st.selectbox("Select a Region to Explore:", options=monthData_grouped['Region'].unique(), index=0)
    filtered_data = monthData[monthData['Region'] == hover_region]
    filtered_data = filtered_data.groupby(['Year', 'Region', 'ParkName'], as_index=False).sum(numeric_only=True)
    fig2 = px.line(
        filtered_data,
        x='Year',
        y='RecreationVisits',
        title=f'Total Recreation Visitors in {hover_region}',
        color='ParkName'
    )
    st.plotly_chart(fig2, use_container_width=True)

    # Dropdown and dynamic graph
    st.subheader("Explore Data by Category")
    selected_column = st.selectbox("Select a Data Column:", options=['Backcountry', 'RVCampers', 'TentCampers'], index=0)
    fig3 = px.line(
        monthData_grouped,
        x='Year',
        y=selected_column,
        color='Region',
        title=f'{selected_column} by Region'
    )
    st.plotly_chart(fig3, use_container_width=True)

# Analysis Page
with tabs[1]:
    st.title("Analysis")

    st.subheader("Graph: Recreation Visits by Region")
    fig4 = px.bar(yearData, x='Year', y='RecreationVisits', color='Region', title='Recreation Visits by Region Over Time')
    st.plotly_chart(fig4, use_container_width=True)

    # Section 1: Annual Recreation Visits by Region
    st.subheader("1. Annual Recreation Visits by Region")
    st.markdown(
        """
        - **Trend Analysis**: Over the past few decades, national parks have experienced a noticeable rise in visitor numbers, reflecting a growing  interest in outdoor recreation and nature-based tourism. This trend suggests not only an appreciation for natural beauty but also significant improvements in park accessibility, infrastructure, and public awareness efforts. The surge in visits points to a cultural shift where people increasingly seek experiences in nature for relaxation, wellness, and adventure.
        - **Historical Events**: The COVID-19 pandemic (2020-2021), for instance, caused a sharp decline in visitor numbers due to park closures and widespread travel restrictions, showing how global health crises can disrupt outdoor tourism. Similarly, during the Great Recession (2007-2009), economic hardships led to reduced leisure travel as financial constraints limited discretionary spending on vacations and recreation. 
        - **Regional Factors**: National parks in the Western U.S., such as Yellowstone and Yosemite, continue to draw millions of visitors annually due to their vast landscapes and iconic landmarks. However, regional fluctuations in visitation reflect environmental challenges and natural disasters. Even in current times, wildfires in the Western states have restricted access and deterred tourists. Hurricanes in the Southeastern U.S. have similarly impacted park safety and accessibility. 
        """
    )



    # Section 2: Hover Over Region Details
    st.subheader("2. The Geography Behind The Data")
    st.markdown(
        """
        - **Region-Specific Insights**: The Western U.S. continues to lead the nation in national park visitation, driven by its expansive wilderness, dramatic landscapes, and iconic parks like Yellowstone, Grand Canyon, and Yosemite. These destinations not only captivate millions but also play a big role in promoting tourism for the entire region. Their popularity highlights how signature landmarks can become anchors for regional tourism economies. On the other hand, the Eastern Region benefits from its closer proximity to densely populated urban centers, making national parks more accessible for day trips and shorter getaways. 
        - **Historical Context**: National park visitation patterns have often reflected broader societal movements and policy shifts. For example, the surge in visitors during the 1980s and 1990s closely coincided with government-led conservation campaigns, increased marketing efforts, and significant infrastructure improvements within the parks themselves. These initiatives not only expanded public interest but also made parks more accommodating for diverse audiences. More recently, the post-pandemic recovery has revealed uneven patterns across regions. While some parks saw swift rebounds in visitation as restrictions lifted, others experienced slower recoveries due to varying reopening policies, lingering safety concerns, and local economic factors. This disparity underscores how both public perception and government policy can influence the pace of recovery in outdoor tourism.
        """
    )


    # Section 3: Explore Data by Category
    st.subheader("3. Explore Data by Category")
    st.markdown(
        """
        - **Backcountry Use**: The steady increase in backcountry usage suggests a rising interest in remote, adventurous outdoor experiences. This trend may stem from a desire to travel and form a deeper connection with nature. The appeal of backcountry exploration also reflects a cultural shift toward more immersive and self-reliant outdoor activities.
        - **RV Camping**: RV camping trends tend to fluctuate based on broader economic conditions. Rising fuel prices and economic downturns can discourage long-distance RV travel due to higher costs, while periods of economic prosperity often lead to increased RV ownership and greater park visitation. 
        - **Tent Camping**: Tent camping remains the most stable and widely practiced form of park use, appreciated for its affordability and accessibility. Its popularity is partly due to its minimal cost, making it a good option for a broad range of visitors. During financial hardships, like the 2008 recession, tent camping often becomes a go-to choice for budget travelers.
        """
    )
    with tabs[2]:
        st.title("A ML-driven prediction for the future of the parks")
        st.subheader("Graph: Recreation Visits by Region")
        fig = go.Figure()


        fig.add_trace(go.Scatter(
        x=df['ds'], 
        y=df['y'], 
        mode='lines',
        name='Historical Data',
        line=dict(color='blue')
        ))

        fig.add_trace(go.Scatter(
        x=forecast_filtered['ds'], 
        y=forecast_filtered['yhat'], 
        mode='lines',
        name='Forecasted Data from 2024-2044',
        line=dict(color='red')
        ))

# Customize layout
        fig.update_layout(
        title='Historical vs Forecasted Data',
        xaxis_title='Date',
        yaxis_title='Recreational Park Visits',
        legend_title='Data Type',
        template='plotly_white'
        )

        st.plotly_chart(fig, use_container_width=True)







        st.markdown("The future trends for the National Parks system is essential to monitor. By utilizing the immense data of the National Parks database, we were able to create a predictive model to outline future growth over the next 20 years. Using FaceBook's Prophet module, we train a Time Series model to analyse the future attendance of the park in this timeframe. " )
        st.markdown("Initial attempts to train a model (Random Forest Regressors, Gradient Boosting Regressors ) provided little information, as the seasonality-based visitation of the Parks altered the consistency of the data. After interpolating the data per month, we found an interesting seasonal cycle to build off.  We ended up training a Time Series model designed to handle outliers and cyclical variation to produce the most accurate prediction for our use case. ")
        st.markdown("The results above showcase that cumaltive park attendance nationwide will cross 16 million yearly by the year 2040.")
        

        st.markdown("A further analysis of the underlying variables is shown in the figure below.")
        st.image( 'monthly.png',caption = 'A Deeper Look into the Data')
        st.markdown("The first plot details the overall trendline of the regression model, along with the possible error bounds for the associated prediction. ")
        st.markdown("The second figure provides an interesting look into the data discrepancies per month. In general, the months June through September lead to an increase in park attendance. The parks continiously lose attendance in every other month.  ")


        st.subheader("Final Conclusions")
        st.markdown("This interdisplinary analysis of the United States National Parks System combined elements from Geography, Mathamatics, History, and Statistics. The conclusions developed in this dashboard detail the past and future directions of the system overall.")
        st.markdown('It remains essential to support our National Parks to ensure that they thrive over the next few decades. Consider donating or visiting a park near you!')
        
       



# Sources Page
with tabs[3]:
    st.title("Sources")
   
    st.markdown(
        """
        - **National Park Service Visitor Data**: [NPS Stats](https://irma.nps.gov/STATS/)
        - **COVID-19 Impact on National Parks**: [National Parks Traveler](https://www.nationalparkstraveler.org/)
        - **Great Recession Effects**: [Bureau of Economic Analysis](https://www.bea.gov/)
        - **Find Your Park Campaign**: [National Park Foundation](https://findyourpark.com/)
        - **Tourism Trends and Recovery**: [US Travel Association](https://www.ustravel.org/)
        - **Wildfires and Park Access**: [US Forest Service](https://www.fs.usda.gov/)
        - **Economic Impacts on Travel**: [World Bank](https://www.worldbank.org/)
        - **General Park Insights**: [Outdoor Industry Association](https://outdoorindustry.org/)
        """
    )
