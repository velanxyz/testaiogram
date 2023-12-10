import logging
import random
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram.utils import executor

API_TOKEN = 'TOKEN'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

questions = [
    {
        "text": "Как вы относитесь к призиденту России?",
        "options": ["A. положительно", "B. выше среднего", "C. ниже среднего", "D. отрицательно"],
        "correct_option": "A"
    },
    {
        "text": "Язык программирования для шизов?",
        "options": ["A. Java", "B. Python", "C. C++", "D. JavaScript"],
        "correct_option": "B"
    },
    {
        "text": "Можно ли просто не прийти на пару физры",
        "options": ["A. Нельзя", "B. Только по уважительной причине", "C. Только с другом", "D. Да"],
        "correct_option": "C"
    },
    {
        "text": "Можно ли не приходить на код будущего",
        "options": ["A. Нет", "Только по уважительной причине", "C. Только с другом", "D. Да"],
        "correct_option": "B"
    },
    {
        "text": "Мне поставят 12 за дз?",
        "options": ["A. Да", "B. Только если ты все сделал", "C. За 100 рублей", "D. Нет"],
        "correct_option": "A"
    }
]

user_scores = {}
random.shuffle(questions)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    user_id = message.from_user.id
    user_scores[user_id] = 0
    await message.reply("Привет! Давай начнем викторину. Напиши /quiz, чтобы получить первый вопрос.")


@dp.message_handler(commands=['quiz'])
async def quiz(message: types.Message):
    user_id = message.from_user.id
    if user_id not in user_scores:
        user_scores[user_id] = 0

    question = questions.pop(0)
    question_text = question["text"]
    options = question["options"]
    correct_option = question["correct_option"]

    keyboard = types.InlineKeyboardMarkup()
    for option in options:
        keyboard.add(types.InlineKeyboardButton(text=option, callback_data=option))

    await message.reply(question_text, reply_markup=keyboard)


@dp.callback_query_handler(lambda c: True)
async def process_callback(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    selected_option = callback_query.data
    question = next(q for q in questions if selected_option in q["options"])

    if selected_option == question["correct_option"]:
        user_scores[user_id] += 1

    await bot.send_message(user_id, f"Твой выбор: {selected_option}\n"
                                      f"Правильный ответ: {question['correct_option']}")
    if questions:
        await bot.send_message(user_id, "Напиши /quiz, чтобы продолжить викторину.")
    else:
        await bot.send_message(user_id, f"Викторина завершена! Твой счет: {user_scores[user_id]}")

if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
