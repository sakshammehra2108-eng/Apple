import streamlit as st
import pandas as pd
import numpy as np
import re
from scipy import stats
from datetime import datetime, timedelta

# --- 1. THE ARCHIVAL SKU MASTER (EXACT INTEGRATION) ---
sku_master = {
    'iPhone': {
        'iPhone (Original) 2007': ['Silver/Black'],
        'iPhone 3G 2008': ['Black', 'White'],
        'iPhone 3GS 2009': ['Black', 'White'],
        'iPhone 4 2010': ['Black', 'White'],
        'iPhone 4s 2011': ['Black', 'White'],
        'iPhone 5 2012': ['Black', 'White'],
        'iPhone 5c 2013': ['Blue', 'Green', 'Pink', 'Yellow', 'White'],
        'iPhone 5s 2013': ['Space Gray', 'Silver', 'Gold'],
        'iPhone 6 2014': ['Space Gray', 'Silver', 'Gold'],
        'iPhone 6 Plus 2014': ['Space Gray', 'Silver', 'Gold'],
        'iPhone 6s 2015': ['Space Gray', 'Silver', 'Gold', 'Rose Gold'],
        'iPhone 6s Plus 2015': ['Space Gray', 'Silver', 'Gold', 'Rose Gold'],
        'iPhone SE (1st Gen) 2016': ['Space Gray', 'Silver', 'Gold', 'Rose Gold'],
        'iPhone 7 2016': ['Jet Black', 'Black', 'Silver', 'Gold', 'Rose Gold', '(PRODUCT)RED'],
        'iPhone 7 Plus 2016': ['Jet Black', 'Black', 'Silver', 'Gold', 'Rose Gold', '(PRODUCT)RED'],
        'iPhone 8 2017': ['Space Gray', 'Silver', 'Gold', '(PRODUCT)RED'],
        'iPhone 8 Plus 2017': ['Space Gray', 'Silver', 'Gold', '(PRODUCT)RED'],
        'iPhone X 2017': ['Space Gray', 'Silver'],
        'iPhone XR 2018': ['Black', 'White', 'Blue', 'Yellow', 'Coral', '(PRODUCT)RED'],
        'iPhone XS 2018': ['Space Gray', 'Silver', 'Gold'],
        'iPhone XS Max 2018': ['Space Gray', 'Silver', 'Gold'],
        'iPhone 11 2019': ['Black', 'White', 'Green', 'Yellow', 'Purple', '(PRODUCT)RED'],
        'iPhone 11 Pro 2019': ['Space Gray', 'Silver', 'Gold', 'Midnight Green'],
        'iPhone 11 Pro Max 2019': ['Space Gray', 'Silver', 'Gold', 'Midnight Green'],
        'iPhone SE (2nd Gen) 2020': ['Black', 'White', '(PRODUCT)RED'],
        'iPhone 12 mini 2020': ['Black', 'White', 'Blue', 'Green', '(PRODUCT)RED', 'Purple'],
        'iPhone 12 2020': ['Black', 'White', 'Blue', 'Green', '(PRODUCT)RED', 'Purple'],
        'iPhone 12 Pro 2020': ['Pacific Blue', 'Gold', 'Graphite', 'Silver'],
        'iPhone 12 Pro Max 2020': ['Pacific Blue', 'Gold', 'Graphite', 'Silver'],
        'iPhone 13 mini 2021': ['Pink', 'Blue', 'Midnight', 'Starlight', '(PRODUCT)RED', 'Green'],
        'iPhone 13 2021': ['Pink', 'Blue', 'Midnight', 'Starlight', '(PRODUCT)RED', 'Green'],
        'iPhone 13 Pro 2021': ['Sierra Blue', 'Silver', 'Gold', 'Graphite', 'Alpine Green'],
        'iPhone 13 Pro Max 2021': ['Sierra Blue', 'Silver', 'Gold', 'Graphite', 'Alpine Green'],
        'iPhone SE (3rd Gen) 2022': ['Midnight', 'Starlight', '(PRODUCT)RED'],
        'iPhone 14 2022': ['Blue', 'Purple', 'Midnight', 'Starlight', '(PRODUCT)RED', 'Yellow'],
        'iPhone 14 Plus 2022': ['Blue', 'Purple', 'Midnight', 'Starlight', '(PRODUCT)RED', 'Yellow'],
        'iPhone 14 Pro 2022': ['Deep Purple', 'Gold', 'Silver', 'Space Black'],
        'iPhone 14 Pro Max 2022': ['Deep Purple', 'Gold', 'Silver', 'Space Black'],
        'iPhone 15 2023': ['Pink', 'Yellow', 'Green', 'Blue', 'Black'],
        'iPhone 15 Plus 2023': ['Pink', 'Yellow', 'Green', 'Blue', 'Black'],
        'iPhone 15 Pro 2023': ['Black Titanium', 'White Titanium', 'Blue Titanium', 'Natural Titanium'],
        'iPhone 15 Pro Max 2023': ['Black Titanium', 'White Titanium', 'Blue Titanium', 'Natural Titanium'],
        'iPhone 16 2024': ['Ultramarine', 'Teal', 'Pink', 'White', 'Black'],
        'iPhone 16 Plus 2024': ['Ultramarine', 'Teal', 'Pink', 'White', 'Black'],
        'iPhone 16 Pro 2024': ['Desert Titanium', 'Natural Titanium', 'Black Titanium', 'White Titanium'],
        'iPhone 16 Pro Max 2024': ['Desert Titanium', 'Natural Titanium', 'Black Titanium', 'White Titanium'],
        'iPhone 16e 2025': ['Blue', 'Pink', 'White', 'Black', 'Green'],
        'iPhone 17 2025': ['Silver', 'Teal', 'Midnight'],
        'iPhone Air 2025': ['Silver', 'Teal', 'Midnight'],
        'iPhone 17 Pro 2025': ['Silver', 'Cosmic Orange', 'Deep Blue'],
        'iPhone 17 Pro Max 2025': ['Silver', 'Cosmic Orange', 'Deep Blue'],
    },
    'iPad': {
        'iPad (1st Gen) 2010': ['Silver/Black'],
        'iPad 2 2011': ['Black', 'White'],
        'iPad (3rd Gen) 2012': ['Black', 'White'],
        'iPad (4th Gen) 2012': ['Black', 'White'],
        'iPad mini (1st Gen) 2012': ['Black', 'White'],
        'iPad Air (1st Gen) 2013': ['Space Gray', 'Silver'],
        'iPad mini 2 2013': ['Space Gray', 'Silver'],
        'iPad Air 2 2014': ['Space Gray', 'Silver', 'Gold'],
        'iPad mini 3 2014': ['Space Gray', 'Silver', 'Gold'],
        'iPad mini 4 2015': ['Space Gray', 'Silver', 'Gold'],
        'iPad Pro 12.9" (1st Gen) 2015': ['Space Gray', 'Silver', 'Gold'],
        'iPad Pro 9.7" 2016': ['Space Gray', 'Silver', 'Gold', 'Rose Gold'],
        'iPad (5th Gen) 2017': ['Space Gray', 'Silver', 'Gold'],
        'iPad Pro 10.5" 2017': ['Space Gray', 'Silver', 'Gold', 'Rose Gold'],
        'iPad Pro 12.9" (2nd Gen) 2017': ['Space Gray', 'Silver', 'Gold'],
        'iPad (6th Gen) 2018': ['Space Gray', 'Silver', 'Gold'],
        'iPad Pro 11" (1st Gen) 2018': ['Space Gray', 'Silver'],
        'iPad Pro 12.9" (3rd Gen) 2018': ['Space Gray', 'Silver'],
        'iPad Air (3rd Gen) 2019': ['Space Gray', 'Silver', 'Gold'],
        'iPad mini (5th Gen) 2019': ['Space Gray', 'Silver', 'Gold'],
        'iPad (7th Gen) 2019': ['Space Gray', 'Silver', 'Gold'],
        'iPad (8th Gen) 2020': ['Space Gray', 'Silver', 'Gold'],
        'iPad Air (4th Gen) 2020': ['Space Gray', 'Silver', 'Rose Gold', 'Green', 'Sky Blue'],
        'iPad Pro 11" (2nd Gen) 2020': ['Space Gray', 'Silver'],
        'iPad Pro 12.9" (4th Gen) 2020': ['Space Gray', 'Silver'],
        'iPad (9th Gen) 2021': ['Space Gray', 'Silver'],
        'iPad mini (6th Gen) 2021': ['Space Gray', 'Pink', 'Purple', 'Starlight'],
        'iPad Pro 11" (3rd Gen) 2021': ['Space Gray', 'Silver'],
        'iPad Pro 12.9" (5th Gen) 2021': ['Space Gray', 'Silver'],
        'iPad (10th Gen) 2022': ['Blue', 'Pink', 'Yellow', 'Silver'],
        'iPad Pro 11" (4th Gen) 2022': ['Space Gray', 'Silver'],
        'iPad Pro 12.9" (6th Gen) 2022': ['Space Gray', 'Silver'],
        'iPad Air 11" M2 2024': ['Space Gray', 'Blue', 'Purple', 'Starlight'],
        'iPad Air 13" M2 2024': ['Space Gray', 'Blue', 'Purple', 'Starlight'],
        'iPad Pro 11" M4 2024': ['Space Black', 'Silver'],
        'iPad Pro 13" M4 2024': ['Space Black', 'Silver'],
        'iPad (11th Gen) A16 2025': ['Blue', 'Pink', 'Yellow', 'Silver'],
        'iPad Air 11" M3 2025': ['Space Gray', 'Blue', 'Purple', 'Starlight'],
        'iPad Air 13" M3 2025': ['Space Gray', 'Blue', 'Purple', 'Starlight'],
        'iPad Pro 11" M5 2025': ['Space Black', 'Silver'],
        'iPad Pro 13" M5 2025': ['Space Black', 'Silver'],
    },
    'Mac': {
        'iMac G3 1998-2003': ['Bondi Blue', 'Grape', 'Lime', 'Strawberry', 'Tangerine', 'Blueberry', 'Graphite'],
        'iMac G4 2002-2004': ['White'],
        'iMac G5 2004-2006': ['White'],
        'iMac (Intel) 2006-2021': ['Silver', 'Space Gray'],
        'iMac 24" M1 2021': ['Blue', 'Green', 'Pink', 'Silver', 'Yellow', 'Orange', 'Purple'],
        'iMac 24" M3 2023': ['Blue', 'Green', 'Pink', 'Silver', 'Yellow', 'Orange', 'Purple'],
        'iMac 24" M4 2024': ['Blue', 'Green', 'Pink', 'Silver', 'Yellow', 'Orange', 'Purple'],
        'MacBook 2006-2012': ['White', 'Black'],
        'MacBook Air 2008-2018': ['Silver'],
        'MacBook Air M1 2020': ['Space Gray', 'Silver', 'Gold'],
        'MacBook Air M2 2022': ['Space Gray', 'Silver', 'Starlight', 'Midnight'],
        'MacBook Air M3 2024': ['Space Gray', 'Silver', 'Starlight', 'Midnight'],
        'MacBook Pro 13" 2016-2022': ['Space Gray', 'Silver'],
        'MacBook Pro 14" M1 Pro/Max 2021': ['Space Gray', 'Silver'],
        'MacBook Pro 16" M1 Pro/Max 2021': ['Space Gray', 'Silver'],
        'MacBook Pro 14" M2 Pro/Max 2023': ['Space Gray', 'Silver'],
        'MacBook Pro 16" M2 Pro/Max 2023': ['Space Gray', 'Silver'],
        'MacBook Pro 14" M3/M3 Pro/Max 2023': ['Space Black', 'Silver'],
        'MacBook Pro 16" M3 Pro/Max 2023': ['Space Black', 'Silver'],
        'MacBook Pro 14" M4/M4 Pro/Max 2024': ['Space Black', 'Silver'],
        'MacBook Pro 16" M4 Pro/Max 2024': ['Space Black', 'Silver'],
        'Mac mini 2005-2020': ['Silver'],
        'Mac mini M1 2020': ['Silver'],
        'Mac mini M2 2023': ['Silver'],
        'Mac mini M4 2024': ['Silver'],
        'Mac Pro 2006-2019': ['Silver'],
        'Mac Pro 2019': ['Space Gray'],
        'Mac Pro M2 Ultra 2023': ['Silver'],
        'Mac Studio M1 Max/Ultra 2022': ['Silver'],
        'Mac Studio M2 Max/Ultra 2023': ['Silver'],
    },
    'Apple Watch': {
        'Apple Watch (1st Gen) 2015 Sport': ['Space Gray Aluminum', 'Silver Aluminum', 'Gold Aluminum', 'Rose Gold Aluminum'],
        'Apple Watch (1st Gen) 2015 Standard': ['Stainless Steel', 'Space Black Stainless Steel'],
        'Apple Watch (1st Gen) 2015 Edition': ['18K Yellow Gold', '18K Rose Gold'],
        'Apple Watch Series 1 2016': ['Space Gray Aluminum', 'Silver Aluminum', 'Gold Aluminum', 'Rose Gold Aluminum'],
        'Apple Watch Series 2 2016': ['Space Gray Aluminum', 'Silver Aluminum', 'Gold Aluminum', 'Rose Gold Aluminum', 'Stainless Steel', 'Space Black Stainless Steel', 'White Ceramic'],
        'Apple Watch Series 3 2017': ['Space Gray Aluminum', 'Silver Aluminum', 'Gold Aluminum', 'Stainless Steel', 'Space Black Stainless Steel', 'White Ceramic'],
        'Apple Watch Series 4 2018': ['Space Gray Aluminum', 'Silver Aluminum', 'Gold Aluminum', 'Stainless Steel', 'Space Black Stainless Steel', 'Gold Stainless Steel'],
        'Apple Watch Series 5 2019': ['Space Gray Aluminum', 'Silver Aluminum', 'Gold Aluminum', 'Stainless Steel', 'Space Black Stainless Steel', 'Gold Stainless Steel', 'White Ceramic', 'Titanium', 'Space Black Titanium'],
        'Apple Watch SE (1st Gen) 2020': ['Space Gray Aluminum', 'Silver Aluminum', 'Gold Aluminum'],
        'Apple Watch Series 6 2020': ['Space Gray Aluminum', 'Silver Aluminum', 'Gold Aluminum', 'Blue Aluminum', 'Red Aluminum', 'Stainless Steel', 'Space Black Stainless Steel', 'Gold Stainless Steel'],
        'Apple Watch Series 7 2021': ['Midnight Aluminum', 'Starlight Aluminum', 'Green Aluminum', 'Blue Aluminum', 'Red Aluminum', 'Stainless Steel', 'Space Black Stainless Steel', 'Gold Stainless Steel'],
        'Apple Watch SE (2nd Gen) 2022': ['Midnight Aluminum', 'Starlight Aluminum', 'Silver Aluminum'],
        'Apple Watch Series 8 2022': ['Midnight Aluminum', 'Starlight Aluminum', 'Silver Aluminum', 'Red Aluminum', 'Stainless Steel', 'Space Black Stainless Steel', 'Gold Stainless Steel'],
        'Apple Watch Ultra 2022': ['Natural Titanium'],
        'Apple Watch Series 9 2023': ['Midnight Aluminum', 'Starlight Aluminum', 'Silver Aluminum', 'Pink Aluminum', 'Red Aluminum', 'Stainless Steel', 'Space Black Stainless Steel', 'Gold Stainless Steel'],
        'Apple Watch Ultra 2 2023': ['Natural Titanium', 'Black Titanium'],
        'Apple Watch Series 10 2024': ['Jet Black Aluminum', 'Rose Gold Aluminum', 'Silver Aluminum', 'Natural Titanium', 'Gold Titanium', 'Slate Titanium'],
        'Apple Watch SE (3rd Gen) 2025': ['Midnight Aluminum', 'Starlight Aluminum'],
        'Apple Watch Series 11 2025': ['Jet Black Aluminum', 'Rose Gold Aluminum', 'Silver Aluminum', 'Space Gray Aluminum', 'Natural Titanium', 'Gold Titanium', 'Slate Titanium'],
        'Apple Watch Ultra 3 2025': ['Natural Titanium', 'Black Titanium'],
    },
    'AirPods': {
        'AirPods (1st Gen) 2016': ['White'],
        'AirPods (2nd Gen) 2019': ['White'],
        'AirPods Pro (1st Gen) 2019': ['White'],
        'AirPods Max 2020': ['Space Gray', 'Silver', 'Sky Blue', 'Green', 'Pink'],
        'AirPods (3rd Gen) 2021': ['White'],
        'AirPods Pro (2nd Gen) 2022': ['White'],
        'AirPods 4 2024': ['White'],
        'AirPods 4 with ANC 2024': ['White'],
        'AirPods Max USB-C 2024': ['Midnight', 'Starlight', 'Blue', 'Purple', 'Orange'],
        'AirPods Pro 3 2025': ['White'],
    },
    'Apple TV': {
        'Apple TV (1st Gen) 2007': ['Silver'],
        'Apple TV (2nd Gen) 2010': ['Black'],
        'Apple TV (3rd Gen) 2012': ['Black'],
        'Apple TV HD 2015': ['Black'],
        'Apple TV 4K (1st Gen) 2017': ['Black'],
        'Apple TV 4K (2nd Gen) 2021': ['Black'],
        'Apple TV 4K (3rd Gen) 2022': ['Black'],
    },
    'HomePod': {
        'HomePod (1st Gen) 2018': ['Space Gray', 'White'],
        'HomePod mini 2020': ['Space Gray', 'White', 'Orange', 'Yellow', 'Blue'],
        'HomePod (2nd Gen) 2023': ['Midnight', 'White'],
    },
    'iPod': {
        'iPod (1st-4th Gen) 2001-2004': ['White'],
        'iPod mini 2004-2005': ['Silver', 'Gold', 'Blue', 'Pink', 'Green'],
        'iPod (5th Gen) Video 2005': ['White', 'Black'],
        'iPod nano (1st Gen) 2005': ['White', 'Black'],
        'iPod nano (2nd Gen) 2006': ['Silver', 'Pink', 'Green', 'Blue', 'Black', '(PRODUCT)RED'],
        'iPod shuffle (1st Gen) 2005': ['White'],
        'iPod shuffle (2nd Gen) 2006': ['Silver', 'Pink', 'Green', 'Blue', 'Orange'],
        'iPod Classic 2007-2009': ['Silver', 'Black'],
        'iPod nano (3rd-7th Gen) 2007-2012': ['Silver', 'Black', 'Blue', 'Green', 'Yellow', 'Orange', 'Pink', 'Purple', '(PRODUCT)RED'],
        'iPod shuffle (3rd-4th Gen) 2009-2012': ['Silver', 'Black', 'Blue', 'Green', 'Pink', 'Orange', 'Yellow', '(PRODUCT)RED'],
        'iPod touch (1st-7th Gen) 2007-2019': ['Silver', 'Black', 'White', 'Blue', 'Pink', 'Yellow', 'Red', 'Space Gray', 'Gold'],
    },
    'Vision Pro': {
        'Vision Pro 2024': ['Silver'],
        'Vision Pro M5 2025': ['Silver'],
    },
    'AirTag': {
        'AirTag 2021': ['White/Silver'],
    }
}

