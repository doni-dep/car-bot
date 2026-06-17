import random
import datetime
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, CallbackQueryHandler, filters

import os

TOKEN = os.getenv("8640511619:AAFCnoVNvOsR1pVpWh3fCW8y_j4WbJvEK-I")

# МЕНЮ
MAIN_KEYBOARD = [
    ["🏎️ LAMBORGHINI", "🐎 FERRARI"],
    ["⚡ PORSCHE", "🧡 McLAREN"],
    ["🚙 LEXUS"],
    ["🎰 КАЗИНО", "🎲 РУЛЕТКА"],
    ["💰 КРЕДИТ 0%", "🔄 ТЕСТ-ДРАЙВ"],
    ["📊 СРАВНЕНИЕ", "🎁 АКЦИИ"],
    ["⭐ ОТЗЫВЫ", "🎮 ИГРЫ"],
    ["📍 КАРТА", "📞 КОНТАКТЫ"],
    ["🏪 О НАС", "💳 ОПЛАТА"],
    ["📝 РЕГИСТРАЦИЯ", "👤 ПРОФИЛЬ"],
    ["🏆 РЕЙТИНГ", "💬 ПОДДЕРЖКА"],
    ["📊 СТАТИСТИКА", "🎁 БОНУСЫ"],
    ["⚡ БЫСТРАЯ ПОКУПКА"],
]

main_reply_markup = ReplyKeyboardMarkup(MAIN_KEYBOARD, resize_keyboard=True)

# ДАННЫЕ МАШИН
car_info = {
    "🏎️ LAMBORGHINI": {"name": "Lamborghini Revuelto", "speed": "350 км/ч", "price": "$1 200 000", "rating": "10/10"},
    "🐎 FERRARI": {"name": "Ferrari SF90 Stradale", "speed": "340 км/ч", "price": "$850 000", "rating": "9.8/10"},
    "⚡ PORSCHE": {"name": "Porsche 911 Turbo S", "speed": "330 км/ч", "price": "$300 000", "rating": "9.5/10"},
    "🧡 McLAREN": {"name": "McLaren Artura", "speed": "420 км/ч", "price": "$900 000", "rating": "9.7/10"},
    "🚙 LEXUS": {"name": "Lexus LC 500", "speed": "270 км/ч", "price": "$120 000", "rating": "9.0/10"},
}

# Хранилище
users_db = {}
user_bonuses = {}
user_ratings = {}
user_balance = {}


# ============================================
# СТАРТ
# ============================================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👑 ДОБРО ПОЖАЛОВАТЬ! 👑\n\nВыберите раздел:",
        reply_markup=main_reply_markup
    )


# ============================================
# МАШИНЫ
# ============================================
async def show_car(update: Update, context: ContextTypes.DEFAULT_TYPE, car_key):
    car = car_info[car_key]
    msg = f"""🏎️ {car['name']}
🚀 Скорость: {car['speed']}
💰 Цена: {car['price']}
⭐ Рейтинг: {car['rating']}"""
    await update.message.reply_text(msg, reply_markup=main_reply_markup)


# ============================================
# ВСЕ КНОПКИ
# ============================================
async def vip_club(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🚀 VIP КЛУБ\n\nСкидка 15%\nЛичный менеджер\nБесплатная доставка",
                                    reply_markup=main_reply_markup)


async def premium_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("💎 ПРЕМИУМ\n\nСкидка 20%\nСтраховка 3 года\nЛичный водитель",
                                    reply_markup=main_reply_markup)


async def casino(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("🎰 КРУТИТЬ (10 бонусов)", callback_data="spin")]]
    await update.message.reply_text("🎰 КАЗИНО\n\nНажмите кнопку:", reply_markup=InlineKeyboardMarkup(keyboard))


