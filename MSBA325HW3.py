import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# Main title
st.title("The Lebanese Condition")

# Subheader
st.subheader("Chapter 1: Lebanon's Flailing infrastructure")

# Load the dataset
df = pd.read_csv('https://linked.aub.edu.lb/pkgcube/data/85ad3210ab85ae76a878453fad9ce16f_20240905_164730.csv')

# Clean column names
df.columns = df.columns.str.strip()

# -------- PIE CHART ---------
# Count the number of towns with and without projects
project_counts = df['Existence of initiatives and projects  in the past five years to improve infrastructure - exists'].value_counts()

# Define labels for the pie chart
labels = ['Towns without Projects', 'Towns with Projects']

# Create the pie chart using Plotly
fig_pie = px.pie(values=project_counts, 
                 names=labels, 
                 title="Towns with projects vs Towns without projects to improve infrastructure - Last 5 years",
                 hole=0.4)

# Emphasize the 'Towns with Projects' slice by "pulling" it out slightly
fig_pie.update_traces(pull=[0, 0.1],  # Pulling out the 'Towns with Projects' slice
                      marker=dict(colors=['#EAC9F0', '#F48FB1']),  # Custom colors (lilac and pink)
                      textinfo='label+percent+value',
                      hoverinfo='label+percent+value')

# Beautifying layout and legend
fig_pie.update_layout(
    title_font_size=16,
    legend_title_text='Project Status',
    legend_title_font_size=16,
    legend_font_size=14,
    legend=dict(
        orientation="h",  # Horizontal legend
        yanchor="bottom",
        y=-0.2,
        xanchor="center",
        x=0.5
    )
)

# Display the pie chart in Streamlit (without checkbox)
st.plotly_chart(fig_pie)

st.markdown('<div style="padding: 10px; border-radius: 5px; margin-bottom: 10px;"><strong style="font-size: 18px;">⬇️ Don\'t miss this! Select the checkbox below:</strong></div>', unsafe_allow_html=True)

# Create a checkbox to show the bar chart
show_bar_chart = st.checkbox('Show the distribution of recent projects (last 5 years) across governorates')

# If the checkbox is checked, show the bar chart
if show_bar_chart:
    # Load the dataset
    df = pd.read_csv('https://linked.aub.edu.lb/pkgcube/data/85ad3210ab85ae76a878453fad9ce16f_20240905_164730.csv')
    df.columns = df.columns.str.strip()

    # Extract Governorate information
    df['Governorate'] = df['refArea'].str.extract(r'/page/([^/]+)|/resource/([^/]+)').fillna('').sum(axis=1)

    # Mapping districts to governorates
    district_to_governorate = {
        'Baabda_District': 'Mount Lebanon',
        'Byblos_District': 'Mount Lebanon',
        'Keserwan_District': 'Mount Lebanon',
        'Aley_District': 'Mount Lebanon',
        'Matn_District': 'Mount Lebanon',
        'Mount_Lebanon_Governorate': 'Mount Lebanon',
        'Tyre_District': 'South',
        'Sidon_District': 'South',
        'South_Governorate': 'South',
        'Akkar_Governorate': 'Akkar',
        'Bsharri_District': 'North',
        'Batroun_District': 'North',
        'Zgharta_District': 'North',
        'Minieh-Danniyeh_District': 'North',
        'Tripoli_District,_Lebanon': 'North',
        'North_Governorate': 'North',
        'MiniyehâDanniyeh_District': 'North',
        'Marjeyoun_District': 'Nabatieh',
        'Bint_Jbeil_District': 'Nabatieh',
        'Hasbaya_District': 'Nabatieh',
        'Nabatieh_Governorate': 'Nabatieh',
        'Zahlé_District': 'Beqaa',
        'Western_Beqaa_District': 'Beqaa',
        'Beqaa_Governorate': 'Beqaa',
        'ZahlÃ©_District': 'Beqaa',
        'Hermel_District': 'Baalbek-Hermel',
        'Baalbek-Hermel_Governorate': 'Baalbek-Hermel'
    }

    # Replace districts with governorates
    df['Governorate'] = df['Governorate'].replace(district_to_governorate)

    # Population data for each governorate (adjusted)
    population_data = {
        'Akkar': 432000,
        'Baalbek-Hermel': 472000,
        'Beqaa': 540000,
        'Mount Lebanon': 1831000,  # Keserwan-Jbeil added to Mount Lebanon
        'Nabatieh': 391000,
        'North': 803000,
        'South': 602000
    }

    # Add a population filter using a slider
    min_population, max_population = st.slider(
        "Filter by population size (Governorates)", 
        min_value=300000, 
        max_value=1831000,  # Max population after including Keserwan-Jbeil
        value=(300000, 1831000)
    )

    # Filter the governorates based on the population range selected by the user
    filtered_governorates = [gov for gov, pop in population_data.items() if min_population <= pop <= max_population]

    # Filter the dataset based on the population-selected governorates
    df_projects = df[df['Governorate'].isin(filtered_governorates)]
    df_projects = df_projects[df_projects['Existence of initiatives and projects  in the past five years to improve infrastructure - exists'] == 1]

    # Count the number of towns with recent projects per governorate
    town_counts = df_projects['Governorate'].value_counts()

    # Create bar chart with a range slider for zooming
    fig = px.bar(
        x=town_counts.index, 
        y=town_counts.values, 
        title="Lebanese towns with recent projects (past 5 years) in each Governorate",
        labels={'x': 'Governorates', 'y': 'Number of towns with recent projects'}
    )

    # Add a range slider to zoom in/out
    fig.update_layout(
        xaxis=dict(
            rangeslider=dict(visible=True),
            type="category"
        )
    )

    # Display the bar chart
    st.plotly_chart(fig)

