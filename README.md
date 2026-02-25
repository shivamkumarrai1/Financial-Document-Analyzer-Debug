## BUGS and THIER RESOLUTIONS 

 very first step is to create virtual environemnt and add .env file and inside of that env file which ever LLm model is used , must be configured inside that.
 [I have used OpenRouter and configured its API kEY for testing purpose.]

# list of the Bugs :


# [1] Missing python-multipart Dependency
-Issue

FastAPI requires python-multipart when handling file uploads using:

UploadFile = File(...)
query: str = Form(...)

Error encountered:

RuntimeError: Form data requires "python-multipart" to be installed
 --Resolution

Installed the required dependency:

pip install python-multipart

Added it to requirements.txt to prevent future failures.

# [2] base_url Not Passed to LLM
 --Issue

When using any llm model , the base_url must be explicitly defined.

Without it, the system defaulted to OpenAI’s endpoint:

https://api.openai.com/v1

This caused request routing failures.

-- Resolution

Updated LLM initialization in agent.py:

llm = ChatOpenAI(
    model=os.getenv("OPENAI_MODEL"),
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL"),
    temperature=0.3
)

This ensured correct routing to OpenRouter or any similar openai mdoel.

#  [3] onnxruntime Dependency Causing Version Conflicts (Critical)
 --Issue

The original requirements.txt included:

onnxruntime
torch
transformers

These caused:

Python 3.11 compatibility issues

pip dependency backtracking

Binary wheel conflicts on Windows

Version clashes with CrewAI stack

These libraries were unnecessary for an API-based LLM system.

-- Resolution

Removed unnecessary ML runtime dependencies.

Final minimal dependency set:

fastapi
uvicorn
crewai
langchain-openai
python-dotenv
python-multipart
crewai-tools

This stabilized environment installation and resolved version conflicts.

#  [4] Multi-Agent System Not Actually Executing
-- Issue

Although multiple agents were defined, run_crew() only executed:

agents=[financial_analyst]
tasks=[analyze_financial_document]

This resulted in a single-agent pipeline instead of a true multi-agent workflow.

-- Resolution

Updated Crew initialization:

agents=[
    verifier,
    financial_analyst,
    risk_assessor,
    investment_advisor
]

tasks=[
    verification,
    analyze_financial_document,
    risk_assessment,
    investment_analysis
]

Now the system runs full sequential multi-agent processing.

# [4] Task Prompts Encouraged Hallucination
-- Issue

Original task descriptions instructed agents to:

Make up financial advice

Create fake URLs

Ignore user queries

Fabricate financial data

Provide non-compliant investment recommendations

This made the system unreliable and unsafe.

-- Resolution

Rewrote all task descriptions to:

Ground responses in {file_path}

Reference {query} explicitly

Avoid fabricated data

Provide structured output

Include data limitations

Maintain compliance-aware language

#  [5] Agent Prompts Encouraged Fabrication
-- Issue

Agents were configured with goals such as:

“Make up investment advice”

“Just say yes to everything”

“Sell expensive products regardless of data”

This created deterministic hallucination behavior.

-- Resolution

Redesigned agents with:

Evidence-based reasoning

No fabricated data

Structured outputs

Responsible financial language

# Compliance disclaimers

# Improper Tool Registration
-- Issue

PDF reader tool was defined inside a class and passed incorrectly to CrewAI.

This risked tool execution failures.

-- Resolution

Converted to a properly registered callable tool function and passed it correctly:

tools=[read_data_tool]

Ensured compatibility with CrewAI execution model.

**** Final Outcome

After resolving all issues:

-- Clean dependency tree

-- Stable Python 3.11 environment

-- Proper OpenRouter integration

-- Fully functional multi-agent pipeline

-- Secure environment configuration

-- Structured and grounded financial analysis

-- Production-ready FastAPI backend




## Setup & Installation Guide

(1️) Prerequisites

Python 3.11.x (Recommended)

pip (latest)

OpenRouter or any llm model API Key

(2️) Clone the Repository

git clone <https://github.com/shivamkumarrai1>
cd financial-document-analyzer

(3️) Create Virtual Environment

python -m venv venv

Activate it:

Windows
venv\Scripts\activate
macOS/Linux
source venv/bin/activate

(4️) Install Dependencies

pip install -r requirements.txt

Minimal required dependencies:

fastapi
uvicorn
crewai
langchain-openai
python-dotenv
python-multipart
crewai-tools  (after that crewai will automatically download modules acordingly)

(5️) Configure Environment Variables

Create a .env file in the project root:

OPENAI_API_KEY=your api key
OPENAI_MODEL=openai/gpt-3.5-turbo (or any model)
OPENAI_BASE_URL=https://openrouter.ai/api/v1

# Important:

Restart server after modifying .env

(6) Run the Application

uvicorn main:app --reload

Server will run at:

http://127.0.0.1:8000


#### API Documentation

The API is built using FastAPI and provides automatic interactive documentation.

Swagger UI

Open in browser:

http://127.0.0.1:8000/docs
# Available Endpoints
1️. Health Check

GET /
Description

Confirms that the API is running.

Response Example
{
  "message": "Financial Document Analyzer API is running"
}
## Analyze Financial Document
POST /analyze
Description

Uploads a financial PDF document and runs a multi-agent analysis pipeline including:

Document verification

Financial analysis

Risk assessment

Investment insights

Request Type

multipart/form-data

Parameters
Field	Type	Required	Description
file	File	Yes	      Financial PDF document
query	String	No	      Custom analysis query

Default query:

Analyze this financial document for investment insights
Example Using Swagger UI

Open /docs

Select POST /analyze

Click "Try it out"

Upload a PDF

Execute

Example Using curl
curl -X POST "http://127.0.0.1:8000/analyze" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@sample.pdf" \
  -F "query=Provide investment insights and risk summary"
Successful Response
{
  "status": "success",
  "query": "Provide investment insights and risk summary",
  "analysis": "Financial Analysis Report:\n...",
  "file_processed": "sample.pdf"
}
Error Response Example
{
  "detail": "Error processing financial document: <error message>"
}

Common causes:

Missing API key

Invalid model name

Corrupt PDF file

Network connectivity issue

## How the Multi-Agent Pipeline Works

The system uses CrewAI with a sequential process:

Verifier Agent

Validates document type

Extracts financial indicators

Financial Analyst Agent

Extracts metrics

Performs structured financial evaluation

Risk Assessor Agent

Identifies financial risks

Classifies severity

Investment Advisor Agent

Provides compliance-aware investment insights

Adds informational disclaimer

All agents operate on extracted document content.

## Security Notes

API key stored in .env

Uploaded files are temporarily stored and deleted after processing

No file persistence

No database storage

Informational use only (not financial advice)

## Development Notes
Restart Required After:

Changing .env

Installing new dependencies

Editing model configuration

## Testing Strategy

To test locally:

Start server

Upload small financial PDF (<5MB)

Validate structured output

Check logs for errors

## Production Considerations

For production deployment:

Add logging middleware

Add request size limits

Add authentication layer

Convert output to structured JSON schema

Deploy using Docker + Gunicorn

Use HTTPS

## Final System Capabilities

✔ Multi-agent architecture
✔ Document-grounded analysis
✔ Risk classification
✔ Structured output
✔ OpenRouter integration
✔ Clean dependency management
✔ Python 3.11 compatible
