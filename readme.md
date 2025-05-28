
# HuiTouZaiShuo Telegram To-Do Bot

A private Telegram bot for managing your personal to-do list, designed with role-based access so that only the root user can clear or modify any task. Normal users can add, list, mark done, and view tasks. Data is stored locally on the server for privacy and persistence.

---

## Features

- Add, list, and mark tasks as done
- View unfinished tasks
- Move finished tasks to the end of the list
- Root user can clear all tasks or modify any task
- All task changes are saved to a local text file

---

## Python Environment Setup (Linux Server)

**Recommended: Use Python 3.10 or higher.**

### 1. Check your current Python version

```bash
python3 --version
```

If it's **3.10.x or higher**, you can skip to dependencies below.  
If not, follow these steps:

### 2. Install Python 3.10+ from Source

```bash
# Install dependencies (Ubuntu/Debian)
sudo apt update
sudo apt install -y make build-essential libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
libncurses5-dev libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev git

# Download Python source
cd /usr/local/src
sudo wget https://www.python.org/ftp/python/3.10.13/Python-3.10.13.tgz
sudo tar -xzf Python-3.10.13.tgz
cd Python-3.10.13

# Configure and build
sudo ./configure --enable-optimizations
sudo make
sudo make altinstall

# Check
/usr/local/bin/python3.10 --version
```

### 3. Install pip (if not included)

```bash
/usr/local/bin/python3.10 -m ensurepip --upgrade
```

### 4. Install dependencies

```bash
/usr/local/bin/python3.10 -m pip install python-telegram-bot
```

Or if using your system Python 3.10+:

```bash
pip install python-telegram-bot
```

---

## Bot Setup and Usage

1. **Clone or upload the project files to your server.**

2. **Set your Telegram bot token and your root user ID:**
   - In `HuiTouZaiShuoBot.py`, set:

     ```python
     BOT_TOKEN = 'YOUR_BOT_TOKEN'
     ROOT_USER_ID = YOUR_TELEGRAM_USER_ID  # Example: 12345678
     ```

   - You can get your Telegram user ID by messaging [@userinfobot](https://t.me/userinfobot) in Telegram.

3. **Run the bot:**

   ```bash
   /usr/local/bin/python3.10 HuiTouZaiShuoBot.py
   ```

   Or, if your system python is 3.10+:

   ```bash
   python3 HuiTouZaiShuoBot.py
   ```

---

## Command List

| Command                  | Description                                                   | Root Only?     |
|--------------------------|---------------------------------------------------------------|----------------|
| `/start`                 | Start the bot and get a welcome message                       | No             |
| `/add <task>`            | Add a new to-do item                                          | No             |
| `/list`                  | List all tasks with their status                              | No             |
| `/done <task_number>`    | Mark a specific task as done (with confirmation)              | No             |
| `/refresh`               | Move all finished tasks to the end of the list                | No             |
| `/unfinished`            | List all unfinished tasks                                     | No             |
| `/help`                  | Show the help message                                         | No             |
| `/clear`                 | Clear all tasks                                               | Yes            |
| `/modify <task_number>`  | Modify a specific task (you will be prompted for new content) | Yes            |

---

## Notes

- Only the **root user** (as set in the code) can clear or modify tasks.
- All data is stored locally in `tasks.txt` in the bot's directory.
- If you wish to run the bot in the background, use `nohup`:

  ```bash
  nohup python3 HuiTouZaiShuoBot.py > bot.log 2>&1 &
  ```

---

## Troubleshooting

- **Bot not responding?** Double-check your bot token and your network connection.
- **Python errors?** Ensure you’re running Python 3.10+ and have installed all dependencies.
- **Telegram messages delayed?** Check your server time and timezone settings.

---

## License

This project is for personal use.

---

**Enjoy your organized to-do life with HuiTouZaiShuo Telegram Bot!**
