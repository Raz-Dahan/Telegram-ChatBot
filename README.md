# Telegram Bot for GitHub Actions

This is a Serverless Telegram bot that interacts with GitHub's API. The bot allows you to check the status of a specified workflow in a GitHub repository and trigger the workflow using Telegram commands from any device.

## Prerequisites

Before using this bot, make sure you have the following:

- Python environment with required packages (`telegram`, `requests`).
- Telegram Bot Token (`TELEGRAM_TOKEN`) obtained by creating a bot on Telegram's @botfather.
- GitHub Personal Access Token (`GITHUB_TOKEN`) with `repo` scope access.
- GitHub repository details: owner, repository name, and workflow filename.

## Usage

1. Start a chat with your Telegram bot and use the following commands:
   - `/start`: Get welcome message and usage instructions.
   - `/status`: Check the status of the latest workflow run.
   - `/details`: Gives more information on the latest run.
   - `/run`: Trigger the workflow.
