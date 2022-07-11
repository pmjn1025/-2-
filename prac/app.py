from flask import Flask, render_template, request
import requests

app = Flask(__name__)


@app.route('/')
def main():
    myname = "Sparta"
    return render_template("index.html", name= myname)


@app.route('/detail/<keyword>')
def detail(keyword):
    r = requests.get(f"https://owlbot.info/api/v4/dictionary/{keyword}", headers={"Authorization": "Token ff0ab0c5d7d41a250d6f369ac0334979358a469e"})
    result = r.json()
    print(result)

    word_recieve = request.args.get("word_give")

    print(word_recieve)
    return render_template("detail.html", word = keyword)


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)