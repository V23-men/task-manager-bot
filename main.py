import json
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# 🔑 ВСТАВЬ СЮДА СВОЙ ТОКЕН
TOKEN = "8506886230:AAFnsWVlKZkPUsw0YO-tWPIvp2zWbTTFqq8"

TASKS_FILE = "tasks.json"


# 📂 Загрузка задач
def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return {}
    with open(TASKS_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


# 💾 Сохранение задач
def save_tasks(tasks):
    with open(TASKS_FILE, "w", encoding="utf-8") as file:
        json.dump(tasks, file, ensure_ascii=False, indent=4)


# 🚀 /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "👋 Привет! Я бот для управления задачами.\n\n"
        "Команды:\n"
        "/add <текст> — добавить задачу\n"
        "/list — список задач\n"
        "/delete <номер> — удалить задачу\n"
        "/clear — очистить всё\n"
        "/help — помощь"
    )
    await update.message.reply_text(text)


# ❓ /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await start(update, context)


# ➕ /add
async def add_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)

    if not update.message.text:
        await update.message.reply_text("❗ Ошибка ввода")
        return

    parts = update.message.text.split(" ", 1)

    if len(parts) < 2:
        await update.message.reply_text("❗ Используй: /add Сделать лабораторную")
        return

    task_text = parts[1]

    tasks = load_tasks()

    if user_id not in tasks:
        tasks[user_id] = []

    tasks[user_id].append(task_text)
    save_tasks(tasks)

    await update.message.reply_text(f"✅ Добавлено: {task_text}")

# 📋 /list
async def list_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    tasks = load_tasks()

    if user_id not in tasks or len(tasks[user_id]) == 0:
        await update.message.reply_text("📭 Список задач пуст.")
        return

    response = "📋 Твои задачи:\n\n"
    for i, task in enumerate(tasks[user_id], start=1):
        response += f"{i}. {task}\n"

    await update.message.reply_text(response)


# ❌ /delete
async def delete_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    tasks = load_tasks()

    if user_id not in tasks or len(tasks[user_id]) == 0:
        await update.message.reply_text("❗ Нет задач для удаления.")
        return

    if not context.args:
        await update.message.reply_text("❗ Используй: /delete 1")
        return

    try:
        index = int(context.args[0]) - 1

        if index < 0 or index >= len(tasks[user_id]):
            await update.message.reply_text("❗ Неверный номер задачи.")
            return

        removed = tasks[user_id].pop(index)
        save_tasks(tasks)

        await update.message.reply_text(f"🗑 Удалено: {removed}")

    except ValueError:
        await update.message.reply_text("❗ Номер должен быть числом.")


# 🧹 /clear
async def clear_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    tasks = load_tasks()

    tasks[user_id] = []
    save_tasks(tasks)

    await update.message.reply_text("🧹 Все задачи удалены.")


# ▶️ Запуск
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("add", add_task))
    app.add_handler(CommandHandler("list", list_tasks))
    app.add_handler(CommandHandler("delete", delete_task))
    app.add_handler(CommandHandler("clear", clear_tasks))

    print("🤖 Бот запущен...")
    app.run_polling()


if __name__ == "__main__":
    main()