st.markdown('<h3 style="font-size: 20px;">Key Insights</h3>', unsafe_allow_html=True)
st.markdown("""
- **80%** of Lebanese towns have not had infrastructure projects in the past 5 years.
- **~27%** of the infrastructure projects in the past 5 years have been in the Mount Lebanon Governorate.
""")

# -------- CONCLUSION & RECOMMENDATION ---------
# For Chapter 1 Conclusion & Recommendation
st.markdown('<h3 style="font-size: 20px;">Conclusion & Recommendation</h3>', unsafe_allow_html=True)

# Conclusion content with bold sections and bullet points
st.markdown("""
**Recommendation**  
Lebanon's infrastructure in towns, particularly in the South, Beqaa, and Baalbeck-Hermel governorates, is in critical need of immediate funding and reconstruction efforts. Despite the ongoing economic and political crises, allocating resources to rebuild and modernize the country's essential infrastructure is imperative.

**Reasons**
- Significant deterioration of infrastructure in recent years, with roads, utilities, and essential services in disrepair or non-functional
- Governorates like South, Beqaa, and Baalbeck-Hermel are the most affected, suffering from lack of sustained funding for public projects
- Poor infrastructure is directly linked to increased accidents, social unrest, and security risks, negatively impacting the quality of life for residents
- Investments in infrastructure can stabilize these regions, improving economic opportunities and restoring public trust in governance

**Outstanding Risks**
- Continued neglect will worsen the state of infrastructure, further exacerbating economic challenges
- Increased frequency of accidents and civil unrest due to deteriorating roads and essential services
- Rising migration from rural towns to urban centers, increasing pressure on already strained cities
- Erosion of what is left of public confidence in government institutions if infrastructure remains ignored

**Next Steps**
- The government should develop a targeted infrastructure recovery plan, focusing on high-priority areas in the South, Beqaa, and Baalbeck-Hermel
- Secure funding through partnerships with international donors and private sector entities
- Establish monitoring and accountability frameworks to ensure transparency and efficiency in the execution of projects
- Prioritize quick wins—projects that can be completed swiftly to address the most urgent needs and demonstrate progress to local communities
""")

st.markdown('<hr style="margin-top: 50px; margin-bottom: 50px; border-top: 2px solid #bbb;">', unsafe_allow_html=True)

# -------- Chapter 2 --------
st.subheader("Chapter 2: Lebanon's Failing Economy")

# Load the dataset for the exchange rate plot (Chapter 2)
df_currency = pd.read_csv('https://linked.aub.edu.lb/pkgcube/data/e780729371ddfbf95a71cbf301ed8ebf_20240906_165005.csv')

# Group and clean data
df_currency = df_currency.groupby('Year', as_index=False)['Value'].mean()  
df_currency = df_currency.sort_values(by='Year')

# Create line chart for currency exchange rate
fig_currency = go.Figure()

