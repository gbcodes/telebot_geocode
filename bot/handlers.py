#Importing packages
import logging
import emoji
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from bot.models import Area, Result


def init_bot(self):
    # Initialiazong updater, dispatcher and log
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)

    updater = Updater(token='1065797989:AAHz-IYgtxWXgtX3_Vns3iZBxY9iywmEBWg', use_context=True)

    dispatcher = updater.dispatcher

    # handlers
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.regex(r'Новый поиск'), search_clicked))
    dispatcher.add_handler(MessageHandler(Filters.regex(r'История'), history_clicked))
    dispatcher.add_handler(MessageHandler(Filters.text, get_address))
    dispatcher.add_handler(MessageHandler(Filters.command, unknown))

    updater.start_polling()


# https://api-maps.yandex.ru/2.1/?apikey=ваш API-ключ&lang=ru_RU
import requests
def response(name):
    url = 'https://geocode-maps.yandex.ru/1.x/?apikey=497be89f-ae64-4f86-9526-4a73edcb8127&format=json&geocode={0}' \
          '&ll=37.13268871914181, 55.55945544545429&spn=38.085747336675574, 55.946698202860325'.format(name)
    respons = requests.get(url)

    try:
        num = 0
        for i in range(len(respons.json()['response']['GeoObjectCollection']['featureMember'])):
            if Area.objects.get(pk=1).name not in respons.json()['response']['GeoObjectCollection']['featureMember'][i]['GeoObject']['metaDataProperty']['GeocoderMetaData']['text']:
                continue
            else:
                return respons.json()['response']['GeoObjectCollection']['featureMember'][i]['GeoObject'][
                    'metaDataProperty'][
                    'GeocoderMetaData']['text']
    except IndexError:
        return 'По вашему запросу ничего не найдено!'


#Settings for start markup board
reply_markup = {
    "keyboard": [[emoji.emojize(':mag: Новый поиск', use_aliases=True), emoji.emojize(':book: История', use_aliases=True)]],
    "resize_keyboard": True,
    "one_time_keyboard": True
}

# creating database by using pandas dataframe
import pandas as pd
# df = pd.DataFrame(columns={'user_id', 'user_name', 'user_request', 'user_response', 'user_date'})
# df.to_excel('db.xlsx', index=False)


#Func that called when user clicked 'Новый поиск'
def search_clicked(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Введите название места, которое хотите найти.')

#Func that called when user clicked 'История'
def history_clicked(update, context):
    st = Result.objects.filter(user_id=update.effective_user.id)
    c = Result.objects.filter(user_id=update.effective_user.id).count()
    txt = 'Вы совершили {0} поисковых запросов\n\n'.format(c)
    for i in range(1,c+1):
        txt += str(st.get(pk=i).request) + ' --> ' + str(st.get(pk=i).result) + ', ' + str(st.get(pk=i).date) +'\n\n'
    context.bot.send_message(chat_id=update.effective_chat.id, text=txt)


#func for start command
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Хелова Джимбо!", reply_markup=reply_markup)

#func for unknown commands
def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

#func for getting address from user message
def get_address(update, context):
    text = update.message.text
    context.bot.send_message(chat_id=update.effective_chat.id, text=response(text))
    user_r = Result(user_id=update.effective_user.id, request=text, result=response(text), date=str(update.message.date))
    user_r.save()