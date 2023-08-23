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
    update.message.reply_text("Welcome to the GitHub Bot!\nUse /status to get workflow status.\nUse /details to get more details on the run.\nUse /run to run the workflow.")

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

def details(update: Update, context: CallbackContext):
    response = requests.get(
        f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/actions/runs",
        headers={"Authorization": f"Bearer {GITHUB_TOKEN}"}
    )
    runs = response.json()["workflow_runs"]
    latest_run = runs[0]
    started_at = latest_run["created_at"]
    finished_at = latest_run["updated_at"]
    branch = latest_run["head_branch"]
    head_commit = latest_run["head_commit"]["message"]
    sha = latest_run["head_sha"]
    committer = latest_run["head_commit"]["committer"]["name"]
    
    message = (
        f"Started at: {started_at} UTC+0\n"
        f"Finished at: {finished_at} UTC+0\n"
        f"Branch: {branch}\n"
        f"HEAD commit name: {head_commit}\n"
        f"HEAD commit sha: {sha}\n"
        f"Committer: {committer}"
    )
    
    update.message.reply_text(message)

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
        elif command == "/details":
            details(update, None)
        elif command == "/run":
            run(update, None)
        else:
            bot.sendMessage(chat_id=chat_id, text="Unknown command")
    
    return "okay"
