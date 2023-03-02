import openai
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

token = 'TokenTelegramBot'
openai.api_key = 'Token_OpenAI'

bot = Bot(token)
dp = Dispatcher(bot)

users = {}
accepted_users = lambda message: message.from_user.id not in users


@dp.message_handler(accepted_users, content_types=['any'])
async def handle_unwanted_users(message: types.Message):
    await message.answer(
        "Извините, бот работает только для одобренных пользователей.")
    return


# Словарь для хранения идентификаторов чатов
chats = {}


@dp.message_handler()
async def send(message: types.Message):
    # Получаем ID пользователя
    user_id = message.chat.id

    # Если чат для этого пользователя еще не создан, создаем его
    if user_id not in chats:
        # Используем ID пользователя в качестве названия чата
        chat_name = f"user_{user_id}"
        # Создаем чат в ChatGPT
        openai.Chat.create(
            name=chat_name,
            provider="telegram",
            configuration={
                "telegram": {
                    "user_id": user_id
                }
            }
        )
        # Сохраняем идентификатор чата для этого пользователя
        chats[user_id] = chat_name

    # Отправляем сообщение в соответствующий чат
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=message.text,
        temperature=0.9,
        max_tokens=4000,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.6,
        stop=[" Human:", " AI:"],
        chat=chats[user_id]
    )

    await message.answer(response['choices'][0]['text'])


max_symbols = lambda message: int(len(message.text)) > 2000


@dp.message_handler(max_symbols, content_types=['any'])
async def handle_unwanted_users(message: types.Message):
    await message.answer(
        "Ошибка! Введенное количество символов превышает максимальное значение в 2000" +
        "\n\nКоличество введенных символов: " + str(len(message.text)) + "\n\nСократите Ваш запрос"
    )
    return


executor.start_polling(dp, skip_updates=True)
