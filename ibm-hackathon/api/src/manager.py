import json
from nlu.aggregation_api3 import watson_helper


def load_data(file_name):
    with open(file_name) as json_file:
        return json.load(json_file)


def get_businesses(data):
    businesses = []
    for entry in data:
        business = {}
        for key, value in entry.items():
            if key == 'reviews':
                continue
            business[key] = value
        businesses.append(business)
    return businesses


def map_id_to_index(businesses):
    map = {}
    index = 0
    for business in businesses:
        map[business['business_id']] = index
        index += 1
    return map


def get_reviews(business_id, business_index, data, page):
    if business_id not in business_index:
        return []
    index = business_index[business_id]
    reviews = data[index]['reviews'][(page * 5):(page * 5 + 5)]
    return reviews


# Deprecated
def get_old_reviews(business_id, business_index, data, page):
    if business_id not in business_index:
        return []
    index = business_index[business_id]
    reviews = data[index]['reviews'][(page * 5):(page * 5 + 5)]
    return reviews


def map_reviews_to_text(data):
    mapped = []
    for business in data:
        review_map = {}
        for review in business['reviews']:
            review_id = review['review_id']
            review_map[review_id] = review['text']
        mapped.append(review_map)
    return mapped


def get_analyzed_reviews(reviews_to_text):
    analyzed_reviews = []
    counter = 0
    for reviews in reviews_to_text:
        print('Analyzing business %d' % counter)
        counter += 1
        watson = watson_helper(reviews)
        for id in watson.input_dict:
            watson.analyze_review_text(id)
        analyzed_reviews.append(watson.raw_watson_dict)
        # print(watson.raw_watson_dict)
        # print(watson.keyword_dict)
        #
        # watson.all_keywords()
        # watson.meta_score()
        # watson.keyword_relevance()
        # print(watson.final_rv)
    return analyzed_reviews


def set_analyzed_data(analyzed_reviews, data):
    # if len(analyzed_reviews) != len(data):
    #     print('fml')
    #     exit(1)
    for index in range(len(data)):
        business = data[index]
        reviews = business['reviews']
        for review in reviews:
            review_id = review['review_id']
            review['raw_watson'] = analyzed_reviews[index][review_id]


def get_reviews_with_keyword(keyword, data):
    pass

