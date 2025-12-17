import telebot
import schedule
import time
from threading import Thread

# Your bot token from BotFather
# Replace with your bot token
bot = telebot.TeleBot("8523474061:AAHuh_y5Js6dUKx7Z6IAuSZCjIgkxkeQTDA")


# Your group ID (get it using @RawDataBot or group settings)
GROUP_ID = "-1003483742586"  # Replace with your group’s ID

# Sample quiz questions
quiz_questions = [
    {"q": "What is 2+2?", "a": "4"},
    {"q": "Capital of France?", "a": "Paris"},
    # Add more questions as needed
]

# Function to send the quiz


def send_daily_quiz():
    question = quiz_questions[0]  # You can rotate through questions
    bot.send_message(GROUP_ID, f"📚 **Daily Quiz!**\n\n{question['q']}")


# Schedule the quiz to send every day at 9:00 AM
schedule.every().day.at("09:00").do(send_daily_quiz)

# Keep checking the schedule


def schedule_checker():
    while True:
        schedule.run_pending()
        time.sleep(1)


# Start the scheduler in a separate thread
Thread(target=schedule_checker).start()

# Start the bot polling
bot.polling()
