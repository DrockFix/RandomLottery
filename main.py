import re
import time

import psycopg2 as psycopg2
from progress.bar import Bar
import requests
import vk_api
import telebot
import random

from telebot import types

BOT_TOKEN = "6293155116:AAEHOJGRfI7M4lEStaqY8Cau4xGeOKQnCFs"
bot = telebot.TeleBot(BOT_TOKEN)
# Авторизация в Вконтакте
vk_session = vk_api.VkApi(
    token='vk1.a.AYZrcpF1ZFZ7XUcEkiUxz85oD-R92NXX0T3DBm5bDDbtS9jr-jK_fSS1kgnZFIobpX'
          '-XY8YlXnWcUV7QaOvBLRUAISVUzIU53gdztnyVfCXVmmgAnWfMp1RgdHHaJaEl0EwqdrJuBH1WPuzXNo6QvdDDJWBtu7ugEA'
          '-cCjrTKAkV9uEaXHb1lsXSLlzwIyVXHe8fn0lyqE45D4yX2J4WzQ')

vk = vk_session.get_api()


def get_all_winners(user_id: str):
    conn = psycopg2.connect(
        dbname="lottery",
        user="postgres",
        password="postgres",
        host="localhost",
        port="5444",
    )
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM winners WHERE user_id = %s', (user_id,))
    winners_rows = cursor.fetchall()
    winners = []
    for row in winners_rows:
        winners_dict = dict(id=row[0], winner=row[2], winner_url=row[3], post=row[4], likes=row[5], create_at=row[6])
        winners.append(winners_dict)
    conn.commit()
    conn.close()
    return winners


def db_user_add(user_id: str):
    conn = psycopg2.connect(
        dbname="lottery",
        user="postgres",
        password="postgres",
        host="localhost",
        port="5444",
    )
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users(user_id) VALUES(%s)', (user_id,))
    conn.commit()
    conn.close()


def db_winner_add(user_id: int, winner: str, winner_url: str, post: str, likes: int):
    conn = psycopg2.connect(
        dbname="lottery",
        user="postgres",
        password="postgres",
        host="localhost",
        port="5444",
    )
    cursor = conn.cursor()
    cursor.execute('INSERT INTO winners(user_id, winner, winner_url, post, likes) VALUES(%s,%s,%s,%s,%s)',
                   (user_id, winner, winner_url, post, likes))
    conn.commit()
    conn.close()


@bot.message_handler(commands=['start'])
def start_message(message):
    conn = psycopg2.connect(
        dbname="lottery",
        user="postgres",
        password="postgres",
        host="localhost",
        port="5444",
    )
    cursor = conn.cursor()
    user_id = message.from_user.id
    # Check if user already exists in the database
    cursor.execute('SELECT COUNT(*) FROM users WHERE user_id=%s', (str(user_id),))
    if cursor.fetchone()[0] == 0:
        conn.close()
        db_user_add(str(user_id))
    bot.send_message(user_id,
                     '''
                     Roketvotile - Универсальный инструмент для организации розыгрышей в Telegram и анализа статистики!🎉🔍
                 
Наш бот позволяет проводить розыгрыши с определением победителей на основе лайков, репостов и подписок на посты в 
VK 🎁🎯

Кроме того, наш бот предоставляет подробную статистику по проведенным розыгрышам. Вы сможете получить информацию 
о количестве участников, числе лайков, репостах и подписках, а также о всех победителях предыдущих розыгрышей 📊🏆

Это поможет вам анализировать эффективность проводимых акций, понимать, какие посты имеют наибольшую 
привлекательность для вашей аудитории, и принимать взвешенные решения для улучшения взаимодействия с вашим 
сообществом💡📈

Roketvotile - ваш незаменимый помощник в организации розыгрышей и анализе результатов. Попробуйте сегодня и 
подарите своему сообществу увлекательные акции и интересные призы!🙌✨ 
                     '''
                     )
    markup = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
    item1 = types.KeyboardButton('🏆 Розыгрыш')
    item2 = types.KeyboardButton('📊 Статистика')
    item3 = types.KeyboardButton('⚙️ Настройки')
    markup.add(item1)
    markup.add(item2, item3)

    bot.send_message(user_id, "Выберите, что вы хотите сделать:", reply_markup=markup)


@bot.message_handler(content_types=['text'])
def handle_message(message):
    if message.text == 'sticker':
        bot.send_sticker(message.chat.id, 'CAADAgADsQADWQMDAAEJK1niI56hlhYE')
    if message.text == "🏆 Розыгрыш":
        bot.send_message(message.from_user.id, 'Отправьте ссылку на пост VK (https://vk.com/wall-************)')
        bot.register_next_step_handler(message, handle_lottery)

    if message.text == "📊 Статистика":
        winners = get_all_winners(str(message.chat.id))  # получаем список выполненных заказов
        if not winners:
            bot.send_message(chat_id=message.chat.id, text="Нет проведенных розыгрышей")
            return

        text = "Список проведенных розыгрышей:\n"
        for idx, winner in enumerate(winners, 1):
            text += f"{idx}) Розыгрыш №{winner['id']} от {winner['create_at'].strftime('%d.%m.%Y %H:%M')} " \
                    f"на посту {winner['post']}, количество " \
                    f"лайков: {winner['likes']}, Победитель: <a href='{winner['winner_url']}'>{winner['winner']}</a>\n"

        bot.send_message(message.chat.id, text, disable_web_page_preview=True, parse_mode="HTML")
    if message.text == "⚙️ Настройки":
        bot.send_message(message.from_user.id, 'Функция в разработке!⏳')


