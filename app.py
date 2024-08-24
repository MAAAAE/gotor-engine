from flask import Flask

import chatgpt

app = Flask(__name__)


@app.route('/parse/<question>')
def parse_text(question):  # put application's code here
    result = chatgpt.parse_text(question=question)
    return result


if __name__ == '__main__':
    app.run()
