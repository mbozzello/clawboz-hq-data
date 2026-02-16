# ClawBoz HQ Data

This repository contains event logs and project data for the ClawBoz headquarters.

## Files

- **events.jsonl**: JSON Lines file containing timestamped event logs
- **projects.json**: JSON file containing project metadata
- **logger.py**: Python utilities for logging events and syncing to GitHub

## Usage

```python
from logger import log_event, sync_to_github

# Log an event
log_event(
    project="my-project",
    agent="agent-name",
    status="completed",
    message="Task completed successfully",
    artifact="path/to/artifact",
    meta={"key": "value"}
)

# Sync changes to GitHub
sync_to_github(commit_message="Update events")
```

## Important: Public-Safe Events Only

⚠️ **All events logged to this repository must be public-safe.**

Do not log:
- Sensitive credentials or API keys
- Personal identifiable information (PII)
- Private business data
- Security-sensitive information
- Internal system details that could pose security risks

This repository may be shared publicly, so ensure all logged events are appropriate for public visibility.
