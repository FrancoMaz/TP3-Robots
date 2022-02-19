import flask
from flask import Flask, jsonify, redirect
import requests
import subprocess

app = Flask(__name__)


@app.errorhandler(404)
def page_not_found(e):
    return jsonify({"message": "No se encontro ningun objeto conocido en la imagen"})


@app.route('/search')
def search():
    # image = request.args.get('image')
    image = "images/cartera.jpeg"
    mates = ['calabaza', 'madera', 'metal', 'plastico']

    coco128 = ['backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'snowboard',
               'sports ball', 'skateboard', 'surfboard', 'tennis racket', 'bottle', 'cup', 'bowl',
               'chair', 'couch', 'refrigerator', 'clock', 'vase', 'teddy bear', 'hair drier']

    values_for_query = {
        "calabaza": "mate calabaza",
        "madera": "mate madera",
        "metal": "mate metal",
        "plastico": "mate plastico",
        "backpack": "mochila",
        "umbrella": "paraguas",
        "handbag": "cartera",
        "tie": "corbata",
        "suitcase": "valija",
        "snowboard": "snowboard",
        "sports ball": "pelota",
        "skateboard": "skateboard",
        "surfboard": "surfboard",
        "tennis racket": "raqueta de tenis",
        "bottle": "botella de agua",
        "cup": "taza",
        "bowl": "bowl",
        "chair": "silla",
        "couch": "sofa",
        "refrigerator": "heladera",
        "clock": "reloj",
        "vase": "jarron",
        "teddy bear": "oso de peluche",
        "hair drier": "secador de pelo"
    }

    out = subprocess.Popen(['python3', 'yolo/detect.py',
                            '--weights', 'yolo/best_materiales.pt', '--img-size', '416',
                            '--conf', '0.4', '--source', image],
                           stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT)

    stdout, stderr = out.communicate()
    query = ''
    for m in mates:
        if ' ' + m in stdout.__str__():
            query = values_for_query[m]
            break

    if query == '':
        out = subprocess.Popen(['python3', 'yolo/detect.py',
                                '--weights', 'yolo/best_coco128.pt', '--img-size', '416',
                                '--conf', '0.4', '--source', image],
                               stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT)

        stdout, stderr = out.communicate()
        for c in coco128:
            if ' ' + c in stdout.__str__():
                query = values_for_query[c]
                break

    if query == '':
        return redirect('/404')

    url = 'https://api.mercadolibre.com/sites/MLA/search?q=:' + query
    x = requests.get(url).json()
    results = x.get("results")
    results_list = []
    for x in range(20):
        results_list.append(results[x])

    # TODO: correr la otra red para detectar la imagen más similar y quedarnos
    #  con results_list[x] siendo x la posición de ese resultado obtenido (campo thumbnail de la respuesta)

    return jsonify({"query": query, "link": results_list[0].get("permalink")})


if __name__ == '__main__':
    app.run()
