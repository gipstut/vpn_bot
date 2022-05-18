from aiogram import Bot, types
from aiogram.types.message import ContentType
from aiogram.types.message import ContentType
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from sqlalchemy import MetaData, Table, Column, Integer, String, Date, create_engine
from sqlalchemy.sql import select, and_
from aiogram.types import CallbackQuery
from keybord import kb_client
import secrets
token_user = secrets.token_hex(16)
print(token_user)
TOKEN = ''
PAYMENTS_TOKEN = '381764678:TEST:37276'
TIMEZONE = 'Europe/Minsk'
TIMEZONE_COMMON_NAME = 'Minsk'
shopId = 506751
shopArticleId = 538350

meta = MetaData()
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

users_database = Table('user_database', meta,
                       Column('user_id', Integer, primary_key=True),
                       Column('user_name', String(250)),
                       Column('user_date', Date),
                       Column('balance', Integer),
                       Column('key', String))


class User():
    def __init__(self, user_id, user_name, data, balance, key):
        self.user_id = user_id
        self.user_name = user_name
        self.data = data
        self.balance = balance
        self.key = key


engine = create_engine('postgresql+psycopg2://max:111111aA@localhost/bot_users')
meta.create_all(engine)

conn = engine.connect()

def foo(message):
    token_user = secrets.token_hex(16)
    print(token_user)
    add_user_from_database = users_database.insert().values(user_name=f'{message.from_user.id}, user_date={message.date}, balance={0}, key={token_user}')
    conn.execute(add_user_from_database)

def days_to_seconds(days):
    return days * 24 * 60 * 60


async def start_up(_):
    print('Бот "VPN", запущен!')

@dp.message_handler(commands=['start'])
async def start_work(message:types.Message):
    await bot.send_message(message.from_user.id, 'Добро пожаловать, в телеграмм бот. Тут вы сможите найти качественное VPN.', reply_markup=kb_client)

@dp.callback_query_handler(text='sub')
async def sub(call:CallbackQuery):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    await bot.send_invoice(chat_id=call.from_user.id, title='Оформление подписки', description='Вы получаете VPN на месяц', payload='subscription', provider_token=PAYMENTS_TOKEN, currency='RUB', start_parameter='test_bot', prices=[{'label':'Руб', 'amount':9900}])

@dp.callback_query_handler(text='sub')
@dp.pre_checkout_query_handler()
async def process_pre_checout_query(chek:types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(chek.id,ok=True)


@dp.callback_query_handler(text='instruction')
async def instruction(call:types.CallbackQuery):
    await bot.send_message(call.from_user.id, text='Инструкция по эксплуатации — документ, в котором излагаются сведения, необходимые для правильной эксплуатации, и клавиатура для принятия решения', reply_markup=kb_client)

@dp.callback_query_handler(text='subscription_date')
async def instruction(call:types.CallbackQuery):
    s = select(users_database).where(str(users_database.c.user_name) == str(call.from_user.id))
    result = conn.execute(s)
    await bot.send_message(call.from_user.id, text=f'Ваш id ', reply_markup=kb_client)


@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def process_pay(message:types.Message):
    if message.successful_payment.invoice_payload == 'subscription':
        foo(message)
        await bot.send_message(message.from_user.id, 'Оплата прошла, ваша подписка активированна')

@dp.message_handler(commands=['info'])
async def info(message):
    end = users_database.select().where()
    result = conn.execute(end)
    for i in result:
        print(i)

executor.start_polling(dp, skip_updates=True, on_startup=start_up)