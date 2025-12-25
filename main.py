import os.path
import shutil
import requests
import telebot
from telebot import types
from ultralytics import YOLO
from moviepy.editor import VideoFileClip
from time import sleep
from Configuration_database import repository
from mapHandler import mark_from_db, mark_from_db_user
import datetime

print("СТАРТУЕМ")
print("Маг")
# model = YOLO("weights/best.pt")
# 2024 ниже 2025 года модель
model = YOLO("weights2025/best.pt")
#модель сортировки убираем
#model_robot = YOLO("weights_robot/best.pt")
location_token = 'pk.fd982708b5201793e2227f61d4c2ccab'
# Токен телеграмм бота EcoSort_Telegram_Bot
bot = telebot.TeleBot('6874994671:AAGWbedCkTSt6yDHbEwQDUCg5z2pJ1J6eYY')
sql = repository.SQL()
status = ["Рассматривается 🔁", "Выполняется 🔸", "Выполнена ✅", "Ошибка ⚠️"]
mark_from_db()


# сделал 071025
if os.path.exists("runs/result"):
    shutil.rmtree("runs/result")


@bot.message_handler(commands=['start'])
def button(message):
    if sql.get_role(message.chat.id) is not None:
        role = sql.get_role(message.chat.id)[0]
    else:
        role = "user"
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    profile = types.KeyboardButton("Профиль 💬")
    #waste_recycling = types.KeyboardButton("Сортировка ТКО♻️🗑🚮")
    application = types.KeyboardButton("Оставить заявку 🖇")
    share_telegram_bot = types.KeyboardButton("Поделиться EcoSort_Telegram_Bot")
    #markup.add(profile, waste_recycling, application, share_telegram_bot)
    markup.add(profile, application, share_telegram_bot)
    if role == "admin":
        admin = types.KeyboardButton("Администратор 👤")
        markup.add(admin)
    photo = open("telegram.png", "rb")
    photo_analisis = photo.read()
    bot.send_photo(message.chat.id, photo_analisis,
                   caption=f"<b>Добро пожаловать, {message.from_user.first_name} {message.from_user.last_name}! EcoSort_Telegram_Bot готов к работе:</b>",
                   reply_markup=markup, parse_mode="html")
    user_id = message.chat.id
    user_name = message.from_user.last_name
    if sql.users_select(user_id) is None:
        print('new user')
        sql.users_insert(user_name, user_id)