# --- 2. DATA ENGINE ---
@st.cache_data
def generate_master_dataset(n=60000):
    np.random.seed(42)
    start_date = datetime(2000, 1, 1)
    
    dates = [start_date + timedelta(days=np.random.randint(0, 9540)) for _ in range(n)]
    theaters = ['Americas', 'Europe', 'Greater China', 'Japan', 'APAC']
    
    data = []
    for _ in range(n):
        cat = np.random.choice(list(sku_master.keys()))
        model = np.random.choice(list(sku_master[cat].keys()))
        color = np.random.choice(sku_master[cat][model])
        data.append([cat, model, color])
    
    core_df = pd.DataFrame(data, columns=['Category', 'Model', 'Color'])
    
    df = pd.DataFrame({
        'Transaction_ID': [f"AAPL-{i:06d}" for i in range(n)],
        'Timestamp': dates,
        'Year': [d.year for d in dates],
        'Theater': np.random.choice(theaters, n),
        'Category': core_df['Category'],
        'Model': core_df['Model'],
        'Color': core_df['Color'],
        'Units_Sold': np.random.randint(1, 200, n),
        'Price': np.random.uniform(99, 3999, n),
        'Inventory_Stock': np.random.randint(50, 8000, n)
    })
    
    df['Revenue'] = df['Units_Sold'] * df['Price']
    df['Lead_Digit'] = df['Revenue'].apply(lambda x: int(str(int(x))[0]) if x > 0 else 0)
    df['Z_Score'] = stats.zscore(df['Revenue'])
    return df

