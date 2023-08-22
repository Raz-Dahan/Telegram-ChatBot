import os
import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
REPO_OWNER = "Raz-Dahan"
REPO_NAME = "NASA-gha-pipeline"
WORKFLOW="workflow.yaml"

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Welcome to the GitHub Bot! Use /status to get workflow status.")

def status(update: Update, context: CallbackContext):
    response = requests.get(
        f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/actions/runs",
        headers={"Authorization": f"Bearer {GITHUB_TOKEN}"}
    )
    runs = response.json()["workflow_runs"]
    latest_run = runs[0]
    latest_run_number = latest_run["run_number"]
    latest_run_status = latest_run["conclusion"]
    latest_run_name = latest_run["display_title"]
    update.message.reply_text(f"Last run #{latest_run_number} - {latest_run_name} status: {latest_run_status}")

def run(update: Update, context: CallbackContext):
    response = requests.post(
        f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/actions/workflows/{WORKFLOW}/dispatches",
        headers={
            "Authorization": f"Bearer {GITHUB_TOKEN}",
            "Accept": "application/vnd.github.v3+json"
        },
        json={"ref": "main"}
    )
    if response.status_code == 204:
        update.message.reply_text("Workflow has been triggered successfully.")
    else:
        update.message.reply_text("Failed to trigger the workflow.")

def main(request):
    updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("status", status))
    dispatcher.add_handler(CommandHandler("run", run))

    updater.start_polling()
    updater.idle()
