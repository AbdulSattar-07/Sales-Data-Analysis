"""
Sales Data Analysis - Advanced Streamlit Dashboard
Interactive dashboard with animations and responsive design
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time

# Page configuration
st.set_page_config(
    page_title="Sales Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for animations and styling
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    .metric-card {
        background: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
    }
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 12px rgba(0,0,0,0.2);
    }
    h1 {
        color: #2c3e50;
        text-align: center;
        animation: fadeIn 1s ease-in;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .stMetric {
        background: white;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False

# Function to generate data
@st.cache_data
def generate_sales_data():
    np.random.seed(42)
    start_date = datetime(2024, 1, 1)
    dates = [start_date + timedelta(days=x) for x in range(365)]
    
    data = {
        'Date': dates,
        'Product': np.random.choice(['Laptop', 'Phone', 'Tablet', 'Headphones', 'Smartwatch'], 365),
        'Quantity': np.random.randint(1, 15, 365),
        'Price': np.random.choice([50000, 80000, 30000, 5000, 15000], 365),
        'Region': np.random.choice(['North', 'South', 'East', 'West'], 365),
        'Customer_Type': np.random.choice(['New', 'Returning'], 365, p=[0.3, 0.7]),
        'Payment_Method': np.random.choice(['Cash', 'Card', 'Online'], 365),
        'Salesperson': np.random.choice(['Ali', 'Sara', 'Ahmed', 'Fatima', 'Hassan'], 365)
    }
    
    df = pd.DataFrame(data)
    df['Total_Sales'] = df['Quantity'] * df['Price']
    df['Month'] = df['Date'].dt.month
    df['Month_Name'] = df['Date'].dt.strftime('%B')
    df['Quarter'] = df['Date'].dt.quarter
    df['Day_of_Week'] = df['Date'].dt.day_name()
    
    return df

# Header with animation
st.markdown("<h1>📊 Sales Analytics Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #7f8c8d;'>Real-time Sales Performance Monitoring</p>", unsafe_allow_html=True)

# Loading animation
if not st.session_state.data_loaded:
    with st.spinner('🔄 Loading sales data...'):
        progress_bar = st.progress(0)
        for i in range(100):
            time.sleep(0.01)
            progress_bar.progress(i + 1)
        st.session_state.data_loaded = True
        st.success('✅ Data loaded successfully!')
        time.sleep(1)
        st.rerun()

# Load data
df = generate_sales_data()

# Sidebar filters
st.sidebar.header("🔍 Filters")
st.sidebar.markdown("---")

# Date range filter
date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(df['Date'].min(), df['Date'].max()),
    min_value=df['Date'].min(),
    max_value=df['Date'].max()
)

# Product filter
products = st.sidebar.multiselect(
    "Select Products",
    options=df['Product'].unique(),
    default=df['Product'].unique()
)

# Region filter
regions = st.sidebar.multiselect(
    "Select Regions",
    options=df['Region'].unique(),
    default=df['Region'].unique()
)

# Apply filters
if len(date_range) == 2:
    mask = (df['Date'] >= pd.to_datetime(date_range[0])) & (df['Date'] <= pd.to_datetime(date_range[1]))
    filtered_df = df[mask]
else:
    filtered_df = df.copy()

filtered_df = filtered_df[filtered_df['Product'].isin(products)]
filtered_df = filtered_df[filtered_df['Region'].isin(regions)]

# Key Metrics Row
st.markdown("### 📈 Key Performance Indicators")
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_revenue = filtered_df['Total_Sales'].sum()
    st.metric(
        label="💰 Total Revenue",
        value=f"₹{total_revenue:,.0f}",
        delta=f"{(total_revenue/df['Total_Sales'].sum()*100):.1f}% of total"
    )

with col2:
    total_orders = len(filtered_df)
    st.metric(
        label="🛒 Total Orders",
        value=f"{total_orders:,}",
        delta=f"{total_orders} orders"
    )

with col3:
    avg_order = filtered_df['Total_Sales'].mean()
    st.metric(
        label="📊 Avg Order Value",
        value=f"₹{avg_order:,.0f}",
        delta=f"₹{avg_order:,.0f}"
    )

with col4:
    total_units = filtered_df['Quantity'].sum()
    st.metric(
        label="📦 Units Sold",
        value=f"{total_units:,}",
        delta=f"{total_units} units"
    )

st.markdown("---")

# Row 1: Product Performance and Regional Distribution
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🏆 Product Performance")
    product_sales = filtered_df.groupby('Product')['Total_Sales'].sum().sort_values(ascending=False)
    
    fig1 = px.bar(
        x=product_sales.index,
        y=product_sales.values,
        labels={'x': 'Product', 'y': 'Revenue (₹)'},
        color=product_sales.values,
        color_continuous_scale='Blues'
    )
    fig1.update_layout(
        showlegend=False,
        height=400,
        xaxis_title="Product",
        yaxis_title="Revenue (₹)"
    )
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.markdown("### 🌍 Regional Distribution")
    region_sales = filtered_df.groupby('Region')['Total_Sales'].sum()
    
    fig2 = px.pie(
        values=region_sales.values,
        names=region_sales.index,
        hole=0.4,
        color_discrete_sequence=px.colors.sequential.RdBu
    )
    fig2.update_traces(textposition='inside', textinfo='percent+label')
    fig2.update_layout(height=400)
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# Row 2: Monthly Trend and Customer Analysis
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📅 Monthly Sales Trend")
    monthly_sales = filtered_df.groupby('Month_Name')['Total_Sales'].sum().reindex([
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ])
    
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(
        x=monthly_sales.index,
        y=monthly_sales.values,
        mode='lines+markers',
        line=dict(color='#3498db', width=3),
        marker=dict(size=10, color='#e74c3c'),
        fill='tozeroy',
        fillcolor='rgba(52, 152, 219, 0.2)'
    ))
    fig3.update_layout(
        height=400,
        xaxis_title="Month",
        yaxis_title="Revenue (₹)",
        hovermode='x unified'
    )
    st.plotly_chart(fig3, use_container_width=True)

with col2:
    st.markdown("### 👥 Customer Type Analysis")
    customer_sales = filtered_df.groupby('Customer_Type')['Total_Sales'].sum()
    
    fig4 = px.bar(
        x=customer_sales.index,
        y=customer_sales.values,
        labels={'x': 'Customer Type', 'y': 'Revenue (₹)'},
        color=customer_sales.index,
        color_discrete_map={'New': '#e74c3c', 'Returning': '#2ecc71'}
    )
    fig4.update_layout(
        showlegend=False,
        height=400,
        xaxis_title="Customer Type",
        yaxis_title="Revenue (₹)"
    )
    st.plotly_chart(fig4, use_container_width=True)

st.markdown("---")

# Row 3: Payment Methods and Salesperson Performance
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 💳 Payment Method Distribution")
    payment_dist = filtered_df.groupby('Payment_Method')['Total_Sales'].sum()
    
    fig5 = px.funnel(
        y=payment_dist.index,
        x=payment_dist.values,
        color=payment_dist.index,
        color_discrete_sequence=px.colors.sequential.Viridis
    )
    fig5.update_layout(height=400)
    st.plotly_chart(fig5, use_container_width=True)

with col2:
    st.markdown("### 👤 Top Salesperson Performance")
    salesperson_sales = filtered_df.groupby('Salesperson')['Total_Sales'].sum().sort_values(ascending=True)
    
    fig6 = px.bar(
        x=salesperson_sales.values,
        y=salesperson_sales.index,
        orientation='h',
        labels={'x': 'Revenue (₹)', 'y': 'Salesperson'},
        color=salesperson_sales.values,
        color_continuous_scale='Greens'
    )
    fig6.update_layout(
        showlegend=False,
        height=400,
        xaxis_title="Revenue (₹)",
        yaxis_title="Salesperson"
    )
    st.plotly_chart(fig6, use_container_width=True)

st.markdown("---")

# Detailed Data Table
st.markdown("### 📋 Detailed Sales Data")
st.dataframe(
    filtered_df.sort_values('Date', ascending=False).head(100),
    use_container_width=True,
    height=400
)

# Download button
csv = filtered_df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="📥 Download Filtered Data as CSV",
    data=csv,
    file_name=f'sales_data_{datetime.now().strftime("%Y%m%d")}.csv',
    mime='text/csv',
)

# Footer
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: #95a5a6;'>Sales Analytics Dashboard © 2024 | Built with Streamlit</p>",
    unsafe_allow_html=True
)
