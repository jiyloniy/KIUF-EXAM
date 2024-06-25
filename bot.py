# import os
# import io
# from aiogram import Bot, Dispatcher, executor, types
# from PIL import Image
# import aiohttp

# API_TOKEN = '5488825517:AAEkQ6dZksQZR029o0vld4bQhY9yJ97apWk'

# bot = Bot(token=API_TOKEN)
# dp = Dispatcher(bot)

# async def download_file(file_path):
#     async with aiohttp.ClientSession() as session:
#         async with session.get(f'https://api.telegram.org/file/bot{API_TOKEN}/{file_path}') as response:
#             file_content = await response.read()
#             return file_content

# @dp.message_handler(content_types=['photo'])
# async def convert_photo(message: types.Message):
#     photos = [p.file_id for p in message.photo]
#     is_forwarded = message.forward_from or message.forward_from_chat or message.forward_from_message_id or message.forward_signature or message.forward_sender_name or message.forward_date or message.forward_from_chat_id or message.forward_from_message_id or message.forward_from_message_id
#     print(is_forwarded)
#     if is_forwarded:
#         file_id = message.effective_attachment.file_id
#         photos = [file_id]

#     for photo_id in photos:
#         photo = await bot.get_file(photo_id)
#         file_path = photo.file_path

#         file_content = await download_file(file_path)

#         img = Image.open(io.BytesIO(file_content))
        
#         # Vaqtinchalik fayl yaratish
#         temp_file = io.BytesIO()
#         img.save(temp_file, format="JPEG")
#         temp_file.seek(0)

#         # Rasmni yuborish
#         await message.reply_photo(temp_file, caption='Rasm JPG formatiga aylantirildi')

# if __name__ == '__main__':
#     executor.start_polling(dp, skip_updates=True)

# if __name__ == '__main__':
#     executor.start_polling(dp, skip_updates=True)

a = [[1,2], [3,4]]
p1 = a[0]
p1[0] = 2 
print(a)