async def roulette(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎲 РУЛЕТКА\n\nНапишите число от 1 до 10", reply_markup=main_reply_markup)
    context.user_data['roulette_mode'] = True


async def credit_calculator(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("💰 КРЕДИТ 0%\n\nОтправьте: /credit 120000 10 5", reply_markup=main_reply_markup)


async def test_drive(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🏎️ ТЕСТ-ДРАЙВ\n\nОтправьте: Имя, Машина, Дата", reply_markup=main_reply_markup)


async def compare_cars(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Lamborghini vs Ferrari", callback_data="cmp1")],
        [InlineKeyboardButton("Porsche vs McLaren", callback_data="cmp2")],
    ]
    await update.message.reply_text("📊 СРАВНЕНИЕ\n\nВыберите пару:", reply_markup=InlineKeyboardMarkup(keyboard))


async def promotions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎁 АКЦИИ\n\n🔥 Скидка 20% на Porsche\n💰 Кредит 0% на Lexus",
                                    reply_markup=main_reply_markup)


async def reviews(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⭐ ОТЗЫВЫ\n\n★★★★★ Алексей: 'Отличный сервис!'\n★★★★★ Михаил: 'Лучший автосалон!'",
                                    reply_markup=main_reply_markup)


async def games_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🎯 УГАДАЙ ЧИСЛО", callback_data="guess")],
        [InlineKeyboardButton("🗿 КАМЕНЬ-НОЖНИЦЫ", callback_data="rps")],
    ]
    await update.message.reply_text("🎮 ИГРЫ\n\nВыберите игру:", reply_markup=InlineKeyboardMarkup(keyboard))


async def show_map(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("📍 КАРТА", callback_data="map")]]
    await update.message.reply_text("📍 КАРТА\n\nг. Бишкек, пр. Манаса 100", reply_markup=InlineKeyboardMarkup(keyboard))


async def contacts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📞 КОНТАКТЫ\n\nТелефон: 0507 065 255\nEmail: hdhhhdhd002@gmail.com",
                                    reply_markup=main_reply_markup)


async def about_us(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🏪 О НАС\n\nЛучший автосалон с 2010 года!\n5000+ клиентов",
                                    reply_markup=main_reply_markup)


async def show_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("💳 ОПЛАТА\n\nО!Деньги\nНомер: 0507 065 255\nКарта: 4169 5858 1234 5678",
                                    reply_markup=main_reply_markup)


async def register_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    if user_id in users_db:
        await update.message.reply_text("✅ Вы уже зарегистрированы!", reply_markup=main_reply_markup)
        return
    users_db[user_id] = {"name": update.effective_user.first_name}
    user_bonuses[user_id] = 100
    user_ratings[user_id] = 1
    user_balance[user_id] = 0
    await update.message.reply_text("🎉 РЕГИСТРАЦИЯ УСПЕШНА!\n💎 +100 бонусов!", reply_markup=main_reply_markup)


async def my_profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    if user_id not in users_db:
        await update.message.reply_text("❌ Зарегистрируйтесь!", reply_markup=main_reply_markup)
        return
    await update.message.reply_text(
        f"👤 ПРОФИЛЬ\n\nИмя: {users_db[user_id]['name']}\n💎 Бонусов: {user_bonuses.get(user_id, 0)}\n⭐ Рейтинг: {user_ratings.get(user_id, 0)}",
        reply_markup=main_reply_markup
    )


async def show_rating(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🏆 РЕЙТИНГ\n\n1️⃣ Вы - 10⭐", reply_markup=main_reply_markup)


async def support_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("💬 ПОДДЕРЖКА\n\nНапишите ваш вопрос, мы ответим!", reply_markup=main_reply_markup)
    context.user_data['support_mode'] = True


async def show_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"📊 СТАТИСТИКА\n\nПользователей: {len(users_db)}\nВсего бонусов: {sum(user_bonuses.values())}",
        reply_markup=main_reply_markup)


async def my_bonuses(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    await update.message.reply_text(f"🎁 БОНУСЫ\n\n💎 {user_bonuses.get(user_id, 0)} бонусов",
                                    reply_markup=main_reply_markup)


async def fast_buy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("LAMBORGHINI", callback_data="buy_LAMBORGHINI")],
        [InlineKeyboardButton("FERRARI", callback_data="buy_FERRARI")],
        [InlineKeyboardButton("PORSCHE", callback_data="buy_PORSCHE")],
    ]
    await update.message.reply_text("⚡ БЫСТРАЯ ПОКУПКА\n\nВыберите машину:",
                                    reply_markup=InlineKeyboardMarkup(keyboard))


