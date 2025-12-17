import telebot
import schedule
import time
import json
import random  # Make sure to import the random module
from threading import Thread

# Your bot token from BotFather
bot = telebot.TeleBot("8215582462:AAGVfaUCsgH7b0hhXRGG4-2J7-yMmEjRSuo")

# Your group ID (replace with your actual group ID)
GROUP_ID = "-1003665927824"  # Replace with your actual group ID

# Load questions from the provided JSON file


def load_questions_from_json(file_name):
    with open(file_name, mode="r", encoding="utf-8") as file:
        questions = json.load(file)
    return questions


# Load the questions from the JSON file
questions = load_questions_from_json("FRM P1 All Questions.json")

# Track used questions (question indices or IDs)
used_questions = []


def get_random_question():
    """Selects a random question, ensuring it's not repeated."""
    available_questions = [q for i, q in enumerate(
        questions) if i not in used_questions]
    if not available_questions:
        # Reset used questions if all have been used
        used_questions.clear()
        available_questions = questions

    # This will now work after importing random
    question = random.choice(available_questions)
    question_index = questions.index(question)
    used_questions.append(question_index)

    return question

# Function to format table data as text (for questions with tables)


def format_table_as_text(table_data):
    rows = table_data["rows"]
    headers = table_data["headers"]
    table_text = " | ".join(headers) + "\n"
    for row in rows:
        table_text += " | ".join(row) + "\n"
    return table_text

# Function to send the quiz


def send_daily_quiz():
    question = get_random_question()

    # Prepare options in the correct format for Telegram
    options = [opt["text"] for opt in question["options"]]

    # If the question has a table, format it as text
    if question.get("tableData"):
        table_text = format_table_as_text(question["tableData"])
        # Append table as text to question text
        question["question_text"] += f"\n\n{table_text}"

    # Send the quiz message (no open_period parameter to keep the poll open indefinitely)
    bot.send_poll(
        GROUP_ID,
        question["question_text"],  # The question text
        options,  # Options
        is_anonymous=False,  # Make the poll public
        type="quiz",  # It's a quiz
        correct_option_id=question["options"].index(next(
            # Correct option index
            opt for opt in question["options"] if opt["id"] in question["correct_option_ids"])),
        explanation=question["explanation"]  # Use explanation
        # No open_period specified (the poll will remain open indefinitely)
    )

# Schedule the quiz to send every 4 hours (6 questions per day)


def schedule_quiz_every_4_hours():
    # Send quiz immediately upon startup
    send_daily_quiz()

    # Then send every 4 hours after that
    schedule.every(4).hours.do(send_daily_quiz)


# Start the quiz scheduling loop
schedule_quiz_every_4_hours()

# Keep checking the schedule


def schedule_checker():
    while True:
        schedule.run_pending()
        time.sleep(1)


# Start the scheduler in a separate thread
Thread(target=schedule_checker).start()

# Start the bot polling (to keep the bot active and listening)
bot.polling()