@bot.message_handler(content_types=['text'])
def text_menu(message):
    if sql.get_role(message.chat.id) is not None:
        role = sql.get_role(message.chat.id)[0]
    else:
        role = "user"
    if message.text == "Администратор 👤" and role == "admin":
        answer_admin = types.InlineKeyboardMarkup(row_width=2)
        button_admin = types.InlineKeyboardButton("Администратор 👤", callback_data='Администратор 👤')
        answer_admin.add(button_admin)
        bot.send_message(message.chat.id, "🤖🤖🤖🤖🤖 ", reply_markup=answer_admin)
    if message.text == "Профиль 💬":
        first_name = message.from_user.first_name
        last_name = message.from_user.last_name
        user_id = message.from_user.id
        count_applications = sql.count_applications(user_id)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        button_contact = types.KeyboardButton("Поделится своим номером телефона:", request_contact=True)
        markup.add(button_contact)
        back_button = types.KeyboardButton('↪️ Назад в меню')
        markup.add(back_button)
        answer_profile = types.InlineKeyboardMarkup(row_width=2)
        button_garbage_profile = types.InlineKeyboardButton("Заявки контейнера🚮", callback_data='профиль заявки')
        button_garbage_profile_map = types.InlineKeyboardButton("📍 Карта 🚯🦠", web_app=types.WebAppInfo(
            url=f"https://centrally-realistic-jackrabbit.cloudpub.ru/garbage/{user_id}"))
        answer_profile.add(button_garbage_profile)
        answer_profile.add(button_garbage_profile_map)
        bot.send_message(message.chat.id, f"<b>Ваше имя: {first_name} {last_name}\nВаш ID: {user_id}</b>"
                                          f"\n<b>Количество заявок на заполненные контейнеры 🚮: {count_applications}\n История отправленых заявок 🚮:</b>",
                         reply_markup=answer_profile, parse_mode="html")
        bot.send_message(message.chat.id, f"\n<b>Поделитесь своим номером телефона: ☎️</b>", reply_markup=markup,
                         parse_mode="html")

    if message.text == "Оставить заявку 🖇":
        answer = types.InlineKeyboardMarkup(row_width=2)
        button_application = types.InlineKeyboardButton("заявка", callback_data='заявка')
        answer.add(button_application)
        bot.send_message(message.chat.id, "<b>Оставьте заявку!</b>", reply_markup=answer, parse_mode="html")
    # if message.text == "Сортировка ТКО♻️🗑🚮":
    #     answer = types.InlineKeyboardMarkup(row_width=2)
    #     button_application = types.InlineKeyboardButton("Сортировка ТКО", callback_data='заявка производство')
    #     answer.add(button_application)
    #     bot.send_message(message.chat.id, "♻️🗑🚮", reply_markup=answer)
    if message.text == '↪️ Назад в меню':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        profile = types.KeyboardButton("Профиль 💬")
        #waste_recycling = types.KeyboardButton("Сортировка ТКО♻️🗑🚮")
        application = types.KeyboardButton("Оставить заявку 🖇")
        share_telegram_bot = types.KeyboardButton("Поделиться EcoSort_Telegram_Bot")
        #markup.add(profile, waste_recycling, application, share_telegram_bot)
        markup.add(profile, application, share_telegram_bot)
        if role == "admin":
            admin = types.KeyboardButton("Администратор 👤")
            markup.add(admin)
        bot.send_message(message.chat.id, "📲", reply_markup=markup)
    if message.text == "Поделиться EcoSort_Telegram_Bot":
        photo_share = open("Qr_code.png", "rb")
        photo_share_read = photo_share.read()
        bot.send_photo(message.chat.id, photo_share_read, caption='<b>QR-код EcoSort_Telegram_Bot</b>',
                       parse_mode="html")
        markup_qr = types.ReplyKeyboardMarkup(resize_keyboard=True)
        back_button_qr = types.KeyboardButton('↪️ Назад в меню')
        markup_qr.add(back_button_qr)
        bot.send_message(message.chat.id, '<b><code>https://t.me/EcoSort_Telegram_Bot</code></b>', parse_mode="HTML",
                         reply_markup=markup_qr)


button_application_general = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
button_photo_application = types.KeyboardButton("фото")
button_video_application = types.KeyboardButton("видео")
button_application = types.KeyboardButton("заявка")
button_application_general.add(button_photo_application, button_video_application)
button_application_general.add(button_application)
button_contact = types.KeyboardButton("контакт")
button_application_general.add(button_contact)
#button_production_general = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
#button_photo_production = types.KeyboardButton("фото")
#button_video_production = types.KeyboardButton("видео")
#button_production = types.KeyboardButton("заявка")
#button_production_general.add(button_photo_production, button_video_production)
#button_production_general.add(button_application)


@bot.message_handler(content_types=['contact'])
def contact(message):
    user_id = message.from_user.id
    user_phone = message.contact.phone_number
    bot.send_message(user_id, f"<b>Ваш номер телефона: +{user_phone}</b>", parse_mode="html")
    if user_phone[0] == '7':
        user_phone = '+' + user_phone
    if user_phone[0] == '8':
        user_phone = '+7' + user_phone[1:-1]
    sql.add_number(user_phone, user_id)


