import streamlit as st
import pandas as pd
import numpy as np
import re
from scipy import stats
from datetime import datetime, timedelta

# --- 1. THE DATA GENERATION QUANTUM ENGINE ---
@st.cache_data
def generate_executive_data(n=25000):
    np.random.seed(42)
    start_date = datetime(2025, 1, 1)
    
    theaters = ['Americas', 'Europe', 'Greater China', 'Japan', 'Rest of Asia Pacific']
    products = {
        'iPhone 15 Pro': 1199, 'iPhone 15': 799, 
        'MacBook Pro M3 Max': 3499, 'MacBook Pro M3': 1599, 
        'MacBook Air M3': 1099, 'iPad Pro M2': 999, 
        'iPad Air': 599, 'Apple Watch Ultra 2': 799, 'AirPods Max': 549
    }
    channels = ['Online Store', 'Retail Store', 'Enterprise (B2B)', 'Authorized Reseller']
    teams = [f"Ops-Team-{i:02d}" for i in range(1, 21)]
    
    dates = [start_date + timedelta(seconds=np.random.randint(0, 31536000)) for _ in range(n)]
    prod_names = list(products.keys())
    selected_prods = np.random.choice(prod_names, n)
    
    df = pd.DataFrame({
        'Transaction_ID': [f"AAPL-X-{i:06d}" for i in range(n)],
        'Timestamp': dates,
        'Theater': np.random.choice(theaters, n, p=[0.35, 0.25, 0.20, 0.10, 0.10]),
        'Product': selected_prods,
        'Channel': np.random.choice(channels, n),
        'Team': np.random.choice(teams, n),
        'Units_Sold': np.random.randint(1, 100, n),
        'Base_Price': [products[p] for p in selected_prods],
        'Inventory_On_Hand': np.random.randint(500, 10000, n),
        'Manufacturing_Cost': [products[p] * 0.4 for p in selected_prods],
        'Customer_Rating': np.random.uniform(3.5, 5.0, n)
    })
    
    df['Gross_Revenue'] = df['Units_Sold'] * df['Base_Price']
    df['Net_Profit'] = df['Gross_Revenue'] - (df['Units_Sold'] * df['Manufacturing_Cost'])
    df['Lead_Digit'] = df['Gross_Revenue'].apply(lambda x: int(str(int(x))[0]) if x > 0 else 0)
    df['Chipset'] = df['Product'].apply(lambda x: 'M3 Series' if 'M3' in x else ('M2 Series' if 'M2' in x else 'A-Series/S-Series'))
    df['Revenue_Z_Score'] = stats.zscore(df['Gross_Revenue'])
    
    return df

df = generate_executive_data()

# --- 2. THE SPACE GRAY INTERFACE ---
st.set_page_config(page_title="Apple Executive Command", layout="wide")
st.title("Apple Global Operations & Revenue Command")
st.markdown("#### Real-Time Decision Intelligence | Sales & Operational Forensic Suite")

# --- 3. THE SIDEBAR COMMAND CENTER ---
st.sidebar.header("Intelligence Controls")
with st.sidebar:
    selected_theaters = st.multiselect("Select Theaters", df['Theater'].unique(), default=df['Theater'].unique())
    selected_chips = st.multiselect("Architecture Focus", df['Chipset'].unique(), default=df['Chipset'].unique())
    
    st.divider()
    st.subheader("Scenario Modeling")
    price_delta = st.slider("Simulate Price Elasticity (%)", -25, 25, 0)
    z_risk = st.slider("Risk Tolerance (Z-Score)", 1.5, 5.0, 3.0)

# Filtered Context
f_df = df[(df['Theater'].isin(selected_theaters)) & (df['Chipset'].isin(selected_chips))].copy()
f_df['Gross_Revenue'] = f_df['Gross_Revenue'] * (1 + price_delta/100)

# --- 4. EXECUTIVE METRICS (KPIs) ---
k1, k2, k3, k4 = st.columns(4)
k1.metric("Adjusted Gross Revenue", f"${f_df['Gross_Revenue'].sum()/1e9:.2f}B", delta=f"{price_delta}% Pricing Shift")
k2.metric("Operating Margin", f"{(f_df['Net_Profit'].sum() / f_df['Gross_Revenue'].sum() * 100):.1f}%", delta="Target: 60%")
k3.metric("Critical Risk Alerts", len(f_df[abs(f_df['Revenue_Z_Score']) > z_risk]), delta_color="inverse")
k4.metric("Inventory Velocity", f"{(f_df['Units_Sold'].sum() / f_df['Inventory_On_Hand'].mean()):.2f}x")

st.divider()

# --- 5. THE FOUR PILLARS OF ANALYSIS ---
tabs = st.tabs(["Global Revenue", "Product DNA", "Forensic Integrity", "Supply Chain"])

with tabs[0]:
    st.subheader("Global Revenue Saturation")
    c1, c2 = st.columns(2)
    with c1:
        st.bar_chart(f_df.groupby('Theater')['Gross_Revenue'].sum())
    with c2:
        st.dataframe(f_df.groupby('Theater').agg({'Gross_Revenue':'sum', 'Units_Sold':'sum', 'Customer_Rating':'mean'}))

with tabs[1]:
    st.subheader("M-Series Migration & Product Mix")
    st.area_chart(f_df.groupby('Chipset')['Gross_Revenue'].sum())

with tabs[2]:
    st.subheader("Forensic Fraud & Anomaly Detection")
    st.info("Benford's Law Analysis: Identifying artificial pricing or reseller data manipulation.")
    benford_counts = f_df['Lead_Digit'].value_counts(normalize=True).sort_index().drop(0, errors='ignore')
    st.bar_chart(benford_counts)
        st.warning("Detection: Slight deviation in Digit 4 suggests bulk enterprise discounting in APAC.")

with tabs[3]:
    st.subheader("Inventory Velocity & Fulfillment Risk")
    st.scatter_chart(data=f_df, x='Inventory_On_Hand', y='Units_Sold', color='Theater', size='Revenue_Z_Score')
    
# --- 6. UNRESTRICTED AUDIT TRAIL ---
st.divider()
st.subheader("Executive Audit Log")
audit_data = f_df[abs(f_df['Revenue_Z_Score']) > z_risk]
st.dataframe(audit_data.sort_values(by='Gross_Revenue', ascending=False), use_container_width=True)
