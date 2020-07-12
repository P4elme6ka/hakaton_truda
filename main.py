from flask import Flask, request
from site_parcer import parce

app = Flask(__name__)


@app.route('/get/', methods=["POST"])
def get_proffecion_words():
    url = request.args['url']
    print(url)
    return parce(url)


if __name__ == '__main__':
    app.run()