@bot.message_handler(func=lambda message: True, content_types=['photo'])
def photo_application(message):
    photo = message.photo
    fileID = photo[-1].file_id
    file_info = bot.get_file(fileID)
    downloaded_file = bot.download_file(file_info.file_path)
    with open(file_info.file_path, 'wb') as new_file:
        new_file.write(downloaded_file)
    photo = open(file_info.file_path, 'rb').read()
    bot.send_message(message.chat.id, "<b>Идет анализ вашего фото. Ожидайте!</b>", parse_mode="html")
    res = model(file_info.file_path, save=True, project="runs/result", name=fileID)
    crowded = 0
    exported = 0
    for i in range(len(res[0].boxes.cls)):
        # if res[0].boxes.cls[i] == 15:
        #     crowded += 1
        # if res[0].boxes.cls[i] == 16:
        #     exported += 1
        if res[0].boxes.cls[i] == 0:
            crowded += 1
        if res[0].boxes.cls[i] == 1:
            exported += 1
    if crowded:  # проверка на обнаружения не вывезенный мусор
        file_name = file_info.file_path.replace("photos/", "")
        print(file_name)
        #detect_photo = open(f"runs/detect/predict/{file_name}", "rb")
        detect_photo = open(f"runs/result/{fileID}/{file_name}", "rb")
        button = types.InlineKeyboardButton("Оставить геопозицию", callback_data='геопозиция')
        answer = types.InlineKeyboardMarkup(row_width=2)
        answer.add(button)
        bot.send_photo(message.chat.id, detect_photo, reply_markup=answer)
        #detect_photo = open(f"runs/detect/predict/{file_name}", "rb").read()
        detect_photo = open(f"runs/result/{fileID}/{file_name}", "rb").read()
        bot.register_next_step_handler(message, location_determination, photo, detect_photo)
    elif exported:
        file_name = file_info.file_path.replace("photos/", "")
        print(file_name)
        #detect_photo = open(f"runs/detect/predict/{file_name}", "rb")
        detect_photo = open(f"runs/result/{fileID}/{file_name}", "rb")
        bot.send_photo(message.chat.id, detect_photo)
        bot.send_message(message.chat.id,
                         f"<b>На данном фото обнаружено, что мусорный контейнер не заполнен! ⚠️ Заявка не будет передана в управляющую компанию. ❌</b>"
                         f"\n<b>Благодарим за Ваше обращение!</b>"
                         f"\n<b>Ждем от Вас новых заявок!</b>"
                         f"\n<b>Только вместе мы можем сделать наш город чистым!❤ </b>"
                         f"\n<b>Если вам интересно узнать, как идет сортировка ТКО на мусороперерабатывающем заводе, перейдите в раздел Сортировка ТКО ♻️🗑🚮.</b>",
                         parse_mode="html")
    else:
        bot.send_message(message.chat.id,
                         "<b>На данном фото не обнаружено ни одного мусорного контейнера! ⚠️ Заявка не будет передана в управляющую компанию. ❌ </b>",
                         parse_mode="html")


# @bot.message_handler(func=lambda message: True, content_types=['photo'])
# def photo_production(message):
#     photo = open(f"waste_production.jpg", "rb")
#     print(photo)
#     bot.send_message(message.chat.id, "<b>Ожидайте!</b>", parse_mode="html")
#     file_name = photo.name
#     print(file_name)
#     res = model_robot(os.path.abspath(file_name), save=True)
#     detect_photo = open(f"runs/detect/predict/{file_name}", "rb")
#     k_plastic = 0
#     k_metal = 0
#     k_cardboard = 0
#     k_paper = 0
#     k_glass = 0
#     for i in range(len(res[0].boxes.cls)):
#         if res[0].boxes.cls[i] == 15:
#             k_plastic += 1
#         if res[0].boxes.cls[i] == 16:
#             k_metal += 1
#         if res[0].boxes.cls[i] == 17:
#             k_cardboard += 1
#         if res[0].boxes.cls[i] == 18:
#             k_paper += 1
#         if res[0].boxes.cls[i] == 19:
#             k_glass += 1
#     bot.send_photo(message.chat.id, detect_photo,
#                    caption=f"<b>Обнаружено следующее количество разного вида ТКО ♻️:\n{k_plastic} - количество мусора из пластика\n{k_metal} - количество мусора из металла ⚙\n{k_cardboard} - количество мусора из картона 📦\n{k_paper} - количество мусора из бумаги 📄\n{k_glass} - количество мусора из стекла 🍾</b>",
#                    parse_mode="html")


