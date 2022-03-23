import os
import json
import requests
from flask import Flask, Response, request, jsonify
from productos import Producto
from bitcoins import Bitcoin
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)

@app.route("/")
def hola_mundo():
    return "<p>Hola, Mundo!</p>"

@app.route("/wallapop/<producto>")
def buscar_Producto_en_wallapop(producto):
    wallapopoKeyWord=producto
    app.logger.info(f"Buscar producto: {producto}")
    wallapopUrl=f"https://api.wallapop.com/api/v3/general/search?keywords={wallapopoKeyWord}%20&category_ids=12900&filters_source=seo_landing&longitude=-3.69196&latitude=40.41956&order_by=closest"
    try:
        responseBuscar = requests.get(wallapopUrl)
    except requests.exceptions.Timeout:
        app.logger.info(f"La busqueda de {producto}, esta tomando mucho tiempo.")
    except requests.exceptions.TooManyRedirects:
        app.logger.info(f"Wallapop esta generando muchos redireccionamientos por la busqueda de {producto}")
    except requests.exceptions.RequestException as e:
        app.logger.info(e)

    if responseBuscar.status_code > 400:
        app.logger.info(f"WallaPop tiene problemas para buscar el producto: {producto}.")
        app.logger.info(f"WallaPop código de status: {responseBuscar.status_code}.")
        return Response({}, status=404, mimetype='application/json')

    objetos_return_api = responseBuscar.json().get("search_objects")
#    app.logger.info(objetos_return_api)

    lista_productos = []
    for p in objetos_return_api:
        lista_productos.append(Producto(titulo=p["title"], valor=p["price"], moneda=p["currency"]))

    lista_productos_dict =[t.to_dict() for t in lista_productos]
#    lista_productos_serializada =json.dumps(lista_productos_dict)
    return jsonify(lista_productos_dict)
#    return Response(jsonify(lista_productos_serializada))

@app.route("/bitcoins")
def api_bitcoins():
    bitcoinsUrl=f"https://www.cryptingup.com/api/markets"
    try:
        responseBitcoin = requests.get(bitcoinsUrl)
    except requests.exceptions.Timeout:
        app.logger.info("API Btcoins, esta tomando mucho tiempo.")
    except requests.exceptions.TooManyRedirects:
        app.logger.info("La API de Bitcoins esta generando muchos redireccionamientos")
    except requests.exceptions.RequestException as e:
        app.logger.info(e)

    if responseBitcoin.status_code > 400:
        app.logger.info("API Bitcoins tiene problemas para cargar")
        app.logger.info(f"API Bitcoins código de status: {responseBitcoin.status_code}.")
        return Response({}, status=404, mimetype='application/json')

    lista_bitcoins = []
    for p in responseBitcoin.json().get("markets"):
        lista_bitcoins.append(Bitcoin(simbolo=p["symbol"], base=p["base_asset"], precioSinConvertir=p["price_unconverted"], precio=p["price"], cambio24H=p["change_24h"], spread=p["spread"], creado=p["created_at"], actualizado=p["updated_at"]))

    lista_bitcoins_dict =[t.to_dict() for t in lista_bitcoins]
    return jsonify(lista_bitcoins_dict)

if __name__ == "__main__":
    # app.run(host='0.0.0.0', debug=True, port=8182)
    # port = int(os.environ.get("PORT", 8182))
    app.run()