from flask import Flask, jsonify
import requests

app = Flask(__name__)


@app.route('/search')
def search():
    query = 'mate'
    url = 'https://api.mercadolibre.com/sites/MLA/search?q=:' + query
    x = requests.get(url).json()
    results = x.get("results")
    results_list = []
    for x in range(20):
        results_list.append(results[x])
    return jsonify({"query": query, "link": results_list[0].get("permalink")})


if __name__ == '__main__':
    app.run()
