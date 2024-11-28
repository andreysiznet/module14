from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio

api = '7798478890:AAEviZPQB4oFDwRcJcMY58AmtZte9m3_OEI'
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup(resize_keyboard=True)
button3 = KeyboardButton(text='Рассчитать')
button4 = KeyboardButton(text='Информация')
bottom5 = KeyboardButton(text= 'Купить')
kb.row(button3, button4,bottom5)

kb1 = InlineKeyboardMarkup(resize_keyboard=True)
button = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
button2 = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
kb1.row(button, button2)

kb2 = InlineKeyboardMarkup(resize_keyboard=True)
button1 = InlineKeyboardButton('Product1', callback_data='product_buying')
button2 = InlineKeyboardButton('Product2', callback_data='product_buying')
button3 = InlineKeyboardButton('Product3', callback_data='product_buying')
button4 = InlineKeyboardButton('Product4', callback_data='product_buying')
kb2.row(button1, button2,button3,button4)




class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup=kb)


@dp.message_handler(text='Информация')
async def inform(message):
    await message.answer('Информация о боте!')


@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup=kb1)


@dp.message_handler(text='Купить')
async def get_buying_list(message):
    with open("1.jpg", "rb") as Яблоко:
        await message.answer_photo(Яблоко, f"Название: Product1 | Описание: Яблоко | Цена: {1*100}")
    with open("2.jpg", "rb") as Банан:
        await message.answer_photo(Банан, f"Название: Product2 | Описание: Банан | Цена: {2*100}")
    with open("3.jpg", "rb") as Груша:
        await message.answer_photo(Груша, f"Название: Product3 | Описание: Груша | Цена: {3*100}")
    with open("4.jpg", "rb") as Яблоко:
        await message.answer_photo(Яблоко, f"Название: Product4 | Описание: Яблоко | Цена: {4*100}")
    await message.answer("Выберите продукт для покупки:", reply_markup=kb2.row())


@dp.callback_query_handler(text=['product_buying'])
async def send_confirm_message(call):
    await  call.message.answer('Вы успешно приобрели продукт!')
    await call.answer()


@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161')
    await call.answer()


@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await call.answer()
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=float(message.text))
    await message.answer('Введите свой рост (см.):')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=float(message.text))
    await message.answer('Введите свой вес (кг.):')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=float(message.text))
    data = await state.get_data()
    calories = (10.0 * data['weight']) + (6.25 * data['growth']) - (5.0 * data['age']) - 161.0
    await message.answer(f'Ваша норма калорий - {calories}')
    await state.finish()


@dp.message_handler()
async def all_massages(message):
    await message.answer('Введите команду /start, чтобы начать общение.')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
