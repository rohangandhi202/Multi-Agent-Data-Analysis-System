"""
Data Cleaning Agent
Analyzes datasets and performs cleaning operations
"""

import os
import pandas as pd
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()


class DataCleaningAgent:
    """Agent responsible for analyzing and cleaning datasets"""
    
    def __init__(self):
        """Initialize the cleaning agent with Claude API"""
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.model = "claude-sonnet-4-20250514"
    
    def analyze_dataset(self, df: pd.DataFrame) -> dict:
        """
        Analyze the dataset and identify issues
        
        Args:
            df: Pandas DataFrame to analyze
            
        Returns:
            dict: Analysis results with identified issues
        """
        # Generate dataset summary
        summary = self._generate_summary(df)
        
        # Ask Claude to analyze
        prompt = f"""You are a data cleaning expert. Analyze this dataset and identify all data quality issues.

Dataset Summary:
{summary}

Identify:
1. Missing values (which columns, how many, percentage)
2. Duplicate rows
3. Potential outliers (based on statistics)
4. Data type issues
5. Any other quality concerns

Respond in this exact format:
ISSUES FOUND:
- [List each issue clearly]

RECOMMENDED ACTIONS:
- [List specific cleaning steps]"""

        message = self.client.messages.create(
            model=self.model,
            max_tokens=1500,
            messages=[{"role": "user", "content": prompt}]
        )
        
        analysis = message.content[0].text
        
        return {
            "analysis": analysis,
            "summary": summary,
            "shape": df.shape,
            "columns": df.columns.tolist()
        }
    
    def clean_dataset(self, df: pd.DataFrame, analysis: dict) -> pd.DataFrame:
        """
        Clean the dataset based on the analysis
        
        Args:
            df: Original DataFrame
            analysis: Analysis results from analyze_dataset
            
        Returns:
            pd.DataFrame: Cleaned dataset
        """
        df_clean = df.copy()
        cleaning_log = []
        
        # 1. Remove duplicates
        initial_rows = len(df_clean)
        df_clean = df_clean.drop_duplicates()
        duplicates_removed = initial_rows - len(df_clean)
        if duplicates_removed > 0:
            cleaning_log.append(f"✓ Removed {duplicates_removed} duplicate rows")
        
        # 2. Handle missing values
        for column in df_clean.columns:
            missing_count = df_clean[column].isnull().sum()
            if missing_count > 0:
                # For numeric columns, fill with median
                if df_clean[column].dtype in ['int64', 'float64']:
                    df_clean[column].fillna(df_clean[column].median(), inplace=True)
                    cleaning_log.append(f"✓ Filled {missing_count} missing values in '{column}' with median")
                # For categorical, fill with mode
                else:
                    mode_value = df_clean[column].mode()[0] if not df_clean[column].mode().empty else "Unknown"
                    df_clean[column].fillna(mode_value, inplace=True)
                    cleaning_log.append(f"✓ Filled {missing_count} missing values in '{column}' with mode")
        
        # 3. Remove outliers (using IQR method for numeric columns)
        for column in df_clean.select_dtypes(include=['int64', 'float64']).columns:
            Q1 = df_clean[column].quantile(0.25)
            Q3 = df_clean[column].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            initial_rows = len(df_clean)
            df_clean = df_clean[(df_clean[column] >= lower_bound) & (df_clean[column] <= upper_bound)]
            outliers_removed = initial_rows - len(df_clean)
            
            if outliers_removed > 0:
                cleaning_log.append(f"✓ Removed {outliers_removed} outliers from '{column}'")
        
        return df_clean, cleaning_log
    
    def _generate_summary(self, df: pd.DataFrame) -> str:
        """Generate a text summary of the dataset"""
        summary_parts = []
        
        # Basic info
        summary_parts.append(f"Shape: {df.shape[0]} rows × {df.shape[1]} columns")
        summary_parts.append(f"\nColumns: {', '.join(df.columns.tolist())}")
        
        # Data types
        summary_parts.append(f"\nData Types:\n{df.dtypes.to_string()}")
        
        # Missing values
        missing = df.isnull().sum()
        if missing.sum() > 0:
            summary_parts.append(f"\nMissing Values:\n{missing[missing > 0].to_string()}")
        
        # Duplicates
        duplicates = df.duplicated().sum()
        summary_parts.append(f"\nDuplicate Rows: {duplicates}")
        
        # Basic statistics for numeric columns
        if len(df.select_dtypes(include=['int64', 'float64']).columns) > 0:
            summary_parts.append(f"\nNumeric Statistics:\n{df.describe().to_string()}")
        
        return "\n".join(summary_parts)


def demo_cleaning_agent():
    """Demo the cleaning agent with sample data"""
    print("=" * 60)
    print("Data Cleaning Agent - Demo")
    print("=" * 60)
    
    # Create sample messy data
    data = {
        'name': ['Alice', 'Bob', 'Charlie', 'Bob', 'Eve', None, 'Frank'],
        'age': [25, 30, None, 30, 22, 150, 28],  # Missing value and outlier
        'salary': [50000, 60000, 55000, 60000, None, 58000, 1000000],  # Missing and outlier
        'department': ['Sales', 'Engineering', 'Sales', 'Engineering', 'Marketing', 'Sales', None]
    }
    
    df = pd.DataFrame(data)
    
    print("\n📊 Original Dataset:")
    print(df)
    print(f"\nShape: {df.shape}")
    
    # Initialize agent
    agent = DataCleaningAgent()
    
    # Analyze
    print("\n🔍 Analyzing dataset...")
    analysis = agent.analyze_dataset(df)
    print("\n" + analysis['analysis'])
    
    # Clean
    print("\n🧹 Cleaning dataset...")
    df_clean, cleaning_log = agent.clean_dataset(df, analysis)
    
    print("\nCleaning Actions Performed:")
    for log in cleaning_log:
        print(f"  {log}")
    
    print("\n✨ Cleaned Dataset:")
    print(df_clean)
    print(f"\nNew Shape: {df_clean.shape}")
    
    print("\n✅ Cleaning complete!")


if __name__ == "__main__":
    demo_cleaning_agent()