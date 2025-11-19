# 5 Pandas Projects - Complete Guide

## Project 1: Sales Data Analysis
**Description:** Analyze sales data to find trends, top products, and revenue insights.

### Implementation:
```python
import pandas as pd
import numpy as np

# Create sample sales data
data = {
    'Date': pd.date_range('2024-01-01', periods=100),
    'Product': np.random.choice(['Laptop', 'Phone', 'Tablet', 'Headphones'], 100),
    'Quantity': np.random.randint(1, 10, 100),
    'Price': np.random.choice([500, 800, 300, 100], 100),
    'Region': np.random.choice(['North', 'South', 'East', 'West'], 100)
}

df = pd.DataFrame(data)
df['Total_Sales'] = df['Quantity'] * df['Price']

# Analysis
print("=== Sales Analysis ===")
print("\n1. Total Revenue:")
print(f"${df['Total_Sales'].sum():,.2f}")

print("\n2. Top 5 Products by Revenue:")
print(df.groupby('Product')['Total_Sales'].sum().sort_values(ascending=False))

print("\n3. Monthly Sales Trend:")
df['Month'] = df['Date'].dt.month
monthly_sales = df.groupby('Month')['Total_Sales'].sum()
print(monthly_sales)

print("\n4. Region-wise Performance:")
print(df.groupby('Region')['Total_Sales'].sum().sort_values(ascending=False))

# Save results
df.to_csv('sales_analysis.csv', index=False)
print("\n✓ Data saved to sales_analysis.csv")
```

---

## Project 2: Student Performance Tracker
**Description:** Track and analyze student grades, calculate averages, and identify top performers.

### Implementation:
```python
import pandas as pd
import numpy as np

# Create student data
students_data = {
    'Student_ID': range(1, 51),
    'Name': [f'Student_{i}' for i in range(1, 51)],
    'Math': np.random.randint(50, 100, 50),
    'Science': np.random.randint(50, 100, 50),
    'English': np.random.randint(50, 100, 50),
    'History': np.random.randint(50, 100, 50),
    'Class': np.random.choice(['A', 'B', 'C'], 50)
}

df = pd.DataFrame(students_data)

# Calculate metrics
df['Total'] = df[['Math', 'Science', 'English', 'History']].sum(axis=1)
df['Average'] = df['Total'] / 4
df['Grade'] = pd.cut(df['Average'], 
                      bins=[0, 60, 70, 80, 90, 100],
                      labels=['F', 'D', 'C', 'B', 'A'])

print("=== Student Performance Analysis ===")
print("\n1. Top 10 Students:")
print(df.nlargest(10, 'Average')[['Name', 'Average', 'Grade']])

print("\n2. Subject-wise Average:")
subjects = ['Math', 'Science', 'English', 'History']
for subject in subjects:
    print(f"{subject}: {df[subject].mean():.2f}")

print("\n3. Grade Distribution:")
print(df['Grade'].value_counts().sort_index())

print("\n4. Class-wise Performance:")
print(df.groupby('Class')['Average'].mean().sort_values(ascending=False))

# Save results
df.to_csv('student_performance.csv', index=False)
print("\n✓ Data saved to student_performance.csv")
```

---

## Project 3: Weather Data Analysis
**Description:** Analyze weather patterns, temperature trends, and seasonal variations.

### Implementation:
```python
import pandas as pd
import numpy as np

# Create weather data
dates = pd.date_range('2023-01-01', '2024-12-31', freq='D')
weather_data = {
    'Date': dates,
    'Temperature': np.random.randint(15, 35, len(dates)) + np.random.randn(len(dates)) * 3,
    'Humidity': np.random.randint(40, 90, len(dates)),
    'Rainfall': np.random.choice([0, 0, 0, 5, 10, 20, 30], len(dates)),
    'Wind_Speed': np.random.randint(5, 25, len(dates))
}

df = pd.DataFrame(weather_data)
df['Month'] = df['Date'].dt.month
df['Season'] = df['Month'].map({
    12: 'Winter', 1: 'Winter', 2: 'Winter',
    3: 'Spring', 4: 'Spring', 5: 'Spring',
    6: 'Summer', 7: 'Summer', 8: 'Summer',
    9: 'Fall', 10: 'Fall', 11: 'Fall'
})

print("=== Weather Analysis ===")
print("\n1. Temperature Statistics:")
print(df['Temperature'].describe())

print("\n2. Hottest and Coldest Days:")
print(f"Hottest: {df.loc[df['Temperature'].idxmax(), 'Date'].date()} - {df['Temperature'].max():.1f}°C")
print(f"Coldest: {df.loc[df['Temperature'].idxmin(), 'Date'].date()} - {df['Temperature'].min():.1f}°C")

print("\n3. Season-wise Average Temperature:")
print(df.groupby('Season')['Temperature'].mean().round(2))

print("\n4. Total Rainfall by Month:")
monthly_rain = df.groupby('Month')['Rainfall'].sum()
print(monthly_rain)

print("\n5. Days with Rainfall:")
rainy_days = len(df[df['Rainfall'] > 0])
print(f"Total rainy days: {rainy_days} ({rainy_days/len(df)*100:.1f}%)")

# Save results
df.to_csv('weather_analysis.csv', index=False)
print("\n✓ Data saved to weather_analysis.csv")
```

---

## Project 4: E-commerce Customer Analysis
**Description:** Analyze customer behavior, purchase patterns, and customer segmentation.

