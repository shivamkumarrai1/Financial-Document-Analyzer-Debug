## Importing libraries and files
import os
from dotenv import load_dotenv

from crewai import Agent
from langchain_openai import ChatOpenAI

from tools import read_data_tool

# Load environment variables
load_dotenv()



# LLM Configuration (OpenRouter)

llm = ChatOpenAI(
    model=os.getenv("OPENAI_MODEL"),
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL"),  # only needed for OpenRouter
    temperature=0.3
)



# 1️⃣ Financial Analyst Agent

financial_analyst = Agent(
    role="Senior Financial Analyst",
    goal=(
        "Analyze the financial document located at {file_path} "
        "and answer the user query: {query}. "
        "Use only verified data extracted from the document. "
        "Do not fabricate financial metrics. "
        "Clearly state when data is unavailable."
    ),
    backstory=(
        "You are a CFA-certified financial analyst with 15 years of experience "
        "in equity research, balance sheet evaluation, and corporate financial modeling. "
        "You provide structured, evidence-based analysis grounded strictly in financial data."
    ),
    tools=[read_data_tool],
    verbose=True,
    memory=False,
    max_iter=3,
    allow_delegation=False,
    llm=llm
)



# 2 Document Verifier Agent

verifier = Agent(
    role="Financial Document Verifier",
    goal=(
        "Determine whether the file at {file_path} is a financial document. "
        "Identify key financial indicators such as revenue, assets, liabilities, "
        "cash flow statements, or balance sheet terminology. "
        "Provide justification for your classification."
    ),
    backstory=(
        "You are a financial compliance officer specializing in document validation "
        "and regulatory review. You verify documents carefully and base conclusions "
        "only on observable financial content."
    ),
    tools=[read_data_tool],
    verbose=True,
    memory=False,
    max_iter=2,
    allow_delegation=False,
    llm=llm
)



# 3️ Risk Assessment Agent

risk_assessor = Agent(
    role="Financial Risk Assessment Specialist",
    goal=(
        "Evaluate financial risks based on extracted data from {file_path}. "
        "Assess liquidity risk, credit risk, operational risk, and market exposure. "
        "Support each risk conclusion with evidence from the document."
    ),
    backstory=(
        "You are a certified risk management professional (FRM) with deep expertise "
        "in financial risk modeling, volatility analysis, and capital structure evaluation."
    ),
    tools=[read_data_tool],
    verbose=True,
    memory=False,
    max_iter=2,
    allow_delegation=False,
    llm=llm
)


# 4️ Investment Advisor Agent

investment_advisor = Agent(
    role="Investment Strategy Advisor",
    goal=(
        "Based strictly on the financial analysis and risk assessment, "
        "provide conservative and compliance-aware investment insights. "
        "Do not provide personalized financial advice. "
        "Include a disclaimer that the information is for educational purposes only."
    ),
    backstory=(
        "You are a licensed financial advisor with extensive experience "
        "in portfolio management and regulatory compliance. "
        "You prioritize evidence-based, responsible financial guidance."
    ),
    tools=[read_data_tool],
    verbose=True,
    memory=False,
    max_iter=2,
    allow_delegation=False,
    llm=llm
)