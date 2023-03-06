import openai
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

token = '1616104100:AAHhcHJDRbdbDBA_ArThvht4JhdyDmremWI'
openai.api_key = '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'

bot = Bot(token)
dp = Dispatcher(bot)


@dp.message_handler()
async def send(message: types.Message):
    print(message)
    chat_name = f"user_{message['from']['first_name']}"
    # openai.Chat.create
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[
            {"role": "user", "content": message["text"]}],
        # name=chat_name,
        # display_name=f"User {message['from']['first_name']}",
        max_tokens=4000,
        temperature=0,
    )

    await message.answer(response["choices"][0]["message"]["content"])


executor.start_polling(dp, skip_updates=True)
