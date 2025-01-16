import streamlit as st
import plotly.express as px
import pandas as pd

# Load data
yearData = pd.read_csv('/Users/nikhilkasam/Desktop/US-National-Parks_RecreationVisits_1979-2023 (1).csv')
monthData = pd.read_csv('/Users/nikhilkasam/Downloads/US-National-Parks_Use_1979-2023_By-Month.csv', delimiter=',', quotechar='"', encoding='utf-8')

# Strip any spaces from region names
monthData['Region'] = monthData['Region'].str.strip()

# Group data by Year and Region
monthData_grouped = monthData.groupby(['Year', 'Region'], as_index=False).sum()
yearData = yearData.groupby(['Year', 'Region'], as_index=False).sum()

# Streamlit app setup
st.set_page_config(page_title="National Parks Analysis", layout="wide")

# Tabs for navigation
tabs = st.tabs(["Main Page", "Analysis", "Sources"])

# Main Page
with tabs[0]:
    # Title and description
    st.title('National Parks Analysis')
    st.markdown('An interactive exploration of visitor trends in the U.S. National Parks System.')

    # Line graph for recreation visits
    st.subheader("Annual Recreation Visits by Region")
    fig1 = px.line(yearData, x='Year', y='RecreationVisits', color='Region', title='Annual Recreation Visits by Region')
    st.plotly_chart(fig1, use_container_width=True)

    # Interactive hover graph
    st.subheader("Hover over a line to see details")
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
    st.subheader("2. Hover Over Region Details")
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



# Sources Page
with tabs[2]:
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
