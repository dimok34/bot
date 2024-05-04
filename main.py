import telebot
from telebot import types
# import atexit
import subprocess
import threading
import hashlib
from PIL import Image
import datetime
import string
import random
import requests
import lyricsgenius
import json
import os
from pyaspeller import YandexSpeller
from io import BytesIO
import qrcode
import wikipedia, re
from gtts import gTTS
from googletrans import Translator
from langdetect import detect
from yookassa import Configuration, Payment
import time


def start_bot():
    YOUR_CHAT_ID = 'xxxx'
    Configuration.account_id = 'xxxx'
    Configuration.secret_key = 'xxxx'
    bot = telebot.TeleBot('xxxx')
    GENIUS_API_TOKEN = 'xxxxxx'
    genius = lyricsgenius.Genius(GENIUS_API_TOKEN)
    virus_total_api_key = 'xxxxxx'
    API = "xxxxxx"  # погода
    translator = Translator()
    chat_pairs = {}
    speller = YandexSpeller()
    wikipedia.set_lang("ru")
    attempts = {}
    pogoda = "pogoda"
    avtopost = "avtopost"
    qrrr = "qr-kod"
    chata = "chat"

    # def process_website(message):
    #     url = message.text

    #     def process():
    #         try:
    #             bot.send_message(message.chat.id, "Загружаю страницу, это может занять некоторое время...")
    #             # Запрос на получение скриншота
    #             response = requests.get(f'https://api.apiflash.com/v1/urltoimage?access_key=805a6c7cf7be4d23b0d1e808978f2c6c& &url={url}')
    #             # Преобразование ответа в изображение
    #             image = Image.open(BytesIO(response.content))

    #             # Отправка изображения пользователю
    #             bot.send_photo(message.chat.id, image)
    #             bot.send_message(message.chat.id, "/start - другие команды\n(кликабельно)")
    #             print("использовал проверка сайта")
    #         except Exception as e:
    #             print(f"Ошибка: {e}")
    #             bot.send_message(message.chat.id, "Произошла ошибка.")
    #             bot.send_message(message.chat.id, "Выполняю команду /start")
    #             start(message)

    #     thread = threading.Thread(target=process)
    #     thread.start()

    def password(message):
        pass_length = 10
        if len(message.text.split()) == 2:
            try:
                pass_length = int(message.text.split()[1])
            except ValueError:
                pass_length = 10
        generated_password = generate_password(pass_length)
        bot.send_message(message.chat.id, f'Сгенерированный пароль: {generated_password}')
        print("использовал пароль")

    def generate_password(length=10):
        letters = string.ascii_letters
        return ''.join(random.choice(letters) for i in range(length))

    # код для бесплатной подписки

    def handle_start(message):
        #     user_id = message.from_user.id  # получаем идентификатор пользователя
        #     if user_id in attempts and attempts[user_id] >= 2:
        #         bot.send_message(message.chat.id, "Ваши попытки закончились.\n"
        #                                           "Оплатите подписку, получив безлимит на попытки, и доступ ко всем остальным платным командам.\n"
        #                                           "Если вы оплатили подписку, пользуйтесь кнопкой 'Пробив номера'\n"
        #                                           "/pay - оплатить")
        #         return

        bot.send_message(message.chat.id, "Введите номер телефона:\nПример: +79XXXXXXXXX или 89XXXXXXXXX")
        bot.register_next_step_handler(message, handle_phone_number1)

    # def handle_phone_number(message):
    #     user_id = message.from_user.id  # получаем идентификатор пользователя
    #     try:
    #         number = message.text
    #         if user_id not in attempts:  # если пользователя нет в словаре, добавляем его
    #             attempts[user_id] = 1
    #         else:  # увеличиваем количество попыток
    #             attempts[user_id] += 1
    #
    #         if attempts[user_id] > 5:  # если количество попыток больше 3, сообщаем пользователю и выходим из функции
    #             bot.send_message(message.chat.id, "Ваши попытки закончились\n"
    #                                               "Оплатите подписку, получив безлимит на попытки, и доступ ко всем остальным платным командам\n"
    #                                               "/pay - оплатить")
    #             return
    #
    #         if number.startswith("+79") and len(number) == 12:
    #             url = "http://num.voxlink.ru/get/"
    #             querystring = {"num": number}
    #             response = requests.get(url, params=querystring)
    #             data = response.json()
    #             operator = data.get("operator")
    #             region = data.get("region")
    #             old_operator = data.get("old_operator")
    #             response_text = f"Оператор: {operator}\nРегион: {region}\nСтарый оператор: {old_operator}"
    #             bot.send_message(message.chat.id, response_text)
    #             bot.send_message(message.chat.id, "\n/phone - еще раз\n"
    #                                               "/start - другие команды")
    #             print("использовал пробив номера")
    #         elif number.startswith("89") and len(number) == 11:
    #             url = "http://num.voxlink.ru/get/"
    #             querystring = {"num": "+7" + number[1:]}
    #             response = requests.get(url, params=querystring)
    #             data = response.json()
    #             operator = data.get("operator")
    #             region = data.get("region")
    #             old_operator = data.get("old_operator")
    #             response_text = f"Оператор: {operator}\nРегион: {region}\nСтарый оператор: {old_operator}"
    #             bot.send_message(message.chat.id, response_text)
    #             bot.send_message(message.chat.id, "\n/phone - еще раз\n"
    #                                               "/start - другие команды")
    #             print("использовал пробив номера")
    #         else:
    #             bot.send_message(message.chat.id, "Вы ввели неверный номер")
    #             handle_start(message)
    #     except Exception as e:
    #         print(f"Ошибка: {e}")
    #         bot.send_message(message.chat.id, 'Произошла ошибка. Выполняю команду /start.')
    #         time.sleep(1)
    #         start(message)

    # код для платного доступа
    def handle_phone_number1(message):

        try:
            number = message.text
            if number.startswith("+79") and len(number) == 12:
                url = "http://num.voxlink.ru/get/"
                querystring = {"num": number}
                response = requests.get(url, params=querystring)
                data = response.json()
                operator = data.get("operator")
                region = data.get("region")
                old_operator = data.get("old_operator")
                response_text = f"Оператор: {operator}\nРегион: {region}\nСтарый оператор: {old_operator}"
                bot.send_message(message.chat.id, response_text)
                bot.send_message(message.chat.id,
                                 "/start - другие команды")
                print("использовал номер телефона")
            elif number.startswith("89") and len(number) == 11:
                url = "http://num.voxlink.ru/get/"
                querystring = {"num": "+7" + number[1:]}
                response = requests.get(url, params=querystring)
                data = response.json()
                operator = data.get("operator")
                region = data.get("region")
                old_operator = data.get("old_operator")
                response_text = f"Оператор: {operator}\nРегион: {region}\nСтарый оператор: {old_operator}"
                bot.send_message(message.chat.id, response_text)
                bot.send_message(message.chat.id,
                                 "/start - другие команды")
                print("использовал номер телефона")
            else:
                bot.send_message(message.chat.id, "Вы ввели неверный номер")
                handle_start(message)
        except Exception as e:
            print(f"Ошибка: {e}")
            bot.send_message(message.chat.id, 'Произошла ошибка. Выполняю команду /start.')
            time.sleep(1)
            start(message)

    # @bot.message_handler(commands=['insta'])
    def handle_instagram_link(message):
        try:
            original_link = message.text
            new_link = re.sub(r'https://www\.instagram\.com/', 'https://ddinstagram.com/', original_link)

            bot.send_message(message.chat.id, new_link)
            bot.send_message(message.chat.id, "/start - другие команды")
            print("использовал инсту")
        except Exception as e:
            print(f"Ошибка: {e}")
            bot.send_message(message.chat.id, 'Произошла ошибка. Выполняю команду /start.')
            time.sleep(1)
            start(message)

    @bot.message_handler(commands=['start'])
    def start(message):
        try:
            markup = types.InlineKeyboardMarkup(row_width=1)
            orf = types.InlineKeyboardButton(text='Орфография', callback_data='/orf')
            film1 = types.InlineKeyboardButton(text='Фильмы', callback_data='/film')
            inst = types.InlineKeyboardButton(text='Скачать из Instargam', callback_data='/insta')
            phone1 = types.InlineKeyboardButton(text='💥Пробив номера💥', callback_data='/phone')
            passw = types.InlineKeyboardButton(text='Генератор паролей', callback_data='/password')
            virus = types.InlineKeyboardButton(text='💥Проверка на вирус💥', callback_data='/virus')
            wikip = types.InlineKeyboardButton(text='Wikipedia', callback_data='/wiki')
            text1 = types.InlineKeyboardButton(text='Перевод', callback_data='/text')
            # imager = types.InlineKeyboardButton(text='✅Проверка сайта✅', callback_data='/imager')
            pogoda = types.InlineKeyboardButton(text='💥Погода💥', callback_data='/pogoda')
            audio1 = types.InlineKeyboardButton(text='💥Голос робота💥', callback_data='/audio')
            cb = types.InlineKeyboardButton(text='Фото в черное-белое', callback_data='/chb')
            qr1 = types.InlineKeyboardButton(text='QR - код', callback_data='/qr')
            pesnya = types.InlineKeyboardButton(text='💥Текст песни💥', callback_data='/pesnya')
            botpay = types.InlineKeyboardButton(text='⭐Купить бота⭐', callback_data='/bots')
            yandexplus = types.InlineKeyboardButton(text='🔥Наш канал🔥', url='https://t.me/Humorhubb')
            yandexplus1 = types.InlineKeyboardButton(text='🔥Wildberries | Ozon | Hub🔥',
                                                     url='https://t.me/WildberriesOzonHub')

            markup.add(yandexplus, inst, pogoda, cb, passw, phone1, qr1, wikip, orf, virus, audio1,
                       pesnya, text1, film1, botpay)

            bot.send_message(chat_id=message.chat.id, text='Выберите кнопку:', reply_markup=markup)
        except Exception as e:
            print(f"Ошибка: {e}")
            bot.send_message(message.chat.id, 'Произошла ошибка. Выполняю команду /start.')
            start(message)

    # откл бота
    # @atexit.register
    # def send_notification():
    #     bot.send_message(YOUR_CHAT_ID, "Ваш бот выключился. Проверьте его статус.")

    def text(message):
        try:
            bot.send_message(message.chat.id, "Введите текст на любом языке:\n"
                                              "P.S Перевод осуществляется на русский язык")
            if message.text == '/exit':
                start(message)
            bot.register_next_step_handler(message, translate_message)
        except Exception as e:
            print(f"Ошибка: {e}")
            bot.send_message(message.chat.id, 'Произошла ошибка. Выполняю команду /start.')
            start(message)

    def translate_message(message):
        try:

            src = detect(message.text)

            # Задаем целевой язык
            dest = 'ru'
            # Берем полученное сообщение и переводим его
            translated_text = translator.translate(message.text, src=src, dest=dest).text
            # Отправляем переведенное сообщение
            bot.send_message(message.chat.id, translated_text)
            bot.send_message(message.chat.id, '/start - другие команды\n'
                                              '(кликабельно)')
            print(f"Использовал переводчик")

        except Exception as e:
            print(f"Ошибка: {e}")
            bot.send_message(message.chat.id, 'Произошла ошибка.')

    @bot.message_handler(commands=['pogoda'])
    def handle_weather_command(message):
        try:
            bot.send_message(message.chat.id, "Введите название города:")
            bot.register_next_step_handler(message, get_weather)
            print(f"Использовал погоду")


        except Exception as e:
            print(f"Ошибка: {e}")
            bot.send_message(message.chat.id, 'Произошла ошибка. Выполняю команду /start.')
            start(message)

    def get_weather(message):
        try:
            city = message.text.strip().lower()
            if not city.isdigit():
                res = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric")
                if res.status_code == 200:
                    data = json.loads(res.text)
                    q = data["main"]["temp"]
                    fee = data["main"]["feels_like"]
                    e = int(q)
                    sunrise = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
                    bot.reply_to(message, f"Сейчас погода в городе {city.capitalize()}: {e}℃\n"
                                          f"Влажность: {data['main']['humidity']}%\n"
                                          f"Скорость ветра: {data['wind']['speed']} м/c\n"
                                          f"Ощущается как: {fee}℃\n"
                                          f"Восход солнца: {sunrise.strftime('%H:%M:%S')}\n"
                                          f"/pogoda - еще раз прогноз\n"
                                          f"/start - другие команды\n"
                                          "(кликабельно)")
                    print("использовал погоду")
                else:
                    bot.send_message(message.chat.id, f"Такого города нет.\n"
                                                      "/pogoda - еще раз прогноз\n"
                                                      f"/start - другие команды\n"
                                                      "(кликабельно)")
            else:
                bot.send_message(message.chat.id, "Название города не должно содержать цифры.\n"
                                                  "/pogoda - еще раз прогноз")
        except Exception as e:
            print(f"Ошибка: {e}")
            bot.send_message(message.chat.id, 'Произошла ошибка. Выполняю команду /start.')
            start(message)

    # функция для поиска текста песни
    def search_song(message):
        try:
            song_name = message.text
            song = genius.search_song(song_name)
            if song:
                lyrics = song.lyrics
                bot.send_message(message.chat.id, lyrics)
                bot.send_message(message.chat.id, "/start - другие команды\n"
                                                  "(кликабельно)")
                print("использовал текст песни")


            else:
                bot.reply_to(message, "Попробуйте еще раз\n"
                                      "/start\n"
                                      "(кликабельно)")
        except Exception as e:
            bot.reply_to(message, "Упс, попробуйте еще раз\n"
                                  "/start\n"
                                  "(кликабельно)")

    def audio(message):
        try:
            bot.send_message(message.chat.id,
                             "Введите текст, который хотите превратить в аудио:\nP.S Озвучка только на руском языке)")
            bot.register_next_step_handler(message, convert_to_audio)
        except Exception as e:
            print(f"Ошибка: {e}")
            bot.send_message(message.chat.id, 'Произошла ошибка. Выполняю команду /start.')
            start(message)

    def convert_to_audio(message):
        try:
            text = message.text
            # Создаем аудио из текста с помощью Google Text-to-Speech
            speech = gTTS(text=text, lang='ru', slow=True)
            # Сохраняем аудио в файл 'audio.mp3'
            speech.save('audio.mp3')
            # Отправляем аудио пользователю
            audio = open('audio.mp3', 'rb')
            bot.send_audio(message.chat.id, audio)
            # Удаляем созданный файл после отправки аудио
            audio.close()
            os.remove('audio.mp3')
            print("использовал аудио")
            bot.send_message(message.chat.id, "/start - другие команды\n"
                                              "(кликабельно)")
        except Exception as e:
            print(f"Ошибка: {e}")
            bot.send_message(message.chat.id, 'Произошла ошибка. Выполняю команду /start.')
            start(message)

    def getwiki(s):
        try:
            ny = wikipedia.page(s)
            # Получаем первую тысячу символов
            wikitext = ny.content[:1000]
            # Разделяем по точкам
            wikimas = wikitext.split('.')
            # Отбрасываем всЕ после последней точки
            wikimas = wikimas[:-1]
            # Создаем пустую переменную для текста
            wikitext2 = ''
            # Проходимся по строкам, где нет знаков «равно» (то есть все, кроме заголовков)
            for x in wikimas:
                if not ('==' in x):
                    # Если в строке осталось больше трех символов, добавляем ее к нашей переменной и возвращаем утерянные при разделении строк точки на место
                    if (len((x.strip())) > 3):
                        wikitext2 = wikitext2 + x + '.'
                else:
                    break
            # Теперь при помощи регулярных выражений убираем разметку
            wikitext2 = re.sub('\([^()]*\)', '', wikitext2)
            wikitext2 = re.sub('\([^()]*\)', '', wikitext2)
            wikitext2 = re.sub('\{[^\{\}]*\}', '', wikitext2)
            # Возвращаем текстовую строку
            return wikitext2
        # Обрабатываем исключение, которое мог вернуть модуль wikipedia при запросе
        except Exception as e:
            return 'В энциклопедии нет информации об этом'

    # @bot.message_handler(commands=["wiki"])
    def wiki(message):
        bot.send_message(message.chat.id, "Отправьте мне любое слово либо фразу, и я найду их значения в Wikipedia\n"
                                          "\n/exit - выйти из 'Википедии' в меню\n"
                                          "(кликабельно)")
        bot.register_next_step_handler(message, handle_text)
        print("использовал вики")

    def handle_text(message):
        try:
            if message.text == '/exit':
                start(message)
            else:
                bot.send_message(message.chat.id, getwiki(message.text))
                bot.send_message(message.chat.id, "/start - другие команды\n"
                                                  "(кликабельно)")
                print("использовал вики")
        except Exception as e:
            print(f"Ошибка: {e}")
            bot.send_message(message.chat.id, 'Произошла ошибка выполняю команду /start')
            start(message)

    @bot.message_handler(commands=['qr'])
    def qr(message):
        bot.send_message(message.chat.id, "Отправьте ссылку, в ответ получите QR код этой ссылки ")
        bot.register_next_step_handler(message, generate_qr_code)
        print("использовал qr")

    def generate_qr_code(message):
        try:
            # Получаем ссылку из сообщения пользователя
            url = message.text

            # Генерируем QR-код
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(url)
            qr.make(fit=True)

            img = qr.make_image(fill_color="black", back_color="white")
            img_bytes_io = BytesIO()
            img.save(img_bytes_io)

            # Отправляем QR-код в ответ на сообщение пользователя
            bot.send_photo(message.chat.id, img_bytes_io.getvalue())
            bot.send_message(message.chat.id, "/qr - еще QR - код\n"
                                              "/start - другие команды\n"
                                              "(кликабельно)")
            print("использовал qr")
        except Exception as e:
            print(f"Ошибка: {e}")
            bot.send_message(message.chat.id, 'Произошла ошибка выполняю команду /start')
            start(message)

    speller = YandexSpeller()

    def orf(message):
        bot.send_message(message.chat.id, "Введи слово, или текст для проверки на ошибку:\n"
                                          "/exit - выйти из 'Орфографии' в меню\n"
                                          "(кликабельно)")
        bot.register_next_step_handler(message, check_spelling)
        print("использовал орф")

    def check_spelling(message):
        try:
            text = message.text
            if message.text == '/exit':
                start(message)
            else:  # Проверяем текст на орфографические ошибки
                result = speller.spell(text)
                if result:
                    # Формируем сообщение с исправленными словами
                    response = "Исправленные слова: "
                    for word in result:
                        response = response + f"{word['word']} -> {word['s'][0]}\n"
                    if response == "Исправленные слова: ":
                        bot.send_message(message.chat.id, "В вашем тексте, нет ошибок\n"
                                                          "\n/start - другие команды\n"
                                                          "(кликабельно)")
                    else:
                        # Отправляем сообщение с исправленными словами
                        bot.send_message(message.chat.id, response)
                        bot.send_message(message.chat.id, "/start - другие команды\n"
                                                          "(кликабельно)")
                else:
                    # Если ошибок нет, отправляем сообщение об этом
                    bot.send_message(message.chat.id, "Ошибок в тексте не найдено.")
        except Exception as e:
            print(f"Ошибка: {e}")
            bot.send_message(message.chat.id, 'Произошла ошибка.\n'
                                              'Выполняю команду /start')
            start(message)

    def photo_handler(message):
        try:
            if message.text == "/start":
                start(message)

            else:
                file_info = bot.get_file(message.photo[-1].file_id)
                downloaded_file = bot.download_file(file_info.file_path)

                with open("image.jpg", 'wb') as new_file:
                    new_file.write(downloaded_file)

                img = Image.open("image.jpg")
                img = img.convert("L")

                img.save("black_and_white_image.jpg")

                with open("black_and_white_image.jpg", 'rb') as photo:
                    bot.send_photo(message.chat.id, photo)
                    bot.send_message(message.chat.id, "/start - другие команды\n"
                                                      "(кликабельно)")
                    print("использовал чб")

                # Удаляем отправленные фото
                os.remove("image.jpg")
                os.remove("black_and_white_image.jpg")
        except Exception as e:
            print(f"Ошибка: {e}")
            bot.send_message(message.chat.id, 'Произошла ошибка. Выполняю команду /start')
            start(message)

    # проверка на вирусы
    def handle_document(message):
        try:
            document = message.document if message.document else message.photo[0]

            if document.file_size <= 50 * 1024 * 1024:  # Проверка размера файла (не более 50 МБ)
                file_info = bot.get_file(document.file_id)
                file_url = f'https://api.telegram.org/file/bot{bot}/{file_info.file_path}'

                file_content = requests.get(file_url).content
                file_hash = hashlib.md5(file_content).hexdigest()
                vt_url = f'https://www.virustotal.com/api/v3/files/{file_hash}'
                headers = {
                    'x-apikey': virus_total_api_key
                }

                response = requests.get(vt_url, headers=headers)

                if response.status_code == 200:
                    vt_data = response.json()
                    if vt_data['data']['attributes']['last_analysis_stats']['malicious'] > 0:
                        bot.reply_to(message, 'Файл содержит вирус!')
                    else:
                        bot.reply_to(message, 'Файл не содержит вирусов\n'
                                              '/start - другие команды')
                        print("использовал вирус")

                else:
                    bot.reply_to(message, 'Ошибка при проверке файла\n'
                                          '/start - другие команды')
            else:
                bot.reply_to(message, 'Размер файла превышает 50 МБ\n'
                                      '/start - другие команды')
        except Exception as e:
            print(f"Ошибка: {e}")
            bot.send_message(message.chat.id, 'Произошла ошибка. Выполняю команду /start.')
            start(message)

    @bot.callback_query_handler(func=lambda call: True)
    def callback_inline(call):
        try:
            # user_id = str(call.message.chat.id)
            # if is_user_allowed(user_id):
            #     if call.data == '/orf':
            #         bot.answer_callback_query(call.id, 'Выполняю')
            #         bot.send_message(chat_id=call.message.chat.id,
            #                          text="Введи слово, или текст для проверки на ошибку:\n/exit - выйти из 'Орфографии' в меню")
            #         bot.register_next_step_handler(call.message, check_spelling)
            #         print("использовал орф")
            #     elif call.data == '/pesnya':
            #         bot.answer_callback_query(call.id, 'Выполняю')
            #         bot.send_message(chat_id=call.message.chat.id,
            #                          text="Просто отправь название песни, а я выдам ее текст.")
            #         bot.register_next_step_handler(call.message, search_song)
            #         print("использовал текст песни")
            #     elif call.data == '/virus':
            #         bot.answer_callback_query(call.id, 'Выполняю')
            #         bot.send_message(chat_id=call.message.chat.id,
            #                          text="Отправь файл, или документ который хочешь проверить на вирусы.\n"
            #                               "Важно: размер файла не должен превышать 50 мб.")
            #         bot.register_next_step_handler(call.message, handle_document)
            #         print("использовал вирус")
            #     elif call.data == '/film':
            #         bot.answer_callback_query(call.id, 'Выполняю')
            #         bot.send_message(call.message.chat.id, "Вот подборки фильмов, которые сейчас идут в кинотеатрах:")
            #         time.sleep(1)
            #         bot.send_message(call.message.chat.id,
            #                          "Мальчик и птица: https://www.kinoafisha.info/movies/8353726/")
            #         bot.send_message(call.message.chat.id, "Ёлки 10: https://www.kinoafisha.info/movies/8371360/")
            #         bot.send_message(call.message.chat.id,
            #                          "Холоп 2: https://www.kinoafisha.info/movies/8367413/")
            #         bot.send_message(call.message.chat.id,
            #                          "Три богатыря и Пуп Земли: https://www.kinoafisha.info/movies/8370804/")
            #         bot.send_message(call.message.chat.id, "Опенгеймер: https://www.kinoafisha.info/movies/8365507/")
            #         bot.send_message(call.message.chat.id, "Наполеон: https://www.kinoafisha.info/movies/8365827/")
            #         bot.send_message(call.message.chat.id,
            #                          "Елки 10: https://www.kinoafisha.info/movies/8371360/")
            #         bot.send_message(call.message.chat.id,
            #                          "Феррари: https://www.kinoafisha.info/movies/8360869/")
            #         bot.send_message(call.message.chat.id,
            #                          "Вредная привычка: https://www.kinoafisha.info/movies/8371824/")
            #         bot.send_message(call.message.chat.id,
            #                          "Тёща: https://www.kinoafisha.info/movies/8372155/")
            #         bot.send_message(call.message.chat.id, "/start - вернуться в меню\n"
            #                                                "(кликабельно)")
            #
            #
            #     elif call.data == "/text":
            #         bot.answer_callback_query(call.id, 'Выполняю')
            #         bot.send_message(chat_id=call.message.chat.id,
            #                          text="Введите текст на любом языке:\nP.S Перевод осуществляется на русский язык")
            #         bot.register_next_step_handler(call.message, translate_message)
            #     elif call.data == "/password":
            #         bot.answer_callback_query(call.id, 'Выполняю')
            #         password(call.message)
            #     elif call.data == "/chb":
            #         bot.answer_callback_query(call.id, 'Выполняю')
            #         bot.send_message(chat_id=call.message.chat.id,
            #                          text="Я делаю из цветных фото = черно-белое. Пришли мне фотографию.")
            #         bot.register_next_step_handler(call.message, photo_handler)
            #     elif call.data == "/pogoda":
            #         bot.answer_callback_query(call.id, 'Выполняю')
            #         bot.send_message(chat_id=call.message.chat.id, text="Введите название города:")
            #         bot.register_next_step_handler(call.message, get_weather)
            #     elif call.data == "/wiki":
            #         bot.answer_callback_query(call.id, 'Выполняю')
            #         bot.send_message(chat_id=call.message.chat.id,
            #                          text="Отправьте мне любое слово либо фразу, и я найду их значения в Wikipedia\n"
            #                               "\n/exit - выйти из 'Википедии' в меню")
            #         bot.register_next_step_handler(call.message, handle_text)
            #     elif call.data == "/audio":
            #         bot.answer_callback_query(call.id, 'Выполняю')
            #         bot.send_message(chat_id=call.message.chat.id,
            #                          text="Введите текст, который хотите превратить в аудио:\nP.S Озвучка только на руском языке)")
            #         bot.register_next_step_handler(call.message, convert_to_audio)
            #     elif call.data == "/phone":
            #         bot.answer_callback_query(call.id, 'Выполняю')
            #         bot.send_message(chat_id=call.message.chat.id,
            #                          text="Введите номер телефона:\nПример: +79XXXXXXXXX или 89XXXXXXXXX")
            #         bot.register_next_step_handler(call.message, handle_phone_number1)
            #     elif call.data == "/qr":
            #         bot.answer_callback_query(call.id, 'Выполняю')
            #         bot.send_message(chat_id=call.message.chat.id,
            #                          text="Отправьте ссылку, в ответ получите QR код этой ссылки ")
            #         bot.register_next_step_handler(call.message, generate_qr_code)
            #     # elif call.data == "/imager":
            #     #     bot.answer_callback_query(call.id, 'Выполняю')
            #     #     bot.send_message(chat_id=call.message.chat.id,
            #     #                      text="Пришли мне ссылку любого сайта, и я отправлю тебе скриншот этой страницы.\n"
            #     #                           "❗️Это полезно, если ты не хочешь попасть на сайт мошенников")
            #     #     bot.register_next_step_handler(call.message, process_website)
            #     elif call.data == "/bots":
            #         bot.answer_callback_query(call.id, 'Выполняю')
            #         bot.send_message(chat_id=call.message.chat.id, text="⭐Для покупки ботов, используйте команды:⭐\n"
            #                                                             "/bot1(клик) - Бот погоды\n"
            #                                                             "/bot2(клик) - Бот Генератор QR - кодов\n"
            #                                                             "/bot3(клик) - Бот Автопостинга\n"
            #                                                             "/bot4(клик - Бот Анонимного чата")
            #         if call.data == "/bot1":
            #             bot.register_next_step_handler(call.message, bot1)
            #         if call.data == "/bot2":
            #             bot.register_next_step_handler(call.message, bot2)
            #         if call.data == "/bot3":
            #             bot.register_next_step_handler(call.message, bot3)
            #         if call.data == "/bot4":
            #             bot.register_next_step_handler(call.message, bot4)
            # else:
            if call.data == "/chb":
                bot.answer_callback_query(call.id, 'Выполняю')
                bot.send_message(chat_id=call.message.chat.id,
                                 text="Я делаю из цветных фото = чёрно-белое. Пришли мне фотографию.")
                bot.register_next_step_handler(call.message, photo_handler)
            # elif call.data == "/info":
            #     info()
            # elif call.data == "/pay":
            #     bot.answer_callback_query(call.id, 'Выполняю')
            #     start_payment()
            #     print("хотел купить подписку 99р")

            if call.data == '/orf':
                bot.answer_callback_query(call.id, 'Выполняю')
                bot.send_message(chat_id=call.message.chat.id,
                                 text="Введи слово, или текст для проверки на ошибку\n"
                                      "Слова принимаются на русском, или английском языке:\n/exit - выйти из 'Орфографии' в меню")
                bot.register_next_step_handler(call.message, check_spelling)
                print("использовал орф")
            elif call.data == '/pesnya':
                bot.answer_callback_query(call.id, 'Выполняю')
                bot.send_message(chat_id=call.message.chat.id,
                                 text="Просто отправь название песни, а я выдам ее текст.")
                bot.register_next_step_handler(call.message, search_song)
                print("использовал текст песни")
            elif call.data == '/virus':
                bot.answer_callback_query(call.id, 'Выполняю')
                bot.send_message(chat_id=call.message.chat.id,
                                 text="Отправь файл, или документ который хочешь проверить на вирусы.\n"
                                      "Важно: размер файла не должен превышать 50 мб.")
                bot.register_next_step_handler(call.message, handle_document)
                print("использовал вирус")
            elif call.data == '/film':
                bot.answer_callback_query(call.id, 'Выполняю')
                bot.send_message(call.message.chat.id, "Вот подборки фильмов, которые сейчас идут в кинотеатрах:")
                time.sleep(1)
                bot.send_message(call.message.chat.id,
                                 "Мальчик и птица: https://www.kinoafisha.info/movies/8353726/")
                bot.send_message(call.message.chat.id,
                                 "Холоп 2: https://www.kinoafisha.info/movies/8367413/")
                bot.send_message(call.message.chat.id,
                                 "Вонка: https://www.kinoafisha.info/movies/8364454/")
                bot.send_message(call.message.chat.id,
                                 "Бременские музыканты: https://www.kinoafisha.info/movies/8328908/")
                bot.send_message(call.message.chat.id,
                                 "Мастер и Маргарита: https://www.kinoafisha.info/movies/8365280/")
                bot.send_message(call.message.chat.id,
                                 "Из гулбины: https://www.kinoafisha.info/movies/8371079/")
                bot.send_message(call.message.chat.id,
                                 "Феррари: https://www.kinoafisha.info/movies/8360869/")
                bot.send_message(call.message.chat.id,
                                 "Три богатыря и Пуп Земли: https://www.kinoafisha.info/movies/8370804/")
                bot.send_message(call.message.chat.id,
                                 "Аквамен и потерянное царство: https://www.kinoafisha.info/movies/8355886/")
                bot.send_message(call.message.chat.id, "/start - вернуться в меню\n"
                                                       "(кликабельно)")
                print("использовал фильмы")

            elif call.data == "/text":
                bot.answer_callback_query(call.id, 'Выполняю')
                bot.send_message(chat_id=call.message.chat.id,
                                 text="Введите текст на любом языке:\nP.S Перевод осуществляется на русский язык")
                bot.register_next_step_handler(call.message, translate_message)
            elif call.data == "/password":
                bot.answer_callback_query(call.id, 'Выполняю')
                password(call.message)
            # elif call.data == "/chb":
            #     bot.answer_callback_query(call.id, 'Выполняю')
            #     bot.send_message(chat_id=call.message.chat.id,
            #                      text="Я делаю из цветных фото = черно-белое. Пришли мне фотографию.")
            #     bot.register_next_step_handler(call.message, photo_handler)
            elif call.data == "/pogoda":
                bot.answer_callback_query(call.id, 'Выполняю')
                bot.send_message(chat_id=call.message.chat.id, text="Введите название города:")
                bot.register_next_step_handler(call.message, get_weather)
            elif call.data == "/wiki":
                bot.answer_callback_query(call.id, 'Выполняю')
                bot.send_message(chat_id=call.message.chat.id,
                                 text="Отправьте мне любое слово либо фразу, и я найду их значения в Wikipedia\n"
                                      "\n/exit - выйти из 'Википедии' в меню")
                bot.register_next_step_handler(call.message, handle_text)
            elif call.data == "/audio":
                bot.answer_callback_query(call.id, 'Выполняю')
                bot.send_message(chat_id=call.message.chat.id,
                                 text="Введите текст, который хотите превратить в аудио:\nP.S Озвучка только на руском языке)")
                bot.register_next_step_handler(call.message, convert_to_audio)
            elif call.data == "/insta":
                bot.answer_callback_query(call.id, 'Выполняю')
                bot.send_message(chat_id=call.message.chat.id,
                                 text='Введите ссылку на "видео", "reels", "историю", или "пост из Instagram", и я отправлю вам медиа файл\n'
                                      '\n❗Важно, аккаунт должет быть открытым')
                bot.register_next_step_handler(call.message, handle_instagram_link)
            elif call.data == "/phone":
                bot.answer_callback_query(call.id, 'Выполняю')
                bot.send_message(chat_id=call.message.chat.id,
                                 text="Введите номер телефона:\nПример: +79XXXXXXXXX или 89XXXXXXXXX")
                bot.register_next_step_handler(call.message, handle_phone_number1)
            elif call.data == "/qr":
                bot.answer_callback_query(call.id, 'Выполняю')
                bot.send_message(chat_id=call.message.chat.id,
                                 text="Отправьте ссылку, в ответ получите QR код этой ссылки ")
                bot.register_next_step_handler(call.message, generate_qr_code)
            # elif call.data == "/imager":
            #     bot.answer_callback_query(call.id, 'Выполняю')
            #     bot.send_message(chat_id=call.message.chat.id,
            #                      text="Пришли мне ссылку любого сайта, и я отправлю тебе скриншот этой страницы.\n"
            #                           "❗️Это полезно, если ты не хочешь попасть на сайт мошенников")
            #     bot.register_next_step_handler(call.message, process_website)

            elif call.data == "/pogoda":
                bot.answer_callback_query(call.id, 'Выполняю')
                bot.send_message(chat_id=call.message.chat.id, text="Введите название города:\n")
                bot.register_next_step_handler(call.message, get_weather)
                print("использовал погоду")
            # elif call.data == "/phone":
            #     bot.answer_callback_query(call.id, 'Выполняю')
            #     bot.send_message(chat_id=call.message.chat.id, text="Введите номер телефона:\nПример: +79XXXXXXXXX или 89XXXXXXXXX")
            #     bot.register_next_step_handler(call.message, handle_phone_number)
            #     print("использовал пробив номера")

            elif call.data == "/bots":
                print("использовал покупку ботов")
                bot.answer_callback_query(call.id, 'Выполняю')
                bot.send_message(chat_id=call.message.chat.id, text="⭐Для покупки ботов, используйте команды:⭐\n"
                                                                    "/bot1(клик) - Бот погоды\n"
                                                                    "/bot2(клик) - Бот генератор QR - кода\n"
                                                                    "/bot3(клик) - Бот Автопостинга\n"
                                                                    "/bot4(клик) - Бот Анонимного чата")
            # else:
            #     bot.answer_callback_query(call.id, 'Выполнено')
            #     bot.send_message(chat_id=call.message.chat.id, text="У вас нет подписки 😔\n"
            #                                                         "Стоимость подписки 199 р \n"
            #                                                         '🎁"Погода"  "Фото в ЧБ"  "Проверка сайта"🎁 работают без подписки\n'
            #                                                         "\n/info - что дает подписка❓ (кликабельно)\n"
            #                                                         "/pay - оплатить (кликабельно)")
            # if call.data == "/text":
            #     bot.send_message(chat_id=call.message.chat.id,
            #                      text="Введите текст на любом языке:\nP.S Перевод осуществляется на русский язык")
            #     bot.register_next_step_handler(call.message, translate_message)
            #     print("использовал перевод")
            # if call.data == '/film':
            #     bot.send_message(call.message.chat.id,
            #                      "Вот подборки фильмов, которые сейчас идут в кинотеатрах:")
            #     time.sleep(1)
            #     print("использовал фмльмы")
            #     bot.send_message(call.message.chat.id,
            #                      "Миссия: невыполнима. Смертельная расплата. Часть 1: https://www.kinoafisha.info/movies/8355846/")
            #     bot.send_message(call.message.chat.id, "Барби: https://www.kinoafisha.info/movies/8324026/")
            #     bot.send_message(call.message.chat.id,
            #                      "Пять ночей с Фредди: https://www.kinoafisha.info/movies/8367896/")
            #     bot.send_message(call.message.chat.id,
            #                      "Легендо о самбо: https://www.kinoafisha.info/movies/8371320/")
            #     bot.send_message(call.message.chat.id,
            #                      "Опенгеймер: https://www.kinoafisha.info/movies/8365507/")
            #     bot.send_message(call.message.chat.id,
            #                      "Наполеон: https://www.kinoafisha.info/movies/8365827/")
            #     bot.send_message(call.message.chat.id,
            #                      "Капитан Марвел 2: https://www.kinoafisha.info/movies/8356868/")
            #     bot.send_message(call.message.chat.id,
            #                      "Бугимен. Начало легенды: https://www.kinoafisha.info/movies/8372203/")
            #     bot.send_message(call.message.chat.id,
            #                      "Человек ниоткуда: https://www.kinoafisha.info/movies/8371558/")
            #     bot.send_message(call.message.chat.id,
            #                      "Голодные игры: Баллада о певчих птицах и змеях: https://www.kinoafisha.info/movies/8367011/")
            #     bot.send_message(call.message.chat.id,
            #                      "Катастрофа: https://www.kinoafisha.info/movies/8371521/")
            #     bot.send_message(call.message.chat.id, "/start - вернуться в меню\n"
            #                                            "(кликабельно)")
            # if call.data == '/virus':
            #     bot.send_message(chat_id=call.message.chat.id,
            #                      text="Отправь файл, или документ который хочешь проверить на вирусы.\n"
            #                           "Важно: размер файла не должен превышать 50 мб.")
            #     bot.register_next_step_handler(call.message, handle_document)
            # if call.data == '/pesnya':
            #     bot.send_message(chat_id=call.message.chat.id,
            #                      text="Просто отправь название песни, а я выдам ее текст.")
            #     bot.register_next_step_handler(call.message, search_song)
            # if call.data == "/audio":
            #      bot.send_message(chat_id=call.message.chat.id, text="Введите текст, который хотите превратить в аудио:\nP.S Озвучка только на руском языке)")
            #      bot.register_next_step_handler(call.message, convert_to_audio)
            #      print("использовал аудио")
            # if call.data == '/orf':
            #     bot.send_message(chat_id=call.message.chat.id, text="Введи слово, или текст для проверки на ошибку:\n/exit - выйти из 'Орфографии' в меню")
            #     bot.register_next_step_handler(call.message, check_spelling)
            #     print("использовал орф")

        except Exception as e:
            print(f"Ошибка: {e}")
            bot.send_message(chat_id=call.message.chat.id, text='Произошла ошибка. Выполните команду /start.')

    # Обработчик команды /bot1

    @bot.message_handler(commands=['bot1'])
    def bot1(message):
        bot.send_message(message.chat.id, text="После оплаты бота вам будет доступно следующее:\n"
                                               "\n● Полный исходный код бота, который будет показывать погоду в любом городе мира и еще 4 параметра к ней.\n"
                                               "● Бот будет доступен вам на 4 языках програмирования: 💻Python, C++, Java, С#💻\n"
                                               "● После оплаты, бот отправит вам 5 смс, в них будут предоставленны четыре txt файла с кодом, и 1 файл с интсрукцией.\n"
                                               "❗Перед покупкой, вы можете протестировать функционал вашего будущего бота, в нашем боте,"
                                               ' нажав кнопку "Погода". У вас будет такой-же функционал как у нас.')
        time.sleep(2)
        bot.send_message(message.chat.id, text="Введите 'Да' или 'нет' для оплаты:")
        bot.register_next_step_handler(message, bot11)

    def bot11(message):
        try:
            payment = None
            user_id = message.chat.id
            if message.text.lower() == "да" or message.text.lower() == "Да":
                payment = Payment.create({
                    "amount": {
                        "value": "300.00",
                        "currency": "RUB"
                    },
                    "confirmation": {
                        "type": "redirect",
                        "return_url": "https://t.me/WalleRobott_bot"
                    },
                    "capture": True,
                    "description": 'Оплата покупки "Бота погоды"'
                })
                payment_url = payment.confirmation.confirmation_url
                keyboard = types.InlineKeyboardMarkup()
                url_button = types.InlineKeyboardButton(text='Нажми на меня', url=payment_url)
                keyboard.add(url_button)
                bot.send_message(message.chat.id,
                                 f'Оплатите 300 рублей, чтобы получить исходный код "Бота погоды", нажав на кнопку ниже:\n',
                                 reply_markup=keyboard)

                threading.Thread(target=payment_check1, args=(payment.id, user_id)).start()
            else:
                start(message)

        except Exception as e:
            print(f"Ошибка: {e}")
            bot.send_message(message.chat.id, 'Произошла ошибка. Выполняю команду /start.')
            start(message)

    def payment_check1(payment_id, user_id):
        try:
            valid_answer = False
            while not valid_answer:
                payment = Payment.find_one(payment_id)
                if payment.status == 'succeeded':
                    files = os.listdir(pogoda)
                    for file_name in files:
                        file_path = os.path.join(pogoda, file_name)
                        with open(file_path, 'rb') as file:
                            bot.send_document(user_id, file)
                    bot.send_message(YOUR_CHAT_ID, "У вас купили бота за 300р")
                    valid_answer = True
                elif payment.status == 'canceled':
                    bot.send_message(user_id, "Оплата отменена!")
                    valid_answer = True
                else:
                    time.sleep(5)
        except Exception as e:
            print(f"Ошибка: {e}")
            bot.send_message(user_id, 'Произошла ошибка.\nВыполните команду /start')

    @bot.message_handler(commands=['bot2'])
    def bot2(message):
        bot.send_message(message.chat.id, text="После оплаты бота вам будет доступно следующее:\n"
                                               "\n● Полный исходный код бота который из ссылки, или фразы делает QR - код, будет доступен вам на 4 языках програмирования: 💻Python,  C++,  Java,  С#💻\n"
                                               "● После оплаты бот отправит вам 5 смс в них будут предоставленны четыре txt файла с кодом, и 1 файл с интсрукцией.\n"
                                               "❗Перед покупкой, вы можете протестировать функционал вашего будущего бота, в нашем боте,"
                                               ' нажав кнопку "QR - код". У вас будет такой-же функционал как у нас.\n')
        time.sleep(2)
        bot.send_message(message.chat.id, text="Введите 'Да' или 'нет' для оплаты:")
        bot.register_next_step_handler(message, bot22)

    def bot22(message):
        try:
            payment = None
            user_id = message.chat.id
            if message.text.lower() == "да" or message.text.lower() == "Да":
                payment = Payment.create({
                    "amount": {
                        "value": "450.00",
                        "currency": "RUB"
                    },
                    "confirmation": {
                        "type": "redirect",
                        "return_url": "https://t.me/WalleRobott_bot"
                    },
                    "capture": True,
                    "description": 'Оплата покупки "Бота генератор QR - кодов"'
                })
                payment_url = payment.confirmation.confirmation_url
                keyboard = types.InlineKeyboardMarkup()
                url_button = types.InlineKeyboardButton(text='Нажми на меня', url=payment_url)
                keyboard.add(url_button)
                bot.send_message(message.chat.id,
                                 f'Оплатите 450 рублей, чтобы получить исходный код "Бота генератор QR - кода", нажав на кнопку ниже:\n',
                                 reply_markup=keyboard)

                threading.Thread(target=payment_check2, args=(payment.id, user_id)).start()
            else:
                start(message)

        except Exception as e:
            print(f"Ошибка: {e}")
            bot.send_message(message.chat.id, 'Произошла ошибка. Выполняю команду /start.')
            start(message)

    def payment_check2(payment_id, user_id):
        try:
            valid_answer = False
            while not valid_answer:
                payment = Payment.find_one(payment_id)
                if payment.status == 'succeeded':
                    files = os.listdir(qrrr)
                    for file_name in files:
                        file_path = os.path.join(qrrr, file_name)
                        with open(file_path, 'rb') as file:
                            bot.send_document(user_id, file)
                    bot.send_message(YOUR_CHAT_ID, "У вас купили бота за 450р")
                    valid_answer = True
                elif payment.status == 'canceled':
                    bot.send_message(user_id, "Оплата отменена!")
                    valid_answer = True
                else:
                    time.sleep(5)
        except Exception as e:
            print(f"Ошибка: {e}")
            bot.send_message(user_id, 'Произошла ошибка.\nВыполните команду /start')

    @bot.message_handler(commands=['bot3'])
    def bot3(message):
        bot.send_message(message.chat.id, text="После оплаты бота вам будет доступно следующее:\n"
                                               "\n● Полный исходный код бота который публикует посты в указанный вами телеграмм канал, с указанием даты, времени, текста и картинки сообщения.\n"
                                               "● Исходный код будет доступен вам на 4 языках програмирования: 💻Python,  C++,  Java,  С#💻\n"
                                               "● После оплаты, бот отправит вам 5 смс, в них будут предоставленны четыре txt файла с кодом, и 1 файл с интсрукцией.\n")
        time.sleep(2)
        bot.send_message(message.chat.id, text="Введите 'Да' или 'нет' для оплаты:")
        bot.register_next_step_handler(message, bot33)

    def bot33(message):
        try:
            payment = None
            user_id = message.chat.id
            if message.text.lower() == "да" or message.text.lower() == "Да":
                payment = Payment.create({
                    "amount": {
                        "value": "900.00",
                        "currency": "RUB"
                    },
                    "confirmation": {
                        "type": "redirect",
                        "return_url": "https://t.me/WalleRobott_bot"
                    },
                    "capture": True,
                    "description": 'Оплата покупки "Бота автопостинга"'
                })
                payment_url = payment.confirmation.confirmation_url
                keyboard = types.InlineKeyboardMarkup()
                url_button = types.InlineKeyboardButton(text='Нажми на меня', url=payment_url)
                keyboard.add(url_button)
                bot.send_message(message.chat.id,
                                 f'Оплатите 900 рублей, чтобы получить исходный код "Бота автопостинга", нажав на кнопку ниже:\n',
                                 reply_markup=keyboard)

                threading.Thread(target=payment_check3, args=(payment.id, user_id)).start()
            else:
                start(message)

        except Exception as e:
            print(f"Ошибка: {e}")
            bot.send_message(message.chat.id, 'Произошла ошибка. Выполняю команду /start.')
            start(message)

    def payment_check3(payment_id, user_id):
        try:
            valid_answer = False
            while not valid_answer:
                payment = Payment.find_one(payment_id)
                if payment.status == 'succeeded':
                    files = os.listdir(avtopost)
                    for file_name in files:
                        file_path = os.path.join(avtopost, file_name)
                        with open(file_path, 'rb') as file:
                            bot.send_document(user_id, file)
                    bot.send_message(YOUR_CHAT_ID, "У вас купили бота за 999р")
                    valid_answer = True
                elif payment.status == 'canceled':
                    bot.send_message(user_id, "Оплата отменена!")
                    valid_answer = True
                else:
                    time.sleep(5)
        except Exception as e:
            print(f"Ошибка: {e}")
            bot.send_message(user_id, 'Произошла ошибка.\nВыполните команду /start')

    @bot.message_handler(commands=['bot4'])
    def bot4(message):
        bot.send_message(message.chat.id, text='После оплаты бота вам будет доступно следующее:\n'
                                               '\n● Полный исходный код бота "Анонимного чата", с неограниченным количеством собеседников. В боте будет команда /stop, чтобы остановить беседу и поменять собеседника.\n'
                                               "● Бот будет доступен вам на 3 языках програмирования: 💻Python, C++, С#💻\n"
                                               '● После оплаты, бот отправит вам 4 смс, в них будут предоставленны три txt файла с кодом, и 1 файл с интсрукцией.\n'
                         )
        time.sleep(2)
        bot.send_message(message.chat.id, text="Введите 'Да' или 'нет' для оплаты:")
        bot.register_next_step_handler(message, bot44)

    def bot44(message):
        try:
            payment = None
            user_id = message.chat.id
            if message.text.lower() == "да" or message.text.lower() == "Да":
                payment = Payment.create({
                    "amount": {
                        "value": "700.00",
                        "currency": "RUB"
                    },
                    "confirmation": {
                        "type": "redirect",
                        "return_url": "https://t.me/WalleRobott_bot"
                    },
                    "capture": True,
                    "description": 'Оплата покупки "Бота Анонимного чата"'
                })
                payment_url = payment.confirmation.confirmation_url
                keyboard = types.InlineKeyboardMarkup()
                url_button = types.InlineKeyboardButton(text='Нажми на меня', url=payment_url)
                keyboard.add(url_button)
                bot.send_message(message.chat.id,
                                 f'Оплатите 700 рублей, чтобы получить исходный код "Бота Анонимного чата", нажав на кнопку ниже:\n',
                                 reply_markup=keyboard)

                threading.Thread(target=payment_check4, args=(payment.id, user_id)).start()
            else:
                start(message)

        except Exception as e:
            print(f"Ошибка: {e}")
            bot.send_message(message.chat.id, 'Произошла ошибка. Выполняю команду /start.')
            start(message)

    def payment_check4(payment_id, user_id):
        try:
            valid_answer = False
            while not valid_answer:
                payment = Payment.find_one(payment_id)
                if payment.status == 'succeeded':
                    files = os.listdir(chata)
                    for file_name in files:
                        file_path = os.path.join(chata, file_name)
                        with open(file_path, 'rb') as file:
                            bot.send_document(user_id, file)
                    bot.send_message(YOUR_CHAT_ID, "У вас купили бота за 700р")
                    valid_answer = True
                elif payment.status == 'canceled':
                    bot.send_message(user_id, "Оплата отменена!")
                    valid_answer = True
                else:
                    time.sleep(5)
        except Exception as e:
            print(f"Ошибка: {e}")
            bot.send_message(user_id, 'Произошла ошибка.\nВыполните команду /start')

    @bot.message_handler(commands=['bots'])
    def boot_pay(message):
        try:
            markup = types.InlineKeyboardMarkup(row_width=1)
            bot1111 = types.InlineKeyboardButton(text='Бот погоды', callback_data='/botpog')
            bot2 = types.InlineKeyboardButton(text='Из текста в аудио', callback_data='/ta')
            bot3 = types.InlineKeyboardButton(text='Отложенный постинг', callback_data='/anonim')
            markup.add(bot1111, bot2, bot3)
            bot.send_message(chat_id=message.chat.id, text='Выберите действие:', reply_markup=markup)
        except Exception as e:
            print(f"Ошибка: {e}")
            bot.send_message(chat_id=message.chat.id, text='Произошла ошибка.\nВыполните команду /start')

    # @bot.message_handler(commands=['info'])
    # def info(message):
    #     bot.send_message(message.chat.id,
    #                      text='\n❗ Без подписки вам будут доступны только: "Погода"  "Фото в ЧБ"  "Проверка сайта".\n'
    #                           '\nОплачивая подписку в нашем боте вы получаете:\n'
    #                           "● Пожизненный доступ ко всем командам бота (подписка выдается навсегда).\n"
    #                           "● Безлимитные запросы на все команды.\n"
    #                           "● Доступ к новым командам (новые команды появляются каждую неделю).")

    # Функция проверки наличия id пользователя в файле

    # @bot.message_handler(commands=['pay'])
    # def start_payment(message):
    #     def payment_thread():
    #         try:
    #             user_id = message.from_user.id
    #             if check_subscription(user_id):
    #                 bot.send_message(message.chat.id, "У вас уже есть подписка")
    #             else:
    #                 payment = Payment.create({
    #                     "amount": {
    #                         "value": "199.00",
    #                         "currency": "RUB"
    #                     },
    #                     "confirmation": {
    #                         "type": "redirect",
    #                         "return_url": "https://t.me/WalleRobott_bot"
    #                     },
    #                     "capture": True,
    #                     "description": "Оплата доступа к командам бота WALL•E"
    #                 })
    #                 # Получение ссылки на оплату
    #                 payment_url = payment.confirmation.confirmation_url
    #                 keyboard = types.InlineKeyboardMarkup()
    #                 url_button = types.InlineKeyboardButton(text='Нажми на меня', url=payment_url)
    #                 keyboard.add(url_button)
    #                 bot.send_message(message.chat.id,
    #                                  f"Оплатите 199 рублей, чтобы приобрести подписку, нажав на кнопку ниже:\n",
    #                                  reply_markup=keyboard)
    #
    #                 while True:
    #                     payment = Payment.find_one(payment.id)
    #                     if payment.status == 'succeeded':
    #                         # Отправка сообщения о успешной оплате пользователю
    #                         bot.send_message(message.chat.id, "Оплата прошла успешно!\nДоступ ко всем командам открыт🤩")
    #                         user_id = message.from_user.id
    #                         with open('user.txt', 'a+') as file:
    #                             file.write(str(user_id) + '\n')
    #                         bot.send_message(YOUR_CHAT_ID, "У вас купили подписку за 199р")
    #                         break
    #                     elif payment.status == 'canceled':
    #                         # Отправка сообщения об отмене оплаты пользователю
    #                         bot.send_message(message.chat.id, "Оплата отменена!")
    #                         break
    #                     else:
    #                         time.sleep(5)
    #         except Exception as e:
    #             print(f"Ошибка: {e}")
    #             bot.send_message(message.chat.id, 'Произошла ошибка.\nВыполняю команду /start')
    #             start(message)
    #
    #     threading.Thread(target=payment_thread).start()
    #
    # def check_subscription(user_id):
    #     try:
    #         with open("user.txt", "r") as file:
    #             for line in file:
    #                 if str(user_id) in line:
    #                     return True
    #         return False
    #     except Exception as e:
    #         print(f"Ошибка: {e}")
    #
    # #
    # def is_user_allowed(user_id):
    #     try:
    #         with open('user.txt', 'r') as file:
    #             allowed_users = file.read().splitlines()
    #         return user_id in allowed_users
    #     except Exception as e:
    #         print(f"Ошибка: {e}")

    bot.polling()


def restart_bot():
    while True:
        try:
            start_bot()
        except Exception as e:
            print(f"Ошибка при работе бота: {e}")
            print("Перезапускаю бота...")
            subprocess.run("main.py", shell=True)


restart_bot()









