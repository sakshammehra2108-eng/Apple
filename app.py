import streamlit as st
import pandas as pd
import numpy as np
import re
from scipy import stats
from datetime import datetime, timedelta

# --- 1. THE "INFINITE LOOP" SALES ENGINE ---
@st.cache_data
def generate_apple_sales_data(n=15000):
    np.random.seed(42)
    start_date = datetime(2025, 1, 1)
    
    # Core Apple Data Structures
    theaters = ['Americas', 'Europe', 'Greater China', 'Japan', 'Rest of Asia Pacific']
    products = {
        'iPhone 15 Pro': 999, 'iPhone 15': 799, 
        'MacBook Pro M3': 1599, 'MacBook Air M3': 1099, 
        'iPad Pro': 799, 'iPad Air': 599, 'Apple Watch Ultra': 799
    }
    teams = [f"Team {chr(65+i)}" for i in range(12)] # Teams A through L
    
    # Generate unique transaction timestamps
    dates = [start_date + timedelta(seconds=np.random.randint(0, 31536000)) for _ in range(n)]
    
    product_list = list(products.keys())
    selected_prods = np.random.choice(product_list, n)
    
    df = pd.DataFrame({
        'Transaction_ID': [f"APL-{i:06d}" for i in range(n)],
        'Timestamp': dates,
        'Theater': np.random.choice(theaters, n),
        'Product': selected_prods,
        'Team': np.random.choice(teams, n),
        'Units_Sold': np.random.randint(1, 50, n),
        'Base_Price': [products[p] for p in selected_prods],
        'Inventory_Stock': np.random.randint(100, 5000, n)
    })
    
    # Financial Logic
    df['Revenue'] = df['Units_Sold'] * df['Base_Price']
    df['Hour'] = df['Timestamp'].dt.hour
    
    # --- FORENSIC & STRATEGIC ANALYTICS ---
    # 1. Price Integrity (Benford's Law Lead Digit)
    df['Lead_Digit'] = df['Revenue'].apply(lambda x: int(str(int(x))[0]) if x > 0 else 0)
    
    # 2. Quota Anomaly (Z-Score of Units Sold per Team)
    df['Team_Z_Score'] = stats.zscore(df['Units_Sold'])
    
    # 3. M-Series Chip Categorization (Regex)
    def chip_type(name):
        if re.search(r'M3', name): return 'M3 Series'
        if re.search(r'M2', name): return 'M2 Series'
        return 'Standard/A-Series'
    
    df['Chip_Architecture'] = df['Product'].apply(chip_type)
    
    return df

df = generate_apple_sales_data()

# --- 2. THE SPACE GRAY INTERFACE ---
st.set_page_config(page_title="Apple Sales Intelligence", layout="wide")
st.title(" Apple Global Sales & Regional Intelligence")
st.markdown("### Executive Sales Operations Suite")

# --- 3. THEATER & PRODUCT CONTROLS ---
st.sidebar.header("Global Theater Control")
with st.sidebar:
    selected_theater = st.multiselect("Select Theater", df['Theater'].unique(), default=df['Theater'].unique())
    selected_chip = st.multiselect("Chip Architecture", df['Chip_Architecture'].unique(), default=df['Chip_Architecture'].unique())
    
    st.divider()
    z_limit = st.slider("Quota Sensitivity (Z-Score)", 1.0, 5.0, 3.0)
    asp_adjust = st.slider("ASP Simulation (%)", -20, 20, 0)

# Filter Data
f_df = df[(df['Theater'].isin(selected_theater)) & (df['Chip_Architecture'].isin(selected_chip))]
f_df['Revenue'] = f_df['Revenue'] * (1 + asp_adjust/100)

# --- 4. EXECUTIVE METRICS (KPIs) ---
k1, k2, k3, k4 = st.columns(4)
k1.metric("Global Revenue", f"${f_df['Revenue'].sum()/1e6:.2f}M")
k2.metric("Avg Unit Sale", f"${f_df['Base_Price'].mean():,.0f}")

outlier_teams = f_df[abs(f_df['Team_Z_Score']) > z_limit]['Team'].nunique()
k3.metric("Outlier Teams", outlier_teams, delta="Requires Audit", delta_color="inverse")

inventory_velocity = f_df['Units_Sold'].sum() / f_df['Inventory_Stock'].mean()
k4.metric("Inventory Velocity", f"{inventory_velocity:.2f}x")

st.divider()

# --- 5. STRATEGIC ANALYTICS GRID ---
col_a, col_b = st.columns(2)

with col_a:
    st.subheader("Price Integrity Monitor (Benford's Law)")
    st.info("Detects unauthorized discounting. Deviations from the logarithmic curve suggest retail pricing breaches.")
    # Benford Analysis
    benford_counts = f_df['Lead_Digit'].value_counts(normalize=True).sort_index().drop(0, errors='ignore')
    st.bar_chart(benford_counts)
    

with col_b:
    st.subheader("M-Series Chip Migration Velocity")
    st.info("Tracking the adoption rate of M3 architecture vs. legacy M2/A-series stock.")
    chip_dist = f_df.groupby('Chip_Architecture')['Revenue'].sum()
    st.bar_chart(chip_dist)

st.divider()

col_c, col_d = st.columns(2)

with col_c:
    st.subheader("Revenue by Global Theater")
    theater_rev = f_df.groupby('Theater')['Revenue'].sum()
    st.line_chart(theater_rev)

with col_d:
    st.subheader("Unit Volume vs. Statistical Deviation")
    st.scatter_chart(data=f_df, x='Units_Sold', y='Revenue', color='Chip_Architecture', size='Team_Z_Score')
    

# --- 6. EXECUTIVE AUDIT TRAIL ---
st.subheader("Regional Performance & Quota Audit")
st.write("Transactions flagging high statistical deviation or critical inventory levels.")
critical_df = f_df[abs(f_df['Team_Z_Score']) > z_limit].sort_values(by='Revenue', ascending=False)
st.dataframe(critical_df[['Transaction_ID', 'Theater', 'Team', 'Product', 'Units_Sold', 'Revenue', 'Team_Z_Score']], use_container_width=True)
