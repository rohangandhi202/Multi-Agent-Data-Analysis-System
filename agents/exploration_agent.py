"""
Data Exploration Agent
Generates statistics, correlations, and visualizations from cleaned data
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()


class DataExplorationAgent:
    """Agent responsible for exploring and visualizing datasets"""
    
    def __init__(self):
        """Initialize the exploration agent with Claude API"""
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.model = "claude-sonnet-4-20250514"
        
        # Set style for visualizations
        sns.set_style("whitegrid")
        plt.rcParams['figure.figsize'] = (10, 6)
    
    def explore_dataset(self, df: pd.DataFrame) -> dict:
        """
        Perform comprehensive exploration of the dataset
        
        Args:
            df: Cleaned DataFrame to explore
            
        Returns:
            dict: Exploration results with statistics and insights
        """
        exploration_results = {}
        
        # 1. Generate descriptive statistics
        exploration_results['statistics'] = self._generate_statistics(df)
        
        # 2. Analyze correlations (for numeric columns)
        exploration_results['correlations'] = self._analyze_correlations(df)
        
        # 3. Ask Claude to interpret the data
        exploration_results['ai_insights'] = self._get_ai_exploration(df, exploration_results)
        
        return exploration_results
    
    def generate_visualizations(self, df: pd.DataFrame, output_dir: str = "output") -> list:
        """
        Generate and save visualizations
        
        Args:
            df: DataFrame to visualize
            output_dir: Directory to save plots
            
        Returns:
            list: Paths to saved visualization files
        """
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        saved_plots = []
        
        # 1. Distribution plots for numeric columns
        numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
        if len(numeric_cols) > 0:
            fig, axes = plt.subplots(len(numeric_cols), 1, figsize=(10, 4 * len(numeric_cols)))
            if len(numeric_cols) == 1:
                axes = [axes]
            
            for idx, col in enumerate(numeric_cols):
                sns.histplot(df[col], kde=True, ax=axes[idx])
                axes[idx].set_title(f'Distribution of {col}')
                axes[idx].set_xlabel(col)
                axes[idx].set_ylabel('Frequency')
            
            plt.tight_layout()
            plot_path = f"{output_dir}/distributions.png"
            plt.savefig(plot_path, dpi=300, bbox_inches='tight')
            plt.close()
            saved_plots.append(plot_path)
            print(f"  ✓ Saved: {plot_path}")
        
        # 2. Correlation heatmap
        if len(numeric_cols) > 1:
            plt.figure(figsize=(10, 8))
            correlation_matrix = df[numeric_cols].corr()
            sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0,
                       square=True, linewidths=1, fmt='.2f')
            plt.title('Correlation Heatmap')
            plt.tight_layout()
            plot_path = f"{output_dir}/correlation_heatmap.png"
            plt.savefig(plot_path, dpi=300, bbox_inches='tight')
            plt.close()
            saved_plots.append(plot_path)
            print(f"  ✓ Saved: {plot_path}")
        
        # 3. Box plots for outlier detection
        if len(numeric_cols) > 0:
            fig, axes = plt.subplots(1, len(numeric_cols), figsize=(5 * len(numeric_cols), 6))
            if len(numeric_cols) == 1:
                axes = [axes]
            
            for idx, col in enumerate(numeric_cols):
                sns.boxplot(y=df[col], ax=axes[idx])
                axes[idx].set_title(f'Box Plot: {col}')
                axes[idx].set_ylabel(col)
            
            plt.tight_layout()
            plot_path = f"{output_dir}/boxplots.png"
            plt.savefig(plot_path, dpi=300, bbox_inches='tight')
            plt.close()
            saved_plots.append(plot_path)
            print(f"  ✓ Saved: {plot_path}")
        
        # 4. Count plots for categorical columns
        categorical_cols = df.select_dtypes(include=['object']).columns
        if len(categorical_cols) > 0:
            fig, axes = plt.subplots(len(categorical_cols), 1, 
                                    figsize=(10, 4 * len(categorical_cols)))
            if len(categorical_cols) == 1:
                axes = [axes]
            
            for idx, col in enumerate(categorical_cols):
                value_counts = df[col].value_counts()
                sns.barplot(x=value_counts.values, y=value_counts.index, ax=axes[idx])
                axes[idx].set_title(f'Count Plot: {col}')
                axes[idx].set_xlabel('Count')
                axes[idx].set_ylabel(col)
            
            plt.tight_layout()
            plot_path = f"{output_dir}/categorical_counts.png"
            plt.savefig(plot_path, dpi=300, bbox_inches='tight')
            plt.close()
            saved_plots.append(plot_path)
            print(f"  ✓ Saved: {plot_path}")
        
        return saved_plots
    
    def _generate_statistics(self, df: pd.DataFrame) -> dict:
        """Generate comprehensive statistics"""
        stats = {
            'basic': df.describe().to_dict(),
            'missing': df.isnull().sum().to_dict(),
            'dtypes': df.dtypes.astype(str).to_dict(),
            'shape': df.shape
        }
        return stats
    
    def _analyze_correlations(self, df: pd.DataFrame) -> dict:
        """Analyze correlations between numeric columns"""
        numeric_df = df.select_dtypes(include=['int64', 'float64'])
        
        if numeric_df.empty or len(numeric_df.columns) < 2:
            return {'message': 'Not enough numeric columns for correlation analysis'}
        
        corr_matrix = numeric_df.corr()
        
        # Find strong correlations (absolute value > 0.5, excluding diagonal)
        strong_correlations = []
        for i in range(len(corr_matrix.columns)):
            for j in range(i + 1, len(corr_matrix.columns)):
                corr_value = corr_matrix.iloc[i, j]
                if abs(corr_value) > 0.5:
                    strong_correlations.append({
                        'feature1': corr_matrix.columns[i],
                        'feature2': corr_matrix.columns[j],
                        'correlation': round(corr_value, 3)
                    })
        
        return {
            'matrix': corr_matrix.to_dict(),
            'strong_correlations': strong_correlations
        }
    
    def _get_ai_exploration(self, df: pd.DataFrame, exploration_results: dict) -> str:
        """Ask Claude to interpret the exploration results"""
        
        # Prepare summary for Claude
        summary = f"""Dataset Shape: {df.shape[0]} rows × {df.shape[1]} columns

