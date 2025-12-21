import telebot
import schedule
import time
import json
import random
import os
from threading import Thread
import pickle

# Your bot token from BotFather
bot = telebot.TeleBot("8215582462:AAGVfaUCsgH7b0hhXRGG4-2J7-yMmEjRSuo")

# Your group ID (replace with your actual group ID)
GROUP_ID = "-1003665927824"  # Replace with your actual group ID

# Load questions from the provided JSON file


def load_questions_from_json(file_name):
    with open(file_name, mode="r", encoding="utf-8") as file:
        data = json.load(file)
        questions = data['questions']  # Access the questions list
    return questions


# Load questions from JSON file
questions = load_questions_from_json("FRM P1 All Questions.json")

# Path for storing used question indices
USED_QUESTIONS_FILE = "used_questions.pkl"

# Load used questions (stored as a set for efficiency)


def load_used_questions():
    if os.path.exists(USED_QUESTIONS_FILE):
        with open(USED_QUESTIONS_FILE, "rb") as f:
            return pickle.load(f)
    else:
        return set()

# Save used questions to a file


def save_used_questions(used_questions):
    with open(USED_QUESTIONS_FILE, "wb") as f:
        pickle.dump(used_questions, f)


# Track used questions as a set for fast lookup and modification
used_questions = load_used_questions()

# Function to get random question ensuring it's not repeated


def get_random_question():
    """Selects a random question, ensuring it's not repeated."""
    available_questions = [q for i, q in enumerate(
        questions) if i not in used_questions]
    if not available_questions:
        # Reset used questions only if all questions have been used
        used_questions.clear()

    question = random.choice(available_questions)
    question_index = questions.index(question)
    used_questions.add(question_index)

    # Save the used questions
    save_used_questions(used_questions)

    return question

# Function to send the quiz


def send_quiz():
    question = get_random_question()

    # Prepare options in the correct format for Telegram
    options = [opt["text"] for opt in question["options"]]

    # Send the quiz message (no open_period, the poll will remain open indefinitely)
    bot.send_poll(
        GROUP_ID,
        question["questionText"],  # The question text
        options,  # Options
        is_anonymous=False,  # Make the poll public
        type="quiz",  # It's a quiz
        correct_option_id=question["options"].index(next(
            # Correct option index
            opt for opt in question["options"] if opt["id"] in question["correctOptionIds"])),
        explanation=question["explanation"]  # Use explanation
    )

# Function to schedule the quiz every 4 hours after the first quiz


def schedule_quiz_every_4_hours():
    # Send quiz immediately upon startup
    send_quiz()

    # Then send every 4 hours after that
    schedule.every(4).hours.do(send_quiz)


# Start the scheduling function
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
