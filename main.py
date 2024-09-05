import telebot
from telebot import types
import random

# Initialize bot with your token
bot = telebot.TeleBot('7525016096:AAHCiT3Y4eOO2p4znuCIbW49z_sMgJsYy6s')


# Define the /start command handler
@bot.message_handler(commands=['start'])
def start(message):
    # Create the inline keyboard for the main menu
    markup = types.InlineKeyboardMarkup(row_width=1)

    # Create main menu buttons
    schedule_button = types.InlineKeyboardButton("Расписание 📝", callback_data="schedule")
    map_button = types.InlineKeyboardButton("Карта 🗺", callback_data="map")
    links_button = types.InlineKeyboardButton("Ссылки и контакты 🔗", callback_data="links")
    about_button = types.InlineKeyboardButton("О проекте ℹ️", callback_data="about")

    # Add buttons to the markup
    markup.add(schedule_button, map_button, links_button, about_button)

    # Send a message with the inline keyboard
    bot.send_message(message.chat.id, "Смотри, что у нас есть:", reply_markup=markup)


# Define the first page of groups
group_buttons_page_1 = [
    ['145', '211п', '221', '231', '241'],
    ['3 ГД', '311п', '321', '331', '341'],
    ['4 ГД', '411п', '421', '511п', '521'],
    ['531', '541', '611п', '621', '631']
]


# Create a function to generate random numbers for page 2
def create_random_groups():
    return [[str(random.randint(600, 900)) for _ in range(5)] for _ in range(4)]


# Create inline keyboards for both pages
def create_group_keyboard(page):
    markup = types.InlineKeyboardMarkup(row_width=5)

    if page == 1:
        groups = group_buttons_page_1
        for row in groups:
            buttons = [types.InlineKeyboardButton(text=group, callback_data=group) for group in row]
            markup.row(*buttons)
        # Add navigation buttons
        markup.add(
            types.InlineKeyboardButton("⬅️ Назад", callback_data="back"),
            types.InlineKeyboardButton("1 / 2", callback_data="page_info"),
            types.InlineKeyboardButton("Вперёд ➡️", callback_data="next"),
            types.InlineKeyboardButton("Вернуться 🔄", callback_data="return")
        )

    elif page == 2:
        groups = create_random_groups()  # Generate random group numbers
        for row in groups:
            buttons = [types.InlineKeyboardButton(text=group, callback_data=group) for group in row]
            markup.row(*buttons)
        # Add navigation buttons
        markup.add(
            types.InlineKeyboardButton("⬅️ Назад", callback_data="previous"),
            types.InlineKeyboardButton("2 / 2", callback_data="page_info"),
            types.InlineKeyboardButton("Вперёд ➡️", callback_data="next"),
            types.InlineKeyboardButton("Вернуться 🔄", callback_data="return")
        )

    return markup


# Handle button presses
@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    if call.data == "schedule":
        # Show the group selection for page 1 when "Расписание" is pressed
        bot.send_message(call.message.chat.id, "Выберите группу:", reply_markup=create_group_keyboard(1))
    elif call.data in [group for row in group_buttons_page_1 for group in row]:
        # Handle group selection from page 1
        bot.answer_callback_query(call.id, f"Вы выбрали группу: {call.data}")
    elif call.data == "next":
        # Go to page 2 with random group numbers
        bot.send_message(call.message.chat.id, "Выберите группу:", reply_markup=create_group_keyboard(2))
    elif call.data == "previous":
        # Go back to page 1
        bot.send_message(call.message.chat.id, "Выберите группу:", reply_markup=create_group_keyboard(1))
    elif call.data == "return":
        bot.answer_callback_query(call.id, "Возвращаемся в главное меню.")
        start(call.message)


# Start the bot
bot.polling()