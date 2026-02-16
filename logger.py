import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path


def log_event(project: str, agent: str, status: str, message: str, artifact: str = None, meta: dict = None):
    """
    Log an event to events.jsonl with UTC ISO timestamp.

    Args:
        project: Project name
        agent: Agent name
        status: Status (started, done, error, etc.)
        message: Event message (must be public-safe)
        artifact: Optional artifact path
        meta: Optional metadata dict
    """
    event = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "project": project,
        "agent": agent,
        "status": status,
        "message": message,
    }

    if artifact:
        event["artifact"] = artifact

    if meta:
        event["meta"] = meta

    # Get the path to events.jsonl
    repo_dir = Path(__file__).parent
    events_file = repo_dir / "events.jsonl"

    # Append to events.jsonl
    with open(events_file, "a") as f:
        f.write(json.dumps(event) + "\n")


def sync_to_github(commit_message: str = "Update events"):
    """
    Sync events to GitHub with git add/commit/push.
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

        # Commit (will fail if nothing to commit, which is fine)
        result = subprocess.run(
            ["git", "commit", "-m", commit_message],
            cwd=repo_dir,
            capture_output=True,
            text=True
        )

        # If commit succeeded, push
        if result.returncode == 0:
            subprocess.run(
                ["git", "push"],
                cwd=repo_dir,
                check=True,
                capture_output=True
            )
            print(f"✅ Synced to GitHub: {commit_message}")
        else:
            # Nothing to commit is not an error
            if "nothing to commit" in result.stdout or "nothing to commit" in result.stderr:
                print("ℹ️  Nothing to commit")
            else:
                print(f"ℹ️  Commit skipped: {result.stderr}")

    except subprocess.CalledProcessError as e:
        # Don't raise error, just log it
        print(f"⚠️  Git sync warning: {e}")
    except Exception as e:
        print(f"⚠️  Git sync warning: {e}")


if __name__ == "__main__":
    # Test the logger
    log_event(
        project="test-project",
        agent="test-agent",
        status="done",
        message="Test event logged successfully",
        artifact="test/path.txt",
        meta={"test": True}
    )
    print("✅ Test event logged to events.jsonl")
