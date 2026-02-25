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