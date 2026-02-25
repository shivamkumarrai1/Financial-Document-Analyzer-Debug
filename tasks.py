## Importing libraries and files
from crewai import Task

from agent import (
    financial_analyst,
    verifier,
    risk_assessor,
    investment_advisor
)

from tools import read_data_tool


# ----------------------------
# 1️ Document Verification Task
# ----------------------------
verification = Task(
    description=(
        "Read the file located at {file_path}. "
        "Determine whether it is a valid financial document. "
        "Look for financial indicators such as revenue, expenses, "
        "assets, liabilities, equity, income statements, balance sheets, "
        "or cash flow statements. "
        "Provide justification for your conclusion."
    ),
    expected_output=(
        "Verification Report:\n"
        "1. Document Type\n"
        "2. Key Financial Indicators Found\n"
        "3. Supporting Evidence\n"
        "4. Confidence Level (High/Medium/Low)\n"
    ),
    agent=verifier,
    tools=[read_data_tool],
    async_execution=False,
)


# ----------------------------
# 2️ Financial Analysis Task
# ----------------------------
analyze_financial_document = Task(
    description=(
        "Using the verified financial document at {file_path}, "
        "analyze it in response to the user's query: {query}. "
        "Extract and reference relevant financial data directly from the document. "
        "Do not fabricate numbers or assumptions. "
        "If certain data is unavailable, clearly mention the limitation."
    ),
    expected_output=(
        "Financial Analysis Report:\n"
        "1. Executive Summary\n"
        "2. Key Financial Metrics Identified\n"
        "3. Profitability Analysis\n"
        "4. Liquidity and Solvency Assessment\n"
        "5. Growth Indicators\n"
        "6. Data Limitations\n"
    ),
    agent=financial_analyst,
    tools=[read_data_tool],
    async_execution=False,
)


# ----------------------------
# 3️ Risk Assessment Task
# ----------------------------
risk_assessment = Task(
    description=(
        "Based strictly on extracted financial data from {file_path}, "
        "assess the potential financial risks. "
        "Evaluate liquidity risk, leverage risk, operational risk, "
        "and market exposure. "
        "Support each identified risk with evidence from the document."
    ),
    expected_output=(
        "Risk Assessment Report:\n"
        "1. Identified Risks\n"
        "2. Supporting Financial Evidence\n"
        "3. Risk Severity (Low/Medium/High)\n"
        "4. Suggested Risk Mitigation Strategies\n"
    ),
    agent=risk_assessor,
    tools=[read_data_tool],
    async_execution=False,
)


# ----------------------------
# 4️ Investment Insight Task
# ----------------------------
investment_analysis = Task(
    description=(
        "Based on the financial analysis and risk assessment results, "
        "provide responsible and compliance-aware investment insights. "
        "Avoid personalized financial advice. "
        "Provide conservative recommendations grounded in document data."
    ),
    expected_output=(
        "Investment Insight Report:\n"
        "1. Overall Financial Health Summary\n"
        "2. Suitable Investor Profile (Conservative/Moderate/Aggressive)\n"
        "3. Investment Considerations\n"
        "4. Disclaimer (Informational Purposes Only)\n"
    ),
    agent=investment_advisor,
    tools=[read_data_tool],
    async_execution=False,
)