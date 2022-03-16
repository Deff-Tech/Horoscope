from flask import Flask, render_template, request
from main import main

app = Flask(__name__)


@app.route('/link/', methods=['post', 'get'])
def link():
    message = 'Нажмите, чтобы получить гороскоп'
    if request.method == 'POST':
        message = 'Гороскоп сгенерирован!'
        main()
    return render_template('link.html', message=message)


if __name__ == "__main__":
    app.run(debug=True)