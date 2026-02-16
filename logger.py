import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, Dict, Any


def log_event(
    project: str,
    agent: str,
    status: str,
    message: str,
    artifact: Optional[str] = None,
    meta: Optional[Dict[str, Any]] = None
) -> None:
    """
    Log an event to events.jsonl with UTC ISO timestamp.

    Args:
        project: Project name/identifier
        agent: Agent name/identifier
        status: Event status (e.g., "started", "completed", "failed")
        message: Human-readable event message
        artifact: Optional artifact reference or path
        meta: Optional metadata dictionary
    """
    event = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "project": project,
        "agent": agent,
        "status": status,
        "message": message
    }

    if artifact is not None:
        event["artifact"] = artifact

    if meta is not None:
        event["meta"] = meta

    events_file = Path(__file__).parent / "events.jsonl"

    with open(events_file, "a") as f:
        f.write(json.dumps(event) + "\n")


def sync_to_github(commit_message: str = "Update events") -> None:
    """
    Sync changes to GitHub via git add/commit/push.
    Does not error if there's nothing to commit.

    Args:
        commit_message: Commit message to use
    """
    repo_dir = Path(__file__).parent

    try:
        # Add all changes
        subprocess.run(
            ["git", "add", "."],
            cwd=repo_dir,
            check=True,
            capture_output=True
        )

        # Commit changes - this will fail if nothing to commit, which is fine
        result = subprocess.run(
            ["git", "commit", "-m", commit_message],
            cwd=repo_dir,
            capture_output=True,
            text=True
        )

        # Only push if commit was successful
        if result.returncode == 0:
            subprocess.run(
                ["git", "push"],
                cwd=repo_dir,
                check=True,
                capture_output=True
            )
    except subprocess.CalledProcessError:
        # Silently ignore errors (e.g., nothing to commit)
        pass
