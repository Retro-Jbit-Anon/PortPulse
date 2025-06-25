import streamlit as st
import pandas as pd
import numpy as np
import plotly as px

# Generate synthetic data
def generate_nclh_data(num_entries=150):
    np.random.seed(42)
    subsidiaries = ["NCL", "Oceania", "Regent Seven Seas"]
    ships = {
        "NCL": ["Norwegian Escape", "Norwegian Joy", "Norwegian Getaway", "Norwegian Pearl"],
        "Oceania": ["Marina", "Riviera", "Sirena", "Nautica"],
        "Regent Seven Seas": ["Seven Seas Splendor", "Seven Seas Navigator", "Seven Seas Mariner"]
    }
    countries = ["Italy", "Spain", "Greece", "France", "Portugal", "UK", "Germany", "Norway", "Croatia", "Netherlands"]
    ports = {
        "Italy": "Port of Naples", "Spain": "Port of Barcelona", "Greece": "Port of Piraeus",
        "France": "Port of Marseille", "Portugal": "Port of Lisbon", "UK": "Port of Southampton",
        "Germany": "Port of Hamburg", "Norway": "Port of Oslo", "Croatia": "Port of Dubrovnik",
        "Netherlands": "Port of Rotterdam"
    }
    
    data = []
    for _ in range(num_entries):
        subsidiary = np.random.choice(subsidiaries)
        ship = np.random.choice(ships[subsidiary])
        country = np.random.choice(countries)
        port = ports[country]
        port_status = np.random.choice(["Busy", "Normal"], p=[0.4, 0.6])
        fuel_used = np.random.uniform(5, 20)
        fuel_cost = np.random.choice([650, 670, 700, 660, 680, 720, 640, 690, 710, 655])
        warmup_time = np.random.choice([10, 12, 15, 18, 20, 22, 25, 28], p=[0.1, 0.1, 0.5, 0.1, 0.1, 0.05, 0.03, 0.02])
        sailing_delay = "Yes" if (port_status == "Busy" and np.random.random() > 0.3) else "No"
        
        data.append([
            subsidiary, ship, country, port, port_status, 
            round(fuel_used, 1), fuel_cost, warmup_time, 15, sailing_delay
        ])
    
    df = pd.DataFrame(data, columns=[
        "Subsidiary", "Ship_Name", "Port_Country", "Port_Name", "Port_Status",
        "Fuel_Used_MetricTons", "Fuel_Cost_Per_Ton ($)", "Engine_WarmUp_Time (mins)",
        "Optimal_WarmUp_Time (mins)", "Sailing_Delay_Due_To_Port_Busy"
    ])
    return df

# Streamlit App
st.set_page_config(layout="wide")
st.title("🚢 NCLH Cruise Ship Fuel Analytics Dashboard")
st.markdown("""
    **Key Features:**  
    - Warm-up efficiency analysis  
    - Fuel consumption and cost tracking  
    - Financial impact of operational delays  
""")

# Generate data
df = generate_nclh_data(150)
df["WarmUp_Status"] = df["Engine_WarmUp_Time (mins)"].apply(
    lambda x: "Optimal (≤15 mins)" if x <= 15 else "Non-Optimal (>15 mins)"
)
df["Extra_Fuel_Wasted"] = df.apply(
    lambda row: (row["Engine_WarmUp_Time (mins)"] - 15) * (row["Fuel_Used_MetricTons"] / 100) 
                if row["WarmUp_Status"] == "Non-Optimal (>15 mins)" else 0,
    axis=1
)
df["Financial_Loss_USD"] = df["Extra_Fuel_Wasted"] * df["Fuel_Cost_Per_Ton ($)"]

# Sidebar filters
st.sidebar.header("Filters")
selected_subsidiary = st.sidebar.multiselect(
    "Subsidiary", 
    options=df["Subsidiary"].unique(), 
    default=df["Subsidiary"].unique()
)

