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
        results_list.append({
            "Thumbnail": results[x].get("thumbnail"),
            "Link": results[x].get("permalink")})
    return jsonify({"Query": query, "Results": results_list})


if __name__ == '__main__':
    app.run()
