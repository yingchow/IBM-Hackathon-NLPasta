from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import manager

app = Flask(__name__)
CORS(app)

# Holds data.json in same structure
data = []
# List of dictionaries representing each business
businesses = []
# Maps business ids to its index in data[] and businesses[]
business_index = {}

# Maps review ids to corresponding review text
reviews_to_text = []

analyzed_reviews = []


@app.route('/api/businesses', methods=['GET'])
def get_businesses():
    return jsonify(businesses)

# Deprecated
@app.route('/api/business/<id>/old_reviews', methods=['GET'])
def get_old_reviews(id):
    page_num = int(request.args.get('page') if 'page' in request.args else 0)
    reviews = manager.get_reviews(id, business_index, data, page_num)
    return jsonify(reviews)


@app.route('/api/business/<id>/reviews', methods=['GET'])
def get_reviews(id):
    page_num = int(request.args.get('page') if 'page' in request.args else 0)
    reviews = manager.get_reviews(id, business_index, data, page_num)
    return jsonify(reviews)


@app.route('/api/business/<id>/keyword/<keyword>', methods=['GET'])
def get_reviews_with_keyword(id, keyword):
    reviews = []
    # get reviews
    manager.get_reviews_with_keyword(keyword, data)
    return jsonify(reviews)


@app.route('/api/analyzed_reviews', methods=['GET'])
def get_analyzed_reviews():
    return jsonify(analyzed_reviews)


if __name__ == '__main__':
    data = manager.load_data('src/data.json')
    businesses = manager.get_businesses(data)
    business_index = manager.map_id_to_index(businesses)
    reviews_to_text = manager.map_reviews_to_text(data)
    print('loaded data')

    analyzed_reviews = manager.get_analyzed_reviews(reviews_to_text)

    # TODO set final_rv stuff
    # temp_analyzed, final_rv = manager.get_analyzed_reviews(reviews_to_text)

    manager.set_analyzed_data(analyzed_reviews, data)

    port = int(os.getenv('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=True)

