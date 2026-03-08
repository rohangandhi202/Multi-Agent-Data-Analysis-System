"""
Multi-Agent Data Analysis System
Main entry point - orchestrates all agents to analyze datasets
"""

import sys
from orchestrator import DataAnalysisOrchestrator


def main():
    """Run the multi-agent data analysis system"""
    
    # Check if user provided a dataset path
    if len(sys.argv) > 1:
        data_path = sys.argv[1]
    else:
        # Use default sample data
        data_path = "data/sample_data.csv"
        print("ℹ️  No dataset specified. Using default: data/sample_data.csv")
        print("   To analyze your own data: python main.py path/to/your/data.csv\n")
    
    # Initialize and run orchestrator
    orchestrator = DataAnalysisOrchestrator()
    
    try:
        results = orchestrator.analyze(data_path)
        
        print("\n✅ SUCCESS! Analysis complete.")
        print(f"\n📊 View your report: {results['report_path']}")
        
    except FileNotFoundError:
        print(f"\n❌ ERROR: File not found: {data_path}")
        print("Please check the file path and try again.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()