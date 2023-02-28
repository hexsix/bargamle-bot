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
    logger.debug(f'/start called')
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="我是自动图床上传机器人，可以将指定群的图片自动上传到流浪图床。"
    )


async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.debug(f'/ping called')
    await context.bot.send_message(chat_id=update.effective_chat.id, text="pong!")


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.debug(f'/help called')
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        parse_mode='MarkdownV2',
        disable_web_page_preview=True,
        text="*删除链接拼接方式*\n" + 
             escape("如果图床地址是\nhttps://p.sda1.dev/{路径}/{文件名}\n") +
             escape("那么删除链接是\nhttps://p.sda1.dev/api/v1/delete/{路径}/{删除令牌}\n") +
             "\n*删除令牌在哪*\n" +
             escape("'|' 前面是图床地址，后面就是删除令牌\n") +
             "\n*为什么用删除令牌，不直接给删除链接*\n" +
             "因为 Telegram 会自动访问每个链接来显示预览，删除链接一访问就把图删除了\n"
    )


async def photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.debug(f'/photo called')
    img = await context.bot.getFile(update.message.photo[-1].file_id)
    filepath = await img.download_to_drive()
    logger.info(f'/photo, image downloaded')
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
                text=f"[图床链接]({url}) \| `{delete_token}`",
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
    logger.info(f'/photo, image removed')


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
    
    application.run_polling()