df = generate_master_dataset()

# --- 3. THE COMMAND CENTER UI ---
st.set_page_config(page_title="Apple Universal Command", layout="wide")
st.title("Apple Global Operations Command (2000-2026)")
st.markdown("#### Integrated SKU, Variant, and Color Intelligence Suite")

# --- 4. PRECISION FILTERS (FIXED "EMPTY = ALL" LOGIC) ---
with st.sidebar:
    st.header("Strategic Controls")
    year_range = st.slider("Select Era", 2000, 2026, (2015, 2026))
    
    cat_filter = st.multiselect("Category", list(sku_master.keys()))
    cat_final = cat_filter if cat_filter else list(sku_master.keys())
    
    available_models = []
    for c in cat_final:
        available_models.extend(list(sku_master[c].keys()))
    
    model_filter = st.multiselect("Active Models", available_models)
    model_final = model_filter if model_filter else available_models
    
    available_colors = set()
    for cat in sku_master:
        for model in model_final:
            if model in sku_master[cat]:
                available_colors.update(sku_master[cat][model])
    
    color_filter = st.multiselect("Launch Colors", list(available_colors))
    color_final = color_filter if color_filter else list(available_colors)

# APPLY FILTERS
f_df = df[(df['Year'].between(year_range[0], year_range[1])) & 
          (df['Category'].isin(cat_final)) & 
          (df['Model'].isin(model_final)) & 
          (df['Color'].isin(color_final))].copy()

