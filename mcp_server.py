
# to run-> mcp dev mcp_server.py

from pydantic import Field
from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.prompts import base

mcp = FastMCP("DocumentMCP", log_level="ERROR")


docs = {
    "deposition.md": "This deposition covers the testimony of Angela Smith, P.E.",
    "report.pdf": "The report details the state of a 20m condenser tower.",
    "financials.docx": "These financials outline the project's budget and expenditures.",
    "outlook.pdf": "This document presents the projected future performance of the system.",
    "plan.md": "The plan outlines the steps for the project's implementation.",
    "spec.txt": "These specifications define the technical requirements for the equipment.",
}

@mcp.tool(
    name="read_doc_contents",
    description="Read the contents of the document and return as the string",
)

# This is a simple implementation of a read tool that returns the contents of the document as a string.
def read_document(
    doc_id: str  = Field(description="The id of the document to read")
):
    if doc_id not in docs:
        raise ValueError(f"Document with id {doc_id} not found")

    return docs[doc_id]    

# This is a simple implementation of an edit tool that replaces the entire contents of the document with the new contents.
@mcp.tool(
    name="edit_doc_contents",
    description="Edit the contents by replacing the " \
        "existing contents with the new contents. " \
        "Return the new contents of the document",
)

def edit_document(
    doc_id: str  = Field(description="The id of the document to edit"),
    new_contents: str  = Field(description="The new contents of the document")
):  
    if doc_id not in docs:
        raise ValueError(f"Document with id {doc_id} not found")

    docs[doc_id] = new_contents
    return docs[doc_id]


# TODO: Write a resource to return all doc id's
@mcp.resource(
    "docs://documents",
    mime_type="application/json",
)
def list_documents() -> list[str]:
    return list(docs.keys())

# TODO: Write a resource to return the contents of a particular doc
@mcp.resource(
    "docs://documents/{doc_id}",
    mime_type="text/plain",
)
def get_document_contents(doc_id: str) -> str:
    if doc_id not in docs:
        raise ValueError(f"Document with id {doc_id} not found")
    return docs[doc_id]


@mcp.prompt(
    name="markdown_doc",
    description="Return a markdown summary of the document with the given id",
)
def format_doc_as_markdown(doc_id: str) -> list[base.Message]:
    if doc_id not in docs:
        raise ValueError(f"Document with id {doc_id} not found")
    
    prompt = f"""Your task is to read the contents of the document with id {doc_id} "
        " and return a markdown summary of the document. "
        " The ID of the document is {doc_id}. """ \

    #contents = docs[doc_id]
    #markdown_contents = f"# Document: {doc_id}\n\n{contents}"
    return [base.UserMessage(prompt)]

@mcp.prompt(    
    name="summarize_doc",
    description="Summarize the document with the given id and return the summary",
)

def summarize_doc(doc_id: str) -> str:
    if doc_id not in docs:
        raise ValueError(f"Document with id {doc_id} not found")
    
    prompt = f"""Your task is to read the contents of the document with id {doc_id} "
        " and summarize it. "
        " The ID of the document is {doc_id}. """ \
        
    return [base.UserMessage(prompt)]

if __name__ == "__main__":
    mcp.run(transport="stdio")
