import os
import json
import requests
from telegram import Update, Bot
from telegram.ext import Dispatcher, CommandHandler, CallbackContext

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
REPO_OWNER = "Raz-Dahan"
REPO_NAME = "NASA-gha-pipeline"
WORKFLOW = "workflow.yaml"

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Welcome to the GitHub Bot!\nUse /status to get workflow status.\nUse /run to run the workflow.")

def status(update: Update, context: CallbackContext):
    response = requests.get(
        f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/actions/runs",
        headers={"Authorization": f"Bearer {GITHUB_TOKEN}"}
    )
    runs = response.json()["workflow_runs"]
    latest_run = runs[0]
    latest_run_number = latest_run["run_number"]
    latest_run_status = latest_run["conclusion"]
    latest_run_name = latest_run["name"]
    update.message.reply_text(f"The last run was #{latest_run_number} named '{latest_run_name}' ended with {latest_run_status}")

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
    bot = Bot(token=os.environ["TELEGRAM_TOKEN"])
    
    if request.method == "POST":
        update = Update.de_json(request.get_json(force=True), bot)
        chat_id = update.message.chat.id
        command = update.message.text
        
        if command == "/start":
            start(update, None)  # None can be passed as the context for simplicity
        elif command == "/status":
            status(update, None)
        elif command == "/run":
            run(update, None)
        else:
            bot.sendMessage(chat_id=chat_id, text="Unknown command")
    
    return "okay"