@bot.message_handler(func=lambda message: True, content_types=['video'])
def video_application(message):
    video = message.video
    fileID = video.file_id
    file_info = bot.get_file(fileID)
    downloaded_file = bot.download_file(file_info.file_path)
    os.makedirs("videos", exist_ok=True)
    with open(file_info.file_path, 'wb') as new_file:
        new_file.write(downloaded_file)
    bot.send_message(message.chat.id, "<b>Идет анализ вашего видео. Ожидайте!</b>", parse_mode="html")
    res = model(file_info.file_path, save=True, project="runs/result", name=fileID)
    file_name = file_info.file_path.replace("videos/", "")
    #input_video_path = f"runs/detect/predict/{file_name}"
    input_video_path = f"runs/result/{fileID}/{file_name}".replace(".mp4", ".avi")
    #output_video_path = input_video_path.replace('.MOV', '.AVI')
    output_video_path = input_video_path.replace('.avi', '.mp4')
    clip = VideoFileClip(input_video_path)
    clip.write_videofile(output_video_path)
    bot.send_video(message.chat.id, video=open(output_video_path, 'rb'))


# @bot.message_handler(func=lambda message: True, content_types=['video'])
# def video_production(message):
#     video = message.video
#     fileID = video.file_id
#     file_info = bot.get_file(fileID)
#     downloaded_file = bot.download_file(file_info.file_path)
#     os.makedirs("videos", exist_ok=True)
#     with open(file_info.file_path, 'wb') as new_file:
#         new_file.write(downloaded_file)
#     bot.send_message(message.chat.id, "<b>Идет анализ вашего видео. Ожидайте!</b>", parse_mode="html")
#     res = model_robot(file_info.file_path, save=True)
#     file_name = file_info.file_path.replace("videos/", "")
#     input_video_path = f"runs/detect/predict/{file_name}"
#     output_video_path = input_video_path.replace('.MOV', '.AVI')
#     clip = VideoFileClip(output_video_path)
#     clip.write_videofile(output_video_path.replace('.AVI', '.MP4'))
#     bot.send_video(message.chat.id, video=open(output_video_path.replace('.AVI', '.MP4'), 'rb'))


