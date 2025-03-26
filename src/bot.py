import telebot
import pandas as pd
from Levenshtein import distance
from src.config import settings

# Укажите токен вашего бота
TOKEN = settings.TELEGRAM_BOT_API_TOKEN
bot = telebot.TeleBot(TOKEN)

with open("../ava.jpg", "rb") as photo:
    bot.set_chat_photo(chat_id=bot.get_me().id, photo=photo)

# Загружаем данные из Excel
FILE_PATH = "../Medbotsheets.xlsx"  # Укажите путь к вашему файлу
df = pd.read_excel(FILE_PATH, header=None)

# Преобразуем данные в словарь для быстрого поиска
medications = {row[0].strip().lower(): row[1] for _, row in df.iterrows()}

def find_closest_match(query):
    for title in medications.keys():
        if distance(query, title) <= 2:
            return medications[title]
    return "Извините, информации о данном лекарстве нет в базе."

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Привет! Отправьте мне название лекарства, и я предоставлю вам информацию о нём. Чтобы узнать, инструкции к каким лекарствам есть в базе чат-бота используйте команду /list")

@bot.message_handler(commands=['list'])
def list_medications(message):
    bot.send_message(message.chat.id, "Список лекарств в базе чат-бота:\n" + medications['алфавитный указатель лекарств'])


@bot.message_handler(content_types=['text'])
def send_medication_info(message):
    query = message.text.strip().lower()
    description = find_closest_match(query)
    if description != "алфавитный указатель лекарств":
        bot.send_message(message.chat.id, description)

if __name__ == "__main__":
    bot.polling(none_stop=True)
