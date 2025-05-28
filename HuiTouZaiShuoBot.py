import logging
import os
from datetime import datetime
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telegram.error import TelegramError
from dotenv import load_dotenv # type: ignore


# Logging configuration
LOG_FILE = "bot_requests.log"
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# Helper function to log requests
def log_request(update: Update, command: str, response: str):
    user_id = update.effective_user.id if update.effective_user else "unknown"
    user_name = update.effective_user.username if update.effective_user else "unknown"
    msg = f"Request: {command} | UserID: {user_id} | Username: {user_name} | Response: {response}"
    logging.info(msg)

tasks = []
confirmation_tasks = {}
modification_tasks = {}

TASKS_FILE = "tasks.txt"

 # Function: save_tasks
 # Usage: Saves current tasks to the local file
 # Parameters: None
 # Creation Date: 2025-05-26
 # Author: Michael
 # Modification Date: 2025-05-26
def save_tasks():
    with open(TASKS_FILE, "w", encoding="utf-8") as f:
        for i, task in enumerate(tasks, 1):
            line = f"{i}|{task['task']}|{'done' if task['done'] else 'todo'}|{task['date_added']}|{task['date_done'] or ''}"
            f.write(line + "\n")

 # Function: load_tasks
 # Usage: Loads tasks from the local file into memory
 # Parameters: None
 # Creation Date: 2025-05-26
 # Author: Michael
 # Modification Date: 2025-05-26