@bot.message_handler(func=lambda message: True, content_types=['location'])
def location_determination(message, photo, detect_photo):
    location = message.location
    print(type(location))
    lat = location.latitude
    long = location.longitude
    mark_from_db()
    headers = {"Accept-Language": "ru"}
    address = requests.get(
        f'https://eu1.locationiq.com/v1/reverse.php?key={location_token}&lat={lat}&lon={long}&format=json',
        headers=headers).json()
    bot.send_message(message.chat.id, address.get("display_name"))
    date = datetime.datetime.now()
    sql.garbage_app_insert(address.get("display_name"), long, lat, message.chat.id, photo, detect_photo, date)
    app_id_garbage = sql.get_last_garbage_id_by_userid(message.chat.id)
    bot.send_message(message.chat.id,
                     f"<b>Спасибо, заявка №{app_id_garbage} принята! </b>"
                     "✅\n<b>Данные по  вашей заявки будут переданы в управляющую компанию. 📨 </b>"
                     "\n<b>Благодарим за Ваше обращение!</b>"
                     "\n<b>Ждем от Вас новых заявок!</b>"
                     "\n<b>Только вместе мы можем сделать наш город чистым!❤ </b>"
                     "\n<b>Если вам интересно узнать, как идет сортировка ТКО на мусороперерабатывающем заводе, перейдите в раздел Сортировка ТКО ♻️🗑🚮.</b>",
                     parse_mode="html")


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == "заявка":
                answer = types.InlineKeyboardMarkup(row_width=2)
                button_photo_application = types.InlineKeyboardButton("фото", callback_data='фото')
                button_video_application = types.InlineKeyboardButton("видео", callback_data='видео')
                answer.add(button_photo_application, button_video_application)
                bot.send_message(call.message.chat.id, f"<b>Вы хотите прикрепить фото или видео?</b>",
                                 reply_markup=answer, parse_mode="html")
            if call.data == "фото":
                bot.send_message(call.message.chat.id, "<b>Прикрепите фото. 📸  </b>", parse_mode="html")
                bot.register_next_step_handler(call.message, photo_application)
                if os.path.exists("runs/result/garbage"):
                    shutil.rmtree("runs/result/garbage")
                # if os.path.exists("runs/detect/predict"):
                #     shutil.rmtree("runs/detect/predict")
            if call.data == "видео":
                bot.send_message(call.message.chat.id, "<b>Прикрепите видео. 🎥  </b>", parse_mode="html")
                bot.register_next_step_handler(call.message, video_application)
                if os.path.exists("runs/result/garbage"):
                    shutil.rmtree("runs/result/garbage")
                # if os.path.exists("runs/detect/predict"):
                #     shutil.rmtree("runs/detect/predict")
            # if call.data == "заявка производство":
            #     answer = types.InlineKeyboardMarkup(row_width=2)
            #     button_photo_production = types.InlineKeyboardButton("фото", callback_data='фото производство')
            #     button_video_production = types.InlineKeyboardButton("видео", callback_data='видео производство')
            #     answer.add(button_photo_production, button_video_production)
            #     bot.send_message(call.message.chat.id, f"<b>Выберите фото или видео.</b>", reply_markup=answer,
            #                      parse_mode="html")
            #     if os.path.exists("runs/detect/predict"):
            #         shutil.rmtree("runs/detect/predict")
            # if call.data == "фото производство":
            #     photo_production(call.message)
            #     if os.path.exists("runs/detect/predict"):
            #         shutil.rmtree("runs/detect/predict")
            # if call.data == "видео производство":
            #     bot.send_message(call.message.chat.id, "<b>Прикрепите видео. 🎥 </b>", parse_mode="html")
            #     bot.register_next_step_handler(call.message, video_production)
            #     if os.path.exists("runs/detect/predict"):
            #         shutil.rmtree("runs/detect/predict")
            if call.data == 'геопозиция':
                bot.send_message(call.message.chat.id,
                                 "<b>Прикрепите геопозицию, где обнаружен заполненный мусорный контейнер.🌐  </b>",
                                 parse_mode="html")
            if call.data == 'контакт':
                bot.send_message(call.message.chat.id, "<b>Поделитесь своим номером телефона: </b>", parse_mode="html")
                bot.register_next_step_handler(call.message, contact)

            if call.data == "профиль заявки":
                user_id = call.message.chat.id
                apps = sql.get_all_garbage_by_userid(user_id)
                ans = types.InlineKeyboardMarkup()
                message = ""
                c = 0
                button_row = []
                for app in apps:
                    c += 1
                    if c <= 3:
                        button_row.append(types.InlineKeyboardButton(app[0], callback_data=f"app_profile_{app[0]}"))
                    else:
                        ans.row(*button_row)
                        c = 1
                        button_row = []
                        button_row.append(types.InlineKeyboardButton(app[0], callback_data=f"app_profile_{app[0]}"))
                if button_row != []:
                    ans.row(*button_row)
                if button_row == []:
                    message = "<b>У Вас нет заявок на переполненные контейнеры!</b>"
                    bot.send_message(call.message.chat.id, f"<b>{message}</b>", reply_markup=ans, parse_mode="html")
                else:
                    bot.send_message(call.message.chat.id,
                                     f"<b>Ваши отправленные заявки на переполненные контейнеры:\n{message}</b>",
                                     reply_markup=ans, parse_mode="html")

            if call.data.startswith("app_profile_"):
                print(call.data)
                app_id = int(call.data.replace("app_profile_", ""))
                app = sql.get_garbage_by_id(app_id)
                s = "️♦️<b>Заявка №</b>" + str(app[0]) + "\t🖇\n<b>Статус заявки: </b>" + app[
                    8] + "\n🌐 <b>Место положение:</b>\n" + app[1] + "\n⏰ <b>Дата и время: </b>\n" + str(app[7]) + "\n"
                bot.send_photo(call.message.chat.id, app[6], caption=f"<b>{s}</b>", parse_mode="html")

            if call.data == "Администратор 👤":
                answer_admin = types.InlineKeyboardMarkup(row_width=2)
                button_admin_garbage = types.InlineKeyboardButton("Заявки на переполненный мусорный контейнер",
                                                                  callback_data='admin_garbage')
                button_admin_garbage_map = types.InlineKeyboardButton("📍 Карта 🚯🦠", web_app=types.WebAppInfo(
            url=f"https://centrally-realistic-jackrabbit.cloudpub.ru/garbage"))
                answer_admin.add(button_admin_garbage)
                answer_admin.add(button_admin_garbage_map)
                bot.send_message(call.message.chat.id, f"🚮🚮🚮🚮🚮", reply_markup=answer_admin)

            if call.data == "admin_garbage":
                usernames = sql.get_all_username()
                answer = types.InlineKeyboardMarkup(row_width=2)
                for username in usernames:
                    b = types.InlineKeyboardButton(username[0], callback_data=f"user_garbage{username[1]}")
                    answer.add(b)
                bot.send_message(call.message.chat.id, "<b>Пользователи: </b>", reply_markup=answer, parse_mode="html")

            if call.data.startswith("user_garbage"):
                user_id = int(call.data.replace("user_garbage", ""))
                apps = sql.get_all_garbage_by_userid(user_id)
                ans = types.InlineKeyboardMarkup()
                message = ""
                c = 0
                button_row = []
                for app in apps:
                    c += 1
                    if c <= 3:
                        button_row.append(types.InlineKeyboardButton(app[0], callback_data=f"app_garbage{app[0]}"))
                    else:
                        ans.row(*button_row)
                        c = 1
                        button_row = []
                        button_row.append(types.InlineKeyboardButton(app[0], callback_data=f"app_garbage{app[0]}"))
                if button_row != []:
                    ans.row(*button_row)
                if button_row == []:
                    message = "<b>У данного пользователя нет заявок на переполненные контейнеры!</b>"
                    bot.send_message(call.message.chat.id, f"<b>{message}</b>", reply_markup=ans, parse_mode="html")
                else:
                    bot.send_message(call.message.chat.id,
                                     f"<b>Отправленные заявки на переполненные контейнеры:\n{message}</b>",
                                     reply_markup=ans, parse_mode="html")

            if call.data.startswith("app_garbage"):
                app_id = int(call.data.replace("app_garbage", ""))
                app = sql.get_garbage_by_id(app_id)
                message = "️♦️<b>Заявка №</b>" + str(app[0]) + "\t🖇\n<b>Статус заявки: </b>" + app[
                    8] + "\n🌐 <b>Место положение:</b>\n" + app[1] + "\n⏰ <b>Дата и время: </b>\n" + str(app[7]) + "\n"
                ans = types.InlineKeyboardMarkup()
                for i in range(len(status)):
                    button = types.InlineKeyboardButton(status[i], callback_data=f"edit_garbage{app_id}_{i}")
                    ans.add(button)
                bot.send_photo(call.message.chat.id, app[6], f"<b>{message}\nВыберите статус заявки: </b>",
                               reply_markup=ans, parse_mode="html")

            if call.data.startswith("edit_garbage"):
                d = call.data.replace("edit_garbage", "")
                list = d.split("_")
                app_id = int(list[0])
                new_status = int(list[1])
                sql.update_status_garbage(app_id, status[new_status])
                message = f"<b>Новый статус заявки №{app_id}: {status[new_status]}</b>"
                bot.send_message(call.message.chat.id, message, parse_mode="html")

    except Exception as e:
        print(repr(e))


# bot.polling(non_stop=True)
while True:
    try:
        bot.polling(none_stop=True)
    except Exception as _ex:
        print(_ex)
        #sleep(15)
# bot.infinity_polling()
