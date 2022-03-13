import string

from flask import Flask, request, make_response, json, jsonify
# from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
import jwt
import datetime
from functools import wraps
from fucntion.fuction import title_ranking, ingredient_ranking
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


@app.route("/ranking/title", methods=['POST'])
def rankingtitle():
    arg1 = request.args['query']
    arg1 = arg1.replace(' ', '')
    arg1 = arg1.lower().translate(str.maketrans('', '', string.punctuation))
    query = arg1
    query = spell_corr(query)[0]
    result = title_ranking(query)
    result = {'result': result, 'correction': query}
    return make_response(jsonify(result), 200)


@app.route("/ranking/ingredient", methods=['POST'])
def rankingingred():
    arg1 = request.args['query']
    arg1 = arg1.replace(' ', '')
    arg1 = arg1.lower().translate(str.maketrans('', '', string.punctuation))
    query = arg1
    query = spell_corr(query)[0]
    result = ingredient_ranking(query)
    result = {'result': result, 'correction': query}

    return make_response(jsonify(result), 200)


@app.route("/api/user")
def getuser():
    mydb = mysql.connector.connect(host=host, user=user, password=password, db=db)
    mycursor = mydb.cursor(dictionary=True)
    mycursor.execute("SELECT * FROM user")
    myresult = mycursor.fetchall()
    print(myresult)
    return make_response(jsonify(myresult), 200)


@app.route("/api/user")
def getuser():
    mydb = mysql.connector.connect(host=host, user=user, password=password, db=db)
    mycursor = mydb.cursor(dictionary=True)
    mycursor.execute("SELECT * FROM user")
    myresult = mycursor.fetchall()
    print(myresult)
    return make_response(jsonify(myresult), 200)


@app.route("/api/user/<id>")
def getuserbyid(id):
    mydb = mysql.connector.connect(host=host, user=user, password=password, db=db)
    mycursor = mydb.cursor(dictionary=True)
    sql = "SELECT * FROM user WHERE id = %s"
    val = (id,)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchall()
    return make_response(jsonify(myresult), 200)


@app.route("/api/user", methods=['POST'])
def createuser():
    data = request.get_json()
    mydb = mysql.connector.connect(host=host, user=user, password=password, db=db)
    mycursor = mydb.cursor(dictionary=True)
    sql = "INSERT INTO user (username, password, email) VALUE (%s,%s,%s)"
    val = (data['username'], data['password'], data['email'])
    mycursor.execute(sql, val)
    mydb.commit()
    return make_response(jsonify({"rowcount": mycursor.rowcount}), 200)


@app.route("/api/user/<id>", methods=['PUT'])
def updateuser(id):
    data = request.get_json()
    mydb = mysql.connector.connect(host=host, user=user, password=password, db=db)
    mycursor = mydb.cursor(dictionary=True)
    sql = "UPDATE user SET username = %s, password = %s, email = %s WHERE id = %s"
    val = (data['username'], data['password'], data['email'], id)
    mycursor.execute(sql, val)
    mydb.commit()
    return make_response(jsonify({"rowcount": mycursor.rowcount}), 200)


@app.route("/api/user/<id>", methods=['DELETE'])
def deleteuser(id):
    mydb = mysql.connector.connect(host=host, user=user, password=password, db=db)
    mycursor = mydb.cursor(dictionary=True)
    sql = "DELETE FROM user WHERE id = %s"
    val = (id,)
    mycursor.execute(sql, val)
    mydb.commit()
    return make_response(jsonify({"rowcount": mycursor.rowcount}), 200)


if __name__ == '__main__':
    app.run(debug=True)
