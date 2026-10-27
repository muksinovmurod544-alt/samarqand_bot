from aiohttp import web
import asyncio
import random
import os
from aiogram import Bot

# Ваши данные
API_TOKEN = "8947560009:AAGdv0meVDjPV_D1N0bw90bGDrTz3uu2buU"
CHANNEL_ID = "@SamarqandImkoniyat"

# Интервал между постами в секундах (4 часа = 14400 сек. Для теста можно поставить 60 сек)
POST_INTERVAL_SECONDS = 7200

bot = Bot(token=API_TOKEN)

# Список тем для автопостинга
TOPICS = [
    ("Молодежные инициативы и стартапы", "Самарқанд ёшлари учун янги бизнес-имкониятлар ва стартап лойиҳалари бошланади! Ёшлар ўз ғояларини амалга ошириш учун барча шароитлар яратилмоқда."),
    ("Развитие туризма и сервиса", "Самарқанд шаҳрида туризм ва хизмат кўрсатиш соҳасини ривожлантириш бўйича янги лойиҳалар ишга туширилмоқда. Тадбиркорлар учун қулай шароитлар яратилган."),
    ("Цифровые технологии и IT", "Самарқандда замонавий IT-технологиялар марказлари ва ўқув курслари кенгаймоқда. Келажак касбларини эгаллаш вақти келди!"),
    ("Малый бизнес и предпринимательство", "Кичик бизнес ва хусусий тадбиркорликни қўллаб-қувватлаш бўйича янги имтиёзлар ва имкониятлар тақдим этилмоқда.")
]

async def generate_smart_post() -> str:
    """Генерация поста"""
    title, uz_text = random.choice(TOPICS)
    
    post = (
        f"☀️ **SAMARQAND IMKONIYAT**\n\n"
        f"📌 **Mavzu / Тема:** *{title}*\n\n"
        f"{uz_text}\n\n"
        f"🇷🇺 В Самарканде открываются новые перспективы для развития бизнеса, молодежных инициатив и современных проектов. Не упустите свой шанс реализовать потенциал!\n\n"
        f"📞 Мурожаат учун / Связь с нами: @SamarqandImkoniyat\n\n"
        f"#{Samarqand} #Imkoniyat #Business #Uzbekistan"
    )
    return post

# Веб-сервер для Render, чтобы сервис не засыпал
async def handle(request):
    return web.Response(text="Bot is running!")

async def web_server():
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 10000))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()

async def main():
    # Запускаем веб-сервер в фоне
    await web_server()
    print("🤖 Бот «SAMARQAND IMKONIYAT» запущен в режиме автопостинга!")

    while True:
        try:
            print("⏳ Формирование нового поста...")
            post_text = await generate_smart_post()
            
            print("🚀 Публикация в канал...")
            await bot.send_message(chat_id=CHANNEL_ID, text=post_text, parse_mode="Markdown")
            print("✅ Пост опубликован! Следующая публикация через 4 часа.")
            
        except Exception as e:
            print(f"⚠️ Ошибка при публикации: {e}")

        # Задержка перед следующим постом (в секундах)
        await asyncio.sleep(POST_INTERVAL_SECONDS)

if __name__ == "__main__":
    asyncio.run(main())
