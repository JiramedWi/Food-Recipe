# Food-Recipe

[![Coverage Status](http://img.shields.io/coveralls/flask-restful/flask-restful/master.svg)](https://coveralls.io/r/flask-restful/flask-restful)
[![PyPI Version](http://img.shields.io/pypi/v/Flask-RESTful.svg)](https://pypi.python.org/pypi/Flask-RESTful)

Using Flask to build a Restful API Server with Swagger document.

Integration with Flask, Flask-Cors, mysql.connector. it began as a simple wrapper around [Werkzeug]https://werkzeug.palletsprojects.com/

## Installation

Install with pip:

```
$ pip install -r requirements.txt
```

## Flask Application Structure 
```
.
| | |────bm25.py
| | |────clean_data.py
| | |────fuction.py
| | |────main.py
| | |────pickle_as_binary.py
| | |────pre_process.py
| | |────spellcorrection.py

```

## Run Flask
1. run `main.py` with `Python console`
2. open `database` with `xamppp`
3. query the database with `user.sql` in `BackEnd/resource/db`

All API use for the front-end project [here]https://github.com/JiramedWi/food-receipe-frontend
