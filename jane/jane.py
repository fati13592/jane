# -*- coding:utf-8 -*-

import asyncio
import telepot
import telepot.aio
from telepot.aio.loop import MessageLoop

import json


async def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print('Chat:', content_type, chat_type, chat_id)

    if content_type != 'text':
        return

    if chat_id not in CHATIDS:
        return

    command = msg['text'].lower().split('.')
    print(command)

    if command[0] == '/la':  # Add item to list
        try:
            with open('list.json', 'r') as f:
                shoplist = json.load(f)
        except FileNotFoundError:
            shoplist = {'count': 0, 'itemlist': []}
        try:
            shoplist['itemlist'].append({'item': command[1], 'id': shoplist['count']})
            await bot.sendMessage(chat_id, 'Item added succesfully.')
        except IndexError:
            await bot.sendMessage(chat_id, 'Error: Item not specified.')
        else:
            shoplist['count'] += 1
            with open('list.json', 'w') as f:
                json.dump(shoplist, f)

    elif command[0] == '/lr':  # Remove item from list
        try:
            item_id = int(command[1])
        except:
            await bot.sendMessage(chat_id, 'Error: Invalid item ID specified.')
        else:
            try:
                with open('list.json', 'r') as f:
                    shoplist = json.load(f)
            except FileNotFoundError:
                await bot.sendMessage(chat_id, 'Error: List not created yet.')
            else:
                shoplist['itemlist'] = list(filter(lambda x: x['id'] != item_id, shoplist['itemlist']))
                with open('list.json', 'w') as f:
                    json.dump(shoplist, f)
                await bot.sendMessage(chat_id, 'Item removed successfully.')

    elif command[0] == '/ls':  # Show list
        try:
            with open('list.json', 'r') as f:
                shoplist = json.load(f)
        except FileNotFoundError:
            await bot.sendMessage(chat_id, 'Error: List not created yet.')
        else:
            if not shoplist['itemlist']:
                await bot.sendMessage(chat_id, 'Error: Empty list.')
            else:
                retval = ''
                for item in shoplist['itemlist']:
                    retval += str(item['id']) + '. ' + item['item'] + '\n'
                await bot.sendMessage(chat_id, retval)

    elif command[0] == '/lc':  # Clear list
        try:
            with open('list.json', 'r') as f:
                shoplist = json.load(f)
        except FileNotFoundError:
            await bot.sendMessage(chat_id, 'Error: List not created yet.')
        else:
            shoplist['count'] = 0
            shoplist['itemlist'].clear()
            with open('list.json', 'w') as f:
                json.dump(shoplist, f)
            await bot.sendMessage(chat_id, 'List cleared.')

    elif command == '/ds':
        await bot.sendMessage(chat_id, 'Show debts. Not Implemented yet.')
    elif command == '/dc':
        await bot.sendMessage(chat_id, 'Clear debt. Not Implemented yet.')
    elif command == '/da':
        await bot.sendMessage(chat_id, 'Assing new debt. Not Implemented yet.')


with open('bot.json', 'r') as f:
    bot_cfg = json.load(f)

TOKEN = bot_cfg['TOKEN']
CHATIDS = bot_cfg['CHATIDS']

bot = telepot.aio.Bot(TOKEN)
loop = asyncio.get_event_loop()

loop.create_task(MessageLoop(bot, handle).run_forever())
print('Listening ...')

loop.run_forever()


