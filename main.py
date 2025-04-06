import telebot
from telebot import types
import logging

# Включаем логирование
logging.basicConfig(level=logging.DEBUG)

BOT_TOKEN = "8147871272:AAEC_BLtdi_DEKvgL7rh5Xpn6qiVLB0A8GY"
CHANNEL_ID = "@trinity_cryptocult"

bot = telebot.TeleBot(BOT_TOKEN)

def check_subscription(user_id, channel_id):
    try:
        member = bot.get_chat_member(chat_id=channel_id, user_id=user_id)
        logging.debug(f"Статус участника: {member.status}")
        return member.status in ("member", "administrator", "creator", "restricted")
    except telebot.apihelper.ApiTelegramException as e:
        logging.error(f"Ошибка при проверке подписки: {e}")
        if e.description == "User not found":
            return False
        elif e.description == "Bad Request: chat not found":
            logging.error("Канал не найден. Проверьте CHANNEL_ID.")
            return False
        elif e.description == "Forbidden: bot was blocked by the user":
            logging.warning(f"Пользователь {user_id} заблокировал бота.")
            return False # Или обработайте как-то иначе
        else:
            logging.error(f"Неизвестная ошибка: {e}")
            return False

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    try:
        is_subscribed = check_subscription(user_id, CHANNEL_ID)

        if is_subscribed:
            # Создаем клавиатуру с основными кнопками
            keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
            button1 = types.KeyboardButton("Тестнеты")
            button2 = types.KeyboardButton("NFT")
            button3 = types.KeyboardButton("Ноды")
            keyboard.add(button1, button2, button3)

            bot.send_message(message.chat.id, "Выберите интересующую вас тему:", reply_markup=keyboard)
        else:
            keyboard = types.InlineKeyboardMarkup()
            url_button = types.InlineKeyboardButton(text="Подписаться на канал", url=f"https://t.me/{CHANNEL_ID[1:]}")
            keyboard.add(url_button)
            bot.send_message(message.chat.id, "Пожалуйста, подпишитесь на канал, чтобы продолжить.", reply_markup=keyboard)
    except Exception as e:
        logging.exception("Ошибка в обработчике /start") # Запишет полную трассировку

# Обработчики для кнопок (пример)
@bot.message_handler(func=lambda message: message.text == "Тестнеты")
def handle_testnets(message):
    # Создаем inline-клавиатуру со ссылками на каналы про тестнеты
    inline_keyboard = types.InlineKeyboardMarkup()
    testnet_channel1 = types.InlineKeyboardButton("Reddio", url="https://t.me/reddiotrinity")
    testnet_channel2 = types.InlineKeyboardButton("Monad", url="https://t.me/monadtrinity")
    testnet_channel2 = types.InlineKeyboardButton("Sahara", url="https://t.me/SaharaTrinity")
    testnet_channel3 = types.InlineKeyboardButton("Inertia", url="https://t.me/Fakemoney95/96")
    testnet_channel4 = types.InlineKeyboardButton("MegaETH", url="https://t.me/megaETHguide")
    testnet_channel5 = types.InlineKeyboardButton("KiteAI", url="https://t.me/kiteaitriniti")
    testnet_channel6 = types.InlineKeyboardButton("Fiamma", url="https://t.me/Fiammatrinity")
    testnet_channel7 = types.InlineKeyboardButton("Backpack", url="https://t.me/trinitybackpack")
    testnet_channel8 = types.InlineKeyboardButton("MonadScore", url="https://t.me/trinitymonad")
    testnet_channel9 = types.InlineKeyboardButton("Zenchain", url="https://t.me/trinityzenchain")
    testnet_channel10 = types.InlineKeyboardButton("0GLabs", url="https://t.me/trinityOGlabs")
    testnet_channel11 = types.InlineKeyboardButton("Coresky", url="https://t.me/trinitycoresky")
    inline_keyboard.add(testnet_channel1, testnet_channel2, testnet_channel3, testnet_channel4, testnet_channel5, testnet_channel6, testnet_channel7, testnet_channel8, testnet_channel9, testnet_channel10, testnet_channel11)

    bot.send_message(message.chat.id, "Лови тестнеты:", reply_markup=inline_keyboard)

@bot.message_handler(func=lambda message: message.text == "NFT")
def handle_nft(message):
    # Аналогично для NFT, создайте inline-клавиатуру со ссылками на каналы про NFT
    inline_keyboard = types.InlineKeyboardMarkup()
    nft_channel1 = types.InlineKeyboardButton("Rogues", url="https://t.me/Roguestrinity")
    nft_channel2 = types.InlineKeyboardButton("Hama", url="https://t.me/Hamatrinity")
    nft_channel3 = types.InlineKeyboardButton("Hollow", url="https://t.me/Hollowstrinity")
    nft_channel4 = types.InlineKeyboardButton("Ghibly Lads", url="https://t.me/Trinityghibly")
    inline_keyboard.add(nft_channel1, nft_channel2, nft_channel3, nft_channel4)

    bot.send_message(message.chat.id, "Апкаминг NFT:", reply_markup=inline_keyboard)

@bot.message_handler(func=lambda message: message.text == "Ноды")
def handle_nodes(message):
    # Аналогично для Нод, создайте inline-клавиатуру со ссылками на каналы про Ноды
    inline_keyboard = types.InlineKeyboardMarkup()
    node_channel1 = types.InlineKeyboardButton("Dawn", url="https://t.me/Dawnguide")
    node_channel2 = types.InlineKeyboardButton("PublickAI", url="https://t.me/publickAItrinity")
    node_channel3 = types.InlineKeyboardButton("Bless", url="https://t.me/blesstrinity")
    node_channel4 = types.InlineKeyboardButton("Nodepay", url="https://t.me/nodepaytrinity")
    inline_keyboard.add(node_channel1, node_channel2, node_channel3,node_channel4)

    bot.send_message(message.chat.id, "Несколько Нод:", reply_markup=inline_keyboard)



bot.infinity_polling()