def handle_lottery(message):
    url = message.text
    post_url = url.split('wall-')[1]
    owner_id = post_url.split('_')[0]
    post_id = post_url.split('_')[1]

    response = vk.likes.getList(type='post', owner_id=f'-{owner_id}', item_id=post_id, extended=1)

    # Вывод списка пользователей, которые лайкнули пост
    # for user in response['items']:
    #     user_info = vk.users.get(user_ids=user['id'], fields='first_name,last_name')[0]
    #     bot.reply_to(message, f'{user_info["first_name"]} {user_info["last_name"]} лайкнул ваш пост')
    likes = len(response['items'])
    bot.reply_to(message, 'Количество лайков: ' + str(likes) + '❤')
    # Выбор случайного пользователя из списка лайков, если пользователи существуют
    valid = False
    fake_index = len(response['items'])
    if response['items']:
        while not valid:
            with Bar('Loading', suffix='%(percent)d%%', max=fake_index) as bar:
                message_text = None
                message_id = None

                for _ in range(1, fake_index + 1):
                    time.sleep(0.1)
                    bar.next()
                    progress = round(bar.index * 100 / bar.max, 1)
                    progress_text = f'<strong>Определяем победителя:</strong> {progress}% ⏳\n'
                    # update_text = f'<strong>Loading {bar.index}/{bar.max}</strong>'
                    new_message_text = f'{progress_text}'

                    if message_text is None:
                        message = bot.send_message(chat_id=message.chat.id, text=new_message_text, parse_mode='HTML')
                        message_id = message.message_id
                    else:
                        bot.edit_message_text(chat_id=message.chat.id, message_id=message_id, text=new_message_text,
                                              parse_mode='HTML')

                    message_text = new_message_text
            random_user_id = random.choice(response['items'])['id']
            random_user_info = vk.users.get(user_ids=random_user_id, fields='first_name,last_name,photo_200_orig')[0]
            if random_user_info["is_closed"]:
                bot.send_message(chat_id=message.chat.id,
                                 text=f'Профиль закрыт: <a href="https://vk.com/id{random_user_id}">'
                                      f'{random_user_info["first_name"]} {random_user_info["last_name"]}</a>',
                                 parse_mode="HTML")
                continue
            subs = vk.users.getSubscriptions(user_id=random_user_id)
            if int(owner_id) not in subs['groups']['items']:
                bot.send_message(chat_id=message.chat.id,
                                 text=f'Нет подписки: <a href="https://vk.com/id{random_user_id}">'
                                      f'{random_user_info["first_name"]} {random_user_info["last_name"]}</a>',
                                 parse_mode="HTML")
                continue
            valid = True
            # bot.reply_to(message, f'Выбранный пользователь: <a href="https://vk.com/id{random_user_id}">'
            #                       f'{random_user_info["first_name"]} {random_user_info["last_name"]}</a>',
            #              parse_mode="HTML")
            photo_url = random_user_info['photo_200_orig']
            imageProfile = requests.get(photo_url)
            photo_path = f'winner_{message.from_user.id}.jpg'  # Путь, по которому вы хотите сохранить фотографию
            with open(photo_path, 'wb') as file:
                file.write(imageProfile.content)
            bot.send_photo(chat_id=message.chat.id, photo=open(photo_path, 'rb'),
                           caption=f'🎉🏆Победитель: <a href="https://vk.com/id{random_user_id}">'
                                   f'{random_user_info["first_name"]} {random_user_info["last_name"]}</a>🎉🏆',
                           parse_mode="HTML")
            db_winner_add(message.chat.id, f'{random_user_info["first_name"]} {random_user_info["last_name"]}',
                          f'https://vk.com/id{random_user_id}', url, likes)


    else:
        bot.reply_to(message, 'Нет пользователей, которые оставили лайк')


bot.polling()

# comments = vk.wall.getComments(owner_id='-202681676', post_id='417')

# Вывод комментариев
# for comment in comments['items']:
#     print(comment['from_id'], comment['text'])

# reposts = vk.wall.getReposts(owner_id=-202681676, post_id=1343595)
#
# # Вывод списка пользователей, которые репостили пост
# for repost in reposts['items']:
#     print(repost['source_id'])


# Вывод информации о посте

#
# if not post:
#     print(f'Пост с owner_id={owner_id} и post_id={post_id} не найден')
#     exit()
#
# if not post_info[0]['from_id'] > 0:
#     print('Пост не является группой')
#     exit()
#
# # Проверка, что пост не закрыт и доступен для просмотра
# if post_info[0]['access_key'] is not None:
#     print('Пост закрыт')
#     exit()
