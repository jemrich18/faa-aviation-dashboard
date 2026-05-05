import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="FAA Aviation Incident Dashboard",
    page_icon="✈️",
    layout="wide"
)

@st.cache_data
def load_data():
    df = pd.read_csv("faa_incidents.csv", low_memory=False)
    df['EventDate'] = pd.to_datetime(df['EventDate'], errors='coerce')
    df['Year'] = df['EventDate'].dt.year
    df['Make'] = df['Make'].str.upper().str.strip()
    purpose_map = {
    'PERS': 'Personal',
    'INST': 'Instructional',
    'AAPL': 'Aerial Application',
    'BUS': 'Business',
    'POSI': 'Positioning',
    'OWRK': 'Other Work',
    'AOBV': 'Aerial Observation',
    'FLTS': 'Flight Test',
    'UNK': 'Unknown',
    'PUBU': 'Public Use',
    'FERY': 'Ferry',
    'SKYD': 'Skydiving',
    'EXEC': 'Executive',
    'MED': 'Medical',
    'FIRE': 'Firefighting'
}
    df['PurposeOfFlight'] = df['PurposeOfFlight'].map(purpose_map).fillna(df['PurposeOfFlight'])
    weather_map = {
    'VMC': 'Visual Meteorological Conditions (VMC)',
    'IMC': 'Instrument Meteorological Conditions (IMC)',
    'Unknown': 'Unknown'
}
    df['WeatherCondition'] = df['WeatherCondition'].map(weather_map).fillna(df['WeatherCondition'])
    return df

df = load_data()

st.title("✈️ FAA Aviation Incident Analysis Dashboard")
st.markdown("Analysis of 39,000+ US aviation incidents from 2000–present | Data: NTSB")

# --- SIDEBAR FILTERS ---
st.sidebar.header("Filters")
years = sorted(df['Year'].dropna().unique())
selected_years = st.sidebar.slider("Year Range", int(min(years)), int(max(years)), (2000, 2024))
selected_injury = st.sidebar.multiselect("Injury Level", df['HighestInjuryLevel'].dropna().unique(), default=df['HighestInjuryLevel'].dropna().unique())
selected_weather = st.sidebar.multiselect("Weather Condition", df['WeatherCondition'].dropna().unique(), default=df['WeatherCondition'].dropna().unique())

filtered = df[
    (df['Year'] >= selected_years[0]) &
    (df['Year'] <= selected_years[1]) &
    (df['HighestInjuryLevel'].isin(selected_injury)) &
    (df['WeatherCondition'].isin(selected_weather))
]

# --- KPI METRICS ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Incidents", f"{len(filtered):,}")
col2.metric("Fatal Incidents", f"{filtered['FatalInjuryCount'].gt(0).sum():,}")
col3.metric("Total Fatalities", f"{int(filtered['FatalInjuryCount'].sum()):,}")
col4.metric("States Affected", f"{filtered['State'].nunique()}")

st.divider()

# --- INCIDENTS BY YEAR ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("Incidents by Year")
    yearly = filtered.groupby('Year').size().reset_index(name='Incidents')
    fig = px.line(yearly, x='Year', y='Incidents', markers=True, color_discrete_sequence=['#00B4D8'])
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Incidents by Weather Condition")
    weather = filtered['WeatherCondition'].value_counts().reset_index()
    weather.columns = ['Weather', 'Count']
    fig2 = px.bar(weather, x='Weather', y='Count', color='Count', color_continuous_scale='Blues')
    fig2.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig2, use_container_width=True)

st.divider()

# --- US MAP ---
st.subheader("Incident Density by State")
map_data = filtered.groupby('State').size().reset_index(name='Incidents')

state_abbrev = {
    'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR',
    'California': 'CA', 'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE',
    'Florida': 'FL', 'Georgia': 'GA', 'Hawaii': 'HI', 'Idaho': 'ID',
    'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA', 'Kansas': 'KS',
    'Kentucky': 'KY', 'Louisiana': 'LA', 'Maine': 'ME', 'Maryland': 'MD',
    'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN', 'Mississippi': 'MS',
    'Missouri': 'MO', 'Montana': 'MT', 'Nebraska': 'NE', 'Nevada': 'NV',
    'New Hampshire': 'NH', 'New Jersey': 'NJ', 'New Mexico': 'NM', 'New York': 'NY',
    'North Carolina': 'NC', 'North Dakota': 'ND', 'Ohio': 'OH', 'Oklahoma': 'OK',
    'Oregon': 'OR', 'Pennsylvania': 'PA', 'Rhode Island': 'RI', 'South Carolina': 'SC',
    'South Dakota': 'SD', 'Tennessee': 'TN', 'Texas': 'TX', 'Utah': 'UT',
    'Vermont': 'VT', 'Virginia': 'VA', 'Washington': 'WA', 'West Virginia': 'WV',
    'Wisconsin': 'WI', 'Wyoming': 'WY'
}

map_data['Code'] = map_data['State'].map(state_abbrev)
map_data = map_data.dropna(subset=['Code'])

fig_map = px.choropleth(
    map_data,
    locations='Code',
    locationmode='USA-states',
    color='Incidents',
    scope='usa',
    color_continuous_scale='Reds',
    labels={'Incidents': 'Total Incidents'},
    hover_name='State'
)
fig_map.update_layout(
    paper_bgcolor='rgba(0,0,0,0)',
    geo=dict(bgcolor='rgba(0,0,0,0)')
)
st.plotly_chart(fig_map, use_container_width=True)

# --- TOP AIRCRAFT AND STATES ---
col3, col4 = st.columns(2)

with col3:
    st.subheader("Top 10 Aircraft Makes by Incidents")
    makes = filtered['Make'].value_counts().head(10).reset_index()
    makes.columns = ['Make', 'Count']
    fig3 = px.bar(makes, x='Count', y='Make', orientation='h', color='Count', color_continuous_scale='Reds')
    fig3.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    st.subheader("Top 10 States by Incidents")
    states = filtered['State'].value_counts().head(10).reset_index()
    states.columns = ['State', 'Count']
    fig4 = px.bar(states, x='Count', y='State', orientation='h', color='Count', color_continuous_scale='Oranges')
    fig4.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig4, use_container_width=True)

st.divider()

# --- INJURY BREAKDOWN AND PURPOSE OF FLIGHT ---
col5, col6 = st.columns(2)

with col5:
    st.subheader("Incidents by Injury Level")
    injury = filtered['HighestInjuryLevel'].value_counts().reset_index()
    injury.columns = ['Injury Level', 'Count']
    fig5 = px.pie(injury, values='Count', names='Injury Level', color_discrete_sequence=px.colors.sequential.RdBu)
    fig5.update_layout(paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig5, use_container_width=True)

with col6:
    st.subheader("Top 10 Purpose of Flight")
    purpose = filtered['PurposeOfFlight'].value_counts().head(10).reset_index()
    purpose.columns = ['Purpose', 'Count']
    fig6 = px.bar(purpose, x='Count', y='Purpose', orientation='h', color='Count', color_continuous_scale='Greens')
    fig6.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig6, use_container_width=True)

st.divider()

# --- RAW DATA ---
st.subheader("Raw Incident Data")
st.dataframe(filtered[['EventDate', 'Make', 'Model', 'State', 'HighestInjuryLevel', 'FatalInjuryCount', 'WeatherCondition', 'PurposeOfFlight', 'AirCraftDamage']].sort_values('EventDate', ascending=False), use_container_width=True)