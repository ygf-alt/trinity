from flask import Flask, request
import telebot
from telebot import types
import logging
import uuid
import sqlite3
import os

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
if not BOT_TOKEN:
    logging.error("Нет TELEGRAM_BOT_TOKEN!")
    exit()

CHANNEL_ID = "@trinity_cryptocult"
DATABASE_URL = 'referrals.db'
bot = telebot.TeleBot(BOT_TOKEN)

# База данных
def create_connection():
    try:
        conn = sqlite3.connect(DATABASE_URL)
        return conn
    except sqlite3.Error as e:
        logging.error(f"Ошибка подключения: {e}")
        return None

def create_table(conn):
    sql = """CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        referral_code TEXT UNIQUE NOT NULL,
        referrer_id INTEGER,
        FOREIGN KEY (referrer_id) REFERENCES users(user_id));"""
    try:
        conn.cursor().execute(sql)
        conn.commit()
    except sqlite3.Error as e:
        logging.error(f"Ошибка таблицы: {e}")

def create_user(conn, user_id):
    referral_code = str(uuid.uuid4())[:8]
    sql = "INSERT OR IGNORE INTO users (user_id, referral_code) VALUES (?, ?)"
    try:
        conn.cursor().execute(sql, (user_id, referral_code))
        conn.commit()
        return referral_code
    except sqlite3.Error as e:
        logging.error(f"Ошибка создания юзера: {e}")
        return None

def get_user(conn, user_id):
    sql = "SELECT * FROM users WHERE user_id = ?"
    try:
        cursor = conn.cursor()
        cursor.execute(sql, (user_id,))
        row = cursor.fetchone()
        if row:
            return {'user_id': row[0], 'referral_code': row[1], 'referrer_id': row[2]}
        return None
    except sqlite3.Error as e:
        logging.error(f"Ошибка получения юзера: {e}")
        return None

def set_referrer(conn, user_id, referral_code):
    sql = "UPDATE users SET referrer_id = (SELECT user_id FROM users WHERE referral_code = ?) WHERE user_id = ? AND referrer_id IS NULL"
    try:
        conn.cursor().execute(sql, (referral_code, user_id))
        conn.commit()
    except sqlite3.Error as e:
        logging.error(f"Ошибка установки реферера: {e}")
def check_subscription(user_id, channel_id):
    try:
        member = bot.get_chat_member(chat_id=channel_id, user_id=user_id)
        return member.status in ("member", "administrator", "creator", "restricted")
    except telebot.apihelper.ApiTelegramException as e:
        logging.error(f"Ошибка проверки подписки: {e}")
        return False
@bot.message_handler(commands=['start', 'referral'])
def start(message):
    conn = create_connection()
    if not conn:
        bot.reply_to(message, "Ошибка базы данных.")
        return
    user_id = message.from_user.id
    user = get_user(conn, user_id)
    if not user:
        referral_code = create_user(conn, user_id)
        if not referral_code:
            bot.reply_to(message, "Ошибка создания пользователя.")
            conn.close()
            return
    else:
        referral_code = user['referral_code']

    if message.text.startswith("/start ") and len(message.text.split()) > 1:
        referrer_code = message.text.split()[1]
        set_referrer(conn, user_id, referrer_code)
    if check_subscription(user_id, CHANNEL_ID):
        keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        keyboard.add("Тестнеты", "NFT", "Ноды", "Мой реферальный код")
        bot.send_message(message.chat.id, "Выберите тему:", reply_markup=keyboard)
    else:
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton("Подписаться", url=f"https://t.me/{CHANNEL_ID[1:]}"))
        bot.send_message(message.chat.id, "Подпишитесь на канал:", reply_markup=keyboard)
    conn.close()
@bot.message_handler(func=lambda m: m.text == "Мой реферальный код")
def show_referral_code(message):
    conn = create_connection()
    user = get_user(conn, message.from_user.id)
    if user:
        bot.reply_to(message, f"Ваша ссылка:\n`https://t.me/{bot.get_me().username}?start={user['referral_code']}`", parse_mode="Markdown")
    conn.close()
@bot.message_handler(func=lambda m: m.text == "Тестнеты")
def handle_testnets(message):
    keyboard = types.InlineKeyboardMarkup()
    links = [
        ("Reddio", "https://t.me/reddiotrinity"),
        ("Monad", "https://t.me/monadtrinity"),
        ("Starknet", "https://t.me/starknettrinity"),
        ("Inertia", "https://t.me/Fakemoney95/96")
        ("MegaETH", "https://t.me/megaETHguide")
        ("KiteAI", "https://t.me/kiteaitriniti")
        ("Fiamma", "https://t.me/Fiammatrinity")
        ("Backpack", "https://t.me/trinitybackpack")
        ("MonadScore", "https://t.me/trinitymonad")
        ("Zenchain", "https://t.me/trinityzenchain")
        ("0GLabs", "https://t.me/trinityOGlabs")
        ("Coresky", "https://t.me/trinitycoresky")
    ]
    for name, url in links:
        keyboard.add(types.InlineKeyboardButton(name, url=url))
    bot.send_message(message.chat.id, "Тестнеты:", reply_markup=keyboard)
@bot.message_handler(func=lambda m: m.text == "NFT")
def handle_nft(message):
    keyboard = types.InlineKeyboardMarkup()
    links = [
        ("Rogues", "https://t.me/Roguestrinity"),
        ("Hama", "https://t.me/Hamatrinity"),
        ("Hollow", "https://t.me/Hollowstrinity"),
        ("Ghibly Lads", "https://t.me/Trinityghibly"),
    ]
    for name, url in links:
        keyboard.add(types.InlineKeyboardButton(name, url=url))
    bot.send_message(message.chat.id, "NFT:", reply_markup=keyboard)

@bot.message_handler(func=lambda m: m.text == "Ноды")
def handle_nodes(message):
    keyboard = types.InlineKeyboardMarkup()
    links = [
        ("Dawn", "https://t.me/Dawnguide"),
        ("PublickAI", "https://t.me/publickAItrinity"),
        ("Bless", "https://t.me/blesstrinity"),
        ("Nodepay", "https://t.me/nodepaytrinity"),
    ]
    for name, url in links:
        keyboard.add(types.InlineKeyboardButton(name, url=url))
    bot.send_message(message.chat.id, "Ноды:", reply_markup=keyboard)


@app.route('/webhook', methods=["POST"])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return '', 200
    else:
        return '', 400


if __name__ == '__main__':
    conn = create_connection()
    if conn:
        create_table(conn)
        conn.close()
    else:
        logging.error("Не удалось подключиться к базе данных при запуске.")
        exit()

    # Установка вебхука
    WEBHOOK_URL = os.environ.get("WEBHOOK_URL", "https://your-app-name.onrender.com")
    bot.remove_webhook()
    bot.set_webhook(url=f"{WEBHOOK_URL}/webhook")
    logging.info(f"Webhook установлен на {WEBHOOK_URL}/webhook")

    # Запуск Flask
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
