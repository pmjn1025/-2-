
from flask import Flask, render_template, request, jsonify, redirect, url_for

from pymongo import MongoClient
import requests

app = Flask(__name__)


client = MongoClient('mongodb+srv://test:sparta@cluster0.32bcc.mongodb.net/cluster0?retryWrites=true&w=majority')
db =  client.dbsparta_plus_week2

@app.route('/')
def main():
    # DB에서 저장된 단어 찾아서 HTML에 나타내기
    return render_template("index.html")


@app.route('/detail/<keyword>')
def detail(keyword):
    # GET방식의 ?status_give = new 할때 new의 키
    status_receive = request.args.get("status_give")
    # API에서 단어 뜻 찾아서 결과 보내기
    # 여기서 데이터를 받아서 html로 보낼 것을 서버에서 정리해준다 jinjia-SSR(서버사이드랜더링)
    r = requests.get(f"https://owlbot.info/api/v4/dictionary/{keyword}", headers={"Authorization": "Token ff0ab0c5d7d41a250d6f369ac0334979358a469e"})
    result = r.json()
    print(result)
    # 받어온 것을 템플릿으로 보낸다.
    return render_template("detail.html", word=keyword, result=result, status=status_receive)


@app.route('/api/save_word', methods=['POST'])
def save_word():
    # 단어 저장하기
    word_receive = request.form["word_give"]
    definition_receive = request.form["definition_give"]
    doc = {"word": word_receive, "definition":definition_receive}
    db.words.insert_one(doc)

    # f-string을 사용하면 문자열 안에서 함수를 호출한 결과를 삽입할 수 도 있습니다.
    return jsonify({'result': 'success', 'msg': f'단어{word_receive} 저장'})


@app.route('/api/delete_word', methods=['POST'])
def delete_word():
    # 단어 삭제하기

    word_receive = request.form["word_give"]
    db.words.delete_one({"word": word_receive})

    return jsonify({'result': 'success', 'msg': f'단어 {word_receive} 삭제'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)