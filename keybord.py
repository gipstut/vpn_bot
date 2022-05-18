from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove, KeyboardButton
#Клавиатура при старте
b1 = InlineKeyboardButton(text='Купить VPN', callback_data='sub')
b2 = InlineKeyboardButton(text='Профиль', callback_data='subscription_date')
b3 = InlineKeyboardButton(text='Инструкция', callback_data='instruction')
kb_client = InlineKeyboardMarkup()
kb_client.add(b1).add(b2).insert(b3)

