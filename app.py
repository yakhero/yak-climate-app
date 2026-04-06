import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import folium_static
from sklearn.ensemble import RandomForestClassifier
import plotly.express as px
import plotly.graph_objects as go

# ==========================================
# 1. HELPER FUNCTIONS (Instructions for Python)
# ==========================================

def get_recommendation(level):
    """Provides text based on the warning level"""
    if "Critical" in level:
        return "Immediate action required. Move herds to higher elevations."
    elif "High" in level:
        return "Prepare for migration within 3-5 days. Stock emergency fodder."
    elif "Moderate" in level:
        return "Monitor conditions. Plan alternate grazing routes."
    else:
        return "No immediate action needed. Continue monitoring."

def generate_sample_data():
    """Create fake but realistic data for prototype"""
    np.random.seed(42)
    n_points = 100
    
    data = {
        'latitude': np.random.uniform(35.5, 37.0, n_points),
        'longitude': np.random.uniform(74.0, 76.0, n_points),
        'elevation': np.random.uniform(2500, 5500, n_points),
        'temperature': np.random.uniform(-5, 15, n_points),
        'ndvi': np.random.uniform(0.1, 0.8, n_points),
        'snow_cover': np.random.uniform(0, 100, n_points),
        'yak_density': np.random.uniform(0, 50, n_points)
    }
    
    return pd.DataFrame(data)

def predict_vulnerability(data):
    """Calculate vulnerability score (0-100)"""
    # Simple weighted scoring for prototype
    vulnerability = (
        (data['temperature'] / 20 * 30) +  # Heat stress
        ((1 - data['ndvi']) * 40) +        # Forage availability
        (data['snow_cover'] / 100 * 30)     # Snow impact
    )
    return np.clip(vulnerability, 0, 100)

# ==========================================
# 2. PAGE CONFIGURATION & UI
# ==========================================

st.set_page_config(
    page_title="Yak Vulnerability Mapper",
    page_icon="🏔️",
    layout="wide"
)

# Title
st.title("🏔️ AI-Powered Yak Climate Vulnerability Mapper")
st.markdown("*Protecting Pakistan's Yak Heritage Through AI*")

# Sidebar for user inputs
with st.sidebar:
    st.header("📍 Select Region")
    region = st.selectbox(
        "Choose area in Gilgit-Baltistan",
        ["Hunza Valley", "Skardu", "Ghizer", "Shigar", "Khaplu"]
    )
    
    st.header("📊 Climate Parameters")
    temperature = st.slider("Temperature Anomaly (°C)", -2.0, 5.0, 1.5)
    snow_coverage = st.slider("Snow Cover Change (%)", -50, 50, -15)
    vegetation = st.slider("Vegetation Index (NDVI)", 0.0, 1.0, 0.3)
    
    st.header("🔮 Prediction Settings")
    forecast_days = st.slider("Forecast Period (days)", 7, 90, 30)
    
    if st.button("🚀 Generate Vulnerability Map", type="primary"):
        st.session_state['run_prediction'] = True

# Create tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "🗺️ Vulnerability Map", 
    "📈 Climate Trends", 
    "🚨 Early Warnings",
    "📋 Recommendations"
])

# ==========================================
# 3. TAB CONTENT
# ==========================================

with tab1:
    st.header("Real-Time Vulnerability Zones")
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Generate map
        m = folium.Map(location=[36.0, 75.0], zoom_start=8)
        df = generate_sample_data()
        df['vulnerability'] = predict_vulnerability(df)
        
        for idx, row in df.iterrows():
            if row['vulnerability'] > 66:
                color = 'red'
            elif row['vulnerability'] > 33:
                color = 'yellow'
            else:
                color = 'green'
            
            folium.CircleMarker(
                location=[row['latitude'], row['longitude']],
                radius=5,
                color=color,
                fill=True,
                popup=f"Vulnerability: {row['vulnerability']:.1f}%<br>Elevation: {row['elevation']:.0f}m"
            ).add_to(m)
        
        folium_static(m, width=800, height=500)
    
    with col2:
        st.metric("High Risk Zones", "23", "-5 from last month")
        st.metric("Safe Grazing Areas", "47", "+12")
        st.metric("Moderate Risk", "30", "-7")
        
        fig = px.pie(values=[23, 47, 30], 
                     names=['High Risk', 'Safe', 'Moderate'],
                     color_discrete_sequence=['red', 'green', 'yellow'])
        st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.header("Climate Trends Analysis")
    dates = pd.date_range(start='2023-01-01', periods=12, freq='ME')
    temp_trend = np.random.normal(0, 2, 12).cumsum() + 10
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dates, y=temp_trend, mode='lines+markers', name='Temperature Trend'))
    fig.update_layout(title='Temperature Anomaly (°C) - Last 12 Months',
                      xaxis_title='Month', yaxis_title='Temperature (°C)')
    st.plotly_chart(fig, use_container_width=True)
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Avg Temperature", "8.2°C", "+1.2°C")
    c2.metric("Snow Cover", "65%", "-15%")
    c3.metric("Vegetation Health", "0.42 NDVI", "-0.08")

with tab3:
    st.header("🚨 Early Warning System")
    warnings = [
        {"level": "⚠️ High", "message": "Heat stress predicted in lower valleys", "time": "2 hours ago"},
        {"level": "🟡 Moderate", "message": "Fodder shortage expected in Ghizer", "time": "5 hours ago"},
        {"level": "🔴 Critical", "message": "Early snowfall likely in Shigar", "time": "1 day ago"},
        {"level": "🟢 Info", "message": "Optimal migration window for Hunza", "time": "2 days ago"}
    ]
    
    for warning in warnings:
        with st.expander(f"{warning['level']} - {warning['message']}"):
            st.write(f"**Time:** {warning['time']}")
            # This now works because the function is defined at the top!
            st.write("**Recommendation:** " + get_recommendation(warning['level']))

with tab4:
    st.header("📋 AI-Powered Recommendations")
    st.subheader(f"Analysis for: {region}")
    
    recs = [
        "✅ **Migration Timing:** Delay by 7-10 days due to late snowmelt",
        "✅ **Grazing Corridor:** Use northern slopes - 40% lower risk",
        "✅ **Fodder Management:** Stock 20% extra fodder for winter",
        "✅ **Health Alert:** Watch for foot rot in lower wetlands",
        "✅ **Breeding Advice:** Postpone breeding by 1 month due to heat stress"
    ]
    for rec in recs:
        st.info(rec)

st.markdown("---")
st.markdown("🚀 *Prototype for Climate Vulnerability Mapping - Gilgit-Baltistan*")
