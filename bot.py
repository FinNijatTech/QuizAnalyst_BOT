import telebot
import schedule
import time
import json
import random
from threading import Thread

# Your bot token from BotFather
bot = telebot.TeleBot("8523474061:AAHuh_y5Js6dUKx7Z6IAuSZCjIgkxkeQTDA")

# Your group ID (get it using @RawDataBot or group settings)
GROUP_ID = "-1003483742586"  # Replace with your group’s ID

# Load questions from the provided JSON file
with open("FRM P1 Questions.json", "r") as f:
    questions_data = json.load(f)

# Create a list of questions
questions = []
for q in questions_data:
    questions.append({
        "question_text": q["question_text"],
        "options": q["options"],
        "correct_option_ids": q["correct_option_ids"]
    })

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

# Function to send the quiz as a Telegram quiz


def send_daily_quiz():
    question = get_random_question()

    # Prepare options in the correct format for Telegram
    options = [opt['text'] for opt in question["options"]]

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
        explanation=question["explanation"],  # Explanation
        # The time in seconds to keep the poll open (adjust as needed)
        open_period=30
    )


# Schedule the quiz to send every day at 9:00 AM
schedule.every().day.at("17:35").do(send_daily_quiz)

# Keep checking the schedule


def schedule_checker():
    while True:
        schedule.run_pending()
        time.sleep(1)


# Start the scheduler in a separate thread
Thread(target=schedule_checker).start()

# Start the bot polling
bot.polling()
