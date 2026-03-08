"""
Multi-Agent Orchestrator
Coordinates the cleaning, exploration, and insights agents to perform end-to-end data analysis
"""

import os
import pandas as pd
from datetime import datetime
from agents import DataCleaningAgent, DataExplorationAgent, InsightsAgent


class DataAnalysisOrchestrator:
    """Orchestrates multi-agent data analysis workflow"""
    
    def __init__(self):
        """Initialize all agents"""
        print("🤖 Initializing Multi-Agent System...")
        self.cleaning_agent = DataCleaningAgent()
        self.exploration_agent = DataExplorationAgent()
        self.insights_agent = InsightsAgent()
        print("✅ All agents initialized!\n")
    
    def analyze(self, data_path: str, output_dir: str = "output") -> dict:
        """
        Run complete analysis pipeline
        
        Args:
            data_path: Path to the dataset (CSV or Excel)
            output_dir: Directory for outputs
            
        Returns:
            dict: Results from the analysis including report path and visualizations
        """
        print("=" * 70)
        print("MULTI-AGENT DATA ANALYSIS SYSTEM")
        print("=" * 70)
        print(f"\n📂 Loading dataset: {data_path}")
        
        # Load data
        original_df = self._load_data(data_path)
        print(f"✅ Loaded: {original_df.shape[0]} rows × {original_df.shape[1]} columns")
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        # Step 1: Data Cleaning Agent
        print("\n" + "=" * 70)
        print("STEP 1: DATA CLEANING")
        print("=" * 70)
        
        cleaning_analysis = self.cleaning_agent.analyze_dataset(original_df)
        print("\n🔍 Analysis from Cleaning Agent:")
        print(cleaning_analysis['analysis'])
        
        print("\n🧹 Performing data cleaning...")
        cleaned_df, cleaning_log = self.cleaning_agent.clean_dataset(
            original_df, 
            cleaning_analysis
        )
        
        print("\nCleaning Actions:")
        for log in cleaning_log:
            print(f"  {log}")
        
        print(f"\n✅ Cleaning complete: {cleaned_df.shape[0]} rows × {cleaned_df.shape[1]} columns")
        
        # Step 2: Data Exploration Agent
        print("\n" + "=" * 70)
        print("STEP 2: DATA EXPLORATION")
        print("=" * 70)
        
        print("\n🔍 Exploring cleaned dataset...")
        exploration_results = self.exploration_agent.explore_dataset(cleaned_df)
        
        print("\n📊 AI-Generated Insights:")
        print(exploration_results['ai_insights'])
        
        print("\n📈 Generating visualizations...")
        visualizations = self.exploration_agent.generate_visualizations(
            cleaned_df, 
            output_dir
        )
        
        print(f"\n✅ Generated {len(visualizations)} visualizations")
        
        # Step 3: Insights Agent
        print("\n" + "=" * 70)
        print("STEP 3: INSIGHTS GENERATION")
        print("=" * 70)
        
        print("\n📝 Generating executive summary...")
        exec_summary = self.insights_agent.generate_executive_summary(exploration_results)
        print("\nExecutive Summary:")
        print(exec_summary)
        
        report_path = self.insights_agent.generate_report(
            original_df,
            cleaned_df,
            cleaning_log,
            exploration_results,
            output_file=f"{output_dir}/analysis_report.md"
        )
        
        # Save cleaned dataset
        cleaned_data_path = f"{output_dir}/cleaned_data.csv"
        cleaned_df.to_csv(cleaned_data_path, index=False)
        print(f"  ✓ Cleaned data saved to: {cleaned_data_path}")
        
        # Final summary
        print("\n" + "=" * 70)
        print("ANALYSIS COMPLETE!")
        print("=" * 70)
        
        results = {
            'report_path': report_path,
            'cleaned_data_path': cleaned_data_path,
            'visualizations': visualizations,
            'executive_summary': exec_summary,
            'original_rows': original_df.shape[0],
            'cleaned_rows': cleaned_df.shape[0],
            'rows_removed': original_df.shape[0] - cleaned_df.shape[0]
        }
        
        self._print_final_summary(results)
        
        return results
    
    def _load_data(self, data_path: str) -> pd.DataFrame:
        """Load data from CSV or Excel file"""
        file_extension = os.path.splitext(data_path)[1].lower()
        
        if file_extension == '.csv':
            return pd.read_csv(data_path)
        elif file_extension in ['.xlsx', '.xls']:
            return pd.read_excel(data_path)
        else:
            raise ValueError(f"Unsupported file format: {file_extension}. Use CSV or Excel.")
    
    def _print_final_summary(self, results: dict):
        """Print final summary of the analysis"""
        print("\n📋 FINAL SUMMARY:")
        print(f"  • Original dataset: {results['original_rows']} rows")
        print(f"  • Cleaned dataset: {results['cleaned_rows']} rows")
        print(f"  • Rows removed: {results['rows_removed']}")
        print(f"  • Visualizations: {len(results['visualizations'])}")
        print(f"\n📁 OUTPUT FILES:")
        print(f"  • Report: {results['report_path']}")
        print(f"  • Cleaned data: {results['cleaned_data_path']}")
        print(f"  • Visualizations: {len(results['visualizations'])} PNG files")
        print(f"\n🎉 All outputs saved to '{os.path.dirname(results['report_path'])}/' directory")


def main():
    """Main entry point for the orchestrator demo"""
    
    # Create sample dataset for demo
    demo_data_path = "data/sample_data.csv"
    
    # Check if data directory exists
    if not os.path.exists("data"):
        os.makedirs("data")
    
    # Create sample data if it doesn't exist
    if not os.path.exists(demo_data_path):
        print("📝 Creating sample dataset for demo...")
        sample_data = {
            'employee_id': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 11],
            'name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve', None, 'Grace', 'Henry', 'Ivy', 'Jack', 'Jack', 'Kelly'],
            'age': [25, 30, 35, 28, None, 45, 32, 150, 27, 33, 33, 29],
            'department': ['Sales', 'Engineering', 'Sales', 'Marketing', 'Engineering', 'Sales', None, 'Marketing', 'Engineering', 'Sales', 'Sales', 'HR'],
            'salary': [50000, 65000, 55000, 52000, None, 58000, 61000, 54000, 5000000, 56000, 56000, 53000],
            'years_experience': [2, 5, 8, 3, 4, 12, 6, 1, 5, 7, 7, 4],
            'performance_score': [85, 92, 88, 78, 90, None, 87, 82, 95, 84, 84, 89]
        }
        
        df = pd.DataFrame(sample_data)
        df.to_csv(demo_data_path, index=False)
        print(f"✅ Sample dataset created at: {demo_data_path}\n")
    
    # Initialize orchestrator
    orchestrator = DataAnalysisOrchestrator()
    
    # Run analysis
    results = orchestrator.analyze(demo_data_path)
    
    print("\n" + "=" * 70)
    print("💡 NEXT STEPS:")
    print("=" * 70)
    print("1. Check the 'output/' folder for your report and visualizations")
    print("2. Open 'output/analysis_report.md' to see the full report")
    print("3. Try running with your own dataset:")
    print("   python main.py")
    print("=" * 70)


if __name__ == "__main__":
    main()