### Implementation:
```python
import pandas as pd
import numpy as np

# Create customer data
np.random.seed(42)
customer_data = {
    'Customer_ID': range(1, 201),
    'Age': np.random.randint(18, 70, 200),
    'Gender': np.random.choice(['Male', 'Female'], 200),
    'Total_Purchases': np.random.randint(1, 50, 200),
    'Total_Spent': np.random.randint(100, 5000, 200),
    'Membership': np.random.choice(['Bronze', 'Silver', 'Gold', 'Platinum'], 200),
    'Last_Purchase_Days': np.random.randint(1, 365, 200)
}

df = pd.DataFrame(customer_data)
df['Avg_Order_Value'] = df['Total_Spent'] / df['Total_Purchases']

# Customer Segmentation
df['Customer_Type'] = pd.cut(df['Total_Spent'], 
                              bins=[0, 1000, 2500, 5000],
                              labels=['Low Value', 'Medium Value', 'High Value'])

print("=== E-commerce Customer Analysis ===")
print("\n1. Customer Demographics:")
print(f"Total Customers: {len(df)}")
print(f"Average Age: {df['Age'].mean():.1f}")
print(f"Gender Distribution:\n{df['Gender'].value_counts()}")

print("\n2. Purchase Behavior:")
print(f"Total Revenue: ${df['Total_Spent'].sum():,.2f}")
print(f"Average Order Value: ${df['Avg_Order_Value'].mean():.2f}")
print(f"Average Purchases per Customer: {df['Total_Purchases'].mean():.1f}")

print("\n3. Customer Segmentation:")
print(df['Customer_Type'].value_counts())

print("\n4. Membership Analysis:")
membership_stats = df.groupby('Membership').agg({
    'Total_Spent': 'mean',
    'Total_Purchases': 'mean'
}).round(2)
print(membership_stats)

print("\n5. Top 10 Customers:")
print(df.nlargest(10, 'Total_Spent')[['Customer_ID', 'Total_Spent', 'Total_Purchases', 'Membership']])

# Churn Risk (customers who haven't purchased in 180+ days)
df['Churn_Risk'] = df['Last_Purchase_Days'] > 180
print(f"\n6. Churn Risk: {df['Churn_Risk'].sum()} customers at risk")

# Save results
df.to_csv('customer_analysis.csv', index=False)
print("\n✓ Data saved to customer_analysis.csv")
```

---

## Project 5: Employee HR Analytics
**Description:** Analyze employee data, salary trends, department performance, and attrition.

### Implementation:
```python
import pandas as pd
import numpy as np

# Create employee data
np.random.seed(100)
departments = ['IT', 'Sales', 'HR', 'Finance', 'Marketing']
employee_data = {
    'Employee_ID': range(1001, 1301),
    'Name': [f'Employee_{i}' for i in range(1, 301)],
    'Department': np.random.choice(departments, 300),
    'Age': np.random.randint(22, 60, 300),
    'Salary': np.random.randint(30000, 120000, 300),
    'Years_Experience': np.random.randint(0, 20, 300),
    'Performance_Score': np.random.randint(1, 6, 300),
    'Attrition': np.random.choice(['Yes', 'No'], 300, p=[0.15, 0.85])
}

df = pd.DataFrame(employee_data)

print("=== HR Analytics Dashboard ===")
print("\n1. Workforce Overview:")
print(f"Total Employees: {len(df)}")
print(f"Average Age: {df['Age'].mean():.1f} years")
print(f"Average Experience: {df['Years_Experience'].mean():.1f} years")

print("\n2. Department Distribution:")
print(df['Department'].value_counts())

print("\n3. Salary Analysis:")
print(f"Average Salary: ${df['Salary'].mean():,.2f}")
print(f"Median Salary: ${df['Salary'].median():,.2f}")
print("\nDepartment-wise Average Salary:")
print(df.groupby('Department')['Salary'].mean().sort_values(ascending=False).round(2))

print("\n4. Performance Analysis:")
print("Performance Score Distribution:")
print(df['Performance_Score'].value_counts().sort_index())
print(f"\nAverage Performance Score: {df['Performance_Score'].mean():.2f}")

print("\n5. Attrition Analysis:")
attrition_rate = (df['Attrition'] == 'Yes').sum() / len(df) * 100
print(f"Overall Attrition Rate: {attrition_rate:.1f}%")
print("\nDepartment-wise Attrition:")
dept_attrition = df.groupby('Department')['Attrition'].apply(
    lambda x: (x == 'Yes').sum() / len(x) * 100
).sort_values(ascending=False)
print(dept_attrition.round(2))

print("\n6. Salary vs Experience Correlation:")
correlation = df['Salary'].corr(df['Years_Experience'])
print(f"Correlation: {correlation:.2f}")

print("\n7. High Performers (Score >= 4):")
high_performers = df[df['Performance_Score'] >= 4]
print(f"Count: {len(high_performers)} ({len(high_performers)/len(df)*100:.1f}%)")

# Save results
df.to_csv('hr_analytics.csv', index=False)
print("\n✓ Data saved to hr_analytics.csv")
```

---

## How to Run These Projects

### Prerequisites:
```bash
pip install pandas numpy
```

### Running Each Project:
1. Copy the code for any project
2. Save it as a Python file (e.g., `sales_analysis.py`)
3. Run: `python sales_analysis.py`
4. Check the generated CSV files for detailed results

### Key Pandas Concepts Covered:
- DataFrame creation and manipulation
- Data aggregation with `groupby()`
- Statistical analysis with `describe()`, `mean()`, `sum()`
- Data filtering and sorting
- Date/time operations
- Data categorization with `cut()` and `map()`
- CSV file operations
- Correlation analysis
- Data visualization preparation

---

## Next Steps:
- Add data visualization using matplotlib or seaborn
- Connect to real databases using SQL
- Create interactive dashboards with Plotly
- Implement machine learning models on the analyzed data
- Export results to Excel with formatting

**Happy Learning! 🐼📊**
