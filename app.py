from flask import Flask
import requests
from result import Result

app = Flask(__name__)

@app.route('/search')
def search():
    query = 'mate'
    url = 'https://api.mercadolibre.com/sites/MLA/search?q=:' + query
    x = requests.get(url).json()
    results = x.get("results")
    first_result = Result(results[0].get("thumbnail"), results[0].get("permalink"), query)
    print(first_result.__str__())
    return first_result.__str__()


if __name__ == '__main__':
    app.run()
