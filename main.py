"""
author: hexsix
date: 2023/02/27
description: main
"""
import logging
import os
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, ContextTypes, CommandHandler

from configs import configs
from psda1dev_utils import upload_images


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger('main')


def escape(text: str):
    escape_chars = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
    for escape_char in escape_chars:
        text = text.replace(escape_char, '\\' + escape_char)
    return text


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="pong!")


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="There is no help.")


async def photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    img = await context.bot.getFile(update.message.photo[-1].file_id)
    filepath = await img.download_to_drive()
    try:
        data = await upload_images(filepath)
    except:
        data = {}
    if data:
        try:
            url = data['url'].replace('p.sda1.dev', 'psda1dev.hexsix.me')
            delete_token = data['delete_url'].split('/')[-1]
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"[url]({url}), delete: `{delete_token}`",
                parse_mode='MarkdownV2',
                disable_web_page_preview=True)
        except Exception as e:
            logger.error(f'/photo, send message failed, e: {e}')
    else:
        try:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Upload Failed.")
        except:
            logger.error(f'/photo, send message failed, e: {e}')
    os.remove(filepath)


async def document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Get document!")


async def delete(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Get delete!")


if __name__ == '__main__':
    logger.info(configs)
    if configs.use_proxies:
        proxy_url = configs.proxies['http://']
        application = ApplicationBuilder().token(configs.tg_token).proxy_url(proxy_url).get_updates_proxy_url(proxy_url).build()
    else:
        application = ApplicationBuilder().token(configs.tg_token).build()
    
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    ping_handler = CommandHandler('ping', ping)
    application.add_handler(ping_handler)

    help_handler = CommandHandler('help', help)
    application.add_handler(help_handler)

    photo_handler = MessageHandler(filters.PHOTO & (~filters.COMMAND) & filters.Chat(configs.chat_id), photo)
    application.add_handler(photo_handler)

    document_handler = MessageHandler(filters.ATTACHMENT & (~filters.COMMAND), document)
    application.add_handler(document_handler)

    delete_handler = CommandHandler('delete', delete)
    application.add_handler(delete_handler)
    
    application.run_polling()
