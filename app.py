import glob
import os
import shutil

from flask import Flask, jsonify, redirect, request, make_response
import requests
import subprocess
import urllib.request
from get_image_feature_vectors import get_image_feature_vectors
from cluster_image_feature_vectors import cluster

app = Flask(__name__)


@app.route('/search', methods=['POST'])
def search():
    shutil.rmtree('feature-vectors/results', ignore_errors=True)
    shutil.rmtree('feature-vectors/uploads', ignore_errors=True)
    shutil.rmtree('images/uploads', ignore_errors=True)
    shutil.rmtree('images/results', ignore_errors=True)
    shutil.rmtree('yolo/runs/detect', ignore_errors=True)

    os.makedirs('images/results', exist_ok=True)
    os.makedirs('images/uploads', exist_ok=True)
    os.makedirs('feature-vectors/uploads', exist_ok=True)
    os.makedirs('feature-vectors/results', exist_ok=True)

    image_path = "images/uploads"

    image_received = request.files['image']
    image_received.save(os.path.join(image_path, 'image.jpg'))

    image_filename = os.path.basename(glob.glob(image_path + '/*')[0]).split('.')[0]
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
                            '--conf', '0.4', '--source', image_path],
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
                                '--conf', '0.4', '--source', image_path],
                               stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT)

        stdout, stderr = out.communicate()
        for c in coco128:
            if ' ' + c in stdout.__str__():
                query = values_for_query[c]
                break

    if query == '':
        return make_response({"message": "No se pudo detectar ningun objeto"}, 404)

    url = 'https://api.mercadolibre.com/sites/MLA/search?q=:' + query
    x = requests.get(url).json()
    results = x.get("results")
    if len(results) == 0:
        return make_response({"message": "No se encontraron resultados para la busqueda " + query}, 404)
    results_list = []
    for x in range(20):
        results_list.append(results[x])
        urllib.request.urlretrieve(results[x].get("thumbnail"),
                                   'images/results/test-' + x.__str__() + '.jpg')

    get_image_feature_vectors()
    nearest_neighbours = cluster()

    filtered = filter(lambda obj: obj['similar_name'] != image_filename, nearest_neighbours)
    similar_filename = list(filtered)[0]['similar_name']
    index_similar_filename = int(similar_filename.split('-')[1])

    return jsonify({"query": query,
                    "link": results_list[index_similar_filename].get("permalink"),
                    "image": results_list[index_similar_filename].get("thumbnail")})


if __name__ == '__main__':
    app.run()
