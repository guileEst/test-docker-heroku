import json
import requests
from flask import Flask, Response, request
from productos import Producto

app = Flask(__name__)

@app.route("/")
def hello_word():
    return "<B>Hello World!!</B>"