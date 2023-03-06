import openai
from chatgpt import utils
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

token = 'TokenTelegramBot'
openai.api_key = 'Token_OpenAI'

bot = Bot(token)
dp = Dispatcher(bot)


@dp.message_handler()
async def send(message: types.Message):
    print(message)
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[
            {"role": "user", "content": message["text"]}],
        max_tokens=2000,
        temperature=0,
    )

    await message.answer(response["choices"][0]["message"]["content"])


executor.start_polling(dp, skip_updates=True)
