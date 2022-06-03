from telegram.ext import Updater, Filters, CommandHandler, MessageHandler
from tensorflow.keras.applications.resnet50 import ResNet50
import cv2
import numpy as np
from labelsRus import label
import os
import json
import string

model = ResNet50()


async def on_startup(_):
    print('Бот вышел в онлайн')


def start(updater, context):
    updater.message.reply_text("Добро пожаловать!")


def help_(updater, context):
    updater.message.reply_text("Просто пришлите любое изображение и я постараюсь определить что это")

def please(updater, context):
    updater.message.reply_text("Поставти зачет, пожалуйста 👉👈")

def message(updater, context):
    msg = updater.message.text
    if {i.lower().translate(str.maketrans('', '', string.punctuation)) for i in msg.split(' ')} \
            .intersection(set(json.load(open('censorship.json')))) != set():
        print(msg)
        updater.message.reply_text(('Ребята, общайтесь без мата, пожалуйста'))
        updater.message.delete()


def image(updater, context):
    photo = updater.message.photo[-1].get_file()  # Загрузка фото, который прислал пользователь
    photo.download("img.jpg")  # Сохранение в формате jpg

    img = cv2.imread("img.jpg")  # Прочтение

    img = cv2.resize(img, (224, 224))  # Изменение размера до 244x244
    img = np.reshape(img, (1, 224, 224, 3))  # преобразование массива

    prediction = np.argmax(model.predict(img))

    prediction = label[prediction]

    print(prediction)  # вывод ожидаемого ответа на изображение

    updater.message.reply_text(prediction)  # ответ пользователю


token = os.getenv('TOKEN')
updater = Updater(token)
dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("help", help_))
dispatcher.add_handler(CommandHandler("please", please))
dispatcher.add_handler(MessageHandler(Filters.text, message))
dispatcher.add_handler(MessageHandler(Filters.photo, image))

updater.start_polling()
updater.idle()
