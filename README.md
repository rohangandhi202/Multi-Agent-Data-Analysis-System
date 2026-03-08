# 🤖 Multi-Agent Data Analysis System

An intelligent data analysis pipeline powered by multiple AI agents that collaborate to clean, explore, and generate insights from messy datasets. Built with Claude AI, LangChain, and modern data science tools.

## 🎯 Project Overview

This system demonstrates **cutting-edge multi-agent AI coordination** where three specialized agents work together to perform comprehensive data analysis:

- **🧹 Data Cleaning Agent** - Identifies and fixes data quality issues
- **🔍 Data Exploration Agent** - Generates statistics, correlations, and visualizations  
- **📝 Insights Agent** - Synthesizes findings into actionable reports

Unlike traditional data analysis scripts, this project leverages **Claude AI's reasoning capabilities** at each step, making intelligent decisions about how to handle messy real-world data.

## ✨ Key Features

- **Automated Data Quality Assessment** - AI-powered detection of missing values, duplicates, and outliers
- **Intelligent Cleaning** - Context-aware strategies for handling data issues
- **Statistical Analysis** - Comprehensive exploration with correlations and distributions
- **Professional Visualizations** - Auto-generated charts (distributions, heatmaps, boxplots)
- **Executive Summaries** - AI-written reports in markdown format
- **End-to-End Pipeline** - From raw CSV to polished analysis in one command
- **Extensible Architecture** - Easy to add new agents or modify existing ones

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Orchestrator                            │
│              (Coordinates Agent Workflow)                   │
└──────────┬──────────────┬──────────────┬────────────────────┘
           │              │              │
           ▼              ▼              ▼
    ┌───────────┐  ┌────────────┐  ┌──────────────┐
    │ Cleaning  │  │Exploration │  │   Insights   │
    │   Agent   │─▶│   Agent    │─▶│    Agent     │
    └───────────┘  └────────────┘  └──────────────┘
         │               │                 │
         ▼               ▼                 ▼
    Clean Data    Visualizations    Final Report
```

**Data Flow:**
1. Raw CSV → Cleaning Agent analyzes issues → Cleaned dataset
2. Cleaned data → Exploration Agent → Statistics + Visualizations
3. All findings → Insights Agent → Comprehensive markdown report

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Anthropic API key ([Get one here](https://console.anthropic.com))

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/multi-agent-data-analysis.git
   cd multi-agent-data-analysis
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up your API key**
   
   Create a `.env` file in the project root:
   ```bash
   ANTHROPIC_API_KEY=your_api_key_here
   ```

### Usage

#### Generate Sample Data
```bash
python generate_data.py
```
Choose from 4 different dataset types with varying levels of messiness.

#### Run Analysis
```bash
# Analyze with default sample data
python main.py

# Analyze your own dataset
python main.py data/sales_data.csv
```

## 📊 Sample Output

After running the analysis, you'll find in the `output/` folder:

```
output/
├── analysis_report.md          # Comprehensive analysis report
├── cleaned_data.csv            # Cleaned dataset
├── distributions.png           # Data distribution charts
├── correlation_heatmap.png     # Correlation matrix visualization
├── boxplots.png               # Outlier detection plots
└── categorical_counts.png      # Category frequency charts
```

### Example Report Structure

The generated markdown report includes:
- **Executive Summary** - Key takeaways and recommendations
- **Data Quality Assessment** - Issues found and how they were resolved
- **Key Findings** - Most important insights from the data
- **Patterns and Trends** - Correlations and relationships discovered
- **Recommendations** - Actionable next steps based on analysis
- **Statistical Appendix** - Complete dataset statistics

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| **AI Model** | Claude Sonnet 4 (Anthropic API) |
| **Agent Framework** | LangChain |
| **Data Processing** | pandas, numpy |
| **Visualization** | matplotlib, seaborn |
| **Environment** | python-dotenv |

## 🎓 What This Demonstrates

This project showcases several advanced concepts relevant to modern data engineering and AI:

### 1. **Multi-Agent AI Systems**
- Agent specialization and coordination
- Passing context between agents
- Emergent intelligence from agent collaboration

### 2. **Production Data Engineering**
- Handling real-world messy data
- Automated data quality pipelines
- ETL workflow orchestration

### 3. **AI/LLM Integration**
- Programmatic API usage
- Prompt engineering for data analysis
- Combining AI reasoning with traditional algorithms

### 4. **Software Engineering Best Practices**
- Modular, extensible architecture
- Clean code organization
- Comprehensive documentation
- Environment configuration management

## 💡 Future Enhancements

Potential features to add:
- [ ] LangGraph integration for sophisticated agent workflows
- [ ] Streamlit web interface for non-technical users
- [ ] PDF report generation with charts embedded
- [ ] Batch processing for multiple datasets
- [ ] Real-time streaming analysis
- [ ] Integration with databases (PostgreSQL, MongoDB)
- [ ] Custom agent creation via configuration files

## 👤 Author

**Rohan Gandhi**
- Recent UCLA CS&E Graduate
- Data Engineer at AT&T
- [LinkedIn](https://www.linkedin.com/in/rohan-gandhi-202/)
- [Portfolio](https://www.rohangandhi202.com/)