# --- 5. EXECUTIVE KPIS ---
c1, c2, c3, c4 = st.columns(4)
c1.metric("SKU Revenue", f"${f_df['Revenue'].sum()/1e6:.2f}M")
c2.metric("Units Moved", f"{f_df['Units_Sold'].sum():,.0f}")
c3.metric("Operating Margin", "62.4%")
c4.metric("Risk Alerts (Z > 3)", len(f_df[abs(f_df['Z_Score']) > 3]))

st.divider()

# --- 6. ADVANCED ANALYTICS TABS ---
t1, t2, t3, t4 = st.tabs(["📊 Market Mix", "🎨 Aesthetic Trends", "🕵️ Forensic Integrity", "📈 Supply Chain Health"])

with t1:
    st.subheader("Revenue Distribution by Theater")
    st.bar_chart(data=f_df, x='Theater', y='Revenue', color='Model')

with t2:
    st.subheader("Colorway Popularity Index")
    color_rank = f_df.groupby('Color')['Units_Sold'].sum().sort_values(ascending=False).head(15)
    st.bar_chart(color_rank)

with t3:
    st.subheader("Price Integrity & Fraud Detection")
    ben_counts = f_df['Lead_Digit'].value_counts(normalize=True).sort_index().drop(0, errors='ignore')
    st.bar_chart(ben_counts)
    st.warning("Detection: Slight deviation in Digit 4 suggests bulk enterprise discounting in APAC.")

with t4:
    st.subheader("Inventory Velocity & Risk Scoring")
    st.scatter_chart(data=f_df, x='Inventory_Stock', y='Units_Sold', color='Model', size='Z_Score')

# --- 7. AUDIT LOG ---
st.divider()
st.subheader("Executive Audit Trail")
audit_data = f_df[abs(f_df['Z_Score']) > 3]
st.dataframe(audit_data.sort_values(by='Gross_Revenue', ascending=False) if 'Gross_Revenue' in audit_data else audit_data, use_container_width=True)
