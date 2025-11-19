"""
FastMCP Release Notes Generator
"""

from fastmcp import FastMCP
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
import uvicorn
import os
from app.services.release_notes_service import ReleaseNotesService
from app.logging import configure_logging
import logging


# Create MCP server for the Release Notes Generator
mcp = FastMCP("Release Notes Generator")

# Initialize the Release Notes Service
_service = ReleaseNotesService()

# Configure the logger
configure_logging()

# Initialize the logger
_logger = logging.getLogger(__name__)
_logger.info("Release Notes Generator MCP Server is starting...")


# Status Tool
@mcp.tool(description="Get the status of the Release Notes Generator", name="status_tool")
def status_tool() -> str:
    """Get the status of the Release Notes Generator"""
    _logger.info("Status tool is called")
    return "status: The Release Notes Generator is running"

# Single Project Release Notes Documents Generator Tool
@mcp.tool(description="Generate the release notes for a given release version of the project GoContact or project Portal", name="single_release_notes_generator_tool")
def single_release_notes_generator_tool(project_name: str, release_version: str) -> str:

    _logger.info(f"Single release notes generator tool is called for the project {project_name} with the release version {release_version}")
    response =_service.generate_single_project_release_notes(project_name, release_version)

    return response

# Multiple Projects Release Notes Documents Generator Tool
@mcp.tool(description="Generate the release notes for a given release versions of the project Communicator", name="multiple_release_notes_generator_tool")
def multiple_release_notes_generator_tool(project_name: str, release_version: str) -> str:
    
    _logger.info(f"Multiple release notes generator tool is called for the project {project_name} with the release versions {release_version}")
    response = _service.generate_multiple_project_release_notes(project_name, release_version)

    return response
    
# Configure CORS for browser-based clients
middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Allow all origins; use specific origins for security
        allow_methods=["GET", "POST", "DELETE", "OPTIONS"],
        allow_headers=[
            "mcp-protocol-version",
            "mcp-session-id",
            "Authorization",
            "Content-Type",
        ],
        expose_headers=["mcp-session-id"],
    )
]
app = mcp.http_app(middleware=middleware)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9898)