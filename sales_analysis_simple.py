"""
Sales Data Analysis - Simple Version
Complete analysis with visualizations
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Set random seed for reproducibility
np.random.seed(42)

print("=" * 60)
print("SALES DATA ANALYSIS SYSTEM")
print("=" * 60)

# Generate sample sales data
print("\n📊 Generating sales data...")
start_date = datetime(2024, 1, 1)
dates = [start_date + timedelta(days=x) for x in range(365)]

data = {
    'Date': dates,
    'Product': np.random.choice(['Laptop', 'Phone', 'Tablet', 'Headphones', 'Smartwatch'], 365),
    'Quantity': np.random.randint(1, 15, 365),
    'Price': np.random.choice([50000, 80000, 30000, 5000, 15000], 365),
    'Region': np.random.choice(['North', 'South', 'East', 'West'], 365),
    'Customer_Type': np.random.choice(['New', 'Returning'], 365, p=[0.3, 0.7]),
    'Payment_Method': np.random.choice(['Cash', 'Card', 'Online'], 365)
}

df = pd.DataFrame(data)
df['Total_Sales'] = df['Quantity'] * df['Price']
df['Month'] = df['Date'].dt.month
df['Month_Name'] = df['Date'].dt.strftime('%B')
df['Quarter'] = df['Date'].dt.quarter

print(f"✓ Generated {len(df)} sales records")

# Save raw data
df.to_csv('sales_data.csv', index=False)
print("✓ Data saved to 'sales_data.csv'")

# Analysis 1: Overall Statistics
print("\n" + "=" * 60)
print("1. OVERALL SALES STATISTICS")
print("=" * 60)
print(f"Total Revenue: ₹{df['Total_Sales'].sum():,.2f}")
print(f"Total Orders: {len(df):,}")
print(f"Average Order Value: ₹{df['Total_Sales'].mean():,.2f}")
print(f"Total Units Sold: {df['Quantity'].sum():,}")

# Analysis 2: Product Performance
print("\n" + "=" * 60)
print("2. PRODUCT PERFORMANCE")
print("=" * 60)
product_sales = df.groupby('Product').agg({
    'Total_Sales': 'sum',
    'Quantity': 'sum'
}).sort_values('Total_Sales', ascending=False)
print(product_sales)

# Analysis 3: Regional Performance
print("\n" + "=" * 60)
print("3. REGIONAL PERFORMANCE")
print("=" * 60)
region_sales = df.groupby('Region').agg({
    'Total_Sales': 'sum',
    'Quantity': 'sum'
}).sort_values('Total_Sales', ascending=False)
print(region_sales)

# Analysis 4: Monthly Trends
print("\n" + "=" * 60)
print("4. MONTHLY SALES TREND")
print("=" * 60)
monthly_sales = df.groupby('Month_Name')['Total_Sales'].sum().reindex([
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
])
print(monthly_sales)

# Analysis 5: Customer Type Analysis
print("\n" + "=" * 60)
print("5. CUSTOMER TYPE ANALYSIS")
print("=" * 60)
customer_analysis = df.groupby('Customer_Type').agg({
    'Total_Sales': ['sum', 'mean', 'count']
})
print(customer_analysis)

# Analysis 6: Payment Method Distribution
print("\n" + "=" * 60)
print("6. PAYMENT METHOD DISTRIBUTION")
print("=" * 60)
payment_dist = df.groupby('Payment_Method')['Total_Sales'].sum().sort_values(ascending=False)
print(payment_dist)

# Create visualizations
print("\n📈 Creating visualizations...")

fig, axes = plt.subplots(2, 3, figsize=(18, 10))
fig.suptitle('Sales Data Analysis Dashboard', fontsize=16, fontweight='bold')

# Plot 1: Product Sales
product_sales['Total_Sales'].plot(kind='bar', ax=axes[0, 0], color='skyblue')
axes[0, 0].set_title('Revenue by Product')
axes[0, 0].set_ylabel('Revenue (₹)')
axes[0, 0].tick_params(axis='x', rotation=45)

# Plot 2: Regional Sales
region_sales['Total_Sales'].plot(kind='pie', ax=axes[0, 1], autopct='%1.1f%%')
axes[0, 1].set_title('Revenue by Region')
axes[0, 1].set_ylabel('')

# Plot 3: Monthly Trend
monthly_sales.plot(kind='line', ax=axes[0, 2], marker='o', color='green', linewidth=2)
axes[0, 2].set_title('Monthly Sales Trend')
axes[0, 2].set_ylabel('Revenue (₹)')
axes[0, 2].tick_params(axis='x', rotation=45)
axes[0, 2].grid(True, alpha=0.3)

# Plot 4: Customer Type
customer_sales = df.groupby('Customer_Type')['Total_Sales'].sum()
customer_sales.plot(kind='bar', ax=axes[1, 0], color=['coral', 'lightgreen'])
axes[1, 0].set_title('Revenue by Customer Type')
axes[1, 0].set_ylabel('Revenue (₹)')
axes[1, 0].tick_params(axis='x', rotation=0)

# Plot 5: Payment Method
payment_dist.plot(kind='bar', ax=axes[1, 1], color='orange')
axes[1, 1].set_title('Revenue by Payment Method')
axes[1, 1].set_ylabel('Revenue (₹)')
axes[1, 1].tick_params(axis='x', rotation=45)

# Plot 6: Quarterly Performance
quarterly_sales = df.groupby('Quarter')['Total_Sales'].sum()
quarterly_sales.plot(kind='bar', ax=axes[1, 2], color='purple')
axes[1, 2].set_title('Quarterly Revenue')
axes[1, 2].set_ylabel('Revenue (₹)')
axes[1, 2].set_xlabel('Quarter')

plt.tight_layout()
plt.savefig('sales_analysis_dashboard.png', dpi=300, bbox_inches='tight')
print("✓ Dashboard saved as 'sales_analysis_dashboard.png'")

# Generate detailed report
print("\n📄 Generating detailed report...")
report = f"""
{'=' * 60}
SALES ANALYSIS REPORT
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
{'=' * 60}

EXECUTIVE SUMMARY
-----------------
Total Revenue: ₹{df['Total_Sales'].sum():,.2f}
Total Orders: {len(df):,}
Average Order Value: ₹{df['Total_Sales'].mean():,.2f}
Total Units Sold: {df['Quantity'].sum():,}

TOP PERFORMING PRODUCT
----------------------
{product_sales.index[0]}: ₹{product_sales['Total_Sales'].iloc[0]:,.2f}

BEST PERFORMING REGION
----------------------
{region_sales.index[0]}: ₹{region_sales['Total_Sales'].iloc[0]:,.2f}

HIGHEST SALES MONTH
-------------------
{monthly_sales.idxmax()}: ₹{monthly_sales.max():,.2f}

RECOMMENDATIONS
---------------
1. Focus marketing efforts on {product_sales.index[0]} (top product)
2. Expand operations in {region_sales.index[0]} region
3. Replicate {monthly_sales.idxmax()} success strategies
4. Increase inventory for high-demand products
5. Develop retention programs for returning customers

{'=' * 60}
"""

with open('sales_report.txt', 'w') as f:
    f.write(report)

print("✓ Report saved as 'sales_report.txt'")

print("\n" + "=" * 60)
print("✅ ANALYSIS COMPLETE!")
print("=" * 60)
print("\nGenerated Files:")
print("1. sales_data.csv - Raw sales data")
print("2. sales_analysis_dashboard.png - Visual dashboard")
print("3. sales_report.txt - Detailed report")
print("\n" + "=" * 60)
