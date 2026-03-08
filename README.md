# Multi-Agent-Data-Analysis-System

### Phase 1
from anthropic import Anthropic
import pandas as pd

client = Anthropic(api_key="your-key")

def cleaning_agent(df_description):
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        messages=[{
            "role": "user",
            "content": f"Analyze this data and suggest cleaning steps: {df_description}"
        }]
    )
    return response.content[0].text

### Phase 2: Multi-Agent with LangGraph (Day 2)
Build the actual multi-agent system. LangGraph lets you define a workflow graph where agents pass information.

**Key concept**: Each agent is a "node" in the graph, and you define edges showing how data flows.

### Phase 3: Polish & Portfolio (Day 3)
- Add error handling
- Create a nice README with architecture diagram
- Deploy to GitHub with example outputs
- (Bonus) Add a Streamlit UI

## Sample Workflow
User uploads messy_sales_data.csv
    ↓
Coordinator analyzes file
    ↓
Cleaning Agent: "I found 15% missing values in 'revenue' column. 
                 I'll use median imputation. 3 duplicate rows removed."
    ↓
Exploration Agent: "Revenue shows strong seasonality. 
                    Q4 averages 40% higher than Q2."
    ↓
Insights Agent: "Recommendation: Increase inventory before Q4. 
                 Revenue correlates 0.78 with marketing_spend."
    ↓
Final PDF Report generated