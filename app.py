from flask import Flask, jsonify, request
import requests
import subprocess

app = Flask(__name__)


@app.route('/search')
def search():
    image = request.args.get('image')

    out = subprocess.Popen(['python3', 'yolo/detect.py',
                            '--weights', 'yolo/best_materiales.pt', '--img-size', '416',
                            '--conf', '0.4', '--source', 'images'],
                           stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT)
    stdout, stderr = out.communicate()
    print(stdout)
    return stdout


"""
    query = 'mate'
    url = 'https://api.mercadolibre.com/sites/MLA/search?q=:' + query
    x = requests.get(url).json()
    results = x.get("results")
    results_list = []
    for x in range(20):
        results_list.append(results[x])

    # TODO: correr la otra red para detectar la imagen más similar y quedarnos
    #  con results_list[x] siendo x la posición de ese resultado obtenido (campo thumbnail de la respuesta)

    return jsonify({"Query": query, "Link": results_list[0].get("permalink")})
"""

if __name__ == '__main__':
    app.run()
