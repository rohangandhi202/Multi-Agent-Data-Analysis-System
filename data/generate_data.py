"""
Fake Data Generator
Creates realistic messy datasets for testing the multi-agent analysis system
"""

import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import os


class DataGenerator:
    """Generates fake datasets with realistic messiness"""
    
    def __init__(self, seed=42):
        """Initialize with random seed for reproducibility"""
        random.seed(seed)
        np.random.seed(seed)
    
    def generate_sales_data(self, n_rows=200, messiness='medium'):
        """
        Generate fake sales data with intentional issues
        
        Args:
            n_rows: Number of rows to generate
            messiness: 'low', 'medium', or 'high' - controls how messy the data is
            
        Returns:
            pd.DataFrame: Messy sales dataset
        """
        print(f"📊 Generating sales dataset with {messiness} messiness...")
        
        # Set messiness parameters
        mess_params = {
            'low': {'missing': 0.02, 'duplicates': 0.01, 'outliers': 0.01},
            'medium': {'missing': 0.10, 'duplicates': 0.05, 'outliers': 0.03},
            'high': {'missing': 0.20, 'duplicates': 0.10, 'outliers': 0.05}
        }
        params = mess_params[messiness]
        
        # Generate clean data first
        data = {
            'order_id': range(1, n_rows + 1),
            'customer_name': [self._random_name() for _ in range(n_rows)],
            'product': [random.choice(['Laptop', 'Phone', 'Tablet', 'Monitor', 'Keyboard', 'Mouse']) 
                       for _ in range(n_rows)],
            'quantity': np.random.randint(1, 10, n_rows),
            'unit_price': np.random.uniform(50, 1500, n_rows).round(2),
            'region': [random.choice(['North', 'South', 'East', 'West']) for _ in range(n_rows)],
            'order_date': [self._random_date() for _ in range(n_rows)],
            'shipping_cost': np.random.uniform(5, 50, n_rows).round(2),
            'discount_percent': np.random.uniform(0, 25, n_rows).round(1)
        }
        
        df = pd.DataFrame(data)
        
        # Add calculated column
        df['total_revenue'] = (df['quantity'] * df['unit_price'] * 
                               (1 - df['discount_percent']/100)).round(2)
        
        # Introduce messiness
        df = self._add_missing_values(df, params['missing'])
        df = self._add_duplicates(df, params['duplicates'])
        df = self._add_outliers(df, params['outliers'])
        
        return df
    
    def generate_employee_data(self, n_rows=150, messiness='medium'):
        """Generate fake employee/HR data"""
        print(f"📊 Generating employee dataset with {messiness} messiness...")
        
        mess_params = {
            'low': {'missing': 0.02, 'duplicates': 0.01, 'outliers': 0.01},
            'medium': {'missing': 0.10, 'duplicates': 0.05, 'outliers': 0.03},
            'high': {'missing': 0.20, 'duplicates': 0.10, 'outliers': 0.05}
        }
        params = mess_params[messiness]
        
        data = {
            'employee_id': range(1, n_rows + 1),
            'name': [self._random_name() for _ in range(n_rows)],
            'department': [random.choice(['Sales', 'Engineering', 'Marketing', 'HR', 'Finance', 'Operations']) 
                          for _ in range(n_rows)],
            'position': [random.choice(['Manager', 'Senior', 'Junior', 'Lead', 'Associate']) 
                        for _ in range(n_rows)],
            'age': np.random.randint(22, 65, n_rows),
            'years_experience': np.random.randint(0, 25, n_rows),
            'salary': np.random.uniform(40000, 150000, n_rows).round(2),
            'performance_score': np.random.randint(60, 100, n_rows),
            'hours_worked_per_week': np.random.uniform(35, 50, n_rows).round(1),
            'projects_completed': np.random.randint(0, 20, n_rows)
        }
        
        df = pd.DataFrame(data)
        
        # Introduce messiness
        df = self._add_missing_values(df, params['missing'])
        df = self._add_duplicates(df, params['duplicates'])
        df = self._add_outliers(df, params['outliers'])
        
        return df
    
    def generate_customer_data(self, n_rows=300, messiness='medium'):
        """Generate fake customer/marketing data"""
        print(f"📊 Generating customer dataset with {messiness} messiness...")
        
        mess_params = {
            'low': {'missing': 0.02, 'duplicates': 0.01, 'outliers': 0.01},
            'medium': {'missing': 0.10, 'duplicates': 0.05, 'outliers': 0.03},
            'high': {'missing': 0.20, 'duplicates': 0.10, 'outliers': 0.05}
        }
        params = mess_params[messiness]
        
        data = {
            'customer_id': range(1, n_rows + 1),
            'name': [self._random_name() for _ in range(n_rows)],
            'email': [self._random_email() for _ in range(n_rows)],
            'age': np.random.randint(18, 80, n_rows),
            'country': [random.choice(['USA', 'UK', 'Canada', 'Germany', 'France', 'Australia']) 
                       for _ in range(n_rows)],
            'customer_since': [self._random_date(start_year=2018) for _ in range(n_rows)],
            'total_purchases': np.random.randint(1, 50, n_rows),
            'total_spent': np.random.uniform(100, 10000, n_rows).round(2),
            'avg_order_value': np.random.uniform(50, 500, n_rows).round(2),
            'email_opens': np.random.randint(0, 100, n_rows),
            'website_visits': np.random.randint(5, 200, n_rows),
            'subscription_tier': [random.choice(['Free', 'Basic', 'Premium', 'Enterprise']) 
                                 for _ in range(n_rows)]
        }
        
        df = pd.DataFrame(data)
        
        # Introduce messiness
        df = self._add_missing_values(df, params['missing'])
        df = self._add_duplicates(df, params['duplicates'])
        df = self._add_outliers(df, params['outliers'])
        
        return df
    
    def _random_name(self):
        """Generate a random name"""
        first_names = ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve', 'Frank', 'Grace', 'Henry',
                      'Ivy', 'Jack', 'Kelly', 'Liam', 'Mia', 'Noah', 'Olivia', 'Peter',
                      'Quinn', 'Rachel', 'Sam', 'Tina', 'Uma', 'Victor', 'Wendy', 'Xavier',
                      'Yara', 'Zack']
        last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller',
                     'Davis', 'Rodriguez', 'Martinez', 'Hernandez', 'Lopez', 'Gonzalez',
                     'Wilson', 'Anderson', 'Thomas', 'Taylor', 'Moore', 'Jackson', 'Martin']
        return f"{random.choice(first_names)} {random.choice(last_names)}"
    
    def _random_email(self):
        """Generate a random email"""
        name = self._random_name().lower().replace(' ', '.')
        domains = ['gmail.com', 'yahoo.com', 'outlook.com', 'company.com']
        return f"{name}@{random.choice(domains)}"
    
    def _random_date(self, start_year=2020):
        """Generate a random date"""
        start = datetime(start_year, 1, 1)
        end = datetime.now()
        delta = end - start
        random_days = random.randint(0, delta.days)
        return (start + timedelta(days=random_days)).strftime('%Y-%m-%d')
    
    def _add_missing_values(self, df, percentage):
        """Randomly introduce missing values"""
        df_copy = df.copy()
        n_missing = int(len(df) * df.shape[1] * percentage)
        
        for _ in range(n_missing):
            row = random.randint(0, len(df) - 1)
            col = random.choice(df.columns[1:])  # Skip ID column
            df_copy.at[row, col] = None
        
        return df_copy
    
    def _add_duplicates(self, df, percentage):
        """Add duplicate rows"""
        n_duplicates = int(len(df) * percentage)
        if n_duplicates == 0:
            return df
        
        duplicate_indices = random.sample(range(len(df)), n_duplicates)
        duplicates = df.iloc[duplicate_indices].copy()
        
        return pd.concat([df, duplicates], ignore_index=True)
    
    def _add_outliers(self, df, percentage):
        """Add outliers to numeric columns"""
        df_copy = df.copy()
        numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
        
        n_outliers = int(len(df) * percentage)
        
        for _ in range(n_outliers):
            row = random.randint(0, len(df) - 1)
            col = random.choice(numeric_cols)
            
            # Make it an extreme outlier
            current_value = df_copy.at[row, col]
            if pd.notna(current_value):
                if random.random() > 0.5:
                    df_copy.at[row, col] = current_value * random.uniform(10, 100)
                else:
                    df_copy.at[row, col] = current_value * random.uniform(0.01, 0.1)
        
        return df_copy


