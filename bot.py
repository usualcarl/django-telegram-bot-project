import requests
import aiohttp
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackContext, ContextTypes

API_URL_PRODUCTS = 'http://127.0.0.1:8000/api/products/'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Hello, you can create and update objects')

async def list_products(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    response = requests.get(API_URL_PRODUCTS)
    products = response.json()
    message = '\n'.join([f"{product['name']} - {product['price']} $" for product in products])
    await update.message.reply_text(message)

async def create_product(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text.split(', ')
    
    if len(text) != 3:
        await update.message.reply_text('Error: Type your data in this format: Name, Price, Description.')
        return
    
    name, price, description = text[0], text[1], text[2]
    data = {'name': name, 'price': price, 'description': description}

    async with aiohttp.ClientSession() as session:
        async with session.post('http://127.0.0.1:8000/api/products/', json=data) as response:
            if response.status == 201:
                await update.message.reply_text('Товар успешно создан!')
            else:
                error_text = await response.text()
                await update.message.reply_text(f'Ошибка создания товара. Статус: {response.status}\nОтвет: {error_text}')

if __name__ == '__main__':
    app = ApplicationBuilder().token("8005783515:AAECcuCfUbtnFvxnWBGWDD5RHDh4j0Agn2g").build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("list", list_products))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, create_product))
    app.run_polling()




