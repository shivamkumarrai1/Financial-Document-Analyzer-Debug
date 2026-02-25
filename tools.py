## Importing libraries and files
import os
from dotenv import load_dotenv
load_dotenv()

from crewai.tools import tool
from langchain_community.document_loaders import PyPDFLoader


@tool
def read_data_tool(path: str) -> str:
    """
    Tool to read financial data from a PDF file.
    """

    if not os.path.exists(path):
        return f"File not found at path: {path}"

    loader = PyPDFLoader(path)
    docs = loader.load()

    full_report = ""

    for data in docs:
        content = data.page_content.strip()
        content = content.replace("\n\n", "\n")
        full_report += content + "\n"

    return full_report