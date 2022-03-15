import requests
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw, ImageFont
import textwrap


# ------------------------- знаки для URL -------------------------------- #
signs = ['oven', 'telets', 'bliznetsi', 'rac', 'lev', 'deva', 'vesy', 'scorpion', 'strelets', 'kozerog', 'vodoley', 'riby']
signs_ru = ['Овен', 'Телец', 'Близнецы', 'Рак', 'Лев', 'Дева', 'Весы', 'Скорпион', 'Стрелец', 'Козерог', 'Водолей', 'Рыбы']
title = dict(zip(signs, signs_ru))

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
    title_font = ImageFont.truetype('comic.ttf', 280)
    draw = ImageDraw.Draw(image)

    # Наносим текст
    x = (image.size[0] - title_font.getsize(title[sign])[0]) // 2
    draw.text((x, 50), title[sign], font=title_font, fill='#FFF')
    y = 500
    for line in textwrap.wrap(t, width=37):
        draw.text((1750, y), line, font=font, fill='#FFF')
        y += font.getsize(line)[1]

    # Настраиваем и вставляем фото знака
    sign_image = Image.open(f'signs\{sign}.jpg')
    w, h = sign_image.size
    sign_image = sign_image.resize((int(w * ((y - 500) / h)), y - 500))
    image.paste(sign_image, (250, 510))

    image.save(f'{sign}_horoscope.jpg')
    

def main():
    for sign in signs:
        gluing_photo(horoscope(sign), sign)


if __name__ == '__main__':
    main()
