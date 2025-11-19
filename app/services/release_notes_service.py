"""
High-level service that orchestrates release notes generation and publishing.

Responsibilities:
- Retrieve issues for a given project and fixVersion from Jira
- Transform issues into concise summaries and aggregate into Markdown via the
  generator pipeline
- Publish the generated document to Confluence (to be implemented)

This service is intended to be called by a CLI or scheduler with the
`project` and `fix_version` parameters.
"""

from typing import Any

from uvicorn.main import logger
from app.integrations.jira import JiraClient
from app.integrations.confluence import ConfluenceClient
from app.generator.pipeline import GeneratorPipeline
from app.config import Config

class ReleaseNotesService:
    """Entry point for end-to-end release notes production and publishing."""

    def __init__(self):
        """Initialize the service with configuration and clients."""
        self.config = Config.from_env()
        self.jira_client = JiraClient(self.config)
        self.confluence_client = ConfluenceClient(self.config)
        self.generator_pipeline = GeneratorPipeline(self.config)

    def generate_single_project_release_notes(self, project: str, fix_version: str) -> Any:
        """Generate the release notes for a project and fix version.

        Steps:
        1) Fetch issues from Jira using project and fixVersion filters
        2) Extract minimal, LLM-friendly fields from the raw issues
        3) Run the generator pipeline to summarize and aggregate
        4) Publish the results to Confluence

        Args:
            project: Jira project key or name used in the JQL filter.
            fix_version: The fixVersion to filter issues by.

        Returns:
            The generated Markdown release notes string, or a publishing result
            in a future iteration. Currently returns None because publishing is
            not implemented.
        """
        try:
            # Validate the project and fix_version
            #TODO: Implement the validation


            #GoContact Project & Communicator Project filter 
            JiraQL = self.jira_client.select_jira_jql_filter(project, fix_version)

            #Get the issues from Jira
            issues = self.jira_client.get_issues(project, JiraQL)

            #Extract the useful information from the issues
            issues_data = self.jira_client.extract_useful_information(project, issues)

            #Run the generator pipeline (per-issue summarization + aggregation)
            generated_release_notes = self.generator_pipeline.run(issues_data, fix_version=fix_version)

            #Publish to Confluence Space Key
            space_key = self.config.confluence_space_key
    
            page_title = f"Ag - Release Notes - {project} - {fix_version}"
            if generated_release_notes:
                try:
                    self.confluence_client.create_page(
                        space=space_key,
                        title=page_title,
                        body_markdown=generated_release_notes,
                        parent_id=None,
                        status="draft",
                    )
                    logger.info(f"The generation of the release notes Document for the project {project}  with the release version {fix_version} is completed")
                    return f"The generation of the release notes Document for the project {project}  with the release version {fix_version} is completed"
                
                except Exception as exc:
                    # For now, don't fail the whole flow; just log
                    logger.error(f"Failed to create Confluence page: {exc}")
                    return f"Failed to create Confluence page for the project {project} with the release version {fix_version}"
            else:
                return f"Failed to generate release notes for the project {project} with the release version {fix_version}"

        except Exception as exc:
            # For now, don't fail the whole flow; just log
            logger.error(f"Failed to generate release notes: {exc}")
            return f"Failed to generate release notes for the project {project} with the release version {fix_version}"


    def generate_multiple_project_release_notes(self, project: str, fix_version: str) -> Any:
        """Generate release notes for multiple projects (Communicator).
        
        Args:
            project: Project name (currently expects "Communicator" or similar)
            fix_version: The fixVersion to filter issues by (same for all projects).
            
        Returns:
            Status string with generation result.
        """
        try:
            # GoContact Project & Communicator Project filter 
            JiraQL = self.jira_client.select_jira_jql_filter(project, fix_version)

            # Get all the issues, already simplified to spare computation time from all Communicator Projects in Jira
            issues = self.jira_client.get_issues(project, JiraQL)

            # Extract the useful information from the issues
            issues_data = self.jira_client.extract_useful_information(project, issues)

            # Extract unique projects from issues_data (each issue already has a "project" field)
            unique_projects = set()
            for issue in issues_data:
                project_key = issue.get("project")
                if project_key:
                    unique_projects.add(project_key)
                # Ensure each issue has fix_version field
                if "fix_version" not in issue:
                    issue["fix_version"] = fix_version

            # Build projects list with same fix_version for all, sorted by priority (BAMA → BIMA2 → CUU2 → COMAPI)
            def _project_priority(project_key: str) -> int:
                key_up = (project_key or "").strip().upper()
                order = {"BAMA": 0, "BIMA2": 1, "CUU2": 2, "COMAPI": 3}
                return order.get(key_up, 100)

            projects_list = [
                {"project": p, "fixVersion": fix_version}
                for p in sorted(unique_projects, key=lambda x: (_project_priority(x), x.upper()))
            ]

            # Run the generator pipeline (per-project + per-issue summarization + aggregation)
            generated_multiproject_release_notes = self.generator_pipeline.run_multiproject(issues_data, projects_list)

            # Publish to Confluence (single combined page)
            space_key = self.config.confluence_space_key
            page_title = f"Ag - Release Notes - Communicator - {fix_version}"
            
            if generated_multiproject_release_notes:
                try:
                    self.confluence_client.create_page(
                        space=space_key,
                        title=page_title,
                        body_markdown=generated_multiproject_release_notes,
                        parent_id=None,
                        status="draft",
                    )
                    logger.info(f"The generation of the release notes Document for the project {project} with the release version {fix_version} is completed")
                    return f"The generation of the release notes Document for the project {project} with the release version {fix_version} is completed"
                
                except Exception as exc:
                    # For now, don't fail the whole flow; just log
                    logger.error(f"Failed to create Confluence page: {exc}")
                    return f"Failed to create Confluence page for the project {project} with the release version {fix_version}"
            else:
                return f"Failed to generate release notes for the project {project} with the release version {fix_version}"

        except Exception as exc:
            # For now, don't fail the whole flow; just log
            logger.error(f"Failed to generate release notes: {exc}")
            return f"Failed to generate release notes for the project {project} with the release version {fix_version}"