Columns: {', '.join(df.columns.tolist())}

Descriptive Statistics:
{df.describe().to_string()}

"""
        
        # Add correlation insights if available
        if 'strong_correlations' in exploration_results['correlations']:
            strong_corrs = exploration_results['correlations']['strong_correlations']
            if strong_corrs:
                summary += "\nStrong Correlations Found:\n"
                for corr in strong_corrs:
                    summary += f"- {corr['feature1']} ↔ {corr['feature2']}: {corr['correlation']}\n"
        
        prompt = f"""You are a data analyst. Analyze this dataset and provide key insights.

{summary}

Provide insights on:
1. Key patterns and trends in the data
2. Notable relationships between variables
3. Distribution characteristics (skewness, outliers, etc.)
4. Any interesting findings worth highlighting

Keep it concise and actionable. Use bullet points."""

        message = self.client.messages.create(
            model=self.model,
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return message.content[0].text


def demo_exploration_agent():
    """Demo the exploration agent with sample data"""
    print("=" * 60)
    print("Data Exploration Agent - Demo")
    print("=" * 60)
    
    # Create sample cleaned data
    data = {
        'name': ['Alice', 'Bob', 'Charlie', 'Eve', 'Frank', 'Grace'],
        'age': [25, 30, 35, 22, 28, 32],
        'salary': [50000, 60000, 55000, 48000, 58000, 62000],
        'department': ['Sales', 'Engineering', 'Sales', 'Marketing', 'Engineering', 'Sales'],
        'years_experience': [2, 5, 8, 1, 3, 6]
    }
    
    df = pd.DataFrame(data)
    
    print("\n📊 Dataset to Explore:")
    print(df)
    
    # Initialize agent
    agent = DataExplorationAgent()
    
    # Explore
    print("\n🔍 Exploring dataset...")
    results = agent.explore_dataset(df)
    
    print("\n📈 AI-Generated Insights:")
    print(results['ai_insights'])
    
    # Generate visualizations
    print("\n📊 Generating visualizations...")
    plots = agent.generate_visualizations(df)
    
    print(f"\n✅ Exploration complete! Generated {len(plots)} visualizations.")
    print("\nVisualization files:")
    for plot in plots:
        print(f"  - {plot}")


if __name__ == "__main__":
    demo_exploration_agent()