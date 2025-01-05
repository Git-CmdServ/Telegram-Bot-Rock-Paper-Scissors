# Логируем всё дерьмо, чтобы потом не искать косяки по всему коду
import logging  

# Чтобы бот кидал ходы не как тупой, а рандомно
import random   

# Асинхронщина, чтобы бот не тормозил, как твой бывший
import asyncio  

# Айограм — король среди либ для Телеги, берём бота и диспетчер
from aiogram import Bot, Dispatcher  

# Всякие штуки для общения с Телеграмом: сообщения, кнопочки и коллбэки
from aiogram.types import (
    Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
)

# Фильтры для команд, например, когда юзер пишет "/start"
from aiogram.filters import Command  

# Фильтр для коллбэков, чтобы понять, какую кнопку нажали
from aiogram import F  

# Настраиваем логирование, чтобы видеть в консоли, когда бот тупит
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

# Токен для входа бота, храни его в секрете, а то сопрут, как твою бывшую
tok = 'Токен'

# Создаём бота и диспетчер — это мозги и руки всей системы
bot = Bot(token=tok)
dp = Dispatcher()

# Словарь с вариантами для игры, чтобы не играть в пустоту
opts = {
    'rock': '✊ Камень',
    'paper': '✋ Бумага',
    'scissors': '✌️ Ножницы'
}

# Эмодзи, потому что без них было бы скучно, как на скучной паре
emj = {
    'rock': '✊',
    'paper': '✋',
    'scissors': '✌️'
}

# Логика победителя — что чем дубасит, камень режет ножницы, а бумага накрывает камень
wins = {
    'rock': 'scissors',
    'paper': 'rock',
    'scissors': 'paper'
}

# Функция для создания кнопочек, чтобы юзер мог тыкнуть, а не писать вручную
def mk_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=opts['rock'], callback_data='rock'),
            InlineKeyboardButton(text=opts['paper'], callback_data='paper'),
            InlineKeyboardButton(text=opts['scissors'], callback_data='scissors')
        ]
    ])

# Обработчик команды /start — бот не игнорит, а шлет приветствие
@dp.message(Command(commands=['start']))
async def start_cmd(msg: Message):
    txt = f"Привет, {msg.from_user.first_name}! 🎮\nДавай сыграем в Камень, Ножницы, Бумага! Выбери свой вариант ниже ⬇️"
    await msg.answer(txt, reply_markup=mk_kb())

# Обработчик команды /help — типа, если кто-то тупит, бот объясняет правила
@dp.message(Command(commands=['help']))
async def help_cmd(msg: Message):
    txt = "Просто нажми на одну из кнопок ниже, чтобы начать игру! 🕹️"
    await msg.answer(txt, reply_markup=mk_kb())

# Обработчик выбора юзера через кнопки — тут решается, кто кого уделал
@dp.callback_query(F.data.in_({'rock', 'paper', 'scissors'}))
async def handle_cb(cb: CallbackQuery):
    await cb.answer()  # Чтобы Телега не показывала бесконечные часики после клика

    # Юзер тыкнул и выбрал ход, сохраняем это в переменную
    u_ch = cb.data  

    # А теперь бот выбирает свой ход — и да, он делает это случайно
    b_ch = random.choice(list(opts.keys()))

    # Логика: сравниваем выборы и определяем победителя
    if u_ch == b_ch:
        outcome = "Ничья! 🤝"  # Если оба выбрали одно и то же
    elif wins[u_ch] == b_ch:
        outcome = "Ты выиграл! 🎉"  # Если юзер переиграл бота
    else:
        outcome = "Ты проиграл! 😞"  # Если бот унизил юзера

    # Эмодзи для отображения выбора
    u_emj = emj[u_ch]
    b_emj = emj[b_ch]

    # Собираем красивое сообщение для отправки
    summary = (
        f"🤖Ты выбрал: {opts[u_ch]} {u_emj}\n"
        f"😎Бот выбрал: {opts[b_ch]} {b_emj}\n\n"
        f"{outcome}"
    )

    # Показываем выборы с задержкой для драматичности
    await cb.message.answer(u_emj)
    await asyncio.sleep(0.5)
    await cb.message.answer(b_emj)
    await asyncio.sleep(0.5)
    await cb.message.answer(summary, reply_markup=mk_kb())

# Основная функция для запуска бота — бот просыпается и начинает мониторить чат
async def main():
    try:
        log.info("Бот запускается...")  # Сообщаем в консоли, что бот запущен
        await dp.start_polling(bot)  # Включаем вечный опрос событий из Телеги
    finally:
        await bot.close()  # Если бот умирает, он закрывает соединение
        log.info("Бот остановлен.")  # И пишет в логи, что он сдох

# Магическая строка, которая запускает всё это безумие
if __name__ == '__main__':
    asyncio.run(main())  # Асинхронно запускаем функцию main()