fig_currency.add_trace(go.Scatter(x=df_currency['Year'], y=df_currency['Value'], 
                                  mode='lines+markers',
                                  line=dict(color='black', dash='dash'),
                                  name="Exchange Rate"))

fig_currency.update_layout(
    title="Historical Lebanese Lira (LBP) Exchange Rate to USD",
    xaxis_title="Time (years)",
    yaxis_title="Lira Exchange Rate (LBP per 1 USD)",
    plot_bgcolor="lightgrey",
    yaxis=dict(tickmode='linear', tick0=0, dtick=1000),
    showlegend=False
)

steps = []
for i in range(len(df_currency)):
    step = dict(
        method="update",
        args=[{"x": [df_currency['Year'][:i+1]], "y": [df_currency['Value'][:i+1]]}], 
        label=str(df_currency['Year'].iloc[i]),
    )
    steps.append(step)

sliders = [dict(
    active=0,
    currentvalue={"prefix": "Time (years)="},
    pad={"t": 50},
    steps=steps
)]

fig_currency.update_layout(sliders=sliders)

# Display currency chart
st.plotly_chart(fig_currency)

st.markdown('<div style="padding: 10px; border-radius: 5px; margin-bottom: 10px;"><strong style="font-size: 18px;">⬇️ Don\'t miss this! Select the checkbox below:</strong></div>', unsafe_allow_html=True)

# -------- Additional Data (External Debt) with Checkbox ---------
show_debt_chart = st.checkbox('See additional plot regarding mounting Lebanese external debt')

if show_debt_chart:
  df_debt = pd.read_csv('https://linked.aub.edu.lb/pkgcube/data/ec4c40221073bbdf6f75b6c6127249c3_20240905_173222.csv')

  df_debt.columns = df_debt.columns.str.strip()

  df_debt_cleaned = df_debt[df_debt['Value'] > 1000]

  df_debt_avg = df_debt_cleaned.groupby('refPeriod', as_index=False)['Value'].mean()

  fig_debt = px.line(
        df_debt_avg,
        x='refPeriod', 
        y='Value',
        title="External Debt as a Function of Time (in Lebanon)",
        labels={'refPeriod': 'Time (years)', 'Value': 'External Debt (USD)'}
    )

  fig_debt.update_traces(line_color='black')  
  fig_debt.update_layout(plot_bgcolor='lightgrey')

  # Display the external debt chart
  st.plotly_chart(fig_debt)


st.markdown('<h3 style="font-size: 20px;">Key Insights</h3>', unsafe_allow_html=True)
st.markdown("""
- The Lebanese Lira exchange rate has increased by **355,465%** since the 1970s
- The Lebanese external debt has skyrocketed over the past 60 years, rising from **42mn USD to around 13bn USD**
""")

# -------- Conclusion for Chapter 2 --------
st.markdown('<h3 style="font-size: 20px;">Conclusion & Recommendation</h3>', unsafe_allow_html=True)

st.markdown("""
**Recommendation**  
Lebanon must implement reforms to halt the ongoing currency collapse and restore the value of the Lebanese Lira, aiming to curb dollarization and stabilize the economy.

**Reasons**  
- Lebanon’s mounting external debt and the 2020 Eurobond default have severely damaged investor confidence and accelerated currency devaluation.  
- The Lira’s freefall has led to rapid dollarization, where significant parts of the economy now rely on foreign currency, worsening inequality.  
- Continued currency depreciation erodes purchasing power, driving inflation and pushing more citizens into poverty.

**Outstanding Risks**  
- Hyperinflation if the Lira continues to lose value unchecked, risking further destabilization of the economy.  
- Additional defaults on international debt obligations, which could isolate Lebanon from financial markets and future investment.  
- Widening economic disparities between those with access to dollars and those relying on the weakening Lira, intensifying social unrest.

**Next Steps**  
- Engage in debt restructuring with international partners, potentially securing IMF support to manage repayments and stabilize the currency.  
- Enforce disciplined monetary policies that focus on reducing inflation and stabilizing the Lira.  
- Initiate structural reforms in critical sectors like banking and energy to reduce inefficiencies and ensure sustainable economic growth.  
- Gradually reduce reliance on the US dollar through strategic economic policies that promote the use of the Lebanese Lira while mitigating further volatility.
""")

