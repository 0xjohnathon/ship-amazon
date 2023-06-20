import requests
from telegram.ext import Updater, CommandHandler
from telegram import ParseMode

# Замените YOUR_TELEGRAM_TOKEN на ваш токен Telegram Bot API
telegram_token = "YOUR_TELEGRAM_TOKEN"

# Замените YOUR_AMAZON_API_URL на URL Amazon API
amazon_api_url = "YOUR_AMAZON_API_URL"

def get_product_info(update, context):
    # Получаем аргументы команды
    args = context.args
    if len(args) < 1:
        update.message.reply_text("Использование: /product <ASIN>")
        return

    asin = args[0]

    # Создаем URL-запрос к Amazon API
    url = f"{amazon_api_url}/products/{asin}"

    # Отправляем запрос и получаем ответ
    response = requests.get(url)
    data = response.json()

    if "error" in data:
        update.message.reply_text("Ошибка при получении информации о товаре.")
        return

    # Получаем информацию о товаре
    product_title = data["title"]
    product_price = data["price"]
    product_image = data["image"]

    # Отправляем информацию о товаре в чат
    message = f"<b>{product_title}</b>\n\n" \
              f"Цена: {product_price} USD\n\n" \
              f"<a href='{product_image}'>Ссылка на изображение</a>"

    update.message.reply_text(message, parse_mode=ParseMode.HTML)

def start(update, context):
    update.message.reply_text("Привет! Я бот для отслеживания товаров на Amazon. " \
                              "Для получения информации о товаре используйте команду /product <ASIN>.")

def main():
    bot = Updater(token=telegram_token, use_context=True)

    dp = bot.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("product", get_product_info))

    bot.start_polling()
    bot.idle()

if __name__ == "__main__":
    main()
