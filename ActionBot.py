import os
import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
REPO_OWNER = "Raz-Dahan"
REPO_NAME = "NASA-gha-pipeline"

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Welcome to the GitHub Bot! Use /status to get workflow status.")

def status(update: Update, context: CallbackContext):
    response = requests.get(
        f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/actions/runs",
        headers={"Authorization": f"Bearer {GITHUB_TOKEN}"}
    )
    runs = response.json()["workflow_runs"]
    latest_run_status = runs[0]["conclusion"]
    update.message.reply_text(f"Last run status: {latest_run_status}")

def main(request):
    updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("status", status))

    updater.start_polling()
    updater.idle()