# Dynamic ship options
available_ships = df[df["Subsidiary"].isin(selected_subsidiary)]["Ship_Name"].unique() if selected_subsidiary else df["Ship_Name"].unique()
selected_ships = st.sidebar.multiselect(
    "Ships (Optional)", 
    options=available_ships,
    default=[]
)

# Apply filters
if selected_subsidiary and not selected_ships:
    filtered_df = df[df["Subsidiary"].isin(selected_subsidiary)]
elif selected_ships:
    filtered_df = df[df["Ship_Name"].isin(selected_ships)]
else:
    filtered_df = df

# ================== METRICS SECTION ==================
st.header("Performance Metrics")
col1, col2 = st.columns(2)
total_wasted_fuel = filtered_df["Extra_Fuel_Wasted"].sum()
total_loss_usd = filtered_df["Financial_Loss_USD"].sum()
col1.metric("Total Extra Fuel Wasted", f"{total_wasted_fuel:.2f} Metric Tons")
col2.metric("Total Financial Loss", f"${total_loss_usd:,.2f} USD")

# ================== WARM-UP EFFICIENCY GRAPH ==================
st.header("Warm-Up Efficiency Analysis")
group_by_warmup = st.selectbox(
    "Group Warm-Up Data By", 
    ["Ship_Name", "Subsidiary", "Port_Country"], 
    key="warmup_group",
    index=0
)

# Calculate percentages
counts = filtered_df.groupby([group_by_warmup, "WarmUp_Status"]).size().unstack(fill_value=0)
percentages = counts.div(counts.sum(axis=1), axis=0) * 100
plot_df = percentages.reset_index().melt(
    id_vars=group_by_warmup, 
    value_vars=["Optimal (≤15 mins)", "Non-Optimal (>15 mins)"], 
    var_name="WarmUp_Status", 
    value_name="Percentage"
)

# Create stacked bar chart
fig_warmup = px.bar(
    plot_df,
    x=group_by_warmup,
    y="Percentage",
    color="WarmUp_Status",
    color_discrete_map={"Optimal (≤15 mins)": "green", "Non-Optimal (>15 mins)": "yellow"},
    title=f"Warm-Up Efficiency by {group_by_warmup}",
    labels={"Percentage": "% of Trips"},
    hover_data={"Percentage": ":.1f%"},
    barmode="stack"
)
st.plotly_chart(fig_warmup, use_container_width=True)

# ================== FUEL USAGE GRAPH ==================
st.header("Fuel Consumption Analytics")
group_by_fuel = st.selectbox(
    "Group Fuel Data By", 
    ["Ship_Name", "Subsidiary", "Port_Country"], 
    key="fuel_group",
    index=0
)

# Aggregate fuel data with warmup status
fuel_df = filtered_df.groupby([group_by_fuel, "WarmUp_Status"]).agg(
    Total_Fuel_Used=("Fuel_Used_MetricTons", "sum"),
    Count=("Fuel_Used_MetricTons", "count")
).reset_index()

# Create stacked bar chart for fuel usage
fig_fuel = px.bar(
    fuel_df,
    x=group_by_fuel,
    y="Total_Fuel_Used",
    color="WarmUp_Status",
    color_discrete_map={"Optimal (≤15 mins)": "green", "Non-Optimal (>15 mins)": "yellow"},
    title=f"Fuel Usage by {group_by_fuel} (Split by Warm-Up Efficiency)",
    labels={"Total_Fuel_Used": "Total Fuel Used (Metric Tons)"},
    hover_data=["Count"],
    barmode="stack"
)

# Update layout
fig_fuel.update_layout(
    yaxis=dict(title="Fuel Used (Metric Tons)"),
    hovermode="x unified",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)

st.plotly_chart(fig_fuel, use_container_width=True)

# ================== RAW DATA SECTION ==================
if st.checkbox("Show Detailed Data"):
    st.dataframe(filtered_df.sort_values("Extra_Fuel_Wasted", ascending=False))
