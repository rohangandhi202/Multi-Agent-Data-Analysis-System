"""
Insights Agent
Synthesizes findings from cleaning and exploration to generate final report
"""

import os
import pandas as pd
from anthropic import Anthropic
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()


class InsightsAgent:
    """Agent responsible for generating final insights and reports"""
    
    def __init__(self):
        """Initialize the insights agent with Claude API"""
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.model = "claude-sonnet-4-20250514"
    
    def generate_report(self, 
                       original_df: pd.DataFrame,
                       cleaned_df: pd.DataFrame,
                       cleaning_log: list,
                       exploration_results: dict,
                       output_file: str = "output/analysis_report.md") -> str:
        """
        Generate a comprehensive analysis report
        
        Args:
            original_df: Original dataset before cleaning
            cleaned_df: Dataset after cleaning
            cleaning_log: List of cleaning actions performed
            exploration_results: Results from exploration agent
            output_file: Path to save the report
            
        Returns:
            str: Path to the generated report
        """
        print("\n📝 Generating comprehensive report...")
        
        # Create output directory if needed
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        # Gather all information
        report_context = self._prepare_report_context(
            original_df, cleaned_df, cleaning_log, exploration_results
        )
        
        # Ask Claude to write the report
        report_content = self._generate_report_with_ai(report_context)
        
        # Add header and metadata
        final_report = self._format_final_report(report_content, original_df, cleaned_df)
        
        # Save to file
        with open(output_file, 'w') as f:
            f.write(final_report)
        
        print(f"  ✓ Report saved to: {output_file}")
        
        return output_file
    
    def generate_executive_summary(self, exploration_results: dict) -> str:
        """
        Generate a brief executive summary of key findings
        
        Args:
            exploration_results: Results from exploration agent
            
        Returns:
            str: Executive summary text
        """
        prompt = f"""Based on this data analysis, create a brief executive summary (3-5 sentences) 
highlighting the most important findings and actionable insights.

Analysis Results:
{exploration_results.get('ai_insights', 'No insights available')}

Correlations:
{self._format_correlations(exploration_results.get('correlations', {}))}

Write a concise summary that a business stakeholder would find valuable."""

        message = self.client.messages.create(
            model=self.model,
            max_tokens=500,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return message.content[0].text
    
    def _prepare_report_context(self, original_df, cleaned_df, cleaning_log, exploration_results):
        """Prepare all context information for the report"""
        context = {
            'original_shape': original_df.shape,
            'cleaned_shape': cleaned_df.shape,
            'rows_removed': original_df.shape[0] - cleaned_df.shape[0],
            'cleaning_actions': cleaning_log,
            'columns': cleaned_df.columns.tolist(),
            'exploration_insights': exploration_results.get('ai_insights', ''),
            'correlations': exploration_results.get('correlations', {}),
            'statistics': exploration_results.get('statistics', {})
        }
        return context
    
    def _generate_report_with_ai(self, context: dict) -> str:
        """Use Claude to generate the main report content"""
        
        correlations_text = self._format_correlations(context['correlations'])
        
        prompt = f"""You are a senior data analyst writing a professional data analysis report.

DATASET INFORMATION:
- Original size: {context['original_shape'][0]} rows × {context['original_shape'][1]} columns
- Final size: {context['cleaned_shape'][0]} rows × {context['cleaned_shape'][1]} columns
- Rows removed: {context['rows_removed']}
- Columns: {', '.join(context['columns'])}

DATA CLEANING PERFORMED:
{self._format_cleaning_log(context['cleaning_actions'])}

EXPLORATION INSIGHTS:
{context['exploration_insights']}

{correlations_text}

Write a professional analysis report with these sections:

## Executive Summary
[Brief overview of the analysis and key takeaways - 2-3 paragraphs]

## Data Quality Assessment
[Discuss the data quality issues found and how they were addressed]

## Key Findings
[List the most important insights discovered in the data - use bullet points]

## Patterns and Trends
[Describe notable patterns, correlations, and trends]

## Recommendations
[Provide 3-5 actionable recommendations based on the analysis]

## Conclusion
[Wrap up with final thoughts and next steps]

Write in a professional, clear style suitable for business stakeholders."""

        message = self.client.messages.create(
            model=self.model,
            max_tokens=2500,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return message.content[0].text
    
    def _format_final_report(self, content: str, original_df: pd.DataFrame, 
                            cleaned_df: pd.DataFrame) -> str:
        """Add header, metadata, and formatting to the report"""
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        header = f"""# Data Analysis Report

**Generated:** {timestamp}  
**Analysis System:** Multi-Agent Data Analysis  
**Original Dataset:** {original_df.shape[0]} rows × {original_df.shape[1]} columns  
**Cleaned Dataset:** {cleaned_df.shape[0]} rows × {cleaned_df.shape[1]} columns  

---

"""
        
        footer = f"""

---

## Dataset Overview

### Original Dataset
- **Shape:** {original_df.shape[0]} rows × {original_df.shape[1]} columns
- **Columns:** {', '.join(original_df.columns.tolist())}

### Cleaned Dataset  
- **Shape:** {cleaned_df.shape[0]} rows × {cleaned_df.shape[1]} columns
- **Data Quality:** All missing values addressed, duplicates removed, outliers handled

### Statistical Summary
```
{cleaned_df.describe().to_string()}
```

---

*Report generated by Multi-Agent Data Analysis System*
"""
        
        return header + content + footer
    
    def _format_cleaning_log(self, cleaning_log: list) -> str:
        """Format cleaning log for the report"""
        if not cleaning_log:
            return "No cleaning actions were necessary."
        return "\n".join([f"- {action}" for action in cleaning_log])
    
    def _format_correlations(self, correlations: dict) -> str:
        """Format correlation information"""
        if 'strong_correlations' not in correlations:
            return ""
        
        strong_corrs = correlations['strong_correlations']
        if not strong_corrs:
            return "CORRELATIONS:\nNo strong correlations found (threshold: |r| > 0.5)"
        
        corr_text = "STRONG CORRELATIONS FOUND:\n"
        for corr in strong_corrs:
            corr_text += f"- {corr['feature1']} ↔ {corr['feature2']}: r = {corr['correlation']}\n"
        
        return corr_text


def demo_insights_agent():
    """Demo the insights agent"""
    print("=" * 60)
    print("Insights Agent - Demo")
    print("=" * 60)
    
    # Create sample data (simulating what we'd get from previous agents)
    original_data = {
        'name': ['Alice', 'Bob', 'Charlie', 'Bob', 'Eve', None, 'Frank'],
        'age': [25, 30, None, 30, 22, 150, 28],
        'salary': [50000, 60000, 55000, 60000, None, 58000, 1000000],
        'department': ['Sales', 'Engineering', 'Sales', 'Engineering', 'Marketing', 'Sales', None]
    }
    
    cleaned_data = {
        'name': ['Alice', 'Bob', 'Charlie', 'Eve', 'Frank'],
        'age': [25, 30, 27, 22, 28],
        'salary': [50000, 60000, 55000, 56000, 58000],
        'department': ['Sales', 'Engineering', 'Sales', 'Marketing', 'Engineering']
    }
    
    original_df = pd.DataFrame(original_data)
    cleaned_df = pd.DataFrame(cleaned_data)
    
    cleaning_log = [
        "✓ Removed 1 duplicate rows",
        "✓ Filled 1 missing values in 'age' with median",
        "✓ Filled 1 missing values in 'salary' with median",
        "✓ Removed 2 outliers from 'age'",
        "✓ Removed 1 outliers from 'salary'"
    ]
    
    # Mock exploration results
    exploration_results = {
        'ai_insights': """Key insights from the data:
• The dataset shows a diverse workforce across Sales, Engineering, and Marketing departments
• Age distribution is relatively balanced, centered around late 20s to early 30s
• Salary shows positive correlation with age, suggesting experience-based compensation
• Sales department has the highest representation in the cleaned dataset
• No extreme outliers remain after cleaning, indicating data quality improvements""",
        'correlations': {
            'strong_correlations': [
                {'feature1': 'age', 'feature2': 'salary', 'correlation': 0.75}
            ]
        },
        'statistics': {'shape': cleaned_df.shape}
    }
    
    # Initialize agent
    agent = InsightsAgent()
    
    # Generate executive summary
    print("\n📊 Generating executive summary...")
    summary = agent.generate_executive_summary(exploration_results)
    print("\nExecutive Summary:")
    print(summary)
    
    # Generate full report
    report_path = agent.generate_report(
        original_df, 
        cleaned_df, 
        cleaning_log, 
        exploration_results
    )
    
    print(f"\n✅ Complete! Full report available at: {report_path}")
    print("\nYou can open the report in any markdown viewer or text editor.")


if __name__ == "__main__":
    demo_insights_agent()