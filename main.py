import requests
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw, ImageFont
import textwrap
from datetime import datetime


# ------------------------- Данные знаков и дат -------------------------------- #
# Для парсинга
signs = ['oven', 'telets', 'bliznetsi', 'rac', 'lev', 'deva', 'vesy', 'scorpion', 'strelets', 'kozerog', 'vodoley', 'riby']
# Для печати на картинке
signs_ru = ['Овен', 'Телец', 'Близнецы', 'Рак', 'Лев', 'Дева', 'Весы', 'Скорпион', 'Стрелец', 'Козерог', 'Водолей', 'Рыбы']
title = dict(zip(signs, signs_ru))
# Для правильного падежа даты
months = {1: 'января', 2: 'февраля', 3: "марта", 4: "апреля", 5: "мая", 6: "июня",
        7: "июля", 8: "августа", 9: "сентября", 10: "октября", 11: "ноября", 12: "декабря"}

# ---------------------- Получаем гороскоп на день ---------------------- #
def horoscope(sign):
    r = requests.get(f'https://www.astrostar.ru/horoscopes/main/{sign}/day.html')
    soup = BeautifulSoup(r.text, 'html.parser')
    info = soup.find('div', class_='col-xs-12 col-sm-9 col-md-7 horoscopes-single-content horoscopes-single')
    return info.find('p').text
    

# ---------------------- Склейка всей инфы ---------------------- #
def gluing_photo(t, sign):
    # Открываем фон, готовим шрифты
    image = Image.open('stars.jpg')
    font = ImageFont.truetype('timesi.ttf', 95)
    title_font = ImageFont.truetype('ANTQUAI.TTF', 300)
    draw = ImageDraw.Draw(image)

    # Наносим название знака
    w_title = title_font.getsize(title[sign])[0]
    x_sign = (image.size[0] // 2 - w_title) // 2 
    draw.text((x_sign, 50), title[sign], font=title_font, fill='#FFF')

    # Наносим сегодняшнюю дату и линию
    today = datetime.now()
    day = f'{today.day} {months[today.month]}' 
    x_date = w_title + x_sign * 2
    draw.text((x_date, 50), day, font=title_font, fill='#FFF')
    draw.line(((200, 450), (3500, 450)), fill='white', width=15)
    
    # Наносим текст гороскопа
    y = 500
    for line in textwrap.wrap(t, width=37):
        draw.text((1750, y), line, font=font, fill='#FFFFFF')
        y += font.getsize(line)[1]

    # Настраиваем и вставляем фото знака
    sign_image = Image.open(f'signs\{sign}.jpg')
    w, h = sign_image.size
    sign_image = sign_image.resize((int(w * ((y - 500) / h)), y - 500))
    image.paste(sign_image, (250, 510))

    # Сохраняем гороскоп
    image.save(f'{sign}_horoscope.jpg')


# ---------------------- Главная функция ---------------------- #
def main():
    # Склеиваем гороскоп для каждого знака
    for sign in signs:
        gluing_photo(horoscope(sign), sign)


if __name__ == '__main__':
    main()
