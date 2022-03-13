import string

from flask import Flask, request, make_response, json, jsonify
# from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
import jwt
import datetime
from functools import wraps
from fucntion.fuction import getdataframe, bookmark_ranking, home_ranking
from spellchecker import SpellChecker
import mysql.connector

spell = SpellChecker(language='en')
spell.word_frequency.load_text_file('../../resource/mergedict.txt')


def spell_corr(query):
    spellcor = [spell.correction(w) for w in query.split()]
    return spellcor


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
CORS(app)
host = "localhost"
user = "root"
password = ""
db = "user"


@app.route("/api/ranking/home", methods=['POST'])
def rankinghome():
    arg1 = request.args['query']
    arg1 = arg1.replace(' ', '')
    arg1 = arg1.lower().translate(str.maketrans('', '', string.punctuation))
    query = arg1
    query = spell_corr(query)[0]
    result = home_ranking(query)
    result = {'result': result, 'correction': query}
    return make_response(jsonify(result), 200)


@app.route("/api/ranking/bookmark", methods=['POST'])
def rankingbookmark():
    user_id = request.args['userid']
    query = request.args['query']
    mydb = mysql.connector.connect(host=host, user=user, password=password, db=db)
    mycursor = mydb.cursor(dictionary=True)
    sql = "SELECT food_id FROM user_bookmark WHERE user_id = %s"
    val = (user_id,)
    mycursor.execute(sql, val)
    myresult = list(mycursor.fetchall())
    menulist = [w['food_id'] for w in myresult]
    print(menulist)

    query = spell_corr(query)[0]
    result = bookmark_ranking(query, menulist)
    result = {'result': result, 'correction': query}
    return make_response(jsonify(result), 200)


@app.route("/api/login", methods=['POST'])
def login():
    user_name = request.args['username']
    pass_word = request.args['password']
    mydb = mysql.connector.connect(host=host, user=user, password=password, db=db)
    mycursor = mydb.cursor(dictionary=True)
    sql = "SELECT * FROM user WHERE username = %s"
    val = (user_name,)
    mycursor.execute(sql, val)
    row = mycursor.fetchone()
    userdb = row['username']
    passdb = row['password']
    iddb = row['id']
    if row:
        if passdb == pass_word:
            userNpass = ({"username": userdb, "password": passdb, "id": iddb, "message": "success"})
            return jsonify(userNpass), 200
        else:
            return jsonify({"message": "Bad request"}), 400
    else:
        return jsonify({"message": "Bad request"}), 400


@app.route("/api/user", methods=['POST'])
def createuser():
    user_name = request.args['username']
    pass_word = request.args['password']
    mydb = mysql.connector.connect(host=host, user=user, password=password, db=db)
    mycursor = mydb.cursor(dictionary=True)
    sql = "INSERT INTO user (username, password) VALUE (%s,%s)"
    val = (user_name, pass_word)
    mycursor.execute(sql, val)
    mydb.commit()
    return make_response(jsonify({"message": "success"}), 200)


@app.route("/api/bookmark")
def getbookmark():
    user_id = request.args['userid']
    mydb = mysql.connector.connect(host=host, user=user, password=password, db=db)
    mycursor = mydb.cursor(dictionary=True)
    sql = "SELECT food_id FROM user_bookmark WHERE user_id = %s"
    val = (user_id,)
    mycursor.execute(sql, val)
    myresult = list(mycursor.fetchall())
    menulist = [w['food_id'] for w in myresult]

    df = getdataframe()
    df = df.iloc[menulist]
    df = df.to_dict('record')
    myresult = ({"message": "success", "result": df})
    return make_response(jsonify(myresult), 200)


@app.route("/api/bookmark", methods=['POST'])
def addbookmark():
    user_id = request.args['userid']
    id_food = request.args['foodid']
    mydb = mysql.connector.connect(host=host, user=user, password=password, db=db)
    mycursor = mydb.cursor(dictionary=True)

    sql_user_bookmark = "INSERT INTO user_bookmark (user_id, food_id) VALUE (%s,%s)"
    val = (user_id, id_food)
    mycursor.execute(sql_user_bookmark, val)
    mydb.commit()
    result = ({"message": "success", "user_id": user_id, "food_id": id_food})
    return make_response(jsonify(result), 200)


@app.route("/api/bookmark", methods=['DELETE'])
def deletebookmark():
    user_id = request.args['userid']
    food_id = request.args['foodid']
    mydb = mysql.connector.connect(host=host, user=user, password=password, db=db)
    mycursor = mydb.cursor(dictionary=True)
    sql = "DELETE FROM user_bookmark WHERE user_id = %s AND food_id = %s"
    val = (user_id, food_id)
    mycursor.execute(sql, val)
    mydb.commit()
    return make_response(jsonify({"message": "success"}), 200)




if __name__ == '__main__':
    app.run(debug=True)