def main():
    """Generate sample datasets"""
    print("=" * 60)
    print("Fake Data Generator for Multi-Agent Analysis")
    print("=" * 60)
    print()
    
    # Create data directory if it doesn't exist
    os.makedirs('data', exist_ok=True)
    
    generator = DataGenerator()
    
    # Generate different datasets
    datasets = {
        'sales_data.csv': lambda: generator.generate_sales_data(n_rows=200, messiness='medium'),
        'employee_data.csv': lambda: generator.generate_employee_data(n_rows=150, messiness='medium'),
        'customer_data.csv': lambda: generator.generate_customer_data(n_rows=300, messiness='medium'),
        'messy_sales.csv': lambda: generator.generate_sales_data(n_rows=250, messiness='high'),
    }
    
    print("Available datasets to generate:")
    print("1. sales_data.csv - E-commerce sales data (200 rows, medium mess)")
    print("2. employee_data.csv - HR/Employee data (150 rows, medium mess)")
    print("3. customer_data.csv - Customer/Marketing data (300 rows, medium mess)")
    print("4. messy_sales.csv - Very messy sales data (250 rows, high mess)")
    print("5. ALL - Generate all datasets")
    print()
    
    choice = input("Enter your choice (1-5): ").strip()
    
    if choice == '5':
        # Generate all
        for filename, generator_func in datasets.items():
            df = generator_func()
            filepath = f"data/{filename}"
            df.to_csv(filepath, index=False)
            print(f"✅ Saved: {filepath} ({len(df)} rows × {df.shape[1]} columns)")
        print(f"\n🎉 All datasets generated in 'data/' folder!")
    elif choice in ['1', '2', '3', '4']:
        # Generate selected dataset
        filenames = list(datasets.keys())
        selected = filenames[int(choice) - 1]
        df = datasets[selected]()
        filepath = f"data/{selected}"
        df.to_csv(filepath, index=False)
        print(f"\n✅ Saved: {filepath} ({len(df)} rows × {df.shape[1]} columns)")
        print("\nPreview:")
        print(df.head())
    else:
        print("Invalid choice!")
        return
    
    print("\n" + "=" * 60)
    print("💡 NEXT STEPS:")
    print("=" * 60)
    print("Run analysis on your generated data:")
    if choice == '5':
        print("  python main.py data/sales_data.csv")
        print("  python main.py data/employee_data.csv")
        print("  python main.py data/customer_data.csv")
    else:
        print(f"  python main.py {filepath}")
    print("\nOr use the orchestrator directly:")
    print("  python orchestrator.py")
    print("=" * 60)


if __name__ == "__main__":
    main()