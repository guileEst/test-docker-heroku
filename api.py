import json
import requests
from flask import Flask, Response, request
from productos import Producto

app = Flask(__name__)

@app.route("/")
def hello_word():
    return "<B>Hello World!!</B>"
@app.route("/buscar")
def buscar_Producto_en_wallapop():
    wallapopBaseUrl="https://api.wallapop.com/api/v3/general/"
    wallapopoKeyWord="nintendo"
#    wallapopoKeyWord=request.args.get('keywords', 'nintendo')
    wallapopUrl=f"https://api.wallapop.com/api/v3/general/search?keywords={wallapopoKeyWord}%20&category_ids=12900&filters_source=seo_landing&longitude=-3.69196&latitude=40.41956&order_by=closest"
    r = requests.get(wallapopUrl)
