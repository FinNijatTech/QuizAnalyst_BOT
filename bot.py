import telebot
import schedule
import time
import csv
import random
import json
from threading import Thread

# Your bot token from BotFather
bot = telebot.TeleBot("8215582462:AAGVfaUCsgH7b0hhXRGG4-2J7-yMmEjRSuo")

# Your group ID (replace with your actual group ID)
GROUP_ID = "-1003665927824"  # Replace with your actual group ID

# Load questions from the provided CSV file


def load_questions_from_csv(file_name):
    questions = []
    with open(file_name, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Parse the options and correct_option_ids (both stored in JSON-like format in CSV)
            # Convert the JSON string to a list
            options = json.loads(row["options"])
            # Same for correct_option_ids
            correct_option_ids = json.loads(row["correct_option_ids"])

            question = {
                "question_text": row["question_text"],
                "options": options,
                "correct_option_ids": correct_option_ids,
                # Directly taken from the CSV
                "explanation": row["explanation"]
            }
            questions.append(question)
    return questions


# Load the questions from the CSV file
questions = load_questions_from_csv("FRM P1 Questions.csv")

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

    question = random.choice(available_questions)
    question_index = questions.index(question)
    used_questions.append(question_index)

    return question

# Function to send the daily quiz


def send_daily_quiz():
    question = get_random_question()

    # Prepare options in the correct format for Telegram
    options = [opt["text"] for opt in question["options"]]

    # Send the quiz message
    bot.send_poll(
        GROUP_ID,
        question["question_text"],  # The question text
        options,  # Options
        is_anonymous=False,  # Make the poll public
        type="quiz",  # It's a quiz
        correct_option_id=question["options"].index(next(
            # Correct option index
            opt for opt in question["options"] if opt["id"] in question["correct_option_ids"])),
        explanation=question["explanation"],  # Use explanation
        # The time in seconds to keep the poll open (adjust as needed)
        open_period=30
    )


# Schedule the quiz to send every day at 9:00 AM (adjust time as needed)
schedule.every().day.at("17:47").do(send_daily_quiz)

# Keep checking the schedule


def schedule_checker():
    while True:
        schedule.run_pending()
        time.sleep(1)


# Start the scheduler in a separate thread
Thread(target=schedule_checker).start()

# Start the bot polling
bot.polling()
