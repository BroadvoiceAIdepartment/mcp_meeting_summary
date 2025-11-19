from dataclasses import dataclass
import os
from dotenv import load_dotenv
from pathlib import Path


@dataclass
class Config:
    jira_url: str
    jira_issue_base_url: str
    jira_email: str
    jira_token: str
    confluence_url: str
    confluence_email: str
    confluence_token: str
    confluence_space_key: str
    openai_api_key: str
    openai_model: str
    dump_folder: str
    feedback_form_url: str

    @staticmethod
    def from_env() -> "Config":
        script_dir = Path(__file__).resolve().parent
        repo_root = script_dir.parent
        env_path = repo_root / ".env"
        load_dotenv(str(env_path))

        env_dump = os.getenv("DUMP_FOLDER", "app/utils/logs/dump_files").strip()
        if os.path.isabs(env_dump):
            dump_folder = env_dump
        else:
            dump_folder = str(repo_root / env_dump)

        return Config(
            jira_url=os.getenv("JIRA_URL", ""),
            jira_issue_base_url=os.getenv("JIRA_ISSUE_BASE_URL", ""),
            jira_email=os.getenv("JIRA_EMAIL", ""),
            jira_token=os.getenv("JIRA_TOKEN", ""),
            confluence_url=os.getenv("CONFLUENCE_URL", ""),
            confluence_email=os.getenv("CONFLUENCE_EMAIL", ""),
            confluence_token=os.getenv("CONFLUENCE_TOKEN", ""),
            confluence_space_key=os.getenv("CONFLUENCE_SPACE_KEY", "ARN"),
            openai_model=os.getenv("OPENAI_MODEL", ""),
            openai_api_key=os.getenv("OPENAI_API_KEY", ""),
            dump_folder=dump_folder,
            feedback_form_url=os.getenv("FEEDBACK_FORM_URL", ""),
        )