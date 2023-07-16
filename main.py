from telegram import Update,InlineKeyboardButton,InlineKeyboardMarkup
from telegram.ext import CallbackContext,Updater,CommandHandler,CallbackQueryHandler
from datetime import datetime
from db import UserDB
TOKEN='6386688038:AAFjDBQlmDjbv6T_sFnO4qWPlgyQ6v-NyOM'
userdb=UserDB()
def start(update: Update, context):
    bot = context.bot
    chat_id = str(update.message.chat.id)
    first_name=update.message.chat.first_name
    username=update.message.chat.username
    last_name=update.message.chat.last_name
    result = userdb.add_user(chat_id, first_name, username, last_name)
    button1 = InlineKeyboardButton(text = "Kategoriyalar", callback_data="kirish")
    keyboard = InlineKeyboardMarkup([[button1]])
    if result:
        bot.sendMessage(chat_id=chat_id, text="Assalomu alaykum! Xush kelipsiz.", reply_markup=keyboard)
    else:
        bot.sendMessage(chat_id=chat_id, text="Assalomu alaykum! Qaytganingizdan xursandmiz ", reply_markup=keyboard)

def kategoriya(update:Update, context: CallbackContext):
    query = update.callback_query
    bot = context.bot
    chat_id = query.message.chat.id
    button1 = InlineKeyboardButton(text = "Navbatni tekshirish", callback_data="tekshirish")
    button2 = InlineKeyboardButton(text = "Navbatga yozilish", callback_data="yozilish")
    keyboard = InlineKeyboardMarkup([[button1],[button2]])
    bot.sendMessage(chat_id=chat_id, text="Kategoriyalarni tanlash:", reply_markup=keyboard)

def tekshirish(update:Update, context: CallbackContext):
    query = update.callback_query
    bot = context.bot
    chat_id = query.message.chat.id
    first_name=query.message.chat.first_name
    data=userdb.get_task(chat_id)
    
    if data!=False:
        time=data['datetime']
        button1= InlineKeyboardButton(text="Orqaga",callback_data="orqaga")
        keyboard= InlineKeyboardMarkup([[button1]])
        bot.sendMessage(chat_id=chat_id, text=f"{first_name} sizning navbatingiz: {time}-{time+1}\nIltimos kechikmang." , reply_markup=keyboard)
    else:
        button1= InlineKeyboardButton(text="Orqaga",callback_data="orqaga")
        keyboard= InlineKeyboardMarkup([[button1]])
        bot.sendMessage(chat_id=chat_id, text="Siz hali navbatga yozilmagansiz!\n" , reply_markup=keyboard)

def yozilish(update:Update, context: CallbackContext):
    query = update.callback_query
    bot = context.bot
    chat_id = query.message.chat.id
    all_time=userdb.check_time(datetime)
    button=[]
    for i in all_time:
        button.append([InlineKeyboardButton(text=f'{i} - {i+1}', callback_data=f'time_{i}')])
    button.append([InlineKeyboardButton(text='Orqaga', callback_data='orqaga')])
    keyboard= InlineKeyboardMarkup(button)
    bot.sendMessage(chat_id=chat_id, text="Bo`sh vaqtlar:", reply_markup=keyboard)

def save(update:Update, context: CallbackContext):
    query = update.callback_query
    bot = context.bot
    chat_id = query.message.chat.id
    first_name=query.message.chat.first_name
    data=update.callback_query.data
    time=int(data.split('_')[1])
    result=userdb.get_task(chat_id)
    if result==False:
        userdb.add_task(time,chat_id,first_name)
        button1= InlineKeyboardButton(text="Boshiga",callback_data="orqaga")
        keyboard= InlineKeyboardMarkup([[button1]])
        bot.sendMessage(chat_id=chat_id, text="Saqlandi ✅",reply_markup=keyboard)
    else:
        button1= InlineKeyboardButton(text="Boshiga",callback_data="orqaga")
        keyboard= InlineKeyboardMarkup([[button1]])
        bot.sendMessage(chat_id=chat_id, text="Siz navbatga yozilgansiz.",reply_markup=keyboard)













updater = Updater(token=TOKEN)
dp = updater.dispatcher
dp.add_handler(CommandHandler("start", start))
dp.add_handler(CallbackQueryHandler(kategoriya, pattern="kirish"))
dp.add_handler(CallbackQueryHandler(tekshirish, pattern="tekshirish"))
dp.add_handler(CallbackQueryHandler(yozilish, pattern="yozilish"))
dp.add_handler(CallbackQueryHandler(kategoriya, pattern="orqaga"))
dp.add_handler(CallbackQueryHandler(save, pattern="time"))

updater.start_polling()
updater.idle()