# ============================================
# CALLBACK
# ============================================
async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "spin":
        await query.edit_message_text("🎰 ВЫ ВЫИГРАЛИ 100 БОНУСОВ!")
    elif query.data == "guess":
        await query.edit_message_text("🎯 Угадайте число от 1 до 10\nНапишите ответ в чат")
    elif query.data == "rps":
        await query.edit_message_text("🗿 КАМЕНЬ-НОЖНИЦЫ\nНапишите: камень, ножницы или бумага")
    elif query.data == "map":
        await query.message.reply_location(latitude=42.8746, longitude=74.5698)
        await query.edit_message_text("📍 пр. Манаса 100, Бишкек")
    elif query.data.startswith("buy_"):
        car_key = query.data.replace("buy_", "")
        car = car_info.get(car_key, {})
        await query.edit_message_text(f"✅ ЗАКАЗ ОФОРМЛЕН!\n\n🏎️ {car.get('name', '')}\n💰 {car.get('price', '')}")
    elif query.data == "cmp1":
        await query.edit_message_text("📊 СРАВНЕНИЕ\n\nLamborghini vs Ferrari\n🏆 Lamborghini быстрее!")
    elif query.data == "cmp2":
        await query.edit_message_text("📊 СРАВНЕНИЕ\n\nPorsche vs McLaren\n🏆 McLaren быстрее!")


# ============================================
# ОБРАБОТЧИК СООБЩЕНИЙ
# ============================================
async def cars(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    # РУЛЕТКА
    if context.user_data.get('roulette_mode'):
        if text.isdigit() and 1 <= int(text) <= 10:
            num = random.randint(1, 10)
            if int(text) == num:
                await update.message.reply_text(f"🎉 ПОБЕДА! Число {num}!\n💰 +100 бонусов!",
                                                reply_markup=main_reply_markup)
            else:
                await update.message.reply_text(f"❌ НЕУДАЧА! Вы {text}, выпало {num}", reply_markup=main_reply_markup)
            context.user_data['roulette_mode'] = False
            return

    # ПОДДЕРЖКА
    if context.user_data.get('support_mode'):
        await update.message.reply_text("✅ Сообщение отправлено менеджеру!", reply_markup=main_reply_markup)
        context.user_data['support_mode'] = False
        return

    # МАШИНЫ
    if text in car_info:
        await show_car(update, context, text)
    elif text == "🚀 VIP КЛУБ":
        await vip_club(update, context)
    elif text == "💎 ПРЕМИУМ":
        await premium_status(update, context)
    elif text == "🎰 КАЗИНО":
        await casino(update, context)
    elif text == "🎲 РУЛЕТКА":
        await roulette(update, context)
    elif text == "💰 КРЕДИТ 0%":
        await credit_calculator(update, context)
    elif text == "🔄 ТЕСТ-ДРАЙВ":
        await test_drive(update, context)
    elif text == "📊 СРАВНЕНИЕ":
        await compare_cars(update, context)
    elif text == "🎁 АКЦИИ":
        await promotions(update, context)
    elif text == "⭐ ОТЗЫВЫ":
        await reviews(update, context)
    elif text == "🎮 ИГРЫ":
        await games_menu(update, context)
    elif text == "📍 КАРТА":
        await show_map(update, context)
    elif text == "📞 КОНТАКТЫ":
        await contacts(update, context)
    elif text == "🏪 О НАС":
        await about_us(update, context)
    elif text == "💳 ОПЛАТА":
        await show_payment(update, context)
    elif text == "📝 РЕГИСТРАЦИЯ":
        await register_user(update, context)
    elif text == "👤 ПРОФИЛЬ":
        await my_profile(update, context)
    elif text == "🏆 РЕЙТИНГ":
        await show_rating(update, context)
    elif text == "💬 ПОДДЕРЖКА":
        await support_chat(update, context)
    elif text == "📊 СТАТИСТИКА":
        await show_stats(update, context)
    elif text == "🎁 БОНУСЫ":
        await my_bonuses(update, context)
    elif text == "⚡ БЫСТРАЯ ПОКУПКА":
        await fast_buy(update, context)
    else:
        await update.message.reply_text("❌ Нажмите кнопку меню!", reply_markup=main_reply_markup)


# ============================================
# ЗАПУСК
# ============================================
if __name__ == "__main__":
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(callback_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, cars))
    print("🚗 БОТ ЗАПУЩЕН!")
    app.run_polling()