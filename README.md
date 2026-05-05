# ✈️ FAA Aviation Incident Analysis Dashboard

An interactive data analysis dashboard built with Python and Streamlit that explores 25 years of US aviation incident data from the NTSB database. Built by an FAA certified Airframe Mechanic with firsthand knowledge of aviation safety, maintenance, and regulatory compliance.

**[Live Demo](https://faa-aviation-dashboard-ceua43sscr4dsjxyvisprs.streamlit.app/)** | **[NTSB Data Source](https://www.ntsb.gov/Pages/AviationQueryv2.aspx)**

---

## Overview

This dashboard analyzes 39,000+ aviation incidents reported to the National Transportation Safety Board (NTSB) between 2000 and 2025. It enables users to explore trends in aviation safety, identify high-risk aircraft types, and understand the conditions surrounding incidents across the United States.

What makes this project unique is the domain expertise behind it. As an FAA certified Airframe Mechanic with 8 years of aerospace manufacturing experience, I understand what these records represent beyond the data — the regulatory frameworks, the maintenance implications, and the real-world consequences behind every row.

---

## Features

- **Interactive Filters** — filter by year range, injury level, and weather condition
- **KPI Metrics** — total incidents, fatal incidents, total fatalities, and states affected update dynamically with filters
- **Incidents by Year** — trend line showing aviation safety improvements over 25 years
- **Weather Condition Breakdown** — VMC vs IMC incident distribution
- **Top 10 Aircraft Makes** — identifies which manufacturers appear most frequently in incident reports
- **Top 10 States by Incidents** — geographic distribution of incidents across the US
- **Injury Level Breakdown** — pie chart showing fatal, serious, and minor injury distribution
- **Purpose of Flight Analysis** — personal, instructional, commercial, and other flight purposes
- **US Choropleth Map** — interactive heatmap showing incident density by state
- **Raw Data Table** — searchable and sortable incident records with key fields

---

## Tech Stack

- **Python** — core data processing and application logic
- **Pandas** — data cleaning, transformation, and analysis
- **Streamlit** — interactive web dashboard framework
- **Plotly** — interactive charts and choropleth map
- **SQLAlchemy** — database interface layer

---

## Key Insights

- Aviation incidents have declined significantly since 2000, reflecting improvements in safety regulation and technology
- The majority of incidents occur under Visual Meteorological Conditions (VMC), suggesting human factors play a larger role than weather
- Cessna aircraft appear most frequently due to their dominance in the general aviation fleet, not disproportionate risk
- California, Texas, and Florida lead in incident counts, correlating directly with registered aircraft population and flight activity
- Personal flight is the most common purpose of flight in incident reports, highlighting general aviation as the highest risk segment

---

## Data Source

Data sourced from the **National Transportation Safety Board (NTSB) Aviation Accident Database**, a public dataset maintained by the US federal government.

- Source: [NTSB Aviation Query](https://www.ntsb.gov/Pages/AviationQueryv2.aspx)
- Date range: January 2000 – Present
- Records: 39,560 incidents
- Geography: United States and territories

---

## Running Locally

```bash
# Clone the repository
git clone https://github.com/jemrich18/faa-aviation-dashboard.git
cd faa-aviation-dashboard

# Install dependencies
pip install -r requirements.txt

# Download the dataset
# Visit https://www.ntsb.gov/Pages/AviationQueryv2.aspx
# Set Event Start Date to 01/01/2000, Country to United States
# Export as CSV and save as faa_incidents.csv in the project root

# Run the dashboard
streamlit run main.py
```

---

## About the Developer

I'm an FAA certified Airframe Mechanic transitioning into software development. I built this project to combine my domain expertise in aviation with my technical skills in Python and data analysis. Every insight in this dashboard is informed by real experience working in aerospace manufacturing under FAA and ITAR compliance frameworks.

Portfolio: [jemrich.dev](https://www.jemrich.dev)
GitHub: [github.com/jemrich18](https://github.com/jemrich18)

---

## License

MIT License — free to use and modify with attribution.