def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return
    with open(TASKS_FILE, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split("|")
            if len(parts) != 5:
                continue
            tasks.append({
                "task": parts[1],
                "done": parts[2] == "done",
                "date_added": parts[3],
                "date_done": parts[4] if parts[4] else None
            })

load_tasks()

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
ROOT_USER_ID = int(os.getenv("ROOT_USER_ID"))
if not BOT_TOKEN or not ROOT_USER_ID:
    raise RuntimeError("BOT_TOKEN and ROOT_USER_ID must be set in the .env file!")

 # Function: is_root_user
 # Usage: Checks if the user is the root user
 # Parameters: update (telegram.Update)
 # Creation Date: 2025-05-26
 # Author: Michael
 # Modification Date: 2025-05-26
def is_root_user(update: Update) -> bool:
    return update.effective_user.id == ROOT_USER_ID

 # Function: start
 # Usage: Sends a welcome message when the bot is started
 # Parameters: update (telegram.Update), context (telegram.ext.ContextTypes.DEFAULT_TYPE)
 # Creation Date: 2025-05-26
 # Author: Michael
 # Modification Date: 2025-05-26
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response = 'Hello! I am a private bot for Melody who is a gorgeous lady.'
    await update.message.reply_text(response)
    log_request(update, "/start", response)

 # Function: add_task
 # Usage: Adds a new task to the task list
 # Parameters: update (telegram.Update), context (telegram.ext.ContextTypes.DEFAULT_TYPE)
 # Creation Date: 2025-05-26
 # Author: Michael
 # Modification Date: 2025-05-26
async def add_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        response = "Please provide a task to add. Usage: /add <task>"
        await update.message.reply_text(response)
        log_request(update, "/add", response)
        return
    task_text = " ".join(context.args)
    date_added = datetime.now().strftime("%Y-%m-%d %H:%M")
    tasks.append({"task": task_text, "done": False, "date_added": date_added, "date_done": None})
    save_tasks()
    response = f"Added task: {task_text} (added on {date_added})"
    await update.message.reply_text(response)
    log_request(update, "/add", response)

 # Function: list_tasks
 # Usage: Lists all tasks with their status
 # Parameters: update (telegram.Update), context (telegram.ext.ContextTypes.DEFAULT_TYPE)
 # Creation Date: 2025-05-26
 # Author: Michael
 # Modification Date: 2025-05-26
async def list_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not tasks:
        response = "Your to-do list is empty."
        await update.message.reply_text(response)
        log_request(update, "/list", response)
        return
    reply = "Your tasks:\n"
    for i, task in enumerate(tasks, 1):
        status = "✅" if task["done"] else "⭕"
        date_done = f" (done on {task['date_done'].split()[0]})" if task["done"] and task["date_done"] else ""
        reply += f"{i}. {status} {task['task']} (added on {task['date_added'].split()[0]}){date_done}\n"
    await update.message.reply_text(reply)
    log_request(update, "/list", reply)

 # Function: clear_tasks
 # Usage: Clears all tasks from the list (root only)
 # Parameters: update (telegram.Update), context (telegram.ext.ContextTypes.DEFAULT_TYPE)
 # Creation Date: 2025-05-26
 # Author: Michael
 # Modification Date: 2025-05-26
async def clear_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_root_user(update):
        response = "Unauthorized. Only the root user can clear the list."
        await update.message.reply_text(response)
        log_request(update, "/clear", response)
        return
    tasks.clear()
    save_tasks()
    response = "All tasks have been cleared."
    await update.message.reply_text(response)
    log_request(update, "/clear", response)

 # Function: help_command
 # Usage: Shows the help message with available commands
 # Parameters: update (telegram.Update), context (telegram.ext.ContextTypes.DEFAULT_TYPE)
 # Creation Date: 2025-05-26
 # Author: Michael
 # Modification Date: 2025-05-26
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    root = is_root_user(update)
    help_lines = [
        "Here are the commands you can use:",
        "/start - Start the bot",
        "/add <task> - Add a new task",
        "/list - Show all tasks",
        "/done <task_number> - Mark a task as done",
    ]
    if root:
        help_lines.append("/clear - Clear all tasks (root only)")
        help_lines.append("/modify <task_number> - Modify a specific task (root only)")
    help_lines += [
        "/refresh - Move completed tasks to the end and show number of pending tasks",
        "/unfinished - Show only unfinished tasks",
        "/help - Show this help message"
    ]
    help_text = "\n".join(help_lines)
    await update.message.reply_text(help_text)
    log_request(update, "/help", help_text)

 # Function: mark_done
 # Usage: Initiates marking a task as done with confirmation
 # Parameters: update (telegram.Update), context (telegram.ext.ContextTypes.DEFAULT_TYPE)
 # Creation Date: 2025-05-26
 # Author: Michael
 # Modification Date: 2025-05-26
async def mark_done(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args or not context.args[0].isdigit():
        response = "Please provide a valid task number. Usage: /done <task_number>"
        await update.message.reply_text(response)
        log_request(update, "/done", response)
        return
    task_index = int(context.args[0]) - 1
    if task_index < 0 or task_index >= len(tasks):
        response = "Invalid task number."
        await update.message.reply_text(response)
        log_request(update, "/done", response)
        return
    if tasks[task_index]["done"]:
        response = "This task is already marked as done."
        await update.message.reply_text(response)
        log_request(update, "/done", response)
        return

    confirmation_tasks[update.effective_user.id] = task_index
    reply_markup = ReplyKeyboardMarkup([["Yes", "No"]], one_time_keyboard=True, resize_keyboard=True)
    response = f"Are you sure you want to mark task {context.args[0]} as done?\n\n\"{tasks[task_index]['task']}\""
    await update.message.reply_text(
        response,
        reply_markup=reply_markup
    )
    log_request(update, "/done", response)

 # Function: handle_confirmation
 # Usage: Handles user confirmation for marking a task as done
 # Parameters: update (telegram.Update), context (telegram.ext.ContextTypes.DEFAULT_TYPE)
 # Creation Date: 2025-05-26
 # Author: Michael
 # Modification Date: 2025-05-26
async def handle_confirmation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    # Handle modification for root user
    if user_id in modification_tasks:
        task_index = modification_tasks[user_id]
        new_content = update.message.text.strip()
        tasks[task_index]["task"] = new_content
        save_tasks()
        response = f"Task {task_index + 1} has been updated."
        await update.message.reply_text(response)
        log_request(update, "/modify", response)
        del modification_tasks[user_id]
        return

    if user_id not in confirmation_tasks:
        return
    task_index = confirmation_tasks[user_id]
    if update.message.text.lower() == "yes":
        tasks[task_index]["done"] = True
        tasks[task_index]["date_done"] = datetime.now().strftime("%Y-%m-%d %H:%M")
        save_tasks()
        response = f"Task {task_index + 1} has been marked as done."
        await update.message.reply_text(response)
        log_request(update, "/done", response)
    else:
        response = "Operation cancelled."
        await update.message.reply_text(response)
        log_request(update, "/done", response)
    del confirmation_tasks[user_id]

 # Function: refresh_tasks
 # Usage: Moves completed tasks to the end and shows number of pending tasks
 # Parameters: update (telegram.Update), context (telegram.ext.ContextTypes.DEFAULT_TYPE)
 # Creation Date: 2025-05-26
 # Author: Michael
 # Modification Date: 2025-05-26
async def refresh_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global tasks
    # Separate not done and done tasks
    not_done_tasks = [t for t in tasks if not t["done"]]
    done_tasks = [t for t in tasks if t["done"]]
    tasks = not_done_tasks + done_tasks
    save_tasks()
    response = f"Refreshed task list. You have {len(not_done_tasks)} unfinished tasks."
    await update.message.reply_text(response)
    log_request(update, "/refresh", response)

 # Function: show_unfinished
 # Usage: Shows only unfinished (not done) tasks
 # Parameters: update (telegram.Update), context (telegram.ext.ContextTypes.DEFAULT_TYPE)
 # Creation Date: 2025-05-26
 # Author: Michael
 # Modification Date: 2025-05-26
async def show_unfinished(update: Update, context: ContextTypes.DEFAULT_TYPE):
    unfinished = [t for t in tasks if not t["done"]]
    if not unfinished:
        response = "You have no unfinished tasks."
        await update.message.reply_text(response)
        log_request(update, "/unfinished", response)
        return
    reply = "Unfinished tasks:\n"
    for i, task in enumerate(unfinished, 1):
        reply += f"{i}. ⭕ {task['task']} (added on {task['date_added'].split()[0]})\n"
    await update.message.reply_text(reply)
    log_request(update, "/unfinished", reply)

 # Function: modify_task
 # Usage: Modify the content of a task (root only). If new content is not provided, prompt for it.
 # Parameters: update (telegram.Update), context (telegram.ext.ContextTypes.DEFAULT_TYPE)
 # Creation Date: 2025-05-28
 # Author: Michael
 # Modification Date: 2025-05-28
async def modify_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_root_user(update):
        response = "Unauthorized. Only the root user can modify tasks."
        await update.message.reply_text(response)
        log_request(update, "/modify", response)
        return
    user_id = update.effective_user.id
    if not context.args or not context.args[0].isdigit():
        response = "Usage: /modify <task_number>"
        await update.message.reply_text(response)
        log_request(update, "/modify", response)
        return
    task_index = int(context.args[0]) - 1
    if task_index < 0 or task_index >= len(tasks):
        response = "Invalid task number."
        await update.message.reply_text(response)
        log_request(update, "/modify", response)
        return
    # If only task_number provided, prompt for new content
    if len(context.args) == 1:
        response = f"Please enter the new content for task {context.args[0]}."
        modification_tasks[user_id] = task_index
        await update.message.reply_text(response)
        log_request(update, "/modify", response)
        return
    # If both task_number and new content provided, update immediately
    new_content = " ".join(context.args[1:])
    tasks[task_index]["task"] = new_content
    save_tasks()
    response = f"Task {task_index + 1} has been updated."
    await update.message.reply_text(response)
    log_request(update, "/modify", response)

from telegram.ext import MessageHandler, filters

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("add", add_task))
app.add_handler(CommandHandler("list", list_tasks))
app.add_handler(CommandHandler("clear", clear_tasks))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CommandHandler("done", mark_done))
app.add_handler(CommandHandler("refresh", refresh_tasks))
app.add_handler(CommandHandler("unfinished", show_unfinished))
app.add_handler(CommandHandler("modify", modify_task))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_confirmation))

# Function: error_handler
# Usage: Handles errors and exceptions globally for the bot, logs them in a concise format
# Parameters: update, context
# Creation Date: 2025-05-28
# Author: Michael
# Modification Date: 2025-05-28
async def error_handler(update, context):
    user_id = update.effective_user.id if update and update.effective_user else "unknown"
    user_name = update.effective_user.username if update and update.effective_user else "unknown"
    logging.error(f"Error occurred for user {user_id} ({user_name}): {context.error}")

app.add_error_handler(error_handler)
app.run_polling()