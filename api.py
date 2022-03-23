import os
import json
import requests
from flask import Flask, Response, request
from productos import Producto
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)

@app.route("/buscar/<producto>")
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
#        raise SystemExit(e)

    if responseBuscar.status_code > 400:
        app.logger.info(f"WallaPop tiene problemas para buscar el producto: {producto}.")
        app.logger.info(f"WallaPop código de status: {responseBuscar.status_code}.")
        return Response({}, status=404, mimetype='application/json')

    objetos_return_api = responseBuscar.json().get("search_objects")
    app.logger.info(objetos_return_api)

    lista_productos = []
    for p in objetos_return_api:
        lista_productos.append(Producto(titulo=p["title"], valor=p["price"], moneda=p["currency"]))

    lista_productos_dict =[t.to_dict() for t in lista_productos]
    lista_productos_serializada =json.dumps(lista_productos_dict)
    return Response(lista_productos_serializada)

if __name__ == "__main__":
    # port = int(os.environ.get("PORT", 8182))
    app.run()