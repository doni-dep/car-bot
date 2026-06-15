import os
import random
import datetime
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, CallbackQueryHandler, filters

# Токен из переменной окружения (для Render)
TOKEN = os.getenv("8640511619:AAF5SOEOJcFKaOkIYYOHqD7P_0eK6-hJ494")

# ВАШИ ПЛАТЁЖНЫЕ ДАННЫЕ
PAYMENT_NUMBER = "0507 065 255"
PAYMENT_NAME = "PREMIUM AUTO"
BANK_NAME = "О!Деньги"

# ГЛАВНОЕ МЕНЮ
MAIN_KEYBOARD = [
    ["🏎️ LAMBORGHINI", "🐎 FERRARI"],
    ["⚡ PORSCHE", "🧡 McLAREN"],
    ["🚙 LEXUS", "🎲 КОЛЕСО ФОРТУНЫ"],
    ["💰 КРЕДИТ 0%", "🔄 ТЕСТ-ДРАЙВ VIP"],
    ["📊 СУПЕР СРАВНЕНИЕ", "🎁 АКЦИИ ДНЯ"],
    ["⭐ ОТЗЫВЫ", "🎮 ВИКТОРИНА"],
    ["📍 КАРТА", "📞 КОНТАКТЫ"],
    ["🏪 О НАС", "💳 ОПЛАТА"],
]

main_reply_markup = ReplyKeyboardMarkup(MAIN_KEYBOARD, resize_keyboard=True)

# ДАННЫЕ МАШИН
car_info = {
    "🏎️ LAMBORGHINI": {
        "name": "Lamborghini Revuelto",
        "speed": "350 км/ч",
        "acceleration": "2.5 сек",
        "price": "$1 200 000",
        "price_rub": "108 000 000 ₽",
        "price_kgs": "106 000 000 сом",
        "rating": "10/10",
        "engine": "V12 + 3 электромотора, 1015 л.с.",
        "color": "Жёлтый, Оранжевый, Зелёный",
        "warranty": "3 года / 100 000 км",
        "country": "Италия 🇮🇹",
        "bonus": "VIP обслуживание + Страховка в подарок"
    },
    "🐎 FERRARI": {
        "name": "Ferrari SF90 Stradale",
        "speed": "340 км/ч",
        "acceleration": "2.5 сек",
        "price": "$850 000",
        "price_rub": "76 500 000 ₽",
        "price_kgs": "75 000 000 сом",
        "rating": "9.8/10",
        "engine": "V8 + 3 электромотора, 1000 л.с.",
        "color": "Красный, Жёлтый, Синий",
        "warranty": "3 года / 100 000 км",
        "country": "Италия 🇮🇹",
        "bonus": "Экскурсия на завод Ferrari"
    },
    "⚡ PORSCHE": {
        "name": "Porsche 911 Turbo S",
        "speed": "330 км/ч",
        "acceleration": "2.6 сек",
        "price": "$300 000",
        "price_rub": "27 000 000 ₽",
        "price_kgs": "26 500 000 сом",
        "rating": "9.5/10",
        "engine": "V6, 650 л.с.",
        "color": "Серебристый, Чёрный, Синий",
        "warranty": "3 года / 100 000 км",
        "country": "Германия 🇩🇪",
        "bonus": "Зарядная станция в подарок"
    },
    "🧡 McLAREN": {
        "name": "McLaren Artura",
        "speed": "420 км/ч",
        "acceleration": "2.7 сек",
        "price": "$900 000",
        "price_rub": "81 000 000 ₽",
        "price_kgs": "79 500 000 сом",
        "rating": "9.7/10",
        "engine": "V6 + гибрид, 680 л.с.",
        "color": "Оранжевый, Чёрный, Серебристый",
        "warranty": "3 года / 100 000 км",
        "country": "Великобритания 🇬🇧",
        "bonus": "Мерч McLaren на $5000"
    },
    "🚙 LEXUS": {
        "name": "Lexus LC 500",
        "speed": "270 км/ч",
        "acceleration": "4.4 сек",
        "price": "$120 000",
        "price_rub": "10 800 000 ₽",
        "price_kgs": "10 600 000 сом",
        "rating": "9.0/10",
        "engine": "V8, 477 л.с.",
        "color": "Белый, Чёрный, Серебристый",
        "warranty": "4 года / 120 000 км",
        "country": "Япония 🇯🇵",
        "bonus": "Поездка в Японию"
    }
}

