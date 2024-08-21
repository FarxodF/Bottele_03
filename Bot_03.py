from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor

API_TOKEN = 'KEY'

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class Form(StatesGroup):
    age = State()
    height = State()
    weight = State()


@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    await message.reply("Привет! Я бот помогающий твоему здоровью.")
    await message.reply("Введите свой возраст:")
    await Form.age.set()


@dp.message_handler(state=Form.age)
async def process_age(message: types.Message, state: FSMContext):
    await state.update_data(age=int(message.text))
    await message.reply("Введите свой рост (в см):")
    await Form.next()


@dp.message_handler(state=Form.height)
async def process_height(message: types.Message, state: FSMContext):
    await state.update_data(height=int(message.text))
    await message.reply("Введите свой вес (в кг):")
    await Form.next()


@dp.message_handler(state=Form.weight)
async def process_weight(message: types.Message, state: FSMContext):
    await state.update_data(weight=int(message.text))
    data = await state.get_data()
    age = data['age']
    height = data['height']
    weight = data['weight']

    # Используем формулу Миффлина - Сан Жеора для мужчин
    bmr = 10 * weight + 6.25 * height - 5 * age + 5

    await message.reply(f"Ваша суточная норма калорий: {bmr} ккал")
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