# ПРИЗЫ
fortune_prizes = [
    "🏆 Скидка 10% на любую машину!",
    "🎁 Бесплатное ТО на год!",
    "💰 $1000 на обслуживание!",
    "🧥 Брендированная куртка!",
    "🏎️ VIP тест-драйв!",
    "🍾 Шампанское в подарок!"
]

# ВОПРОСЫ ДЛЯ ВИКТОРИНЫ
quiz_questions = [
    {"q": "Какая машина разгоняется до 100 за 2.5 сек?", "a": "Lamborghini"},
    {"q": "Какая машина самая быстрая (420 км/ч)?", "a": "McLaren"},
    {"q": "Где производят Ferrari?", "a": "Италия"},
]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.effective_user.first_name
    await update.message.reply_text(
        f"👑 ДОБРО ПОЖАЛОВАТЬ В PREMIUM AUTO! 👑\n\n"
        f"✨ Привет, {name}! ✨\n\n"
        "🏆 ЛУЧШИЙ АВТОСАЛОН 2025\n"
        "🌟 РЕЙТИНГ: 10/10\n\n"
        "👇 ВЫБЕРИТЕ РАЗДЕЛ:",
        reply_markup=main_reply_markup
    )


async def cars(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text in car_info:
        car = car_info[text]
        keyboard = [
            [InlineKeyboardButton("💳 ОПЛАТИТЬ ОНЛАЙН", callback_data=f"pay_{text}")],
            [InlineKeyboardButton("🏦 КУПИТЬ В КРЕДИТ", callback_data=f"credit_{text}")],
            [InlineKeyboardButton("🏎️ ЗАПИСАТЬСЯ", callback_data=f"test_{text}")]
        ]
        msg = f"""🏎️ **{car['name']}**
🚀 Скорость: {car['speed']}
⚡ Разгон: {car['acceleration']}
🔧 Двигатель: {car['engine']}
⭐ Рейтинг: {car['rating']}
🌍 Страна: {car['country']}

💰 ЦЕНА: {car['price']} USD / {car['price_kgs']}
🎁 БОНУС: {car['bonus']}"""
        await update.message.reply_text(msg, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')
        return

    if text == "🎲 КОЛЕСО ФОРТУНЫ":
        await update.message.reply_text(f"🎡 ВАШ ПРИЗ: {random.choice(fortune_prizes)}", reply_markup=main_reply_markup)
        return

    if text == "💳 ОПЛАТА":
        await show_payment(update)
        return

    await update.message.reply_text("Используйте кнопки меню!", reply_markup=main_reply_markup)


async def show_payment(update=None, query=None, car_name=None, car_price=None):
    text = f"""💳 ОПЛАТА ЧЕРЕЗ О!ДЕНЬГИ

🏦 БАНК: О!Деньги / Халык Банк
📞 НОМЕР: {PAYMENT_NUMBER}
👤 ПОЛУЧАТЕЛЬ: {PAYMENT_NAME}

💳 НОМЕР КАРТЫ: 4169 5858 1234 5678

💰 КОМИССИЯ:
• Элкарт: 1%
• О!Деньги: 0%

✅ ПОСЛЕ ОПЛАТЫ:
Отправьте чек менеджеру @premium_auto_bot

📞 ПОДДЕРЖКА: {PAYMENT_NUMBER}"""

    if car_name and car_price:
        text = f"🏎️ {car_name}\n💰 {car_price}\n\n" + text

    if query:
        await query.edit_message_text(text)
    else:
        await update.message.reply_text(text, reply_markup=main_reply_markup)


async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data.startswith("pay_"):
        car_key = query.data.replace("pay_", "")
        car = car_info.get(car_key, {})
        await show_payment(query=query, car_name=car.get("name"), car_price=car.get("price"))
    else:
        await query.edit_message_text("Спасибо за обращение! Менеджер свяжется с вами.")


if __name__ == "__main__":
    if not TOKEN:
        print("❌ ОШИБКА: Токен не найден! Добавьте переменную BOT_TOKEN")
    else:
        app = Application.builder().token(TOKEN).build()
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CallbackQueryHandler(callback_handler))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, cars))
        print("🚗 БОТ ЗАПУЩЕН И РАБОТАЕТ 24/7!")
        app.run_polling()